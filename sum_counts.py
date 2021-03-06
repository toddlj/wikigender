import os
import re
import timeit
import requests
from bs4 import BeautifulSoup


url = "https://es.wikipedia.org/wiki/Ingeniería"

page_html = requests.get(url).text
page_soup = BeautifulSoup(page_html, "html.parser")

page_title = page_soup.find(id="firstHeading").contents[0]
links_to_check = []
for link in page_soup.find(id="mw-content-text").find_all("a"):
    if link.get("href") and re.match(r"^/wiki/", link.get("href")):
        links_to_check += [link.get("title")]

neighbours_number_of_masculine_nouns = 0
neighbours_number_of_feminine_nouns = 0
page_number_of_masculine_nouns = 0
page_number_of_feminine_nouns = 0
neighbours_checked = 0

start_time = timeit.default_timer()
for counts_file_name in os.listdir("counts/"):
    counts_file_path = "counts/" + counts_file_name
    with open(counts_file_path, "r") as counts_file:
        for line in counts_file:
            masculine_nouns = line.split()[0]
            feminine_nouns = line.split()[1]
            title = line.lstrip(f"{masculine_nouns} {feminine_nouns} ").rstrip("\n")

            try:
                if links_to_check.index(title) and masculine_nouns != '-':
                    neighbours_checked += 1
                    neighbours_number_of_masculine_nouns += int(masculine_nouns)
                    neighbours_number_of_feminine_nouns += int(feminine_nouns)
            except ValueError:
                if title == page_title and masculine_nouns != '-':
                    page_number_of_masculine_nouns += int(masculine_nouns)
                    page_number_of_feminine_nouns += int(feminine_nouns)
            # break

print(f"The page \"{page_title}\" has {page_number_of_masculine_nouns} masculine nouns and {page_number_of_feminine_nouns} feminine nouns.")
print(f"Its {neighbours_checked} neighbours have {neighbours_number_of_masculine_nouns} masculine nouns and {neighbours_number_of_feminine_nouns} feminine nouns.")
print()
print(f"Totals for \"{page_title}\":")
print(f"{page_number_of_masculine_nouns + neighbours_number_of_masculine_nouns} masculine nouns.")
print(f"{page_number_of_feminine_nouns + neighbours_number_of_feminine_nouns} feminine nouns.")
print(f"{page_number_of_masculine_nouns + page_number_of_masculine_nouns + neighbours_number_of_masculine_nouns + neighbours_number_of_masculine_nouns} m/f nouns in total")
try:
    print(f"Ratio: {round((page_number_of_masculine_nouns + neighbours_number_of_masculine_nouns) / (page_number_of_feminine_nouns + neighbours_number_of_feminine_nouns), 4)} M/F")
except ZeroDivisionError:
    pass
try:
    print(f"Page ratio: {round(page_number_of_masculine_nouns / page_number_of_feminine_nouns, 4)} M/F")
except ZeroDivisionError:
    pass
print()
print(f"Time taken: {timeit.default_timer() - start_time} seconds")
