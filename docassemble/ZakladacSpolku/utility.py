from docassemble.base.util import validation_error, value
import json
import requests

def contains_spolek(x):
  x = x.lower()
  if "spolek" in x:
    return True
  elif "z.s." in x:
    return True
  elif "zapsaný spolek" in x:
    return True
  else:
    validation_error('Název spolku <strong>musí</strong> obsahovat "z.s.", "spolek", nebo "zapsaný spolek"')
  return

def string_pole(x):
  x = x.split('\r\n')
  return x

def ziskejPolozky(kat):
  page = requests.get("https://da-test.frankbold.org/playgroundstatic/Zakladac/1/checklist.json")
  y = json.loads(page.content)
  list_duvody = {}

  for x in y['checklist']:
    if x["kategorie"] == kat:
      if x["hodnota"] == value(str(x["podminka"])):
        list_duvody[x["id"]] = x["text"]

  return list_duvody
