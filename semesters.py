"""
Code relating to semesters
"""
import requests
from typing import List

class Semester:
  """A standard teaching period at the university
  """
  # UQ's identifier for the semester
  id: int = -1
  # UQ's name for the semester
  name: str = ""
  # the semester number for the year
  number: int = -1
  # the week the semester starts in
  start_week: int = -1
  # the midsemester week
  midsemester_week: int = -1
  # the week the semester finishes in
  finish_week: int = -1
  # whether this is a current semester
  current: bool = False
  # preceeding semester id
  preceeding: int = -1
  # succeeding semester
  succeeding: int = -1

  def valid(self):
    """Whether the semester object represents a valid semester"""
    return not (self.id < 6000 or self.name == "")

  def __init__(self, id: int):
    """Initialises the semester object based on information retrieved from Rota"""
    self.id = id
    self.update()

  def update(self):
    """Updates the semester object with information from the Rota API"""
    url = 'http://rota.eait.uq.edu.au/semester/{}.json'.format(self.id)
    res = requests.get(url)
    
    try:
      data = res.json()
    except:
      raise ValueError("Response from rota API was not valid JSON")
    
    self.name = data.name
    if data.number != "?":
      self.number = int(data.number)
    self.start_week = data.start_week
    self.midsemester_week = data.midsem_week
    self.finish_week = data.finish_week
    self.current = data
    try:
      self.preceeding = data.pred.id
    except:
      pass
    try:
      self.succeeding = data.succ.id
    except:
      pass
    
def get_all_semesters():
  url = 'http://rota.eait.uq.edu.au/semesters.json'
  res = requests.get(url)
  try:
    data = res.json()
  except:
    raise ValueError("Response from rota API was not valid JSON")

  semesters: List[Semester] = []

  for semester in data:
    sid = semester.id
    sem = Semester(sid)
    semesters.append(sem)

  return semesters
  