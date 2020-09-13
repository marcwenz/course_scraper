#!/usr/bin/env python3

import requests
from lxml import html
import html2text

NOTHING = "-"


class TimeTable:
    def __init__(self):
        raise NotImplementedError
        pass

    def set_slot(self, time, course):
        pass


class TimeSlot:
    def __init__(self):
        pass


def get_tree(page):
    return html.fromstring(page)


def get_html(url):
    return requests.get(url).text


def ex_table(tree):
    return tree.xpath("/html/body/div[3]/article/div/section/article/div/div/table")[0]


def tostr(e):
    return str(html.tostring(e))


def clean_up(e):
    return (
        e.replace("b'", "")
        .replace(r"\-", "-")
        .replace("_", "")
        .replace("'", "")
        .replace("|", " |")
    )


def main():
    url = "http://studentnet.cs.manchester.ac.uk/ugt/2020/timetable/timetable.php?year=2020&timetable=SPLUSF04C72-2020&weeks=SEM1&printing=true"
    tree = get_tree(get_html(url))
    table = ex_table(tree)
    # print(html.tostring(table))
    ht = html2text.HTML2Text()
    raw_rows = []
    prows = []

    for row in table.findall(".//tr")[:-2]:
        row = clean_up(ht.handle(tostr(row))).strip().split()
        raw_rows.append(row)

    raw_rows[1].append("|")

    for r in raw_rows[2:]:
        r.insert(0, "|")
        r.append("|")
        print(r)

    prows = [" ".join(e) for e in raw_rows]
    prows[1] = "| Time " + prows[1]
    prows[0] = prows[0].replace("|", "")

    with open("tt.org", mode="w") as f:
        f.writelines([p + "\n" for p in prows])


if __name__ == "__main__":
    main()
