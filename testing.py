import json

weather_data = json.loads(open("bad.txt", "r+").read())
print(weather_data)