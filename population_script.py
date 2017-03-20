#!/usr/bin/python
# -*- coding: latin-1 -*-
import os
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RateMyLecturer.settings')
import django

django.setup()
from lecturer.models import University
from lecturer.models import Department
from log.models import UserProfile
from lecturer.models import Lecturer
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.utils import timezone
from lecturer.models import Rating
from lecturer.models import Comment

# Reading a file and creating dictionaries for the population script.
# Universities_Shortened looks like: {'University of St Andrews': 'St Andrews', 'Cardiff University': 'Cardiff',...}
# Universities_Departments looks like: {'University of St Andrews': ['Maths', 'Chemistry', 'Computing Science'..]..}
# Universities_Domains looks like: {'University of St Andrews: ['gla.ac.uk']
# User looks like: {'username':['firstname','secondname,'email','password']..}
Universities_Shortened = {}
Universities_Departements = {}
Universities_Domains = {}
User = {}
comments = ["Best Lecturer Ever", "Decent Lecturer", "Nice Lessons", "Meh", "Had a good nap during the lesson",
            "More memes please"]

f = open("UniversityList2.txt", "r")
lineCount = 0
for line in f:
    if lineCount == 3:
        lineCount = 0
    lineCount += 1

    lineStripped = line.strip("\n").rsplit(";")
    if lineCount == 1:
        Universities_Shortened[lineStripped[0]] = lineStripped[1]
        name = lineStripped[0]

    if lineCount == 2:
        Universities_Departements[name] = lineStripped

    if lineCount == 3:
        Universities_Domains[name] = lineStripped

f = open("User.txt", "r")
for line in f:
    lineStripped = line.strip("\n").rsplit(";")
    User[lineStripped[0]] = lineStripped[1:]

f = open("Lecturers.txt", "r")
LecturersArray = []
for line in f:
    lineStripped = line.strip("\n")
    LecturersArray.append(lineStripped)


# Population script:

def add_University(name, short_name, domain):
    u = University.objects.get_or_create(name=name, short_name=short_name, domain=domain)[0]
    u.save()
    return u


def add_Department(name, university):
    d = Department.objects.get_or_create(name=name, university=university)[0]
    d.save()
    return d


def add_Users(username, firstname, lastname, email, password):
    user = get_user_model().objects.get_or_create(username=username, email=email, password=password)[0]
    user.first_name = firstname
    user.last_name = lastname
    user.save()
    return user


def add_UserProfile(user, picture, date_joined, last_active, university):
    userProfile = \
        UserProfile.objects.get_or_create(user=user, picture=picture, date_joined=date_joined, last_active=last_active,
                                          university=university)[0]
    userProfile.save()
    return userProfile


def add_Lecturers(title, firstname, lastname, date_added, university, department, added_by):
    lecturer = Lecturer.objects.get_or_create(title=title, first_name=firstname, last_name=lastname,
                                              date_added=date_added, university=university, department=department,
                                              added_by=added_by)[0]
    lecturer.save()
    return lecturer


def add_Rating(value, user, lecturer, date_rated):
    rating = Rating.objects.get_or_create(value=value, user=user, lecturer=lecturer, date_rated=date_rated)[0]
    rating.save()


def add_Comment(comment_text, user, lecturer, date_commented, is_anonymous):
    comment = Comment.objects.get_or_create(comment_text=comment_text, user=user, lecturer=lecturer,
                                            date_commented=date_commented, is_anonymous=is_anonymous)[0]
    comment.save()


def populate():
    for U in Universities_Shortened:
        print("Populating Universities...")
        university = add_University(U, Universities_Shortened[U], Universities_Domains[U][0])
        for d in Universities_Departements[U]:
            print("Populating University Departments...")
            add_Department(d, university)
        for V in User:
            print("Populating Users and User Profiles...")
            user = add_Users(V + Universities_Shortened[U], User[V][0], User[V][1],
                             User[V][2] + "@" + Universities_Domains[U][0], User[V][3])
            add_UserProfile(user, None, timezone.now(), timezone.now(), university)

    # Populate Lecturers
    for departments in Department.objects.all():
        print("Populating Lecturers...")
        # Get or Create User that will add the lecturers.
        user = add_Users("addlectureruser" + departments.university.short_name, "AddLecturer", "User",
                         "addlectureruser@" + departments.university.domain, "password12345")
        if not UserProfile.objects.filter(user=user).exists():
            add_UserProfile(user, None, timezone.now(), timezone.now(), departments.university)
        firstRand = random.randrange(0, len(LecturersArray))
        secondRand = random.randrange(0, len(LecturersArray))

        # Changes second random number in case its equal to first, otherwhise will give me an error when populating same
        # person for same department
        while secondRand == firstRand:
            secondRand = random.randrange(0, len(LecturersArray))

        firstLecturer = LecturersArray[firstRand].rsplit(" ")
        secondLecturer = LecturersArray[secondRand].rsplit(" ")

        # Populates Lecturers
        lecturer1 = add_Lecturers("Dr", firstLecturer[0], firstLecturer[1], timezone.now(), departments.university,
                                  departments,
                                  user)
        lecturer2 = add_Lecturers("Dr", secondLecturer[0], secondLecturer[1], timezone.now(), departments.university,
                                  departments,
                                  user)
        # Populates the rating of those lecturers
        Rating1 = random.randrange(0, 11)
        Rating2 = random.randrange(0, 11)
        add_Rating(Rating1, user, lecturer1, timezone.now())
        add_Rating(Rating2, user, lecturer2, timezone.now())

        # Adds comments to the lecturers.
        commentNumber1 = random.randrange(0,len(comments))
        commentNumber2 = random.randrange(0,len(comments))
        if not Comment.objects.filter(user=user, lecturer=lecturer1).exists():
            add_Comment(comments[commentNumber1], user, lecturer1, timezone.now(), 0)
        if not Comment.objects.filter(user=user, lecturer=lecturer2).exists():
            add_Comment(comments[commentNumber2], user, lecturer2, timezone.now(), 0)



    print("Population script completed!")
    print("¯\_(ツ)_/¯")


if __name__ == '__main__':
    print("Starting RateMyLecturer population script...")
    populate()
