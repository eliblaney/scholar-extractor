from bs4 import BeautifulSoup
import requests
import csv
import re

base_url = "https://goldwater.scholarsapply.org/"
pages = ["2006-scholars", "2007-scholars", "2008-scholars", "2009-scholars", "2010-scholars", "2011-scholars", "2012-scholars", "2013-scholars", "2014-scholars", "2015-scholars", "2016-scholars", "2017-scholars", "2018-scholars-by-state-of-legal-residence", "2019-scholars-by-state-of-legal-residence", "2020-goldwater-scholars-by-legal-state-of-residence", "2021-goldwater-scholars-by-legal-state-of-residence"]

outfile = "scholars.csv"
field_names = ["year", "name", "institution", "field_of_study", "career_goal", "mentors", "campus_representative"]
num_fields = len(field_names)
scholars = []

for page in pages:
    year = page[:page.index("-")] 
    print("Loading scholars for " + year + "...")
    url = base_url + page
    res = requests.get(url).content

    # Fixing bad HTML
    res = res.decode('utf-8').replace("<p><H2>", "<h2>").replace("<h2>Alabama</h1>", "<h2>Alabama</h2>")
    if year == "2011":
        res = re.sub("^\w+(?: \w+)?<br \/>$", "</p><p>",
                re.sub("^\w+(?: \w+)?<\/p>$", "</p>",
                    res,
                    flags=re.MULTILINE),
                flags=re.MULTILINE)

    soup = BeautifulSoup(res, "html.parser")
    container = soup.find("div", class_="entry-content")

    print("Extracting scholars...")
    for child in container.findChildren("p", recursive=False):
        props = child.text
        scholar = {"year": year}

        ### Special exceptions

        # Two-lined career goal description
        if year == "2017":
            if len(props) > num_fields:
                props = props.replace("Ecology.\nResearch", "Ecology. Research")
            props = props.replace("Mentor(s) Career Goal: ", "Mentor(s): \nCareer Goal: ")

        if year == "2018":
            props = re.sub("Lauren Pedersen.*Lauren Pedersen", "Lauren Pederson", props, flags=re.DOTALL)

        if year == "2019":
            props = props.replace("conduct\nacademic", "conduct academic").replace("Neuroscience.\nConduct", "Neuroscience. Conduct")

        if year == "2020":
            props = props.replace("and\nconduct", "and conduct").replace("in\nthe", "in the").replace("Astronomy\nConduct", "Astronomy. Conduct")

        props = props.split("\n")

        # Skip header text for the year
        if props[0].startswith("20"):
            continue

        # Skip header text "Listed by state of legal residence"
        if "listed" in props[0].lower():
            continue

        ### End special exceptions

        i = 1
        for p in props:
            if p == "":
                continue

            try:
                # Remove identifiers
                p = p[p.index(":")+2:]
            except:
                pass

            scholar[field_names[i]] = re.sub("\s+", ' ', p)
            i = i + 1

        if scholar:
            scholars.append(scholar)
            print("Extracted: " + scholar[field_names[1]])

print("Finished extracting. Saving to " + outfile + "...")
with open(outfile, 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=field_names)
    writer.writeheader()
    writer.writerows(scholars)

print("Extraction complete.")
