import os
os.environ["SCRAPERWIKI_DATABASE_NAME"] = "sqlite:///data.sqlite"
import scraperwiki
import lxml.html
import re

url_pattern = re.compile("/dev/peps/pep-\d*/?$")

def parse_header(root):
    data = {}
    for row in root.cssselect(".header, .field-list")[0].cssselect("tr"):
        td = row.cssselect("th, td")
        data[td[0].text_content().strip(" \t\r\n:")] = td[1].text_content().strip()
    print("Parsed", data)
    return data

if __name__ == "__main__":
    startingLink = "https://www.python.org/dev/peps/"
    print("Fetching", startingLink)
    tree = lxml.html.fromstring(scraperwiki.scrape(startingLink))
    scraperwiki.sqlite.save(unique_keys=['PEP'], data=parse_header(tree))

    tree.make_links_absolute(startingLink)
    links = set()
    for element, attribute, link, pos in tree.iterlinks():
        if url_pattern.search(link) and link not in links:
            links.add(link)
            print("Fetching", link)
            tree = lxml.html.fromstring(scraperwiki.scrape(link))
            scraperwiki.sqlite.save(unique_keys=['PEP'], data=parse_header(tree))

    scraperwiki.sql.execute("drop view if exists data")
    scraperwiki.sql.execute("create view data as select * from swdata order by cast(pep as int)")
