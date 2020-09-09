#!/usr/bin/env python3

class Course:
    """
    Course object.
    id(str): course ID format COMPXXXXX
    name(str): course name
    syllabus(str): link to syllabus
    sem(list(int)): semester the course is taught, if full year list(1,2)
    credits(int): number of credits the course gives
    rl(list(list(str))): reading list in format [title, author, publisher, year]
    """
    def __init__(self, id, name, syllabus, sem, yr, credits, rl=None):
        self.id = id
        self.name = name
        self.syllabus = syllabus
        self.sem = sem
        self.yr = yr
        self.credits = credits
        if rl:
            self.rl = rl
        else:
            self.rl = [["NO READING LIST"]]
