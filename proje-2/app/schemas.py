from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field, ConfigDict


# ==========================================
# 1. ENUMLAR
# ==========================================

class DietaryRestriction(str, Enum):
    NONE = "none"
    GLUTEN_FREE = "gluten_free"
    REFINED_SUGAR_FREE = "refined_sugar_free"
    VEGAN = "vegan"
    VEGETARIAN = "vegetarian"
    KETOGENIC = "ketogenic"
    PALEO = "paleo"
    DAIRY_FREE = "dairy_free"


class MealType(str, Enum):
    BREAKFAST = "breakfast"
    LUNCH = "lunch"
    DINNER = "dinner"
    SNACK = "snack"
    DESSERT = "dessert"


class DifficultyLevel(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class IngredientCategory(str, Enum):
    PRODUCE = "produce"          # Sebze / Meyve
    DAIRY = "dairy"              # Süt Ürünleri
    MEAT_POULTRY = "meat"        # Et / Tavuk / Balık
    PANTRY = "pantry"            # Kiler / Bakliyat / Temel Gıda
    SPICES_OILS = "spices_oils"  # Baharat / Sıvı Yağ
    BAKERY = "bakery"            # Unlu Mamuller
    OTHER = "other"


# ==========================================
# 2. GİRDİ MODELLERİ (REQUEST)
# ==========================================

class PantryIngredient(BaseModel):
    name: str = Field(..., description="Malzeme adı (örn: Yumurta)")
    amount: Optional[str] = Field(None, description="Mevcut miktar (örn: 3 adet)")


class RecipePreferences(BaseModel):
    dietary_restrictions: List[DietaryRestriction] = Field(
        default_factory=lambda: [DietaryRestriction.NONE],
        description="Diyet kısıtlamaları listesi"
    )
    allergies: List[str] = Field(
        default_factory=list,
        description="Kullanılmaması gereken alerjen maddeler"
    )
    meal_type: MealType = Field(MealType.DINNER, description="Öğün türü")
    max_prep_time_minutes: int = Field(45, ge=5, le=180, description="Maksimum toplam süre (dakika)")
    servings: int = Field(2, ge=1, le=10, description="Porsiyon / Kişi sayısı")
    difficulty: DifficultyLevel = Field(DifficultyLevel.MEDIUM, description="Zorluk seviyesi")
    cuisine_type: Optional[str] = Field("Akdeniz", description="Mutfak türü / konsept")


class GenerateRecipeRequest(BaseModel):
    pantry_items: List[PantryIngredient] = Field(
        ...,
        min_length=1,
        description="Kullanıcının elindeki mevcut malzemeler"
    )
    preferences: RecipePreferences = Field(
        default_factory=RecipePreferences,
        description="Kullanıcı tercihleri ve kısıtları"
    )


# ==========================================
# 3. ÇIKTI MODELLERİ (RESPONSE & LLM STRUCTURED)
# ==========================================

class NutritionEstimate(BaseModel):
    calories: int = Field(..., description="Porsiyon başına tahmini kalori (kcal)")
    protein_g: float = Field(..., description="Porsiyon başına protein (g)")
    carbs_g: float = Field(..., description="Porsiyon başına karbonhidrat (g)")
    fat_g: float = Field(..., description="Porsiyon başına yağ (g)")
    fiber_g: Optional[float] = Field(0.0, description="Lif miktarı (g)")


class RecipeIngredient(BaseModel):
    name: str = Field(..., description="Malzemenin adı")
    amount: str = Field(..., description="Tarif için gereken miktar")
    category: IngredientCategory = Field(IngredientCategory.PANTRY, description="Reyon / kategori")
    is_in_pantry: bool = Field(..., description="Kullanıcının kilerinde var mı?")


class CookingStep(BaseModel):
    step_number: int = Field(..., ge=1, description="Adım sırası")
    title: str = Field(..., description="Adım başlığı")
    instruction: str = Field(..., description="Detaylı talimat")
    duration_minutes: Optional[int] = Field(None, description="Tahmini adım süresi (dk)")
    chef_tip: Optional[str] = Field(None, description="Şefin püf noktası")


class Recipe(BaseModel):
    title: str = Field(..., description="Tarifin adı")
    description: str = Field(..., description="Kısa ve iştah açıcı özet")
    prep_time_minutes: int = Field(..., description="Hazırlık süresi")
    cook_time_minutes: int = Field(..., description="Pişirme süresi")
    total_time_minutes: int = Field(..., description="Toplam süre")
    servings: int = Field(..., description="Porsiyon sayısı")
    difficulty: DifficultyLevel = Field(..., description="Zorluk seviyesi")
    ingredients: List[RecipeIngredient] = Field(..., description="Tüm malzeme listesi")
    steps: List[CookingStep] = Field(..., description="Yapılış adımları")
    nutrition: NutritionEstimate = Field(..., description="Besin değerleri tahmini")


class ShoppingItem(BaseModel):
    name: str = Field(..., description="Satın alınması gereken eksik malzeme")
    amount: str = Field(..., description="Satın alınacak önerilen miktar")
    category: IngredientCategory = Field(..., description="Reyon kategorisi")


class GenerateRecipeResponse(BaseModel):
    recipe: Recipe = Field(..., description="Üretilen tarif")
    shopping_list: List[ShoppingItem] = Field(
        default_factory=list,
        description="Eksik malzemelerden türetilen alışveriş listesi"
    )
    pantry_match_rate_percentage: float = Field(
        ...,
        ge=0.0,
        le=100.0,
        description="Eldeki malzemelerin tarifi karşılama oranı (%)"
    )

    model_config = ConfigDict(extra="ignore")