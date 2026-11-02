import io
import subprocess
import sys
from pathlib import Path
from unittest.mock import MagicMock

import pytest
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import datetime as dt
import json
from unittest.mock import patch

from recipe_core import alternatives, engine, foods, gemini, images, pdf, safety, usage
from recipe_core.models import RecipeImage
from recipe_core.recipes import RAW

ALL = [engine.build_recipe(r) for r in RAW]


class Resp:
    def __init__(self, payload=None, content=b""):
        self.payload, self.content = payload or {}, content
    def json(self): return self.payload
    def raise_for_status(self): pass


def test_collection_size_and_unique():
    assert len(RAW) >= 50 and len({r["title"] for r in RAW}) == len(RAW)


@pytest.mark.parametrize("recipe", ALL, ids=lambda r: r.title)
def test_every_recipe_meets_targets(recipe):
    assert safety.health_flags(recipe) == []
    assert 120 <= recipe.nutrition.calories_per_serving <= 700
    assert recipe.steps and recipe.add_on_suggestions and recipe.healthy_choices
    assert recipe.dish_image_search and recipe.ingredient_image_searches


@pytest.mark.parametrize("raw", RAW, ids=lambda r: r["title"])
def test_steps_do_not_use_other_allergens(raw):
    """An allergen in the method must also come from the ingredient list."""
    recipe = engine.build_recipe(raw)
    names = " ".join(i.name for i in recipe.ingredients)
    for allergen in safety.COMMON_ALLERGENS:
        in_text = safety.find_allergen_hits(" ".join(recipe.steps + [recipe.title]), [allergen])
        assert not in_text or safety.find_allergen_hits(names, [allergen]) or allergen in recipe.hidden_allergens, allergen


def test_no_pork_or_alcohol():
    text = " ".join(str(r) for r in RAW).lower()
    assert not any(w in text for w in ("pork", "bacon", "ham ", "lard", "wine", "beer", "rum ", "mirin"))


def test_alternative_tables_reference_real_items():
    assert set(alternatives.INGREDIENTS) <= set(foods.FOODS)
    assert set(alternatives.UTENSIL_ALTERNATIVES) <= set(foods.UTENSILS)
    for food in foods.FOODS.values():
        for alt in alternatives.INGREDIENTS.get(food.name, []):
            assert alt["name"] in foods.FOODS, alt["name"]


@pytest.mark.parametrize("text,expected", [
    ("chicken", {"chicken breast", "chicken thigh"}), ("Chicken breasts", {"chicken breast"}), ("ayam", {"chicken breast", "chicken thigh"}),
    ("tomatoes", {"tomato"}), ("rice", {"brown rice", "white rice"}), ("rice noodles", {"rice noodles"}), ("soy sauce", {"light soy sauce"}), ("xyzzy", set()),
])
def test_resolve_food(text, expected):
    assert foods.resolve_food(text) == expected


@pytest.mark.parametrize("text,allergen,expected", [
    ("eggplant", "Eggs", False), ("2 eggs", "Eggs", True), ("coconut milk", "Milk / dairy", False), ("low-fat milk", "Milk / dairy", True),
    ("peanut butter", "Milk / dairy", False), ("peanut butter", "Peanuts", True), ("almond milk", "Tree nuts", True), ("nutmeg", "Tree nuts", False),
    ("light soy sauce", "Wheat / gluten", True), ("light soy sauce", "Soy", True), ("rice noodles", "Wheat / gluten", False),
    ("belacan", "Shellfish (crustaceans)", True), ("oyster sauce", "Molluscs", True), ("kiwis", "kiwi", True),
])
def test_allergen_words(text, allergen, expected):
    assert bool(safety.find_allergen_hits(text, [allergen])) is expected


