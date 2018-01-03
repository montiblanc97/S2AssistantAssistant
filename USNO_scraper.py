from bs4 import BeautifulSoup
import requests
import pytz
import datetime
import json
import calendar


def scrape_fix_usno(task_name, year="2018", state="MA", city="Cambridge", timezone="eastern",
                    write_html=True, write_unfixed_dict=True, write_fixed_dict = True):
    html = scrape_usno_html(task_name, year, state, city, write_html)
    formatted = format_HTML_to_list(html)
    processed = process_data_list(task_name, year, state, city, formatted, write_unfixed_dict)
    fixed = fix_DST(processed, timezone, write_fixed_dict)

    return fixed

def pass_fix_usno(html_path, task_name, year="2018", state="MA", city="Cambridge", timezone="eastern",
             write_unfixed_dict=True, write_fixed_dict = True):
    html = data = open(html_path, "r+").read()
    formatted = format_HTML_to_list(html)
    processed = process_data_list(task_name, year, state, city, formatted, write_unfixed_dict)
    fixed = fix_DST(processed, timezone, write_fixed_dict)

    return fixed

def scrape_usno_html(task_name, year="2018", state="MA", city="Cambridge", write=True):
    """
    Scrapes USNO data in HTML format
    :param task_name: of data to be scraped. Valid paramters are "sun", "moon",
        "nautical twilight", "civil twilight", "astronomical twilight"
    :param year: of data to be scraped
    :param state: ditto, must be in initial format
    :param city: ditto
    :param write: whether or not to save scraped data as HTML file
    :return: tuple of strings of task name, year, state, city, and
            USNO data as specified in paramters in HTML format
    """
    url = "http://aa.usno.navy.mil/cgi-bin/aa_rstablew.pl?ID=AA"
    url += "&year=" + year

    # specific to USNO website url
    task_lookup = {"sun": "0",
                   "moon": "1",
                   "civil twilight": "2",
                   "nautical twilight": "3",
                   "astronomical twilight": "4"}
    url += "&task=" + task_lookup[task_name]

    url += "&state=" + state
    city = city.replace(" ", "+")
    url += "&place=" + city

    response = requests.get(url)

    if write:
            #to save date gathered
            filename = "Data/RAW_%s_data_%s_%s_%s.html" % (task_name.lower().replace(" ", "_"), year, state, city)

            writing = open(filename, "w+")
            writing.write(response.text)
            writing.close()

    return response.text


def format_HTML_to_list(HTML):
    """
    Formats and strips USNO data HTML file into just the applicable fields necessary for further processing
    :param HTML: string of USNO data in HTML
    :return: formatted and stripped USNO data in list, no longer has identifying data or in HTML format
        will be in form: day time_for_January time_for_January ...for each month
        e.g. 01 0943 2127... which contains sunrise and sunset data of January 1 (other tasks supported)
    """
    soup = BeautifulSoup(HTML, 'html.parser')
    info = soup.find("pre").text.split("\n")[10:-2]
    return info


def process_data_list(task_name, year, state, city, data_list, write=True):
    """
    Process USNO data in list form into a dictionary, can also write a .JSON.
    Also adds an hour to times within data if under DST.
    "****" will be used to designate a carried over time (e.g. sunset occurs next day).
    :param task_name: of data to be scraped. Valid paramters are "sun", "moon",
        "nautical twilight", "civil twilight", "astronomical twilight"
    :param year: of data to be scraped
    :param state: ditto, must be in initial format
    :param city: ditto
    :param timezone: ditto, valid inputs are:
            "eastern", "pacific", "mountain", "central", "alaska", "hawaii", "samoa"
    :param data_list: USNO data in list form as formatted by format_HTML_to_list
    :param write: whether or not to write output as a .JSON
    :return: a dictionary of USNO data with human-friendly labels
        e.g. {"task_name": "sun",
            "year": "2017",
            "state": "MA",
            "city": "Cambridge",
            "data": {1:
                        {1: {"sunrise": 0943, "sunset": 2127}...}
                    ...}
            ...}
        template: {"task_name": task_name,
            "year": year,
            "state": state,
            "city": city,
            "data": {month:
                        {day: {task_specific_data: time, other_task_specific_data: time}...}
                    ...}
            ...}
    """
    out = {"task_name": task_name,
           "year": year,
           "state": state,
           "city": city,
           "data": {}
           }

    task_time_lookup = {"sun" : ("sunrise", "sunset"), "moon": ("moonrise", "moonset"),
                        "nautical twilight": ("BMNT", "EENT"), "astronomical twilight": ("BMAT", "EEAT"),
                        "civil twilight": ("BMCT", "EECT")}
    task_time_1 = task_time_lookup[task_name][0]
    task_time_2 = task_time_lookup[task_name][1]

    # full_day_data example:
    # '01  0943 2127  1033 2307  0915 2200  1027 2356  1112       1252 0053  1322 0049  1436 0121  1545 0215  1552 0239  1632 0405  1637 0445'
    # note that large blank space is a carried over time (not just spacing), sunrise/sunset occurs next day
    for full_day_data in data_list:
        day = full_day_data[:2].lstrip("0")
        stripped_day_data = full_day_data[4:]
        for month in range(1, 13):
            start_index = (month-1) * 11
            end_index = start_index + 9
            single_day_data = stripped_day_data[start_index: end_index]

            first_time = single_day_data[0:4] if single_day_data[0:4] != "    " else "****"  # for visibility
            second_time = single_day_data[5:9] if single_day_data[5:9] != "    " else "****"

            if str(month) not in out["data"]:
                out["data"][str(month)] = {}

            out["data"][str(month)][day] = {task_time_1: first_time, task_time_2: second_time}

    if write:
            #to save date gathered
            filename = "Data/%s_data_%s_%s_%s.json" % (task_name.lower().replace(" ", "_"), year, state, city)
            writing = open(filename, "w+")
            written_out = json.dumps(out)
            writing.write(written_out)
            writing.close()

    return out

