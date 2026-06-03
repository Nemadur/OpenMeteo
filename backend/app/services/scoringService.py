from app.utils.utils import average

# This service is responsible for calculating a score for each city based on the weather data retrieved from the Open-Meteo API. 
# The score is computed using a weighted formula that takes into account temperature, wind speed, humidity, and cloud cover. 
# Each of these factors contributes to the overall score in a way that reflects their impact on the perceived weather quality. 
# The ScoringService provides a static method calculate that takes in the weather data and returns a final score for the city, which is then used to rank the cities in the WeatherService.
class ScoringService:

    @staticmethod
    def calculate(weather_data: dict) -> float:

        avgTemp = average(weather_data["temperature_2m"])
        avgWind = average(weather_data["wind_speed_10m"])
        avgHumidity = average(weather_data["relative_humidity_2m"])
        avgCloud = average(weather_data["cloud_cover"])

        score = ScoringService.compute_city_score(avgTemp, avgWind, avgHumidity, avgCloud)

        return round(score, 2)
    
    def temperature_score(temp: float) -> float:
        score = 10 - abs(temp - 24)
        return max(0, score)
    
    def wind_score(wind: float) -> float:
        score = 10 - wind
        return max(0, score)

    def humidity_score(h: float) -> float:
        # Ideal relative humidity is around 50% for good weather. 
        # The score decreases as we move away from this ideal point, with a maximum of 10 at 50% and decreasing to 0 at 0% and 100%.
        return max(0, 10 - abs(h - 50) / 5)

    def cloud_score(c: float) -> float:
        # Ideal cloud cover is around 25% for good weather. 
        # The score decreases as we move away from this ideal point, with a maximum of 10 at 25% and decreasing to 0 at 0% and 100%.
        if c <= 25:
            return (c / 25) * 10
        else:
            return ((100 - c) / 75) * 10

    def compute_city_score(temp: float, wind: float, humidity: float, cloud: float) -> float:

        temp_score = ScoringService.temperature_score(temp)
        wind_score = ScoringService.wind_score(wind)
        humidity_score = ScoringService.humidity_score(humidity)
        cloud_score = ScoringService.cloud_score(cloud)

        # The final score is a weighted average of the individual scores, with temperature contributing 35%, wind speed 20%, humidity 20%, and cloud cover 25%.
        final = (
            temp_score * 0.35 +
            wind_score * 0.20 +
            humidity_score * 0.20 +
            cloud_score * 0.25
        )

        return round(final, 2)