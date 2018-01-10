Background: Spent 30 mins or more every week making staff slides as Assistant S2 (Staff Intelligence Officer) for ROTC, even using very streamlined Excel spreadsheets. Since I really was just looking up weather data and current events, this is definitely all stuff I can write a program for. Even though I won’t be Assistant S2 next semester, this seems like a cool project to get some API and GUI experience while also helping next year’s Assistant S2.

Idea: 
1.	Weather and sun-moon data gathered from weatherbit.io through API and USNO through string parsing into JSON. Combined into first a day’s weather representation, which is then fed into a two week span’s weather representation. Two week rep will have a method to write to .csv for use in copy-pasting onto slides. Some logic implemented to figure out S2 staff slides specific information (e.g. guidance on PT/training)

2.	Current events to be scraped off some news site, user selects and categorizes some events, formatted properly for copy and paste.

3.	GUI to make settings and select current events.

4.	Can be expanded for Harvard/MIT lectures through exported calendar. 

5.	Cadet events (sports meets) may be too hard to automate because websites for each sport are different. Instead could probably make manual input of entire seasons, then export large .csv for copy and pasting chunks of.