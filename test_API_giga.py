import requests
from conftest import api_key, api_token

#token = 'Bearer eyJjdHkiOiJqd3QiLCJlbmMiOiJBMjU2Q0JDLUhTNTEyIiwiYWxnIjoiUlNBLU9BRVAtMjU2In0.r3HJKDCNtwFPy0oM3vE50ZxU03eVgnzrHKviM7qtgfNQW4og8Dn_b7b-_evELVfAPQg4KcMbA9Sb6jxZ1tQYJujQzHVOH0sns_5FOAYjEtRZ4WRIpgzn03QypYR0OMnFhY29ZdPfMUKwQdwniYU2RSc89MGK9-daYNGTfW4Oq_WaZJo7UdM7CCAseZa4iEazCJ7mwU96y8iJhhhKSFXFJdhINZvPCBReyLzN9nwowj-9UaW8fC3CzGa3I9XTEu6DWAJiZFXO0i4WtRrzjYLcLOjKJ8d3UqactWgrlTzGdxGWokxIuyOe9C-7Yzsf24bd5dAPDLIGt_aE9G9gbWJrbQ.ZIvZZtnyDt7ZuetIxmyC1g.hCbLMWmESJeFT-EaFwu2qLc5_sm408jeMnS-h6NEd9IVeb-U2ztnpWc6WK_nVTa7PsMM81Fh4bKzwymHocDM9D5I91OVMT-WlkxrjWOE-iVPwTfaePsR0TArvbcBjUaLno7i2hyV1IA8Fcbv1E07ez4HdtAF2lNZrGGUnuyUk6enysa0fsX7KlPNsHCLPbMQT_wRA0Qf7hvyjfA5r2nduIy8rGySorNTcMf1SF2DtmCdTUdO8Zn2azXVgu8XwF0JvnoQUXyFSliWq40TcLoh8biUzRcXPnV7sHUe1yMa9wMqfM2ynbwopOBQUbZiXWY8DYINITL5nZpNE1bVWzQT6AUYJk7iI_GRLGxxTOb2eGSMvv4daFLjeFSnkyHCLZH5mpe2fDGOC4yi8yLRafvS7M1UPqNQnzIbXKHY37LnZopHRYBWY0qJvIXEk1ieYS5bJQY3HmEQB98FEphnXw0Ey8Z8ZQVt7Q29dChTb4piM0VerqfYhhnakVerljrNaJx6nirfjbIGryGByGVejYgBeqqMOjiRRiIxXH9iBg0RW36CsvB3zGfkqcy29KlCmpwqwfDD_PF54FeqXvXVKbr9z6DvuITfktsVfwa6vy9xmgp10uJWip6FcQ_r3WNiA8hIKLGZy0CysDsYVNogFtUbkIctttbKQ6GzrdCYTi57O_nUTeFIrSCXiIO5iPucJ8JtUzPLYJN_n63BkEcngE5nt80NqJkH6GL4RnxPjhdSiok.R1w6aaRNUUTdf7xSc2kqaGMhXd1Ltt4fAQCVMMF_jiY'
def test_get_token(api_key):

    url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

    payload={
        'scope': 'GIGACHAT_API_PERS'
        }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
        'RqUID': '8bfd8083-bac0-4126-802f-1e915b224649',
        'Authorization': 'Basic ' + api_key
        }
    response = requests.post(url, headers=headers, data=payload, verify=False)

    
    print(response.text)


def test_get_models(api_token):

    url = "https://gigachat.devices.sberbank.ru/api/v1/models"
    token = api_token
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {api_token}'
    }
    response = requests.get(url, headers=headers, verify=False)
    assert response.status_code == 200
    body = response.json()
    assert body['object'] == 'list'
    assert body['data'][0]['id'] == 'GigaChat'  
    print(body)

def test_token_amount(api_token):
    url = "https://gigachat.devices.sberbank.ru/api/v1/tokens/count"

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {api_token}'
    }
    payload = {
        "model": "GigaChat",
        "input": ["Я к вам пишу — чего же боле?"]
    }
    response = requests.post(url, headers=headers, json=payload, verify=False)
    body = response.json()
    assert response.status_code == 200
    assert len(body) > 0
    print(body)

def test_get_tokens_balance(api_token):
    url = "https://gigachat.devices.sberbank.ru/api/v1/balance"

    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {api_token}'
    }

    response = requests.get(url, headers=headers, verify=False)
    assert response.status_code == 200
    body = response.json()
    assert body['balance'][0]['value'] > 0
    print(body)


def test_generate_answer(api_token):

    url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {api_token}'
    }

    payload = {
        "model": "GigaChat-Max",
        "messages": [
            {
                "role": "user",
                "content": "Погода в Москве"
            }
        ],
        "temperature": 0,
        "top_p": 0,
        "stream": False,
        "max_tokens": 30,
        "repetition_penalty": 1,
        "update_interval": 0
        }
    response = requests.post(url, headers=headers, json=payload, verify=False)

    assert response.status_code == 200, f"Ошибка: {response.status_code} - {response.text}"
    body = response.json()
    message = body['choices'][0]['message']
    assert message['role'] == 'assistant'
    content = message['content']
    expected_phrases = [
        "нет доступа",
        "рекомендую",
        "специализированными",
        "сервисами"
    ]
    has_expected_phrase = any(phrase in content for phrase in expected_phrases)
    assert has_expected_phrase, \
        f"Ответ не содержит ожидаемых фраз.\nОжидалось что-то из: {expected_phrases}\nПолучено: {content}"
    
    print(f"✓ Ответ успешно проверен: {content}")
def test_embending(api_token):

    url = "https://gigachat.devices.sberbank.ru/api/v1/embeddings"

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {api_token}'
    }

    payload = {
        "model": "Embeddings-2",
        "input": "Расскажи о современных технологиях"
    }

    response = requests.post(url, headers=headers, json=payload, verify=False)
    assert response.status_code == 402
    body = response.json()
    assert body['status'] == 402
    assert body['message'] == 'Payment Required'
    print(body)

def test_validate(api_token):

    url = "https://gigachat.devices.sberbank.ru/api/v1/functions/validate"

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {api_token}'
    }

    payload = {
        "name": "weather_forecast",
        "description": "Прогноз погоды",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "Местоположение, например, название города"
                }
            },
            "required": ["location"]
        }
    }

    response = requests.post(url, headers=headers, json=payload, verify=False)

    assert response.status_code == 200
    body = response.json()
    assert body['status'] == 200
    assert body['message'] == 'Function is valid'
    print(body)

def test_check_text(api_token):

    url = "https://gigachat.devices.sberbank.ru/api/v1/ai/check"

    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {api_token}'
    }

    payload = {
        "input": "Регулярные занятия спортом ведут свою историю с античных Олимпийских игр (776 г. до н.э.). Тогда атлеты соревновались в беге и борьбе. Сегодня доказано: спорт укрепляет сердце, дисциплинирует ум и продлевает жизнь. Движение — основа здоровья.",
        "model": "GigaCheckDetection"
    }

    response = requests.post(url, headers=headers, json=payload, verify=False)

    assert response.status_code == 403
    body = response.json()
    assert body['status'] == 403
    assert body['message'] == 'Permission denied'
    print(body)

    













