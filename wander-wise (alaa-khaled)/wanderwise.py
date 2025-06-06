import os
import gc
import requests
from datetime import datetime, timedelta
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generate_plan(prompt, max_new_tokens=4000, temperature=0.85, top_p=0.9):
    try:
        if not os.getenv("GEMINI_API_KEY"):
            print("Error: GEMINI_API_KEY not found in environment variables")
            return None
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(
            prompt,
            generation_config={
                "max_output_tokens": max_new_tokens,
                "temperature": temperature,
                "top_p": top_p
            }
        )
        generated_text = response.text.strip()
        if not generated_text:
            print("Error: Empty response from Gemini API")
            return None
        return generated_text
    except Exception as e:
        print(f"Error generating plan: {str(e)}")
        return None

def get_weather_data(destination, dates):
    try:
        openweather_api_key = os.getenv("OPENWEATHER_API_KEY")
        start_date_str, end_date_str = dates.split(" - ")
        for fmt in ["%Y-%m-%d", "%d %B %Y", "%d %b %Y"]:
            try:
                start_date = datetime.strptime(start_date_str.strip(), fmt).date()
                end_date = datetime.strptime(end_date_str.strip(), fmt).date()
                break
            except ValueError:
                continue
        else:
            raise ValueError("Invalid date format")
        
        date_range = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]

        if not openweather_api_key:
            print("Error: OPENWEATHER_API_KEY not found in environment variables")
            return "\n".join([f"{d.strftime('%Y-%m-%d')}: Sunny, 30°C" for d in date_range])

        geocoding_url = f"http://api.openweathermap.org/geo/1.0/direct?q={destination}&limit=1&appid={openweather_api_key}"
        geo_response = requests.get(geocoding_url)
        geo_response.raise_for_status()
        geo_data = geo_response.json()

        if not geo_data:
            print(f"Could not find coordinates for {destination}. Using default weather data.")
            return "\n".join([f"{d.strftime('%Y-%m-%d')}: Sunny, 30°C" for d in date_range])

        latitude = geo_data[0]["lat"]
        longitude = geo_data[0]["lon"]

        current_date = datetime.now().date()
        max_forecast_date = current_date + timedelta(days=7)

        if start_date > max_forecast_date or end_date > max_forecast_date:
            print(f"Requested dates ({start_date} to {end_date}) are beyond the 7-day forecast window (up to {max_forecast_date}). Using default weather data.")
            return "\n".join([f"{d.strftime('%Y-%m-%d')}: Sunny, 30°C" for d in date_range])

        weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&daily=temperature_2m_max,weathercode&timezone=auto&start_date={start_date.strftime('%Y-%m-%d')}&end_date={end_date.strftime('%Y-%m-%d')}"

        weather_response = requests.get(weather_url)
        weather_response.raise_for_status()
        weather_data = weather_response.json()
        daily_data = weather_data["daily"]

        weather_codes = {
            0: "Sunny",
            1: "Mostly Sunny",
            2: "Partly Cloudy",
            3: "Cloudy",
            45: "Foggy",
            51: "Rainy",
            53: "Rainy",
            61: "Rainy",
            63: "Rainy",
            80: "Light Rain Showers",
            81: "Rain Showers",
            95: "Thunderstorm",
        }

        weather_forecast = []
        for i, date in enumerate(date_range):
            if i < len(daily_data["time"]):
                temp_max = round(daily_data["temperature_2m_max"][i])
                weather_code = daily_data["weathercode"][i]
                weather_desc = weather_codes.get(weather_code, "Unknown")
                weather_forecast.append(f"{date.strftime('%Y-%m-%d')}: {weather_desc}, {temp_max}°C")
            else:
                weather_forecast.append(f"{date.strftime('%Y-%m-%d')}: Sunny, 30°C")

        return "\n".join(weather_forecast)
    except Exception as e:
        print(f"Error in get_weather_data: {str(e)}")
        return "Weather data unavailable due to an error."

def get_trip_style(budget):
    if budget < 500:
        return "Budget Cultural"
    elif budget < 1000:
        return "Cultural"
    elif budget < 2000:
        return "Adventure"
    else:
        return "Luxury"

