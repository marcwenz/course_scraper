#!/usr/bin/env python3

import requests
from lxml import html, etree

from course import Course
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


class CourseDir:
    def __init__(self):
        self.courses = {}
        self.current = None

    def __str__(self):
        return "\n\n---------------------------------------\n\n".join(
            [":\n".join((i, str(c))) for i, c in self.courses.items()]
        )

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

    def get_uportal_tree(self):
        return html.fromstring(
            self.session.get(
                "https://my.manchester.ac.uk/uPortal/f/mylearning/normal/render.uP"
            ).text
        )

    def dl_url(self, url):
        return (url, str(requests.get(url).text))

    def parse_tree(self, page):
        return html.fromstring(page)

    def get_dir_tree(self):
        return self.parse_tree(self.dl_url(self.course_dir_url)[-1])

    def ex_courses_links(self):
        cp = self.get_uportal_tree()
        c = cp.xpath('//*[@id="Pluto_179_u29l1n5206_238410_programPlan"]')[0]
        for y in c.findall(".//tbody"):
            for r in y.findall(".//tr"):
                cols = r.findall(".//td")[:6]
                t = cols[0].find("a")
                att = {
                    "id": t.text,
                    "name": cols[1].find("a").text,
                    "uportal_link": t.get("href"),
                }
                for aa, cc in zip(("level", "semester", "credits", "req"), cols[2:]):
                    att[aa] = cc.text

                course = Course(**att)
                self.courses.add_course(course)

    def dl_course(self, url):
        pass

    def gen_course_obj(self, **kw):
        return Course(**kw)

    def ex_id(self):
        pass

    def ex_name(self):
        pass

    def ex_syllabus(self):
        pass

    def ex_sem(self):
        pass

    def ex_level(self):
        pass

    def ex_course_times(self):
        pass

    def ex_yr(self):
        pass

    def ex_credits(self):
        pass

    def ex_reading_list(self):
        pass

    def ex_professor(self):
        pass

    def ex_professor_email(self):
        pass

    def ex_course_links(self):
        pass

    def ex_assess_methods(self):
        pass

    def ex_department(self):
        pass

    def ex_requirement(self):
        pass


def gen_files_for_all_courses():
    cd = CourseDownloader()
    links = cd.ex_courses_links(cd.get_dir_tree())


def main():
    cd = CourseDownloader()
    cd.ex_courses_links()
    print(cd.courses)


if __name__ == "__main__":
    main()
