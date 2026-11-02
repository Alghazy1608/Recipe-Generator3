"""Build, filter, rank and scale the built-in recipes."""
from __future__ import annotations

from urllib.parse import quote_plus

from .alternatives import INGREDIENTS, UTENSIL_ALTERNATIVES
from .foods import BASIC_UTENSILS, FOODS, STAPLES, format_amount, grams, norm_words, parse_amount, resolve_food, resolve_utensil
from .models import Alternative, AlternativeResult, Ingredient, Nutrition, Recipe, RecipeMatch
from .recipes import RAW
from .safety import COMMON_ALLERGENS, expand_allergens, filter_alternatives, find_allergen_hits, recipe_allergen_hits

BASE_SERVINGS = 2
DIETS = ["Halal", "Vegetarian", "Vegan", "Lower sugar", "Lower salt", "High protein"]


def build_recipe(raw: dict, servings: int = BASE_SERVINGS, allergens: list[str] | None = None) -> Recipe:
    factor = servings / BASE_SERVINGS
    totals = [0.0] * 8
    ingredients, hidden = [], []
    for spec in raw["items"]:
        name, qty, unit = parse_amount(spec)
        food = FOODS[name]
        weight = grams(food, qty, unit)
        for i, value in enumerate(food.n):
            totals[i] += value * weight / 100 / BASE_SERVINGS
        amount, label = format_amount(food, qty * factor, unit)
        ingredients.append(Ingredient(name=label, amount=amount))
        hidden += [a for a in food.hidden if a not in hidden]
    keys = ("calories_per_serving", "protein_g", "carbs_g", "fat_g", "saturated_fat_g", "sugar_g", "fibre_g", "sodium_mg")
    addons = [a for a in raw["addons"] if not find_allergen_hits(a, allergens or [])]
    names = " ".join(i.name for i in ingredients)
    contains = [a for a in COMMON_ALLERGENS if find_allergen_hits(names, [a]) or a in hidden]
    return Recipe(title=raw["title"], description=raw["description"], servings=servings, prep_minutes=raw["prep"], cook_minutes=raw["cook"],
                  difficulty="Easy" if len(raw["steps"]) <= 4 else "Medium", ingredients=ingredients,
                  utensils=[*raw["utensils"], *[b for b in BASIC_UTENSILS[:3] if b not in raw["utensils"]]], steps=raw["steps"],
                  nutrition=Nutrition(**dict(zip(keys, totals))), healthy_choices=raw["healthy"], add_on_suggestions=addons,
                  allergens_present=contains, hidden_allergens=hidden, meal=raw["meal"], dish_image_search=raw["image"],
                  ingredient_image_searches=list(raw["ingredient_images"]))


def _foods(raw):
    return [parse_amount(spec)[0] for spec in raw["items"]]


def meets_diets(raw, recipe: Recipe, diets: list[str]) -> bool:
    cats = {FOODS[f].cat for f in _foods(raw)}
    n = recipe.nutrition
    rules = {"Vegetarian": not cats & {"m", "f"}, "Vegan": not cats & {"m", "f", "d", "e", "h"}, "Halal": True,
             "Lower sugar": n.sugar_g <= 10, "Lower salt": n.sodium_mg <= 500, "High protein": n.protein_g >= 25}
    return all(rules.get(d, True) for d in diets)


def recognise_ingredients(items: list[str]) -> tuple[set[str], list[str]]:
    known, unknown = set(), []
    for item in items:
        found = resolve_food(item)
        if found:
            known |= found
        else:
            unknown.append(item)
    return known, unknown


def recognise_utensils(items: list[str]) -> tuple[set[str], list[str]]:
    known, unknown = set(), []
    for item in items:
        found = resolve_utensil(item)
        if found:
            known |= found
        else:
            unknown.append(item)
    return known, unknown


def _swap_for(food: str, have: set[str], allergens: list[str]) -> str | None:
    for alt in INGREDIENTS.get(food, []):
        if alt["name"] in have and not find_allergen_hits(alt["name"], allergens):
            return f"No {food}? Use your {alt['name']}: {alt['ratio_or_adjustment'] or 'same amount'}. {alt['how_to_use']}"
    return None


def _utensil_swap(utensil: str, have: set[str]) -> str | None:
    for alt in UTENSIL_ALTERNATIVES.get(utensil, []):
        if resolve_utensil(alt["name"]) & have:
            return f"No {utensil}? {alt['name'].capitalize()}: {alt['how_to_use']}"
    return None


