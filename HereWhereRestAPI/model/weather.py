import requests

def get_weather_info(lat, lng, api_key):
    url = f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lng}&appid={api_key}&lang=kr'
    response = requests.get(url)
    data = response.json()

    # Determine the weather condition
    weather_main = data['weather'][0]['main']

    # Map weather condition to Font Awesome icon
    icon_map = {
        'Clear': 'fas fa-sun',
        'Clouds': 'fas fa-cloud',
        'Rain': 'fas fa-cloud-showers-heavy',
        'Drizzle': 'fas fa-cloud-rain',
        'Thunderstorm': 'fas fa-bolt',
        'Snow': 'fas fa-snowflake',
        'Mist': 'fas fa-smog',
        'Smoke': 'fas fa-smog',
        'Haze': 'fas fa-smog',
        'Dust': 'fas fa-smog',
        'Fog': 'fas fa-smog',
        'Sand': 'fas fa-smog',
        'Ash': 'fas fa-smog',
        'Squall': 'fas fa-wind',
        'Tornado': 'fas fa-poo-storm'
    }

    image_map = {
        'Clear': 'https://images.unsplash.com/photo-1502082553048-f009c37129b9?ixlib=rb-1.2.1&auto=format&fit=crop&w=675&q=80',
        # Clear Sky
        'Clouds': 'https://images.unsplash.com/photo-1446776811953-b23d57bd21aa?ixlib=rb-1.2.1&auto=format&fit=crop&w=675&q=80',
        # Cloudy Sky
        'Rain': 'https://images.unsplash.com/photo-1486016006115-74a41448aea2?ixlib=rb-1.2.1&auto=format&fit=crop&w=675&q=80',
        # Rainy Weather
        'Drizzle': 'https://images.unsplash.com/photo-1556485689-33e55ab56127?q=80&w=1470&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
        # Light Rain
        'Thunderstorm': 'https://images.unsplash.com/photo-1605727216801-e27ce1d0cc28?q=80&w=1471&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
        # Thunderstorm
        'Snow': 'https://images.unsplash.com/photo-1414541944151-2f3ec1cfd87d?ixlib=rb-1.2.1&auto=format&fit=crop&w=675&q=80',
        # Snowy Weather
        'Mist': 'https://images.unsplash.com/photo-1676451774855-41336e3faf0e?q=80&w=1470&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
        # Misty Weather
        'Smoke': 'https://images.unsplash.com/photo-1602070118389-05c28ddc1bc2?q=80&w=1287&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
        # Smoky Air
        'Haze': 'https://plus.unsplash.com/premium_photo-1668791193861-383d104d7cd8?q=80&w=1375&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
        # Hazy Weather
        'Dust': 'https://images.unsplash.com/photo-1545134969-8debd725b007?q=80&w=1287&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
        # Dusty Air
        'Fog': 'https://images.unsplash.com/photo-1438803235109-d737bc3129ec?ixlib=rb-1.2.1&auto=format&fit=crop&w=675&q=80',
        # Foggy Weather
        'Sand': 'https://images.unsplash.com/photo-1658503606413-9d822871835c?q=80&w=1568&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
        # Sandstorm
        'Ash': 'https://images.unsplash.com/photo-1664973866211-5827308e4ab4?q=80&w=1288&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
        # Volcanic Ash
        'Squall': 'https://images.unsplash.com/photo-1605727216801-e27ce1d0cc28?ixlib=rb-1.2.1&auto=format&fit=crop&w=675&q=80',
        # Squall
        'Tornado': 'https://images.unsplash.com/photo-1454789476662-53eb23ba5907?q=80&w=1352&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D',
        # Tornado
    }

    weather_icon = icon_map.get(weather_main, 'fas fa-question')  # Default icon if no match is found
    weather_image= image_map.get(weather_main)

    weather_info = {
        'weather': weather_main,
        'country': data['name'],
        'weather_ko': data['weather'][0]['description'],
        'temp': f"{round(data['main']['temp'] - 273.15, 1)} ℃",
        'temp_min': f"{round(data['main']['temp_min'] - 273.15, 1)} ℃",
        'temp_max': f"{round(data['main']['temp_max'] - 273.15, 1)} ℃",
        'humidity': f"{data['main']['humidity']} %",
        'wind': f"{data['wind']['speed']} m/s",
        'weather_icon': weather_icon,  # Add the weather icon to the response,
        'weather_image': weather_image

    }

    return weather_info