#!/usr/bin/env python3


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
        uportal_link=None,
        assessment=None,
        prerequisites=None,
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
        self.uportal_link = uportal_link
        self.assessment = assessment
        self.prerequisites = prerequisites

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
            self.uportal_link,
            self.assessment,
            self.prerequisites,
        ]

    def __str__(self):
        names = [
            "ID",
            "Name",
            "Credits",
            "Semester",
            "Requirement",
            "Level",
            "Department",
            "Professor",
            "Professor Email",
            "Reading List",
            "Time table",
            "Syllabus link",
            "uPortal link",
            "Assessment menthods",
            "Requisites",
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

    def get(self, n):
        if isinstance(n, int):
            return list(self.courses.values())[n]
        elif isinstance(n, str):
            return self.courses[n]
        else:
            raise ValueError("arg n must either be int or str")

    def add(self, c, replace=True):
        if not replace and c.id in self.courses.keys():
            return 0
        self.courses[c.id] = c
        return 1