def find_recipes(ingredients: list[str], utensils: list[str], allergens: list[str], diets: list[str], servings=2, count=3,
                 max_minutes=45, max_missing=2, meal="Any", basics=True, allow_other_utensils=False) -> tuple[list[RecipeMatch], int]:
    """Return the best matches, and how many recipes the allergen check excluded."""
    have, _ = recognise_ingredients(ingredients)
    kit, _ = recognise_utensils(utensils)
    if basics:
        kit |= set(BASIC_UTENSILS)
    allergens = expand_allergens(allergens)
    removed, matches = 0, []
    for raw in RAW:
        recipe = build_recipe(raw, servings, allergens)
        if recipe_allergen_hits(recipe, allergens):
            removed += 1
            continue
        if recipe.total_minutes > max_minutes or not meets_diets(raw, recipe, diets) or (meal != "Any" and meal.split()[0] not in recipe.meal):
            continue
        used, missing, swaps, score, total = [], [], [], 0.0, 0.0
        for food in _foods(raw):
            if food in STAPLES:
                continue
            weight = 1.0 if FOODS[food].role == "main" else 0.3
            total += weight
            if food in have:
                used.append(food)
                score += weight
                continue
            swap = _swap_for(food, have, allergens)
            if swap:
                swaps.append(swap)
                score += weight * 0.7
            else:
                missing.append(food)
        if not any(FOODS[f].role == "main" for f in used) or len(missing) > max_missing:
            continue
        kit_missing, kit_swaps = [], []
        for utensil in raw["utensils"]:
            if utensil not in kit:
                swap = _utensil_swap(utensil, kit)
                (kit_swaps.append(swap) if swap else kit_missing.append(utensil))
        if kit_missing and not allow_other_utensils:
            continue
        final = score / max(total, 1) - 0.25 * len(kit_missing)
        matches.append(RecipeMatch(recipe=recipe, score=final, have=used, missing_ingredients=missing, ingredient_swaps=swaps,
                                   missing_utensils=kit_missing, utensil_swaps=kit_swaps))
    matches.sort(key=lambda m: (-m.score, len(m.missing_ingredients), m.recipe.title))
    return matches[:count], removed


def _in_list(item: str, available: list[str]) -> bool:
    words = {w for w in norm_words(item) if len(w) > 2}
    for option in available:
        other = {w for w in norm_words(option) if len(w) > 2}
        if other and (other <= words or words <= other):
            return True
    return False


def match_ai_recipe(recipe: Recipe, ingredients: list[str], utensils: list[str], basics: bool = True) -> RecipeMatch:
    """Check an AI recipe against what the user said they have."""
    have, _ = recognise_ingredients(ingredients)
    kit, _ = recognise_utensils(utensils)
    if basics:
        kit |= set(BASIC_UTENSILS)
    used, missing = [], []
    for item in recipe.ingredients:
        known = resolve_food(item.name)
        if known & STAPLES:
            continue
        if known & have or _in_list(item.name, ingredients):
            used.append(item.name)
        else:
            missing.append(item.name)
    kit_missing = [u for u in recipe.utensils if not (resolve_utensil(u) & kit or _in_list(u, utensils))]
    return RecipeMatch(recipe=recipe, score=1.0, have=used, missing_ingredients=missing, missing_utensils=kit_missing)


def find_alternatives(item: str, kind: str, allergens: list[str]) -> AlternativeResult:
    allergens = expand_allergens(allergens)
    entries = []
    if kind == "utensil":
        for utensil in sorted(resolve_utensil(item)):
            entries += UTENSIL_ALTERNATIVES.get(utensil, [])
        converted = [Alternative(name=e["name"], how_to_use=e["how_to_use"], ratio_or_adjustment=e["ratio_or_adjustment"]) for e in entries]
    else:
        for food in sorted(resolve_food(item)):
            entries += INGREDIENTS.get(food, [])
        seen, converted = set(), []
        for e in entries:
            if e["name"] not in seen:
                seen.add(e["name"])
                converted.append(Alternative(**e))
    safe, removed = filter_alternatives(converted, allergens)
    url = "https://www.google.com/search?q=" + quote_plus(f"substitute for {item} famous cookbook")
    return AlternativeResult(item=item, kind=kind, alternatives=safe, removed_for_allergens=removed, search_url=url, origin="built-in")
