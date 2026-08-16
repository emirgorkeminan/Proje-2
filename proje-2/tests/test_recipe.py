import pytest
from app.schemas import (
    Recipe,
    RecipeIngredient,
    CookingStep,
    NutritionEstimate,
    IngredientCategory,
    DifficultyLevel
)
from app.services.recipe_service import recipe_service


@pytest.fixture
def dummy_recipe():
    return Recipe(
        title="Mantarlı Ispanaklı Omlet",
        description="Harika bir pratik kahvaltılık.",
        prep_time_minutes=5,
        cook_time_minutes=10,
        total_time_minutes=15,
        servings=2,
        difficulty=DifficultyLevel.EASY,
        ingredients=[
            RecipeIngredient(name="Yumurta", amount="3 adet", category=IngredientCategory.DAIRY, is_in_pantry=True),
            RecipeIngredient(name="Mantar", amount="150 gr", category=IngredientCategory.PRODUCE, is_in_pantry=True),
            RecipeIngredient(name="Zeytinyağı", amount="1 yemek kaşığı", category=IngredientCategory.SPICES_OILS, is_in_pantry=False),
            RecipeIngredient(name="Tuz", amount="1 çay kaşığı", category=IngredientCategory.PANTRY, is_in_pantry=True),
        ],
        steps=[
            CookingStep(step_number=1, title="Soteleme", instruction="Mantarları soteleyin.", duration_minutes=5)
        ],
        nutrition=NutritionEstimate(calories=220, protein_g=14.0, carbs_g=3.0, fat_g=16.0, fiber_g=1.0)
    )


def test_calculate_pantry_match_and_shopping_list(dummy_recipe):
    # 4 malzemeden 3'ü kilerde (is_in_pantry=True), 1'i eksik (Zeytinyağı)
    match_rate, shopping_list = recipe_service.calculate_pantry_match_and_shopping_list(dummy_recipe)

    # %75 eşleşme oranı beklenir
    assert match_rate == 75.0
    assert len(shopping_list) == 1
    assert shopping_list[0].name == "Zeytinyağı"
    assert shopping_list[0].category == IngredientCategory.SPICES_OILS