def test_expand_typed_allergens():
    assert safety.expand_allergens(["gluten"]) == ["Wheat / gluten"]
    assert set(safety.expand_allergens(["seafood"])) == {"Fish", "Shellfish (crustaceans)", "Molluscs"}
    assert safety.expand_allergens(["kiwi"]) == ["kiwi"]
    assert safety.expand_allergens(["Eggs", "egg"]) == ["Eggs"]


@pytest.mark.parametrize("allergen", safety.COMMON_ALLERGENS + ["gluten", "seafood", "nuts", "tomato", "ginger"])
def test_search_never_returns_allergen(allergen):
    stock = [f.name for f in foods.FOODS.values()]
    matches, _ = engine.find_recipes(stock, list(foods.UTENSILS), [allergen], [], count=100, max_minutes=120, max_missing=5)
    assert matches
    for m in matches:
        r = m.recipe
        text = " ".join([*[i.name for i in r.ingredients], *r.steps, *r.add_on_suggestions, r.title, r.description, *m.ingredient_swaps])
        assert not safety.find_allergen_hits(text, safety.expand_allergens([allergen]))
        assert not set(r.hidden_allergens) & set(safety.expand_allergens([allergen]))


def test_matching_ranks_and_reports():
    matches, _ = engine.find_recipes(["chicken", "brown rice", "broccoli", "garlic", "soy sauce"], ["wok", "pot"], [], [])
    assert matches[0].recipe.title == "Garlic Chicken and Broccoli Rice"
    assert matches[0].missing_ingredients == [] and matches[0].missing_utensils == []


def test_missing_items_swaps_and_limits():
    matches, _ = engine.find_recipes(["chicken thigh", "brown rice", "broccoli", "garlic", "soy sauce"], ["pot"], [], [], count=50, max_minutes=120, max_missing=0)
    garlic = next(m for m in matches if m.recipe.title == "Garlic Chicken and Broccoli Rice")
    assert any("chicken thigh" in s for s in garlic.ingredient_swaps)
    assert all(not m.missing_ingredients for m in matches)
    assert any("pot" in s.lower() for s in garlic.utensil_swaps)


def test_recipes_needing_other_utensils_are_hidden_by_default():
    stock = [f.name for f in foods.FOODS.values()]
    default, _ = engine.find_recipes(stock, ["rice cooker"], [], [], count=100, max_minutes=120, max_missing=5, basics=False)
    wider, _ = engine.find_recipes(stock, ["rice cooker"], [], [], count=100, max_minutes=120, max_missing=5, basics=False, allow_other_utensils=True)
    assert all(not m.missing_utensils for m in default) and len(wider) > len(default)
    assert "Rice Cooker Chicken and Mushroom Rice" in {m.recipe.title for m in default}


def test_filters():
    stock = [f.name for f in foods.FOODS.values()]
    kit = list(foods.UTENSILS)
    veg, _ = engine.find_recipes(stock, kit, [], ["Vegan"], count=100, max_minutes=120, max_missing=5)
    assert veg
    for m in veg:
        assert not {foods.FOODS[engine.parse_amount(s)[0]].cat for s in next(r for r in RAW if r["title"] == m.recipe.title)["items"]} & set("mfdeh")
    fast, _ = engine.find_recipes(stock, kit, [], [], count=100, max_minutes=20, max_missing=5)
    assert fast and all(m.recipe.total_minutes <= 20 for m in fast)
    assert engine.find_recipes(["xyzzy"], kit, [], [])[0] == []


def test_scaling_keeps_per_serving_nutrition():
    raw = next(r for r in RAW if r["title"] == "Garlic Chicken and Broccoli Rice")
    two, four = engine.build_recipe(raw, 2), engine.build_recipe(raw, 4)
    assert two.nutrition == four.nutrition and four.total_calories == 2 * two.total_calories
    amounts = {i.name: i.amount for i in four.ingredients}
    assert amounts["chicken breast"] == "520 g" and amounts["garlic"] == "6 cloves" and amounts["cooking oil"] == "4 tsp"
    one = engine.build_recipe(raw, 1)
    assert {i.name: i.amount for i in one.ingredients}["garlic"] == "1½ cloves"


