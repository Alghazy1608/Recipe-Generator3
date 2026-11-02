"""Healthy Recipe Generator: run with `streamlit run app.py`. The Gemini key is read from Streamlit Secrets."""
import streamlit as st

from recipe_core.engine import DIETS, find_alternatives, find_recipes, match_ai_recipe, recognise_ingredients, recognise_utensils
from recipe_core.gemini import GeminiError, find_alternatives as find_ai_alternatives, generate_recipes
from recipe_core.images import find_recipe_images
from recipe_core.pdf import build_recipe_pdf
from recipe_core.recipes import RAW
from recipe_core.usage import DailyLimit
from recipe_core.safety import COMMON_ALLERGENS, calorie_mismatch, expand_allergens, find_allergen_hits, health_flags, parse_items

st.set_page_config(page_title="Healthy Recipe Generator", page_icon="🍲", layout="wide")


def secret(name, default=""):
    try:
        return st.secrets.get(name, default)
    except Exception:  # Streamlit raises when no secrets file exists.
        return default


API_KEY = secret("GEMINI_API_KEY")
MODELS = [secret("GEMINI_MODEL")] if secret("GEMINI_MODEL") else None
SESSION_LIMIT = 15


@st.cache_resource
def shared_limit():
    return DailyLimit(int(secret("DAILY_AI_LIMIT", 200)))


def ai_allowed():
    """Reserve one AI request, or return False if the app should use its built-in data."""
    used = st.session_state.get("ai_used", 0)
    if not API_KEY or used >= SESSION_LIMIT or not shared_limit().try_use():
        return False
    st.session_state["ai_used"] = used + 1
    return True


@st.cache_data(ttl=86400, show_spinner="Finding photos...")
def cached_images(dish, ingredients):
    return find_recipe_images(dish, list(ingredients))


st.title("Healthy Recipe Generator")
st.write("Tell me what is in your kitchen and I'll create healthy recipes you can make.")
st.caption("No sign-up or key is needed. What you enter, including allergens, is sent to Google Gemini to create recipes, so please don't enter personal details. "
           f"If the AI is unavailable, the app uses its {len(RAW)} built-in recipes instead.")

left, right = st.columns(2)
with left:
    ingredients_text = st.text_area("Ingredients you have", height=130, placeholder="chicken, brown rice, broccoli, garlic")
with right:
    utensils_text = st.text_area("Utensils you have", height=130, placeholder="wok, pot, oven")
basics = st.checkbox("I also have a knife, chopping board, spoon and bowl", value=True)

st.subheader("Allergens")
a_left, a_right = st.columns(2)
with a_left:
    picked = st.multiselect("Select any allergens to avoid", COMMON_ALLERGENS)
with a_right:
    other = st.text_input("Other allergens not on the list", placeholder="kiwi, strawberries")
no_allergies = st.checkbox("I have no allergens to avoid")
allergens = expand_allergens(picked + parse_items(other))

with st.expander("Recipe options", expanded=True):
    o1, o2, o3, o4 = st.columns(4)
    servings = o1.number_input("Servings", 1, 12, 2)
    count = o2.slider("Number of recipes", 1, 5, 3)
    max_minutes = o3.slider("Maximum time (minutes)", 5, 120, 60, step=5)
    max_missing = o4.slider("Ingredients I can buy", 0, 5, 2)
    meal = st.radio("Meal", ["Any", "Breakfast", "Lunch or dinner"], horizontal=True)
    allow_other_utensils = st.checkbox("Also show recipes that need other utensils")
    diets = st.multiselect("Dietary requirements (optional)", DIETS)
    if "Halal" in diets:
        st.caption("None of the built-in recipes use pork or alcohol. Choose halal-certified meat and products.")

ingredients, utensils = parse_items(ingredients_text), parse_items(utensils_text)
listed_allergens = [i for i in ingredients if find_allergen_hits(i, allergens)]
if listed_allergens:
    st.warning("These listed ingredients match an allergen and won't be used: " + ", ".join(listed_allergens))
usable = [i for i in ingredients if i not in listed_allergens]

