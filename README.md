![alt text](https://raw.githubusercontent.com/montiblanc97/S2AssistantAssistant/master/demo.png)

Background: Spent 30 mins or more every week making staff slides as Assistant S2 (Staff Intelligence Officer) for ROTC, even using very streamlined Excel spreadsheets. Since I really was just looking up weather data and current events, this is definitely all stuff I can write a program for. Even though I won’t be Assistant S2 next semester, this seems like a cool project to get some API and GUI experience while also helping next year’s Assistant S2.

Features:
-Scrapes weather information up to 14 days (powered by the Weatherbit API) and twilight information for almost any day (powered by USNO Astronomical Applications)
-Weather information contains general description, temperature, precipitation/humidity, wind speed/direction
-Twilight information contains rise and set times for sun and moon as well as start and end times for nautical, astronomical, and civil twilight
-PT/Training guidance can be inferred based on weather
-Allows saving/import of data
-Option to apply Daylight Savings Time to twilight information
-Allows any combination of weather and twilight information


How It Works:
1. Using packaged zip for your OS, unzip and run "run.exe/.app". Or using python, run "/commander/run.py".
2. Fill out input panel. Visit weatherbit.io and sign-up as a free developer to get a key.
3. HOOAH!
4. Copy output to a text editor, save it as a .csv file, and display it in Google Sheets (Excel is not friendly with this).



Ideas for Next Steps: 

1. Current events to be scraped off some news site, user selects and categorizes some events, formatted properly for copy and paste.


2. Can be expanded for Harvard/MIT lectures through exported calendar. 


3. Cadet events (sports meets) may be too hard to automate because websites for each sport are different. Instead could probably make manual input of entire seasons, then export large .csv for copy and pasting chunks of.