def test_calories_match_hand_calculation():
    raw = next(r for r in RAW if r["title"] == "Banana Cinnamon Oats")
    # oats 380, milk 141, banana 89, cinnamon 3 kcal, divided by 2 servings
    assert engine.build_recipe(raw).nutrition.calories_per_serving == pytest.approx((380 + 141 + 89 + 3.09) / 2, abs=1)


def test_alternatives():
    result = engine.find_alternatives("Soy sauce", "ingredient", [])
    assert {a.name for a in result.alternatives} >= {"salt", "fish sauce"} and "famous+cookbook" in result.search_url
    safe = engine.find_alternatives("soy sauce", "ingredient", ["fish"])
    assert "fish sauce" not in {a.name for a in safe.alternatives} and safe.removed_for_allergens
    assert engine.find_alternatives("wok", "utensil", []).alternatives
    assert engine.find_alternatives("xyzzy", "ingredient", []).alternatives == []


def jpeg(size=(800, 600)):
    out = io.BytesIO(); Image.new("RGB", size, (190, 120, 60)).save(out, "JPEG"); return out.getvalue()


def page(title, licence="CC BY-SA 4.0", url="https://upload.wikimedia.org/x.jpg", index=1):
    return {"index": index, "title": f"File:{title}.jpg", "imageinfo": [{"thumburl": url, "mime": "image/jpeg", "descriptionurl": "https://commons.wikimedia.org/wiki/File:x",
            "extmetadata": {"LicenseShortName": {"value": licence}, "Artist": {"value": "<a href='x'>Jo &amp; Co</a>"}}}]}


def test_image_selection_and_dish_flag():
    pages = {"1": page("Chicken rice logo", index=1), "2": page("Fried noodles", index=2), "3": page("Chicken rice", "All rights reserved", index=3),
             "4": page("Chicken rice", url="https://evil.example/x.jpg", index=4), "5": page("Hainanese chicken rice plate", index=5)}
    session = MagicMock()
    session.get.side_effect = [Resp({"query": {"pages": pages}}), Resp(content=jpeg())]
    img = images.find_image("chicken rice", session)
    assert "Jo & Co" in img.credit and session.get.call_args.args[0] == "https://upload.wikimedia.org/x.jpg"
    session = MagicMock()
    session.get.side_effect = [Resp({"query": {"pages": {}}}), Resp({"query": {"pages": {"1": page("Broccoli")}}}), Resp(content=jpeg())]
    found = images.find_recipe_images("no such dish", ["broccoli"], session)
    assert len(found) == 1 and not found[0].is_dish


def test_pdf_for_every_recipe(tmp_path):
    pics = [RecipeImage(data=jpeg((1200, 800)), label="dish", credit="Jo, CC BY 4.0, via Wikimedia Commons", source_url="https://commons.wikimedia.org/wiki/File:x", is_dish=True),
            RecipeImage(data=jpeg(), label="broccoli", credit="Jo, CC BY 4.0, via Wikimedia Commons", source_url="https://commons.wikimedia.org/wiki/File:y")]
    for recipe in ALL:
        assert pdf.build_recipe_pdf(recipe, pics, ["Sesame"], ["Ingredients to buy: x"]).startswith(b"%PDF")
    f = tmp_path / "r.pdf"; f.write_bytes(pdf.build_recipe_pdf(ALL[0], pics, ["Sesame", "kiwi"], ["Ingredients to buy: garlic"]))
    text = " ".join(subprocess.run(["pdftotext", "-layout", str(f), "-"], capture_output=True, text=True).stdout.split())
    for expected in ("Lighter Nasi Goreng", "Ingredients", "Method", "kcal", "read product labels", "Ingredients to buy: garlic", "Add-on suggestions", "Image credits", "built-in food table"):
        assert expected in text, expected
    assert " AI " not in text