def is_DST(aware_dt):
    """
    Determines if given datetime object is under DST
    https://stackoverflow.com/questions/31146092/how-to-determine-if-a-timezone-specific-date-in-the-past-is-daylight-saving-or-n
    :param aware_dt: datetime object that has a timezone property assigned (under aware_dt.tzinfo)
    :return: boolean on whether or not aware_dt is under DST
    """
    assert aware_dt.tzinfo is not None
    assert aware_dt.tzinfo.utcoffset(aware_dt) is not None
    return bool(aware_dt.dst())


def localized_date_time(year, month, day, time, timezone):
    """
    Create a datetime object with a timezone property assigned
    :param year: of datetime
    :param month: ditto
    :param day: ditto
    :param time: ditto
    :param timezone: to assign, valid inputs are:
            "eastern", "pacific", "mountain", "central", "alaska", "hawaii", "samoa"
    :return: datetime object with timezone property
    https://stackoverflow.com/questions/31146092/how-to-determine-if-a-timezone-specific-date-in-the-past-is-daylight-saving-or-n
    """
    year, month, day = int(year), int(month), int(day)
    dt = datetime.datetime(year=year, month=month, day=day, hour=int(time[:2]), minute=int(time[2:]))
    tz = pytz.timezone("US/" + timezone.title())
    dt = tz.localize(dt, is_dst=True)  # defaults to true if ambiguous

    return dt


def next_day(year, month, day):
    """
    Gives next day as tuple (month, day).
    Year not necessary for our purposes (DST adjusting)
    :param year: of current date
    :param month: ditto
    :param day: ditto
    :return: tuple (month, day) of the next calendar date
    """
    year, month, day = int(year), int(month), int(day)

    if month == 12 and day == 31:
        return str(year + 1), "1", "1"

    is_leap = calendar.isleap(year)
    days_lookup = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
    if (day < days_lookup[month]) or (month == 2 and day == 28 and is_leap):
        return str(year), str(month), str(day+1)
    return str(month+1), str(1)


def add_hour(time):
    """
    Given a time in 24-hour format, adds an hour to it. Flags whether or not time overflowed (2318 to 0018)
    :param time: e.g. 1349
    :return: Time with hour added and boolean with whether or not it overflowed
    """
    overflow = False
    hour = int(time[:2])
    hour += 1

    if hour > 23:
        hour = 0
        overflow = True

    hour = str(hour) if hour >= 10 else "0" + str(hour)
    return hour + time[2:], overflow


def fix_DST(processed_data, timezone, write=True):
    """
    Given data processed as in process_data_list, adjusts times to account for DST
    :param processed_data: as in spec of process_data_list
    :param timezone: of data
    :param write: whether or not to write output as a .JSON
    :return: data in same format as input but with adjusted DST times
    """
    ignore = set()  # ignore entries that were already fixed by date before (due to overflow)
    # set of tuples with (month, day, time_task)
    current = (processed_data["year"], "1", "1")
    year = current[0]

    while current[1] is not None:
        # print(current)
        month = current[1]
        day = current[2]
        for time_task in processed_data["data"][month][day].keys():
            if (month, day, time_task) in ignore:
                continue

            time = processed_data["data"][month][day][time_task]
            if time == "****":
                continue

            dt = localized_date_time(year, month, day, time, timezone)
            if is_DST(dt):
                new_time, flag = add_hour(time)
                if flag:
                    chain_fix(year, month, day, time_task, processed_data, ignore)
                else:
                    processed_data["data"][month][day][time_task] = new_time


        next_iter = next_day(year, month, day)
        if next_iter[0] != year: #new year (end of data)
            break
        current = next_iter

    if write:
        # to save date gathered
        filename = "Data/DST_%s_data_%s_%s_%s.json" % (processed_data["task_name"].lower().replace(" ", "_"),
                                                       year, processed_data["state"], processed_data["city"])
        writing = open(filename, "w+")
        written_out = json.dumps(processed_data)
        writing.write(written_out)
        writing.close()

    return processed_data


def chain_fix(year, month, day, time_task, processed_data, ignore):
    current = (month, day) #find where overflow stops (first instance of "****")
    current_value = processed_data["data"][current[0]][current[1]][time_task]
    history = []
    while current_value != "****":
        history.append(current)
        current = next_day(year, current[0], current[1])
        current_value = processed_data["data"][current[1]][current[2]][time_task]

    while len(history) > 0:
        working = history.pop()
        working_month = working[0]
        working_day = working[1]
        new_time = add_hour(processed_data["data"][working_month][working_day][time_task])[0]
        dummy, new_month, new_day = next_day(year, working_month, working_day) #year unused
        processed_data["data"][new_month][new_day][time_task] = new_time
        ignore.add((new_month, new_day, time_task))

    processed_data["data"][month][day][time_task] = "****"
