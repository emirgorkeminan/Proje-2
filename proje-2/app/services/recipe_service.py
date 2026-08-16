from typing import List, Tuple
from app.schemas import (
    GenerateRecipeRequest,
    GenerateRecipeResponse,
    Recipe,
    ShoppingItem
)
from app.services.llm_service import llm_service


class RecipeService:
    def calculate_pantry_match_and_shopping_list(self, recipe: Recipe) -> Tuple[float, List[ShoppingItem]]:
        """
        Tarifteki malzemeleri analiz eder:
        1. Kullanıcının elinde olmayanları alışveriş listesine dönüştürür.
        2. Kiler eşleşme oranını (%) hesaplar.
        """
        if not recipe.ingredients:
            return 0.0, []

        total_ingredients = len(recipe.ingredients)
        pantry_count = sum(1 for item in recipe.ingredients if item.is_in_pantry)

        match_rate = round((pantry_count / total_ingredients) * 100.0, 1)

        shopping_list = [
            ShoppingItem(
                name=item.name,
                amount=item.amount,
                category=item.category
            )
            for item in recipe.ingredients
            if not item.is_in_pantry
        ]

        return match_rate, shopping_list

    async def create_recipe_workflow(self, request: GenerateRecipeRequest) -> GenerateRecipeResponse:
        # 1. LLM'den structured tarifi al
        raw_recipe = await llm_service.generate_recipe_json(request)

        # 2. İş mantığını uygula (Eksik malzeme ve kiler oranı tespiti)
        match_rate, shopping_list = self.calculate_pantry_match_and_shopping_list(raw_recipe)

        # 3. Sonuç nesnesini birleştirip döndür
        return GenerateRecipeResponse(
            recipe=raw_recipe,
            shopping_list=shopping_list,
            pantry_match_rate_percentage=match_rate
        )


recipe_service = RecipeService()