#!/usr/bin/env python3

import requests
from lxml import html, etree
import re

from auth import manc_session
from course import *


class CourseDownloader:
    def __init__(self):
        self.course_dir_url = "http://studentnet.cs.manchester.ac.uk/ugt/syllabus.php"
        self.session = manc_session()
        self.courses = CourseDir()
        self.url_ext = "https://my.manchester.ac.uk"
        self.open_ext = "http://studentnet.cs.manchester.ac.uk/ugt/"

    def session_get_tree(self, url):
        return html.fromstring(self.session_get_html(url))

    def session_get_html(self, url):
        return self.session.get(url).text

    def run(self):
        self.uportal_stage()
        self.syllabus_page_stage()

    def uportal_stage(self):
        cp = self.session_get_tree(
            "https://my.manchester.ac.uk/uPortal/f/mylearning/normal/render.uP"
        )
        c = cp.xpath('//*[@id="Pluto_179_u29l1n5206_238410_programPlan"]')[0]
        for y in c.findall(".//tbody"):
            for r in y.findall(".//tr"):
                cols = r.findall(".//td")[:6]
                t = cols[0].find("a")
                # print("Extracting stage 1 for", t.text)
                att = {
                    "id": t.text,
                    "name": cols[1].find("a").text,
                    "uportal_link": self.url_ext + t.get("href"),
                }
                for aa, cc in zip(("level", "semester", "credits", "req"), cols[2:]):
                    att[aa] = cc.text

                course = Course(**att)
                self.courses.add(course)

    def syllabus_page_stage(self):
        for id in list(self.courses.courses.keys()):
            c = self.courses.get(id)
            c.department = self.ex_department(id)
            if not id[:4] == "COMP":
                continue
            url = self.gen_course_syllabus_link(id)
            # print(url)
            c.syllabus_link = url
            tree = html.fromstring(requests.get(url).text)
            c.prof, c.prof_email = self.ex_professor_and_email(tree)
            c.time_table = self.ex_course_times(tree)
            c.assessment = self.ex_assess_methods(tree)
            c.prerequisites = self.ex_requisites(tree)
            # print(c)

    def gen_course_syllabus_link(self, id):
        return self.open_ext + id + "/syllabus/"

    def ex_course_times(self, p):
        div = p.xpath(
            "/html/body/div[3]/article/div[1]/section/article/div[1]/div/div"
        )[0]
        for d in div.findall(".//div"):
            if d.text is not None and d.text == "Timetable":
                table = d.getnext()

        times = []
        for row in table.findall(".//tr"):
            r = []
            for cell in row.xpath(".//th | .//td"):
                r.append(cell.text)
            times.append(r)

        return times

    def ex_reading_list(self, p):
        raise NotImplementedError

    def ex_professor_and_email(self, tree):
        elem = tree.xpath(
            "/html/body/div[3]/article/div[1]/section/article/div[1]/div/div/p[3]/a"
        )[0]
        return (elem.text, elem.get("href").replace("mailto:", ""))

    def ex_requisites(self, p):
        div = p.xpath(
            "/html/body/div[3]/article/div[1]/section/article/div[1]/div/div"
        )[0]
        ul = None
        for d in div.findall(".//strong"):
            if d.text is not None and d.text == "Requisites":
                ul = d.getparent().getnext()
        if not ul:
            return ["No requisites"]
        req = []
        for l in ul.findall(".//li"):
            req.append(re.sub("\s+", " ", l.text))
        return req

    def ex_assess_methods(self, p):
        div = p.xpath(
            "/html/body/div[3]/article/div[1]/section/article/div[1]/div/div"
        )[0]
        for d in div.findall(".//strong"):
            if d.text is not None and d.text == "Assessment methods":
                ul = d.getparent().getnext()
        assess = []
        for l in ul.findall(".//li"):
            assess.append(l.text)
        return assess

    def ex_department(self, id):
        id = id[:4]
        if id == "COMP":
            return "Department of Computer Science"
        elif id in ["MCEL", "BMAN"]:
            return "Alliance Manchester Business School"
        elif id[:2] == "UL":
            return "University Language Centre"
        else:
            return "Not found"


def main():
    cd = CourseDownloader()
    cd.run()


if __name__ == "__main__":
    main()
