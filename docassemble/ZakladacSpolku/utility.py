from docassemble.base.util import validation_error, value
import json
import requests
import xmltodict

def contains_spolek(x):
  x = x.lower()
  if "spolek" in x:
    return True
  elif "z. s." in x:
    return True
  elif "zapsaný spolek" in x:
    return True
  else:
    validation_error('Název spolku <strong>musí</strong> obsahovat "z. s.", "spolek", nebo "zapsaný spolek"')
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

def overitXml(firma):
  URL = 'https://wwwinfo.mfcr.cz/cgi-bin/ares/darv_std.cgi'
  params = {'obchodni_firma': firma}
  page = requests.get(URL, params=params)
  page.encoding = 'utf-8'
  ares_data = xmltodict.parse(page.text)
  response_root_wrapper = ares_data['are:Ares_odpovedi']
  response_root = response_root_wrapper['are:Odpoved']
  number_of_results = response_root['are:Pocet_zaznamu']

  info = []
  try:
    if int(number_of_results) == 0:
      return "False"
    elif int(number_of_results) == 1:
      company_record = response_root['are:Zaznam']
      info.append(company_record.get('are:Obchodni_firma'))
    else:
      info = []
      company_record = response_root['are:Zaznam']
      for zaznam in company_record:
        info.append(zaznam.get('are:Obchodni_firma'))
    return info
  except:
    return "False"