if st.button("Find healthy recipes", type="primary"):
    if not usable:
        st.error("Enter at least one ingredient that is safe for you.")
    elif not utensils and not basics:
        st.error("Enter at least one utensil.")
    elif allergens and no_allergies:
        st.error("You selected allergens and also ticked 'no allergens'. Please correct one.")
    elif not allergens and not no_allergies:
        st.error("Select your allergens, or tick 'I have no allergens to avoid'.")
    else:
        notice = ""
        matches = None
        kit = utensils + (["knife", "chopping board", "spoon", "bowl"] if basics else [])
        if ai_allowed():
            with st.spinner("Creating your recipes..."):
                try:
                    recipes, removed_ai = generate_recipes(API_KEY, usable, kit, allergens, diets, int(servings), count, max_minutes,
                                                           max_missing > 0, models=MODELS)
                    matches = [match_ai_recipe(r, usable, utensils, basics) for r in recipes]
                    if not allow_other_utensils:
                        matches = [m for m in matches if not m.missing_utensils]
                    removed = len(removed_ai)
                except GeminiError as exc:
                    notice = f"{exc} Showing built-in recipes instead."
        else:
            notice = "AI recipes aren't available right now, so these are built-in recipes."
        if not matches:
            if matches is not None:
                notice = "The AI recipes didn't pass the allergen or utensil checks, so these are built-in recipes."
            matches, removed = find_recipes(usable, utensils, allergens, diets, int(servings), count, max_minutes, max_missing, meal, basics, allow_other_utensils)
        st.session_state.results = {"matches": matches, "removed": removed, "allergens": allergens, "notice": notice,
                                    "unknown": recognise_ingredients(usable)[1], "unknown_utensils": recognise_utensils(utensils)[1]}
        st.session_state.pop("alternatives", None)


def show_recipe(match, index, results):
    recipe = match.recipe
    images = cached_images(recipe.dish_image_search, tuple(recipe.ingredient_image_searches))
    dish = next((img for img in images if img.is_dish), None)
    st.header(recipe.title)
    st.write(recipe.description)
    if dish:
        st.image(dish.data, caption="Similar dish for illustration: " + dish.credit)
    elif images:
        st.image(images[0].data, caption=f"{images[0].label.title()}: {images[0].credit}")
    else:
        st.caption("No suitable freely licensed photo was found for this dish.")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Calories per serving", f"{recipe.nutrition.calories_per_serving:.0f} kcal")
    c2.metric("Whole recipe", f"{recipe.total_calories:.0f} kcal")
    c3.metric("Total time", f"{recipe.total_minutes} min")
    c4.metric("Servings", recipe.servings)
    if recipe.origin == "ai":
        st.caption("AI-created recipe. Calories and nutrition are AI estimates, so check that the steps and amounts look sensible.")
        if calorie_mismatch(recipe):
            st.caption("This calorie figure doesn't closely match the protein, carbohydrate and fat figures, so treat it as rough.")
    else:
        st.caption("Built-in recipe. Calories and nutrition are estimates from a built-in food table.")
    for flag in health_flags(recipe):
        st.warning(flag)
    if results["allergens"]:
        st.info("Automatic checks found none of your allergens: " + ", ".join(results["allergens"]) +
                ". Always read product labels and check for cross-contamination.")
    elif recipe.allergens_present:
        st.info("Contains or may contain: " + ", ".join(recipe.allergens_present))

    notes = []
    if match.missing_ingredients:
        notes.append("Ingredients to buy: " + ", ".join(match.missing_ingredients))
    if match.missing_utensils:
        notes.append("Utensils you may need: " + ", ".join(match.missing_utensils))
    for note in notes:
        st.warning(note)
    for swap in match.ingredient_swaps + match.utensil_swaps:
        st.info(swap)

    col_a, col_b = st.columns([2, 3])
    with col_a:
        st.subheader("Ingredients")
        for item in recipe.ingredients:
            st.markdown(f"- **{item.amount}** {item.name}")
        st.subheader("Utensils")
        st.write(", ".join(recipe.utensils))
    with col_b:
        st.subheader("Method")
        for number, step in enumerate(recipe.steps, 1):
            st.markdown(f"{number}. {step}")
        if recipe.servings > 2:
            st.caption("Cooking times are for 2 servings. Larger amounts may take longer and need bigger pans.")

    n = recipe.nutrition
    st.subheader("Nutrition per serving (estimated)")
    st.table({"Protein": [f"{n.protein_g:.0f} g"], "Carbs": [f"{n.carbs_g:.0f} g"], "Fat": [f"{n.fat_g:.0f} g"],
              "Saturated fat": [f"{n.saturated_fat_g:.0f} g"], "Sugar": [f"{n.sugar_g:.0f} g"],
              "Fibre": [f"{n.fibre_g:.0f} g"], "Sodium": [f"{n.sodium_mg:.0f} mg"]})
    if recipe.healthy_choices:
        st.subheader("Why it's healthy")
        for note in recipe.healthy_choices:
            st.markdown(f"- {note}")
    if recipe.add_on_suggestions:
        st.subheader("Add-on suggestions")
        for note in recipe.add_on_suggestions:
            st.markdown(f"- {note}")

    pdf = build_recipe_pdf(recipe, images, results["allergens"], notes + match.ingredient_swaps + match.utensil_swaps)
    safe_name = "".join(ch if ch.isalnum() else "-" for ch in recipe.title.lower()).strip("-") or "recipe"
    st.download_button("Download recipe PDF", pdf, file_name=f"{safe_name}.pdf", mime="application/pdf", key=f"pdf-{index}")


