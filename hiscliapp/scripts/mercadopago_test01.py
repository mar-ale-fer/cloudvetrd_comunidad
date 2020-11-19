import mercadopago
import json
#fuente
#https://www.mercadopago.com.ar/developers/es/plugins_sdks/sdks/official/python/

# produccion --> MERCADOPAGO_ACCESS_TOKEN='TEST-6015287505031146-042317-7bcefbd149244d8721aa1deeaa3af24f-198115648'
MERCADOPAGO_CLIENT_ID= '7580862969623751' #vendedor de prueba
MERCADOPAGO_CLIENT_SECRET= '88t4Ij3mgBF6UA59GuY2r8SyFuYTLUr4' #vendedor de prueba

#mp = mercadopago.MP("ACCESS_TOKEN")
mp = mercadopago.MP(MERCADOPAGO_CLIENT_ID, MERCADOPAGO_CLIENT_SECRET)

def run():
    preference = {
        "items": [
            {
                "id":"redivetpremium",
                "title": "un mes del plan redi-vet premium TEST 3",
                "quantity": 1,
                "currency_id": "USD",
                "unit_price": 0.5
            }
        ],
        "payer": {
            "email": 'test_user_50347152@testuser.com'
        }        
    }

    preferenceResult = mp.create_preference(preference)

    print(json.dumps(preferenceResult, indent=4))