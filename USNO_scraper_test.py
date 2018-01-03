from USNO_scraper import *

# raw_html = scrape_USNO("moon", "2015", "HI", "Honolulu")
# print("SCRAPE_USNO")
# # print(raw_html)
# print("\n\n\n")

data = open("Data/RAW_moon_data_2015_HI_Honolulu.html", "r+").read()
raw_html = "moon", "2015", "HI", "Honolulu", data


list_form = format_HTML_to_list(raw_html[4])
print("LIST FORM")
# print(list_form)
print("\n\n\n")

dict_form = process_data_list(raw_html[0], raw_html[1], raw_html[2], raw_html[3], list_form, "hawaii")
print("DICT FORM")
print(dict_form)
print("\n\n\n")

fixed_dst = fix_DST(dict_form, "eastern")
print("FIX DST")
print(fixed_dst)
print("\n\n\n")


# print(add_hour("2212"))

#TEST NEW TIME, DST HELPERS