results = st.session_state.get("results")
if results:
    if results["notice"]:
        st.warning(results["notice"])
        if results["unknown"]:
            st.warning("Not recognised, so not used for built-in matching: " + ", ".join(results["unknown"]))
        if results["unknown_utensils"]:
            st.warning("Utensils not recognised for built-in matching: " + ", ".join(results["unknown_utensils"]))
    if results["removed"]:
        st.caption(f"{results['removed']} recipes were excluded by the allergen check.")
    if results["matches"]:
        tabs = st.tabs([m.recipe.title[:32] for m in results["matches"]])
        for index, (tab, match) in enumerate(zip(tabs, results["matches"])):
            with tab:
                show_recipe(match, index, results)
    else:
        st.error("No recipes matched. Try adding ingredients, or allowing more ingredients to buy or more time.")

st.divider()
st.subheader("Find an alternative")
st.write("Missing something? I'll search online, looking first for famous cookbooks, and show the sources found.")
alt_a, alt_b = st.columns([3, 1])
item = alt_a.text_input("Ingredient or utensil to replace", placeholder="soy sauce, or rice cooker")
kind = alt_b.radio("Type", ["ingredient", "utensil"], horizontal=True)
if st.button("Find alternatives"):
    if not item.strip():
        st.error("Enter an ingredient or utensil.")
    elif not allergens and not no_allergies:
        st.error("Select your allergens, or tick 'I have no allergens to avoid'.")
    else:
        built_in = find_alternatives(item.strip(), kind, allergens)
        answer = built_in
        if ai_allowed():
            with st.spinner("Searching for alternatives..."):
                try:
                    answer = find_ai_alternatives(API_KEY, item.strip(), kind, allergens, diets, models=MODELS)
                    answer.search_url = built_in.search_url
                except GeminiError:
                    pass
        if answer.origin != "built-in" and not answer.alternatives:
            answer = built_in
        st.session_state.alternatives = answer

result = st.session_state.get("alternatives")
if result:
    if result.origin == "built-in":
        st.warning("Online search wasn't available, so these come from the app's built-in list, not from cookbooks.")
    elif result.origin == "unverified":
        st.warning("Google Search returned no sources for this answer, so these suggestions are unverified.")
    if result.removed_for_allergens:
        st.warning("Removed because of your allergens: " + "; ".join(result.removed_for_allergens))
    if not result.alternatives:
        st.info(f"The built-in list has no safe alternative for {result.item}.")
    for alt in result.alternatives:
        st.markdown(f"**{alt.name.capitalize()}**")
        st.write(alt.how_to_use)
        if alt.ratio_or_adjustment:
            st.caption("Amount or adjustment: " + alt.ratio_or_adjustment)
        if alt.healthier_note:
            st.caption("Health note: " + alt.healthier_note)
        if alt.cookbook_or_site:
            st.caption("Named by the AI from its search: " + alt.cookbook_or_site)
    if result.sources:
        st.markdown("**Sources found by Google Search**")
        for source in result.sources:
            st.markdown(f"- [{source.title}]({source.url})")
    st.markdown(f"[Search for more cookbook advice on {result.item}]({result.search_url})")
