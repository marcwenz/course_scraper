#!/usr/bin/env python3

from course_scraper import CourseDownloader, Course
import re
import os

# C = Course(
#     "COMP11120",
#     "Fundamentals of whatever",
#     credits="20",
#     semester="F",
#     req="Compulsory",
#     level="2",
#     department="Department of Computer Science",
#     prof="Professor Doofenschmirz",
#     prof_email="thisisan@email.com",
#     reading_list="Nothing",
#     time_table=[
#         ["Semester", "Event", "Location", "Day", "Time", "Group"],
#         ["Sem 2 w20-25", "Lecture", "IT407", "Mon", "10:00 - 12:00", " - "],
#         ["Sem 2 w26,29-31", "Lecture", "1.8", "Mon", "12:00 - 14:00", " - "],
#         ["Sem 2 w32", "Lecture", "1.8", "Mon", "12:00 - 13:00", " - "],
#         ["Sem 2 w32", "Lecture", "IT407", "Mon", "13:00 - 14:00", " - "],
#         ["Sem 2 w33", "Lecture", "IT407", "Mon", "14:00 - 16:00", " - "],
#     ],
#     syllabus_link="https://www.thisisalink.com/",
#     uportal_link="https://www.anotherdecentlink.com/",
#     assessment=["Some of this", "And some of that stuff"],
#     prerequisites=["None"],
# )

DIR = "./courses/"
TAB = "  "
DTAB = 2 * TAB
TTAB = 3 * TAB
NL = "\n"
SCHEDULE_SH = "** Schedule"
INFO_SH = "** Course Information"
READING_SH = "** Reading list"


def title(t):
    return "#+TITLE: " + t


def extras():
    return "#+STARTUP: content"


def make_header(i, j):
    return "* " + i + " - " + j


def scheduled():
    return (
        "SCHEDULED: <2020-10-08 Thu 15:00-16:00>--<2020-12-17 Thu 15:00-16:00>"
        + NL
        + "SCHEDULED: <2020-10-08 Thu 15:00-16:00>--<2020-12-17 Thu 15:00-16:00>"
    )


def timetable(t):
    t[0].insert(1, "Week")
    print(t)
    e = ["| " + " | ".join([e if e else "-" for e in row]) + " |" for row in t]

    e.insert(
        1,
        "|----------+--------------+----------------+----------+-----+---------------+-------|",
    )

    e = re.sub("Sem 2", "Sem 2 |", re.sub("Sem 1", "Sem 1 |", NL.join(e)))

    return e


def infoblock(id, name, credits, req, level, prof, email):
    return (
        ""
        + ("- ID           | " + id + NL)
        + ("- Name         | " + name + NL)
        + ("- Credits      | " + credits + NL)
        + ("- Requirement  | " + req + NL)
        + ("- Level        | " + level + NL)
        + ("- Professor    | " + prof + NL)
        + ("- Email        | mailto:" + email)
    )


def assessment(d):
    t = "- Assessment methods"
    for n in d:
        t += NL + TAB + "+ " + n
    return t


def requisites(d):
    t = "- Requisites"
    for n in d:
        t += NL + TAB + "+ " + n
    return t


def reading_link():
    return "- [[*Reading list][Reading list]]"


def schedule_link():
    return "- [[*Schedule][Timetable]]"


def syllabus_link(l):
    return f"- [[{l}][Syllabus]]"


def uportal_link(l):
    return f"- [[{l}][uPortal]]"


def blackboard_link():
    return (
        "- [[https://online.manchester.ac.uk/webapps/portal/execute/tabs/"
        + "tabAction?tab_tab_group_id=_92_1][Blackboard]]"
    )


def gen_file_text(course):
    text = [
        title(course.name),
        extras(),
        "",
        make_header(course.id, course.name),
        scheduled(),
        SCHEDULE_SH,
        "",
        timetable(list(course.time_table)),
        "",
        INFO_SH,
        infoblock(
            course.id,
            course.name,
            course.credits,
            course.req,
            course.level,
            course.prof,
            course.prof_email,
        ),
        assessment(course.assessment),
        requisites(course.prerequisites),
        schedule_link(),
        reading_link(),
        syllabus_link(course.syllabus_link),
        uportal_link(course.uportal_link),
        blackboard_link(),
        "",
        READING_SH,
    ]
    return NL.join(text)


def make_course_dir(course):
    path = DIR + course
    if not os.path.exists(path):
        os.mkdir(path)

    return path


def write_file(path, text):
    with open(path, mode="w") as f:
        f.write(text)


def main():
    cd = CourseDownloader()
    cd.run()
    for course in cd.courses.courses.values():

        if course.id[:4] == "COMP":
            print("Generating file for", course.id)
            path = make_course_dir(course.id.lower())
            o = gen_file_text(course)
            print(o)
            write_file(path + "/" + course.id.lower() + ".org", o)


if __name__ == "__main__":
    main()
