from fastapi import APIRouter, HTTPException, status
from app.schemas import (
    GenerateRecipeRequest,
    GenerateRecipeResponse,
    PantryIngredient,
    RecipePreferences,
    DietaryRestriction,
    MealType,
    DifficultyLevel
)
from app.services.recipe_service import recipe_service

router = APIRouter(prefix="/recipes", tags=["Recipes"])


@router.post(
    "/generate",
    response_model=GenerateRecipeResponse,
    status_code=status.HTTP_200_OK,
    summary="Eldeki malzemelere göre AI tarif ve alışveriş listesi üret"
)
async def generate_recipe(request: GenerateRecipeRequest):
    try:
        response = await recipe_service.create_recipe_workflow(request)
        return response
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get(
    "/sample-payload",
    response_model=GenerateRecipeRequest,
    summary="Swagger'da test etmek için hazır örnek istek gövdesi"
)
def get_sample_payload():
    """Hocanın veya geliştiricinin tek tıkla test edebilmesi için örnek veri."""
    return GenerateRecipeRequest(
        pantry_items=[
            PantryIngredient(name="Yumurta", amount="3 adet"),
            PantryIngredient(name="Kültür Mantarı", amount="200 gr"),
            PantryIngredient(name="Bebek Ispanak", amount="1 demet"),
            PantryIngredient(name="Kaşar Peyniri", amount="100 gr")
        ],
        preferences=RecipePreferences(
            dietary_restrictions=[DietaryRestriction.GLUTEN_FREE, DietaryRestriction.REFINED_SUGAR_FREE],
            allergies=["Fıstık"],
            meal_type=MealType.DINNER,
            max_prep_time_minutes=30,
            servings=2,
            difficulty=DifficultyLevel.EASY,
            cuisine_type="Akdeniz"
        )
    )