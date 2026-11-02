"""Built-in food table. Nutrition values are approximate, per 100 g, for estimates only."""
from __future__ import annotations

import re
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Food:
    name: str
    cat: str  # m meat, f fish/seafood, d dairy, e egg, h honey, v plant
    role: str  # main, season, staple
    # kcal, protein, carbs, fat, saturated fat, sugar, fibre, sodium (mg)
    n: tuple
    aliases: tuple = ()
    each: float = 0  # grams per countable item
    unit: str = ""  # label for a countable item, such as clove
    hidden: tuple = ()  # allergens that may be present but are not in the name
    tsp: float = 5  # grams per teaspoon


GLUTEN = "Wheat / gluten"
_F = [
    Food("chicken breast", "m", "main", (120, 22.5, 0, 2.6, .6, 0, 0, 45), ("chicken", "ayam", "chicken fillet")),
    Food("chicken thigh", "m", "main", (120, 19.7, 0, 4.3, 1.1, 0, 0, 85), ("chicken", "ayam", "boneless chicken")),
    Food("lean beef", "m", "main", (170, 21, 0, 9, 3.6, 0, 0, 60), ("beef", "daging", "daging lembu", "steak")),
    Food("lean minced beef", "m", "main", (176, 20, 0, 10, 4, 0, 0, 66), ("beef", "mince", "minced beef", "ground beef", "daging cincang")),
    Food("white fish fillet", "f", "main", (90, 19, 0, 1, .2, 0, 0, 60), ("fish", "ikan", "white fish", "fish fillet", "tilapia", "snapper", "grouper", "cod")),
    Food("salmon fillet", "f", "main", (208, 20, 0, 13, 3, 0, 0, 59), ("salmon",)),
    Food("canned tuna in water", "f", "main", (90, 20, 0, .8, .2, 0, 0, 250), ("tuna", "canned tuna", "tin tuna")),
    Food("canned sardines in tomato sauce", "f", "main", (185, 20, 1, 10, 2.5, 1, 0, 400), ("sardine", "canned sardine", "tin sardine")),
    Food("prawns", "f", "main", (85, 20, 0, .5, .1, 0, 0, 120), ("prawn", "shrimp", "udang")),
    Food("egg", "e", "main", (143, 12.6, .7, 9.5, 3.1, .4, 0, 142), ("eggs", "telur"), each=50),
    Food("firm tofu", "v", "main", (144, 17, 3, 9, 1.3, .6, 2, 14), ("tofu", "tauhu", "bean curd")),
    Food("tempeh", "v", "main", (192, 20, 8, 11, 2.2, 0, 0, 9), ("tempe",)),
    Food("red lentils", "v", "main", (352, 25, 63, 1, .2, 2, 11, 6), ("lentil", "dhal", "dal")),
    Food("canned chickpeas", "v", "main", (139, 7, 23, 2.5, .3, 4, 6, 240), ("chickpea", "kacang kuda")),
    Food("canned kidney beans", "v", "main", (100, 7, 18, .5, .1, 2, 6, 240), ("kidney bean", "red bean")),
    Food("plain low-fat yoghurt", "d", "main", (73, 10, 4, 2, 1.2, 4, 0, 36), ("yoghurt", "yogurt", "greek yogurt", "greek yoghurt")),
    Food("low-fat milk", "d", "main", (47, 3.4, 5, 1.5, 1, 5, 0, 44), ("milk", "susu")),
    Food("cheddar cheese", "d", "season", (403, 25, 1.3, 33, 21, .5, 0, 620), ("cheese", "keju")),
    Food("brown rice", "v", "main", (360, 7.5, 76, 2.7, .5, .8, 3.5, 5), ("rice", "beras", "nasi")),
    Food("white rice", "v", "main", (360, 6.7, 80, .6, .2, .1, 1.3, 1), ("rice", "beras", "nasi", "jasmine rice")),
    Food("rice noodles", "v", "main", (360, 6, 80, .6, .2, 0, 1.6, 180), ("rice vermicelli", "bihun", "beehoon", "vermicelli", "kway teow", "rice noodle")),
    Food("wholewheat pasta", "v", "main", (350, 13, 70, 2.5, .5, 3, 10, 6), ("pasta", "spaghetti", "macaroni", "penne")),
    Food("wholewheat noodles", "v", "main", (350, 13, 70, 2.5, .5, 3, 8, 200), ("noodles", "noodle", "mee", "mi", "egg noodles")),
    Food("wholemeal bread", "v", "main", (250, 12, 42, 3.5, .7, 5, 7, 450), ("bread", "roti", "toast"), each=40, unit="slice"),
    Food("wholemeal tortilla wrap", "v", "main", (290, 9, 48, 7, 2.5, 2, 6, 600), ("tortilla", "wrap", "wraps"), each=60),
    Food("rolled oats", "v", "main", (380, 13, 67, 7, 1.2, 1, 10, 5), ("oat", "oatmeal"), hidden=(GLUTEN,)),
    Food("wholemeal flour", "v", "season", (340, 13, 72, 2.5, .4, .4, 11, 2), ("flour", "tepung", "wheat flour")),
    Food("potato", "v", "main", (77, 2, 17, .1, 0, .8, 2.2, 6), ("kentang",), each=150),
    Food("sweet potato", "v", "main", (86, 1.6, 20, .1, 0, 4.2, 3, 55), ("ubi", "keledek"), each=150),
    Food("broccoli", "v", "main", (34, 2.8, 7, .4, 0, 1.7, 2.6, 33)),
    Food("carrot", "v", "main", (41, .9, 10, .2, 0, 4.7, 2.8, 69), ("lobak merah",), each=80),
    Food("onion", "v", "season", (40, 1.1, 9, .1, 0, 4.2, 1.7, 4), ("bawang besar", "red onion", "brown onion"), each=100),
    Food("shallot", "v", "season", (72, 2.5, 17, .1, 0, 8, 3, 12), ("bawang merah",), each=15),
    Food("garlic", "v", "season", (149, 6.4, 33, .5, .1, 1, 2.1, 17), ("bawang putih",), each=5, unit="clove"),
    Food("ginger", "v", "season", (80, 1.8, 18, .8, .2, 1.7, 2, 13), ("halia",)),
    Food("tomato", "v", "main", (18, .9, 3.9, .2, 0, 2.6, 1.2, 5), ("tomato fresh",), each=120),
    Food("canned chopped tomatoes", "v", "main", (32, 1.6, 7, .3, 0, 4, 1.5, 130), ("canned tomato", "tin tomato", "chopped tomato")),
    Food("cucumber", "v", "main", (15, .7, 3.6, .1, 0, 1.7, .5, 2), ("timun",), each=200),
    Food("bell pepper", "v", "main", (31, 1, 6, .3, 0, 4.2, 2.1, 4), ("capsicum", "pepper fresh", "red pepper", "green pepper"), each=150),
    Food("cabbage", "v", "main", (25, 1.3, 6, .1, 0, 3.2, 2.5, 18), ("kobis", "kubis", "chinese cabbage")),
    Food("kangkung", "v", "main", (19, 2.6, 3.1, .2, 0, 0, 2.1, 113), ("water spinach", "morning glory")),
    Food("spinach", "v", "main", (23, 2.9, 3.6, .4, .1, .4, 2.2, 79), ("bayam",)),
    Food("long beans", "v", "main", (47, 2.8, 8, .4, 0, 2, 3, 4), ("long bean", "green bean", "french bean", "kacang panjang")),
    Food("eggplant", "v", "main", (25, 1, 6, .2, 0, 3.5, 3, 2), ("aubergine", "terung", "brinjal"), each=250),
    Food("okra", "v", "main", (33, 1.9, 7.5, .2, 0, 1.5, 3.2, 7), ("lady finger", "lady's finger", "bendi")),
    Food("mushrooms", "v", "main", (22, 3.1, 3.3, .3, .1, 2, 1, 5), ("mushroom", "cendawan")),
    Food("sweet corn", "v", "main", (86, 3.3, 19, 1.4, .2, 3.2, 2.7, 15), ("corn", "jagung")),
    Food("green peas", "v", "main", (81, 5.4, 14, .4, .1, 5.7, 5, 5), ("pea", "peas", "frozen peas")),
    Food("pumpkin", "v", "main", (26, 1, 6.5, .1, .1, 2.8, .5, 1), ("labu", "squash")),
    Food("bean sprouts", "v", "main", (30, 3, 6, .2, 0, 4, 1.8, 6), ("beansprout", "bean sprout", "taugeh", "tauge")),
    Food("lettuce", "v", "main", (15, 1.4, 2.9, .2, 0, .8, 1.3, 28), ("salad leaves",)),
    Food("avocado", "v", "main", (160, 2, 8.5, 14.7, 2.1, .7, 6.7, 7), ("avocado",), each=140),
    Food("banana", "v", "main", (89, 1.1, 23, .3, .1, 12, 2.6, 1), ("pisang",), each=100),
    Food("apple", "v", "main", (52, .3, 14, .2, 0, 10, 2.4, 1), (), each=150),
    Food("mango", "v", "main", (60, .8, 15, .4, .1, 14, 1.6, 1), ("mangga",)),
    Food("pineapple", "v", "main", (50, .5, 13, .1, 0, 10, 1.4, 1), ("nanas",)),
    Food("fresh chilli", "v", "season", (40, 2, 9, .4, 0, 5, 1.5, 9), ("chilli", "chili", "cili", "lada", "red chilli"), each=10),
    Food("spring onion", "v", "season", (32, 1.8, 7, .2, 0, 2.3, 2.6, 16), ("scallion", "daun bawang"), each=15),
    Food("coriander leaves", "v", "season", (23, 2.1, 3.7, .5, 0, .9, 2.8, 46), ("cilantro", "coriander", "daun ketumbar")),
    Food("lemongrass", "v", "season", (99, 1.8, 25, .5, .1, 0, 0, 6), ("serai",), each=20, unit="stalk"),
    Food("lime", "v", "season", (30, .7, 10, .2, 0, 1.7, 2.8, 2), ("limau", "calamansi", "lime juice"), each=45),
    Food("lemon", "v", "season", (29, 1.1, 9, .3, 0, 2.5, 2.8, 2), ("lemon juice",), each=60),
    Food("water", "v", "staple", (0, 0, 0, 0, 0, 0, 0, 0)),
    Food("salt", "v", "staple", (0, 0, 0, 0, 0, 0, 0, 38700), ("garam",), tsp=6),
    Food("black pepper", "v", "staple", (250, 10, 64, 3, 1, .6, 25, 20), ("pepper", "lada hitam"), tsp=2.5),
    Food("cooking oil", "v", "staple", (884, 0, 0, 100, 8, 0, 0, 0), ("oil", "minyak", "vegetable oil", "canola oil")),
    Food("olive oil", "v", "season", (884, 0, 0, 100, 14, 0, 0, 2)),
    Food("sesame oil", "v", "season", (884, 0, 0, 100, 14, 0, 0, 0)),
    Food("light soy sauce", "v", "season", (57, 8, 6, 0, 0, 1, .5, 5500), ("soy sauce", "kicap", "soya sauce")),
    Food("fish sauce", "f", "season", (35, 5, 4, 0, 0, 4, 0, 7800), ("budu",)),
    Food("oyster sauce", "f", "season", (51, 1.4, 11, .3, 0, 7, .1, 2700)),
    Food("tomato paste", "v", "season", (82, 4.3, 19, .5, .1, 12, 4, 60), ("tomato puree",)),
    Food("ground turmeric", "v", "season", (312, 10, 67, 3.2, 1.8, 3.2, 22, 27), ("turmeric", "kunyit"), tsp=2.5),
    Food("curry powder", "v", "season", (325, 14, 56, 14, 2.2, 2.8, 53, 52), ("serbuk kari", "curry"), hidden=("Mustard", "Celery"), tsp=2.5),
    Food("ground cumin", "v", "season", (375, 18, 44, 22, 1.5, 2.3, 11, 168), ("cumin", "jintan"), tsp=2.5),
    Food("ground coriander", "v", "season", (298, 12, 55, 18, 1, 0, 42, 35), ("ketumbar",), tsp=2.5),
    Food("chilli powder", "v", "season", (282, 13, 50, 14, 2.5, 7, 35, 90), ("chili powder", "cili serbuk", "paprika"), tsp=2.5),
    Food("ground cinnamon", "v", "season", (247, 4, 81, 1.2, .3, 2.2, 53, 10), ("cinnamon", "kayu manis"), tsp=2.5),
    Food("vinegar", "v", "season", (19, 0, 1, 0, 0, .4, 0, 5), ("cuka",)),
    Food("honey", "h", "season", (304, .3, 82, 0, 0, 82, .2, 4), ("madu",), tsp=7),
    Food("peanuts", "v", "season", (567, 26, 16, 49, 7, 4, 8.5, 18), ("peanut", "kacang tanah", "groundnut")),
    Food("sesame seeds", "v", "season", (573, 18, 23, 50, 7, 0, 12, 11), ("sesame", "bijan"), tsp=3),
    Food("almonds", "v", "season", (579, 21, 22, 50, 3.8, 4.4, 12.5, 1), ("almond", "badam")),
    Food("light coconut milk", "v", "main", (70, .7, 2.5, 6.5, 5.5, 1, 0, 40), ("coconut milk", "santan")),
    Food("belacan", "f", "season", (200, 35, 10, 2, 1, 2, 0, 7000), ("shrimp paste",)),
    Food("tamarind paste", "v", "season", (239, 2.8, 62, .6, .3, 57, 5, 28), ("tamarind", "asam jawa")),
]
FOODS = {f.name: f for f in _F}
STAPLES = {f.name for f in _F if f.role == "staple"}