def ai_recipe(**over):
    data = dict(title="AI Chicken Bowl", description="Light.", servings=2, prep_minutes=5, cook_minutes=20, difficulty="Easy",
                ingredients=[dict(name="chicken breast", amount="300 g", healthy_note=""), dict(name="cooking oil", amount="1 tsp", healthy_note=""), dict(name="quinoa", amount="100 g", healthy_note="")],
                utensils=["wok", "knife", "air fryer"], steps=["Cook the chicken to 75°C."],
                nutrition=dict(calories_per_serving=500, protein_g=40, carbs_g=50, fat_g=15, saturated_fat_g=3, sugar_g=4, fibre_g=7, sodium_mg=400),
                healthy_choices=["Lean"], add_on_suggestions=["Cucumber", "Sesame dressing"], allergens_present=[], dish_image_search="chicken", ingredient_image_searches=["chicken"])
    data.update(over)
    return data


class AI:
    def __init__(self, status=200, payload=None):
        self.status_code, self.payload = status, payload or {}
        self.text = json.dumps(self.payload)
    def json(self): return self.payload


def answer(text, **candidate):
    return AI(payload={"candidates": [{"content": {"parts": [{"text": text}]}, **candidate}]})


def test_ai_recipes_filtered_and_sent_safely():
    session = MagicMock()
    bad = ai_recipe(title="Hidden", allergens_present=["soy"], )
    session.post.return_value = answer(json.dumps({"recipes": [ai_recipe(), ai_recipe(title="Sesame Bowl", steps=["Add sesame."]), bad]}))
    safe, removed = gemini.generate_recipes("test-key", ["chicken"], ["wok"], ["Sesame", "gluten", "Soy"], ["Halal"], session=session)
    assert [r.title for r in safe] == ["AI Chicken Bowl"] and len(removed) == 2
    assert safe[0].origin == "ai" and safe[0].add_on_suggestions == ["Cucumber"]
    call = session.post.call_args
    assert "test-key" not in call.args[0] and call.kwargs["headers"]["x-goog-api-key"] == "test-key"
    prompt = call.kwargs["json"]["contents"][0]["parts"][0]["text"]
    assert all(t in prompt for t in ("Wheat / gluten", "Halal", "wok", "healthy"))


def test_ai_match_reports_missing_items():
    r = engine.Recipe(**ai_recipe())
    m = engine.match_ai_recipe(r, ["chicken"], ["wok"])
    assert m.missing_ingredients == ["quinoa"] and m.missing_utensils == ["air fryer"]


def test_ai_errors_and_model_fallback():
    session = MagicMock()
    session.post.side_effect = [AI(404), answer(json.dumps({"recipes": [ai_recipe()]}))]
    assert len(gemini.generate_recipes("k", ["a"], ["b"], [], [], session=session)[0]) == 1
    session = MagicMock(); session.post.return_value = AI(429)
    with pytest.raises(gemini.GeminiError, match="limit"):
        gemini.generate_recipes("k", ["a"], ["b"], [], [], session=session)
    session = MagicMock(); session.post.return_value = AI(400, {"error": "API key not valid"})
    with pytest.raises(gemini.GeminiError) as err:
        gemini.generate_recipes("secret-value", ["a"], ["b"], [], [], session=session)
    assert "secret-value" not in str(err.value)


ALT = {"alternatives": [{"name": "Lidded pot", "how_to_use": "Simmer gently", "ratio_or_adjustment": "", "healthier_note": "", "cookbook_or_site": "Joy of Cooking"}]}


