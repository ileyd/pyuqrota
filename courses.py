"""
Code relating to courses (subjects)
"""
import requests
import datetime
import arrow
import json
from typing import List

class Course:
  """Describes a subject available at the University of Queensland"""
  
  # subject code of form ABCD1234
  code: str = ""
  # subject name
  name: str = ""
  # subject description
  description: str = ""
  # unit value of the course
  units: int = -1
  # duration in semesters
  duration: int = -1
  # course coordinator information
  coordinator: str = ""
  # faculty the course belongs to
  faculty: str = ""
  # school the course belongs to
  school: str = ""
  # last updated time
  last_update: datetime.datetime = None
  # prerequisite course codes -- NOTE: you do not necessarily need all of these
  prerequisites: List[str] = []
  # dependent course codes; courses that have this course as a prerequisite
  dependents: List[str] = []
  # incompatible course codes
  incompatibilities: List[str] = []
  # actual prerequisite structure
  prerequisites_structure: dict = {}
  # recommended prerequisite structure
  recommended_structure: dict = {}
  # prerequisite text
  prerequisites_text: str = ""
  # recommended text
  recommended_text: str = ""
  # incompatible text
  incompatibilities_text: str = ""
  # offering ids
  offerings: List[int] = []

  def valid(self):
    """Determines whether the Course object represents a valid course"""
    return not (self.code == "" or self.name == "" or self.units < 1 or self.duration < 1)

  def __init__(self, code: str):
    self.code = code
    self.update()

  def children(self):
    """Obtains and returns child plans from UQ's Rota API"""
    url = 'http://rota.eait.uq.edu.au/course/{}/plans.json'.format(self.code)
    res = requests.get(url)
    try:
      data = res.json()
    except:
      raise ValueError('Response from Rota API is not valid JSON.')
    plan_ids: List[int] = []
    for plan in data:
      plan_ids.append(plan["id"])
    # plans: List[Plan] = []
    # for id in plan_ids:
    #   plans.append(Plan(id))
    # return plans
    return plan_ids    

  def update(self):
    """Update self with information from UQ's Rota API"""
    url = 'http://rota.eait.uq.edu.au/course/{}.json'.format(self.code)
    res = requests.get(url)
    try:
      data = res.json()
    except:
      raise ValueError('The response from the Rota API was not valid JSON.')
    self.name = data["name"]
    self.description = data["description"]
    self.units = data["units"]
    self.duration = data["duration"]
    self.coordinator = data["coordinator"]
    self.faculty = data["faculty"]
    self.school = data["school"]
    self.last_update = arrow.get(data["last_update"]).datetime
    self.prerequisites = []
    for prereq in data["prereqs"]:
      self.prerequisites.append(prereq["code"])
    self.dependents = []
    for dep in data["dependents"]:
      self.dependents.append(dep["code"])
    self.incompatibilities = []
    for inc in data["incompatibles"]:
      self.incompatibilities.append(inc["code"])
    self.prerequisites_structure = data["prereq_struct"] # lazy; todo fix up slightly
    self.recommended_structure = data["recommended_struct"] #lazy; todo fix up slightly
    self.prerequisites_text = data["prereq_text"]
    self.recommended_text = data["recommended_text"]
    self.incompatibilities_text = data["incompatible_text"]
    self.offerings = []
    for offer in data["offerings"]:
      self.offerings.append(offer["id"])
  
def courses_by_criteria(query: dict):
  params = {
    "with": query
  }
  url = 'http://rota.eait.uq.edu.au/courses/find.json'
  res = requests.get(url, params=params)
  try:
    data = res.json()
  except:
    raise ValueError('Response from Rota API was not valid JSON.')
  courses: List[Course] = []
  for course in data:
    courses.append(Course(course["code"]))
  return courses