def norm_words(text: str) -> list[str]:
    words = re.findall(r"[a-z]+", text.lower())
    out = []
    for w in words:
        if w.endswith("oes"):
            w = w[:-2]
        elif w.endswith("ies") and len(w) > 4:
            w = w[:-3] + "y"
        elif w.endswith("s") and not w.endswith("ss") and len(w) > 3:
            w = w[:-1]
        out.append(w)
    return out


def _contains(words: list[str], phrase: list[str]) -> bool:
    n = len(phrase)
    return any(words[i:i + n] == phrase for i in range(len(words) - n + 1))


def resolve_food(text: str) -> set[str]:
    """Return the food names meant by the text, preferring the longest matching name."""
    words = norm_words(text)
    best, found = 0, set()
    for food in _F:
        for alias in (food.name, *food.aliases):
            phrase = norm_words(alias)
            if phrase and _contains(words, phrase):
                if len(phrase) > best:
                    best, found = len(phrase), {food.name}
                elif len(phrase) == best:
                    found.add(food.name)
    return found


UTENSILS: dict[str, tuple] = {
    "pan": ("frying pan", "pan", "wok", "kuali", "skillet", "non stick pan"),
    "pot": ("pot", "saucepan", "periuk", "stock pot", "casserole"),
    "oven": ("oven", "air fryer", "ketuhar"),
    "baking tray": ("baking tray", "baking sheet", "oven tray", "baking dish", "roasting tin", "tray"),
    "steamer": ("steamer", "pengukus", "steaming rack"),
    "grill": ("grill", "griddle", "griddle pan", "bbq", "barbecue", "pemanggang"),
    "blender": ("blender", "food processor", "mortar and pestle", "lesung", "mortar", "mixer", "pengisar"),
    "mixing bowl": ("mixing bowl", "bowl", "mangkuk", "large bowl"),
    "rice cooker": ("rice cooker", "periuk nasi"),
    "knife": ("knife", "pisau"),
    "chopping board": ("chopping board", "cutting board", "papan pemotong"),
    "spoon": ("spoon", "sudu", "spatula", "ladle", "wooden spoon", "senduk"),
    "foil": ("foil", "aluminium foil", "banana leaf", "baking paper", "parchment"),
}
BASIC_UTENSILS = ("knife", "chopping board", "spoon", "mixing bowl")


