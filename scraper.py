import scraperwiki
import lxml.html
import os

def parse_header(root):
    data = {}
    for row in root.cssselect(".header tr"):
        td = row.cssselect("th,td")
        data[td[0].text_content().strip(" \t\r\n:")] = td[1].text_content().strip()
    return data

if __name__ == "__main__":
    os.environ["SCRAPERWIKI_DATABASE_NAME"] = "sqlite:///data.sqlite"
    tree = lxml.html.parse("https://www.python.org/dev/peps/")
    scraperwiki.sqlite.save(unique_keys=['PEP'], data=parse_header(root))

    for element, attribute, link, pos in tree.iterlinks():
        if link.

    scraperwiki.sql.execute("drop view if exists data")
    scraperwiki.sql.execute("create view data as select * from swdata order by pep")
