import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'RateMyLecturer.settings')
import django

django.setup()
from lecturer.models import University
from lecturer.models import Department


# Reading a file and creating dictionaries for the population script.
# Universities_Shortened looks like: {'University of St Andrews': 'St Andrews', 'Cardiff University': 'Cardiff',...}
# Universities_Departments looks like: {'University of St Andrews': ['Maths', 'Chemistry', 'Computing Science'..]..}
# Universities_Domains looks like: {'University of St Andrews: ['gla.ac.uk']

Universities_Shortened = {}
Universities_Departements = {}
Universities_Domains = {}

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

# Population script:

def add_University(name, short_name, domain):
    u = University.objects.get_or_create(name=name, short_name=short_name, domain=domain)[0]
    u.save()
    return u
def add_Department(name, university):
    d = Department.objects.get_or_create(name=name, university=university)[0]
    d.save()
    return d

def populate():
    for U in Universities_Shortened:
        university = add_University(U, Universities_Shortened[U], Universities_Domains[U][0])
        for d in Universities_Departements[U]:
             add_Department(d, university)


    # print out universities we have added:
    for U in University.objects.all():
        print(str(U))

if __name__ == '__main__':
    print("Starting RateMyLecturer population script...")
    populate()
