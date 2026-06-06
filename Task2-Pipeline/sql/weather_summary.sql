SELECT
    hour,
    ROUND(AVG(temperature), 2) AS avg_temperature,
    ROUND(AVG(humidity), 2) AS avg_humidity
FROM `decisive-unison-415017.weather_dataset.chennai_weather`
GROUP BY hour
ORDER BY avg_temperature DESC;