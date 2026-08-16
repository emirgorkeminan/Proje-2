import json
import logging
from google import genai
import google.genai
from app.config import settings
from app.schemas import GenerateRecipeRequest, Recipe

logger = logging.getLogger(__name__)


class LLMService:
    def __init__(self):
        if settings.GEMINI_API_KEY:
            self.client = genai.Client(api_key=settings.GEMINI_API_KEY)
        else:
            self.client = None

    def _build_prompt(self, request: GenerateRecipeRequest) -> str:
        pantry_list_str = "\n".join(
            [f"- {item.name} ({item.amount if item.amount else 'Miktar belirtilmedi'})" for item in request.pantry_items]
        )
        dietary_str = ", ".join([d.value for d in request.preferences.dietary_restrictions])
        allergies_str = ", ".join(request.preferences.allergies) if request.preferences.allergies else "Yok"

        return f"""
Sen profesyonel bir şef ve beslenme uzmanısın. Kullanıcının elindeki malzemeleri öncelikli olarak kullanarak lezzetli, pratik ve sağlıklı bir yemek tarifi üretmelisin.

KULLANICININ ELİNDEKİ MALZEMELER:
{pantry_list_str}

KULLANICI TERCİHLERİ VE KISITLAMALARI:
- Diyet Kısıtlamaları: {dietary_str}
- Kesinlikle Kullanılmayacak Alerjenler: {allergies_str}
- Öğün Türü: {request.preferences.meal_type.value}
- Maksimum Süre: {request.preferences.max_prep_time_minutes} dakika
- Porsiyon: {request.preferences.servings} kişilik
- Zorluk Derecesi: {request.preferences.difficulty.value}
- Mutfak Stili: {request.preferences.cuisine_type}

KURALLAR:
1. Tarifin ana omurgasını kullanıcının elindeki malzemeler üzerine kur.
2. Eğer tarifin tamamlanması için elinde olmayan temel/tamamlayıcı malzemeler (örn: zeytinyağı, tuz, sarımsak, krema vb.) gerekiyorsa bunları da ekle ancak o malzemenin `is_in_pantry` değerini `false` olarak işaretle.
3. Kullanıcının elinde olan malzemeler için `is_in_pantry` değerini `true` olarak işaretle.
4. Alerjen listesinde belirtilen hiçbir malzemeyi veya türevini asla kullanma!
5. Porsiyon başına kalori ve makro besin değerlerini (protein, karbonhidrat, yağ) gerçekçi tahmin et.
6. Yanıtını STRICT JSON formatında, Recipe şemasına tam uyumlu olarak döndür.
"""

    async def generate_recipe_json(self, request: GenerateRecipeRequest) -> Recipe:
        if not self.client:
            raise ValueError("GEMINI_API_KEY tanımlanmamış. Lütfen .env dosyasını kontrol edin.")

        prompt = self._build_prompt(request)

        try:
            response = self.client.models.generate_content(
                model=settings.GEMINI_MODEL,
                contents=prompt,
                config=google.genai.types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=Recipe,
                    temperature=0.4,
                ),
            )

            response_text = response.text.strip()
            data = json.loads(response_text)
            return Recipe(**data)

        except Exception as e:
            logger.error(f"LLM Generation Error: {str(e)}")
            raise RuntimeError(f"Yemek tarifi üretilirken model hatası oluştu: {str(e)}")


llm_service = LLMService()