def generate_itinerary(destination, dates, budget):
    try:
        trip_style = get_trip_style(budget)
        weather_data = get_weather_data(destination, dates)
        start_date_str, end_date_str = dates.split(" - ")
        for fmt in ["%Y-%m-%d", "%d %B %Y", "%d %b %Y"]:
            try:
                start_date = datetime.strptime(start_date_str.strip(), fmt).date()
                end_date = datetime.strptime(end_date_str.strip(), fmt).date()
                break
            except ValueError:
                continue
        else:
            raise ValueError("Invalid date format")

        date_range = [start_date + timedelta(days=i) for i in range((end_date - start_date).days + 1)]
        daily_budget = budget / len(date_range) if len(date_range) > 0 else budget
        activity_budget = daily_budget * 0.4
        accommodation_budget = daily_budget * 0.3
        food_budget = daily_budget * 0.2
        transport_budget = daily_budget * 0.1

        itinerary_parts = []
        weather_lines = weather_data.split("\n")
        for day_num in range(len(date_range)):
            day = day_num + 1
            weather_for_day = weather_lines[day_num] if day_num < len(weather_lines) else f"{date_range[day_num].strftime('%Y-%m-%d')}: Sunny, 30°C"
            
            prompt = f"""Generate a detailed itinerary for Day {day} of a {len(date_range)}-day trip to {destination} on {date_range[day_num].strftime('%Y-%m-%d')} with a daily budget of ${daily_budget:.0f} USD.
Trip style: {trip_style}.
Weather forecast: {weather_for_day}

Include the following sections:
- Weather: Use the provided weather forecast (e.g., 'Sunny, 30°C').
- Activities: One or two specific places with descriptions and costs in USD (total ≤ ${activity_budget:.0f}).
- Accommodation: Specific type and name with cost in USD (≤ ${accommodation_budget:.0f}/night).
- Meals: Specific options with costs in USD (total ≤ ${food_budget:.0f}).
- Transportation: Specific options with costs in USD (total ≤ ${transport_budget:.0f}).

Format as plain text starting with 'Day {day}: {destination}', followed by the sections in the order: Weather, Activities, Accommodation, Meals, Transportation. Ensure all sections are included and filled with unique content for each day. Use USD for all costs. Do not use HTML tags or special formatting. Do not skip any sections or days."""
            itinerary_day = generate_plan(prompt)
            if not itinerary_day:
                print(f"Warning: Generating fallback for Day {day} (None response)")
                itinerary_day = f"""Day {day}: {destination}
Weather: {weather_for_day.split(': ')[1]}
Activities: Free day to explore {destination} (self-paced, $0)
Accommodation: Budget Hostel {destination} (${accommodation_budget:.0f}/night)
Meals: Local street food ($10); Dinner at a local café ($10)
Transportation: Walking ($0)"""
            else:
                lines = itinerary_day.split('\n')
                has_content = len(lines) > 1 and any(line.strip() for line in lines[1:])
                sections_present = any(section in itinerary_day for section in ["Weather:", "Activities:", "Accommodation:", "Meals:", "Transportation:"])
                if not has_content or not sections_present:
                    print(f"Warning: Generating fallback for Day {day} (Incomplete response: {repr(itinerary_day)})")
                    itinerary_day = f"""Day {day}: {destination}
Weather: {weather_for_day.split(': ')[1]}
Activities: Free day to explore {destination} (self-paced, $0)
Accommodation: Budget Hostel {destination} (${accommodation_budget:.0f}/night)
Meals: Local street food ($10); Dinner at a local café ($10)
Transportation: Walking ($0)"""
            print(f"Day {day} itinerary_day before append: {repr(itinerary_day)}")
            lines = itinerary_day.split('\n')
            has_content_final = len(lines) > 1 and any(line.strip() for line in lines[1:])
            if not has_content_final:
                print(f"Error: Day {day} still empty after fallback, forcing content: {repr(itinerary_day)}")
                itinerary_day = f"""Day {day}: {destination}
Weather: {weather_for_day.split(': ')[1]}
Activities: Free day to explore {destination} (self-paced, $0)
Accommodation: Budget Hostel {destination} (${accommodation_budget:.0f}/night)
Meals: Local street food ($10); Dinner at a local café ($10)
Transportation: Walking ($0)"""
            itinerary_parts.append(itinerary_day)
            print(f"After Day {day}, itinerary_parts: {[repr(part) for part in itinerary_parts]}")

        itinerary = "\n".join(itinerary_parts)
        print(f"Final itinerary before return: {repr(itinerary)}")
        return itinerary, weather_data
    except Exception as e:
        print(f"Error generating itinerary: {str(e)}")
        return None, weather_data

def wanderwise_plan(destination, dates, budget):
    try:
        print(f"Planning trip to {destination} for {dates} with budget ${budget}")
        trip_style = get_trip_style(budget)
        print(f"Trip style: {trip_style}")
        weather = get_weather_data(destination, dates)
        
        start_date_str, end_date_str = dates.split(" - ")
        for fmt in ["%Y-%m-%d", "%d %B %Y", "%d %b %Y"]:
            try:
                start_date = datetime.strptime(start_date_str.strip(), fmt).date()
                break
            except ValueError:
                continue
        else:
            raise ValueError("Invalid date format")
        
        current_date = datetime.now().date()
        max_forecast_date = current_date + timedelta(days=7)
        weather_warning = None
        if start_date > max_forecast_date:
            weather_warning = "Note: Weather data is unavailable for the selected dates (beyond 7-day forecast). Using default sunny weather (30°C)."
        
        print(f"Weather data retrieved: {weather}")
        itinerary, weather_data = generate_itinerary(destination, dates, budget)
        if itinerary:
            return {
                "destination": destination,
                "dates": dates,
                "budget": budget,
                "trip_style": trip_style,
                "itinerary": itinerary,
                "weather_warning": weather_warning,
                "weather_data": weather_data 
            }
        else:
            return {"error": "Failed to generate itinerary", "weather_data": weather_data}
    except Exception as e:
        print(f"Error in wanderwise_plan: {str(e)}")
        gc.collect()
        return {"error": str(e), "weather_data": weather}