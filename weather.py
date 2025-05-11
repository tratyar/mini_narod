import requests


KOORD = {0: [67.427302, 36.647812],
         1: [63.878925, 30.160803],
         2: [64.540260, 40.547804],
         3: [61.668796, 50.836500],
         4: [67.638050, 53.006926],
         5: [66.529865, 66.614507],
         6: [56.010543, 92.852581],
         7: [62.027221, 129.732178],
         8: [64.735815, 177.518911]}


def get_weather_data(lat, lon, api_key):
    url = "http://api.weatherapi.com/v1/current.json"
    params = {
        "key": api_key,
        "q": f"{lat},{lon}",
        "lang": "ru"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Проверка на ошибки HTTP

        data = response.json()
        current = data["current"]

        temperature = current["temp_c"]
        pressure_mb = current["pressure_mb"]  # Давление в миллибарах
        humidity = current["humidity"]  # Влажность в %

        return [temperature, pressure_mb, humidity]

    except requests.exceptions.RequestException as e:
        print(f"Ошибка запроса: {e}")
        return None
    except KeyError as e:
        print(f"Ошибка в структуре ответа: {e}")
        return None


# Пример использования
WEATHERAPI_KEY = "8110d9cbe95740c2b66154946250505"


def reg_weather(region):
    latitude = KOORD[region][0]
    longitude = KOORD[region][1]
    weather_data = get_weather_data(latitude, longitude, WEATHERAPI_KEY)
    if weather_data:
        return (f"Данные по региону на данный момент:\n"
                f"  * Температура: {weather_data[0]}°C\n"
                f"  * Давление: {weather_data[1]} мБар\n"
                f"  * Влажность: {weather_data[2]}%\n")

    else:
        print("Не удалось получить данные.")