def resolve_utensil(text: str) -> set[str]:
    words = norm_words(text)
    best, found = 0, set()
    for name, aliases in UTENSILS.items():
        for alias in (name, *aliases):
            phrase = norm_words(alias)
            if _contains(words, phrase):
                if len(phrase) > best:
                    best, found = len(phrase), {name}
                elif len(phrase) == best:
                    found.add(name)
    return found


def parse_amount(spec: str):
    """Parse 'food:300', 'food:2 tsp' or 'food:2'. Return food, quantity and unit."""
    name, _, amount = spec.partition(":")
    parts = amount.split()
    return name, float(parts[0]), parts[1] if len(parts) > 1 else ""


def grams(food: Food, qty: float, unit: str) -> float:
    if unit == "tsp":
        return qty * food.tsp
    if unit == "tbsp":
        return qty * food.tsp * 3
    if food.each:
        return qty * food.each
    return qty


def _number(value: float) -> str:
    value = round(value * 4) / 4 or 0.25
    whole, frac = int(value), value - int(value)
    tail = {0.25: "¼", 0.5: "½", 0.75: "¾"}.get(frac, "")
    return f"{whole}{tail}" if whole and tail else tail or str(whole)


def format_amount(food: Food, qty: float, unit: str) -> tuple[str, str]:
    """Return the amount text and the ingredient name in the right singular or plural form."""
    if unit in ("tsp", "tbsp"):
        return f"{_number(qty)} {unit}", food.name
    if food.each:
        plural = qty > 1
        if food.unit:
            label = food.unit + ("s" if plural else "")
            return f"{_number(qty)} {label}", food.name
        name = food.name + ("es" if plural and food.name.endswith("o") else "s" if plural else "")
        return _number(qty), name
    rounded = max(5, round(qty / 5) * 5)
    return (f"{rounded} ml" if food.name in ("water", "low-fat milk", "light coconut milk") else f"{rounded} g"), food.name