def test_search_alternatives_sources_and_unverified():
    session = MagicMock()
    meta = {"groundingChunks": [{"web": {"uri": "https://example.org/a", "title": "Book"}}, {"web": {"uri": "https://example.org/a", "title": "Dup"}}]}
    session.post.return_value = answer(json.dumps(ALT), groundingMetadata=meta)
    found = gemini.find_alternatives("k", "rice cooker", "utensil", [], [], session=session)
    assert found.origin == "search" and len(found.sources) == 1 and found.alternatives[0].cookbook_or_site == "Joy of Cooking"
    assert session.post.call_args.kwargs["json"]["tools"] == [{"google_search": {}}]
    session.post.return_value = answer("```json\n" + json.dumps(ALT) + "\n```")
    plain = gemini.find_alternatives("k", "rice cooker", "utensil", [], [], session=session)
    assert plain.origin == "unverified" and plain.alternatives[0].cookbook_or_site == ""


def test_daily_limit_resets():
    limit = usage.DailyLimit(2)
    day = dt.date(2026, 1, 1)
    assert limit.try_use(day) and limit.try_use(day) and not limit.try_use(day)
    assert limit.try_use(dt.date(2026, 1, 2))


class State(dict):
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__


def stub_streamlit(secrets, primary_clicked=False):
    st = MagicMock()
    def columns(spec):
        cols = [MagicMock() for _ in range(spec if isinstance(spec, int) else len(spec))]
        for c in cols:
            c.number_input.return_value = 2
            c.slider.side_effect = lambda label, *a, **k: {"Number of recipes": 3, "Maximum time (minutes)": 60}.get(label, 2)
            c.radio.return_value = "ingredient"
            c.text_input.return_value = ""
            c.__enter__ = MagicMock(return_value=c); c.__exit__ = MagicMock(return_value=False)
        return cols
    st.columns.side_effect = columns
    st.tabs.side_effect = lambda labels: [MagicMock(__enter__=MagicMock(), __exit__=MagicMock(return_value=False)) for _ in labels]
    st.session_state = State()
    st.button.side_effect = lambda label, **_: primary_clicked and label == "Find healthy recipes"
    st.multiselect.return_value = []
    st.text_area.side_effect = lambda label, **_: "chicken, brown rice, broccoli, garlic, soy sauce" if "Ingredients" in label else "wok, pot"
    st.text_input.return_value = ""
    st.checkbox.side_effect = lambda label, **_: "no allergens" in label or "knife" in label
    st.radio.return_value = "Any"
    st.secrets = secrets
    st.cache_data = lambda **_: (lambda fn: fn)
    st.cache_resource = lambda fn: fn
    return st


def run_app(st):
    sys.modules["streamlit"] = st
    try:
        with patch("recipe_core.images.find_recipe_images", return_value=[]):
            namespace = {"__name__": "__main__"}
            exec(compile((Path(__file__).resolve().parent.parent / "app.py").read_text(), "app.py", "exec"), namespace)
        return namespace
    finally:
        del sys.modules["streamlit"]


def test_app_has_no_key_box_and_uses_ai():
    st = stub_streamlit({"GEMINI_API_KEY": "k"}, True)
    with patch("recipe_core.gemini.requests.post", return_value=answer(json.dumps({"recipes": [ai_recipe(utensils=["wok"])]}))) as post:
        run_app(st)
    assert post.called and st.session_state["results"]["matches"][0].recipe.origin == "ai"
    assert st.download_button.called
    assert not any("key" in str(c.args[0]).lower() for c in st.text_input.call_args_list)


def test_app_falls_back_without_key_or_on_error():
    st = stub_streamlit({}, True)
    run_app(st)
    assert st.session_state["results"]["matches"][0].recipe.origin == "built-in" and st.session_state["results"]["notice"]
    st = stub_streamlit({"GEMINI_API_KEY": "k"}, True)
    with patch("recipe_core.gemini.requests.post", return_value=AI(429)):
        run_app(st)
    assert st.session_state["results"]["matches"][0].recipe.origin == "built-in"


def test_no_key_shaped_text_in_project():
    root = Path(__file__).resolve().parent.parent
    for path in [root / "app.py", root / "README.md", *root.glob("recipe_core/*.py"), *root.glob(".streamlit/*")]:
        assert "AIza" not in path.read_text() and "AQ.A" not in path.read_text(), path
