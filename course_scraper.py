#!/usr/bin/env python3

import requests
from lxml import html, etree

from cas_auth import manc_session


class Course:
    def __init__(
        self,
        id=None,
        name=None,
        credits=None,
        semester=None,
        req=None,
        level=None,
        department=None,
        prof=None,
        prof_email=None,
        reading_list=None,
        time_table=None,
        syllabus_link=None,
        materials_link=None,
        uportal_link=None,
        assessment=None,
        prerequisites=None,
        corequisites=None,
    ):
        self.id = id
        self.name = name
        self.credits = credits
        self.semester = semester
        self.req = req
        self.level = level
        self.department = department
        self.prof = prof
        self.prof_email = prof_email
        self.reading_list = reading_list
        self.time_table = time_table
        self.syllabus_link = syllabus_link
        self.materials_link = materials_link
        self.uportal_link = uportal_link
        self.assessment = assessment
        self.prerequisites = prerequisites
        self.corequisites = corequisites

    def all_values(self):
        return [
            self.id,
            self.name,
            self.credits,
            self.semester,
            self.req,
            self.level,
            self.department,
            self.prof,
            self.prof_email,
            self.reading_list,
            self.time_table,
            self.syllabus_link,
            self.materials_link,
            self.uportal_link,
            self.assessment,
            self.prerequisites,
            self.corequisites,
        ]

    def __str__(self):
        names = [
            "ID",
            "Name",
            "Credits",
            "Semester",
            "Requirements",
            "Level",
            "Department",
            "Professor",
            "Professor Email",
            "Reading List",
            "Time table",
            "Syllabus link",
            "Materials link",
            "uPortal link",
            "Assessment menthods",
            "Prerequisites",
            "Corequisites",
        ]

        return str(
            "\t"
            + "\n\t".join(
                [": ".join((n, str(i))) for n, i in zip(names, self.all_values())]
            )
        )

    def extend_attrs(self, attrs):
        for attr, val in attrs.items():
            setattr(self, attr, val)


class CourseDir:
    def __init__(self):
        self.courses = {}
        self.current = None

    def __str__(self):
        return "\n\n---------------------------------------\n\n".join(
            [":\n".join((i, str(c))) for i, c in self.courses.items()]
        )

    def __getitem__(self, x):
        return self.courses[x]

    def all(self):
        return self.courses

    def get_course(self, n):
        if isinstance(n, int):
            return self.courses.values()[n]
        elif isinstance(n, str):
            return self.courses[n]
        else:
            raise ValueError("arg n must either be int or str")

    def add_course(self, c, replace=False):
        if not replace and c.id in self.courses.keys():
            return 0
        self.courses[c.id] = c
        return 1


class CourseDownloader:
    def __init__(self):
        self.course_dir_url = "http://studentnet.cs.manchester.ac.uk/ugt/syllabus.php"
        self.session = manc_session()
        self.courses = CourseDir()
        self.url_ext = "https://my.manchester.ac.uk"

    def session_get_tree(self, url):
        return html.fromstring(self.session.get(url).text)

    def run(self):
        self.uportal_stage()

    def uportal_stage(self):
        cp = self.session_get_tree(
            "https://my.manchester.ac.uk/uPortal/f/mylearning/normal/render.uP"
        )
        c = cp.xpath('//*[@id="Pluto_179_u29l1n5206_238410_programPlan"]')[0]
        for y in c.findall(".//tbody"):
            for r in y.findall(".//tr"):
                cols = r.findall(".//td")[:6]
                t = cols[0].find("a")
                print("Extracting stage 1 for", t.text)
                att = {
                    "id": t.text,
                    "name": cols[1].find("a").text,
                    "uportal_link": self.url_ext + t.get("href"),
                }
                for aa, cc in zip(("level", "semester", "credits", "req"), cols[2:]):
                    att[aa] = cc.text

                course = Course(**att)
                self.courses.add_course(course)

    def gen_course_obj(self, **kw):
        return Course(**kw)

    def ex_materials(self, p):
        pass

    def ex_syllabus(self, p):
        pass

    def ex_course_times(self, p):
        pass

    def ex_reading_list(self, p):
        pass

    def ex_professor(self, p):
        pass

    def ex_professor_email(self, p):
        pass

    def ex_assess_methods(self, p):
        m = []
        t = p.xpath('//*[@id="Pluto_179_u29l1n5206_238410_cuAdditionalDetails"]')[0]
        for r in t.findall(".//h4"):
            if r.text == "Assessment methods":
                t = r.getnext()
                break
        for r in t.findall(".//tr"):
            for e in r.xpath(".//th | .//td | .//p"):
                if j := e.text:
                    if i := j.strip():
                        m.append(i)
        if len(m) == 0:
            for r in t.findall(".//p"):
                if j := r.text:
                    if i := j.strip():
                        m.append(i.strip())
        return m

    def ex_department(self, p):
        d = p.xpath('//*[@id="$(n)cui-container"]/div[2]/div/dl/dd[5]')[0].text.strip()
        return d


def gen_files_for_all_courses():
    cd = CourseDownloader()
    links = cd.run(cd.get_dir_tree())


def main():
    cd = CourseDownloader()
    cd.run()
    print(cd.courses)


if __name__ == "__main__":
    main()
