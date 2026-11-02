# Healthy Recipe Generator

A Streamlit app that creates healthy recipes from the ingredients and utensils you have. Users don't need their own key: the owner's Gemini key is stored privately in Streamlit Secrets.

- Creates recipes with Google Gemini and falls back to 52 built-in recipes if AI is unavailable
- Finds alternatives with Google Search, looking first for famous cookbooks, and lists the sources found
- Asks about allergens from a list, with a box for anything not listed, and removes recipes that match
- Suggests healthy add-ons and shows estimated calories and nutrition
- Downloads each recipe as an A4 PDF with credited photos when available

## Put it online

1. Create a key at <https://aistudio.google.com/apikey>. Never put it in a GitHub file.
2. Upload everything in this folder to a GitHub repository.
3. At <https://share.streamlit.io>, deploy the repository with `app.py` as the main file.
4. In **Settings > Secrets**, add:

   ```toml
   GEMINI_API_KEY = "your-key"
   ```

## Limits

Everyone shares your Gemini quota, and any paid usage goes on your account. The app allows 15 AI requests per browser session and 200 per day across the app until it restarts, then uses built-in data. Set `DAILY_AI_LIMIT` in Secrets to change the daily limit. These are simple safeguards, so also check your usage and any billing in Google's dashboard.

Gemini's free tier may let Google use submitted content to improve its products. Check Google's current terms, and tell users not to enter personal details.

## Run it on your computer

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Add a recipe

Add an `R(...)` entry to `recipe_core/recipes.py`, written for 2 servings. Any new ingredient must also be added to `recipe_core/foods.py`. Then run the tests:

```bash
pip install pytest
python -m pytest tests
```

The PDF test also needs `pdftotext` from Poppler.

## Good to know

- **Allergens:** the check looks for known food words and some likely hidden allergens, so it can't catch everything. Always read product labels and check for cross-contamination.
- **Nutrition:** AI and food-table figures are estimates, not lab values or medical advice.
- **Recipes:** AI and built-in recipes haven't been kitchen-tested. Built-in recipes were written for this app and aren't taken from any cookbook.
- **Alternatives:** full cookbooks are often not freely available online, so check the source links. The fallback list isn't taken from any cookbook.
- **Halal:** the recipes use no pork or alcohol, but users should choose halal-certified meat and products.
- **Images:** photos come from Wikimedia Commons under free licences and are credited. They show a similar dish, not the exact recipe, and some recipes may have no photo.

Fonts: DejaVu, see <https://dejavu-fonts.github.io/License.html>.
