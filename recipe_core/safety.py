"""Allergen and nutrition checks for every recipe and alternative.

Matching is deliberately cautious: a false alarm removes a recipe, while a miss
could harm someone. No automatic check is complete, so the app still tells
users to read product labels.
"""
from __future__ import annotations

import re

from .models import Alternative, Recipe

ALLERGEN_KEYWORDS: dict[str, list[str]] = {
    "Milk / dairy": ["milk", "butter", "cheese", "cream", "yoghurt", "yogurt", "ghee", "whey", "casein",
                     "lactose", "custard", "condensed milk", "evaporated milk", "paneer", "mozzarella",
                     "parmesan", "cheddar", "feta", "dairy", "buttermilk"],
    "Eggs": ["egg", "mayonnaise", "mayo", "meringue", "albumen", "aioli"],
    "Peanuts": ["peanut", "groundnut", "satay sauce", "kacang"],
    "Tree nuts": ["almond", "cashew", "walnut", "pecan", "pistachio", "hazelnut", "macadamia", "brazil nut",
                  "pine nut", "praline", "marzipan", "chestnut", "nut"],
    "Fish": ["fish", "salmon", "tuna", "anchovy", "anchovies", "sardine", "mackerel", "cod", "tilapia", "snapper",
             "trout", "ikan", "ikan bilis", "budu", "worcestershire"],
    "Shellfish (crustaceans)": ["shellfish", "shrimp", "prawn", "crab", "lobster", "crayfish", "belacan", "shrimp paste",
                                "udang", "cincalok"],
    "Molluscs": ["shellfish", "mollusc", "mussel", "oyster", "clam", "squid", "octopus", "scallop", "cockle", "calamari", "sotong"],
    "Soy": ["soy", "soya", "tofu", "tempeh", "edamame", "miso", "kicap", "tamari", "tauhu", "teriyaki", "hoisin"],
    "Wheat / gluten": ["wheat", "flour", "bread", "breadcrumb", "pasta", "spaghetti", "noodle", "couscous", "semolina",
                       "barley", "rye", "gluten", "seitan", "soy sauce", "kicap", "tepung", "roti", "pastry",
                       "cracker", "tortilla", "bulgur", "mee", "oat", "oyster sauce", "hoisin", "teriyaki", "worcestershire"],
    "Sesame": ["sesame", "tahini", "bijan"],
    "Mustard": ["mustard"],
    "Celery": ["celery", "celeriac"],
    "Sulphites": ["sulphite", "sulfite", "wine", "dried apricot"],
    "Lupin": ["lupin", "lupine"],
}
COMMON_ALLERGENS = list(ALLERGEN_KEYWORDS)

# Phrases that contain an allergen word but are a different food. Only the named
# allergen ignores the phrase: almond milk is still a tree-nut hit.
SAFE_PHRASES: dict[str, list[str]] = {
    "Milk / dairy": ["coconut milk", "almond milk", "oat milk", "soy milk", "soya milk", "rice milk", "cashew milk",
                     "coconut cream", "peanut butter", "almond butter", "cashew butter", "cocoa butter",
                     "butter bean", "butternut", "cream of tartar", "buttercup"],
    "Tree nuts": ["coconut", "nutmeg", "water chestnut", "butternut", "tiger nut", "peanut", "groundnut"],
    "Wheat / gluten": ["rice flour", "corn flour", "cornflour", "chickpea flour", "almond flour", "coconut flour",
                       "tapioca flour", "potato flour", "oat flour", "rice noodle", "glass noodle",
                       "gluten-free", "gluten free", "breadfruit"],
    "Eggs": ["eggplant"],
}

# Per-serving targets set for this app; they are general guides, not medical advice.
HEALTH_LIMITS = {
    "calories_per_serving": (700, "kcal", "calories"),
    "saturated_fat_g": (7, "g", "saturated fat"),
    "sugar_g": (15, "g", "sugar"),
    "sodium_mg": (800, "mg", "sodium"),
}


def parse_items(text: str) -> list[str]:
    """Split comma, semicolon or line separated input and remove duplicates."""
    seen, items = set(), []
    for raw in re.split(r"[,;\n]+", text or ""):
        item = re.sub(r"\s+", " ", raw).strip(" .-•*\t")
        if item and item.lower() not in seen:
            seen.add(item.lower())
            items.append(item)
    return items


def _contains_term(text: str, term: str) -> bool:
    return re.search(rf"(?<![a-z]){re.escape(term.lower())}(?:s|es)?(?![a-z])", text) is not None


def find_allergen_hits(text: str, allergens: list[str]) -> list[str]:
    """Return every selected or custom allergen found in the text."""
    lower = re.sub(r"\s+", " ", (text or "").lower())
    hits = []
    for allergen in allergens:
        working = lower
        for phrase in SAFE_PHRASES.get(allergen, []):
            working = re.sub(rf"(?<![a-z]){re.escape(phrase)}(?:s|es)?(?![a-z])", " ", working)
        terms = ALLERGEN_KEYWORDS.get(allergen, [allergen])
        if any(_contains_term(working, term) for term in terms):
            hits.append(allergen)
    return hits


def expand_allergens(allergens: list[str]) -> list[str]:
    """Map typed allergens to the full listed groups, so 'gluten' also catches soy sauce."""
    groups = {"seafood": ["Fish", "Shellfish (crustaceans)", "Molluscs"], "shellfish": ["Shellfish (crustaceans)", "Molluscs"],
              "nut": ["Peanuts", "Tree nuts"], "nuts": ["Peanuts", "Tree nuts"]}
    out: list[str] = []
    for allergen in allergens:
        low = allergen.strip().lower()
        matched = list(groups.get(low, []))
        if not matched:
            for name, terms in ALLERGEN_KEYWORDS.items():
                singular = low[:-1] if low.endswith("s") else low
                if low == name.lower() or low in terms or singular in terms or low in re.split(r"[^a-z]+", name.lower()):
                    matched.append(name)
        for item in matched or [allergen]:
            if item not in out:
                out.append(item)
    return out


def recipe_allergen_hits(recipe: Recipe, allergens: list[str]) -> list[str]:
    parts = [recipe.title, recipe.description, *recipe.steps, *recipe.healthy_choices, *[i.name for i in recipe.ingredients]]
    hits = find_allergen_hits("\n".join(parts), allergens)
    hits += [a for a in recipe.hidden_allergens if a in allergens and a not in hits]
    return hits


def filter_alternatives(alternatives: list[Alternative], allergens: list[str]) -> tuple[list[Alternative], list[str]]:
    safe, removed = [], []
    for alt in alternatives:
        hits = find_allergen_hits(f"{alt.name} {alt.how_to_use}", allergens)
        if hits:
            removed.append(f"{alt.name} ({', '.join(hits)})")
        else:
            safe.append(alt)
    return safe, removed


def health_flags(recipe: Recipe) -> list[str]:
    flags = []
    for field, (limit, unit, label) in HEALTH_LIMITS.items():
        value = getattr(recipe.nutrition, field)
        if value > limit:
            flags.append(f"Higher in {label}: {value:.0f} {unit} per serving (app target: {limit} {unit} or less)")
    return flags


def calorie_mismatch(recipe: Recipe) -> bool:
    """True when stated calories disagree by over 20% with protein, carbs and fat."""
    n = recipe.nutrition
    computed = 4 * n.protein_g + 4 * n.carbs_g + 9 * n.fat_g
    return computed > 0 and abs(computed - n.calories_per_serving) / computed > 0.20
