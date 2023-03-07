import requests
import csv
import json
from bs4 import BeautifulSoup

url = "https://en.wikipedia.org/wiki/The_Weeknd_discography"
url2 = "https://en.wikipedia.org/wiki/Kendrick_Lamar_discography"

# requesting server for info and creating beautifulsoup object
page = requests.get(url)
soup = BeautifulSoup(page.content, "html.parser")

# opening a file and adding fiels header
header = ["Title", "Released", "Label", "Format"]
f = open("weeknddiscog.csv", "w", newline="", encoding="UTF-8")
writer = csv.writer(f)
writer.writerow(header)

# list for json parsing
albums = []
j = open("weeknddiscog.json", "w", newline="", encoding="UTF-8")


def scrap(rows):
    for row in rows:
        # if the last row with text containing "denotes" is there then the last row will be skipped
        if """"—" denotes""" in row.td.text:
            continue
        rowtoadd = list()
        cells = row.find_all("td")  # finding all cells inside a single row
        # appending the first th element of row in list as it contain title
        rowtoadd.append(row.find("th"))
        for cell in cells:
            rowtoadd.append(cell)

        title = rowtoadd[0].text.strip()
        # creating list of all li in detail element
        details = rowtoadd[1].find_all("li")
        # [10:] skipping "Released: " which is already written in tag
        released = details[0].text[10:]
        label = details[1].text[7:]
        formatt = details[2].text[9:]
        certificates = rowtoadd[-1].text

        # for writing rows below the header
        csvrow = [title, released, label, formatt]
        writer.writerow(csvrow)

        # for getting data as json
        data = {
            "Title": title,
            "Released": released,
            "Label": label.split(","),
            "Format": formatt.split(",")
        }
        albums.append(data)

        print(
            f"Title : {title}\nDetails :- \nReleased: {released}\nLabel: {label}\nFormats: {formatt}\nCertificates : {certificates}")


# selecting first 4 table element
tables = soup.find_all("table", class_="wikitable plainrowheaders")[:6]
# skipping first 2 and last row of the table
for table in tables:
    rows = table.tbody.find_all("tr")[2:]
    scrap(rows)
f.close
# json final after loop a list will be created naming albums
main = {"albums": albums}
main_string = json.dumps(main, indent=2, ensure_ascii=False)
j.write(main_string)
j.close
