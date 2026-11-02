"""Data structures shared across the app."""
from __future__ import annotations

from pydantic import BaseModel, Field


class Ingredient(BaseModel):
    name: str
    amount: str = ""
    healthy_note: str = ""


class Nutrition(BaseModel):
    calories_per_serving: float = Field(ge=0)
    protein_g: float = Field(ge=0)
    carbs_g: float = Field(ge=0)
    fat_g: float = Field(ge=0)
    saturated_fat_g: float = Field(ge=0)
    sugar_g: float = Field(ge=0)
    fibre_g: float = Field(ge=0)
    sodium_mg: float = Field(ge=0)


class Recipe(BaseModel):
    title: str
    description: str
    servings: int = Field(ge=1)
    prep_minutes: int = Field(ge=0)
    cook_minutes: int = Field(ge=0)
    difficulty: str = "Easy"
    ingredients: list[Ingredient]
    utensils: list[str]
    steps: list[str]
    nutrition: Nutrition
    healthy_choices: list[str] = []
    add_on_suggestions: list[str] = []
    allergens_present: list[str] = []
    hidden_allergens: list[str] = []
    meal: str = "Lunch or dinner"
    origin: str = "built-in"
    dish_image_search: str = ""
    ingredient_image_searches: list[str] = []

    @property
    def total_minutes(self) -> int:
        return self.prep_minutes + self.cook_minutes

    @property
    def total_calories(self) -> float:
        return self.nutrition.calories_per_serving * self.servings


class RecipeBatch(BaseModel):
    recipes: list[Recipe]


class Source(BaseModel):
    title: str
    url: str


class Alternative(BaseModel):
    name: str
    how_to_use: str
    ratio_or_adjustment: str = ""
    healthier_note: str = ""
    cookbook_or_site: str = ""


class AlternativeBatch(BaseModel):
    alternatives: list[Alternative]


class AlternativeResult(BaseModel):
    item: str
    kind: str
    alternatives: list[Alternative] = []
    removed_for_allergens: list[str] = []
    search_url: str = ""
    sources: list[Source] = []
    origin: str = "built-in"


class RecipeMatch(BaseModel):
    recipe: Recipe
    score: float
    have: list[str] = []
    missing_ingredients: list[str] = []
    ingredient_swaps: list[str] = []
    missing_utensils: list[str] = []
    utensil_swaps: list[str] = []


class RecipeImage(BaseModel):
    data: bytes
    label: str
    credit: str
    source_url: str
    is_dish: bool = False
