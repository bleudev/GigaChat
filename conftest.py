import pytest
import requests

@pytest.fixture(scope = "session")
def api_key():
    try:
        with open("Authorization_key.txt", "r") as file:
            authkey = file.read().strip()

            if not authkey:
                pytest.fail("Файл Authorization_key.txt пуст!")

            return authkey
        
    except FileNotFoundError:
        pytest.fail("Файл Authorization_key.txt не найден!")

@pytest.fixture(scope="session", autouse=True)
def update_token_file(api_key):
    """Автоматически обновляет файл токена перед выполнением тестов"""
    url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
    
    payload = {'scope': 'GIGACHAT_API_PERS'}
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
        'RqUID': '8bfd8083-bac0-4126-802f-1e915b224649',
        'Authorization': 'Basic ' + api_key
    }
    
    response = requests.post(url, headers=headers, data=payload, verify=False)
    
    if response.status_code == 200:
        token_data = response.json()
        access_token = token_data.get('access_token')
        
    
        with open("token.txt", 'w') as f:
            f.write(access_token)
        
        print("Токен успешно обновлен")
    else:
        print(f"Не удалось обновить токен: {response.status_code}")


@pytest.fixture(scope = "session")
def api_token():
    try:
        with open("token.txt", "r") as file:
            token = file.read().strip()

            if not token:
                pytest.fail("Файл token.txt пуст!")

            return token
        
    except FileNotFoundError:
        pytest.fail("Файл token.txt не найден!")