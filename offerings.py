import requests
import arrow
import datetime

class Offering:
  """An instance of a particular course in a particular semester"""
  # is this a rota id number, or...?
  id: int = -1
  # location
  location: str = ""
  # mode
  mode: str = ""
  # last updated
  last_update: datetime.datetime = None
  # sinet_class -- what is this?
  sinet_class: int = -1
  # assessment tasks
  assessment: list = []
  # course code
  course: str = ""
  # semester id
  semester: int = -1
  # campus code
  campus: str = ""
  # classes series
  series: list = []

  def valid(self):
    """Returns whether the Offering object represents a valid offering or not"""
    return not (self.id <= 0 or self.course == "" or self.semester < 6000)

  def __init__(self, oid: int):
    if oid <= 0:
      raise ValueError('Provided offering id is invalid.')
    else:
      self.update()

  def update(self):
    url = 'http://rota.eait.uq.edu.au/offering/{}.json'.format(self.id)
    res = requests.get(url)
    try:
      data = res.json()
    except:
      raise ValueError('Response from Rota API was not valid JSON.')
    self.location = data["location"]
    self.mode = data["mode"]
    self.last_update = arrow.get(data["last_update"]).datetime
    self.sinet_class = data["sinet_class"]
    self.assessment = data["assessment_tasks"] # TODO fix
    self.course = data["course"]["code"]
    self.semester = data["semester"]["id"]
    self.campus = data["campus"]["code"]