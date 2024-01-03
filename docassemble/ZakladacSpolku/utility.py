from docassemble.base.util import validation_error, value, path_and_mimetype
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
  (filename, mimetype) = path_and_mimetype('data/static/checklist.json')
  soubor = open(filename, "r", encoding="utf-8")
  y = json.load(soubor)
  soubor.close()
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

def overitJson(ico = None, firma = None):
    # Use the same URL as in the 'overit' function
    URL = 'https://ares.gov.cz/ekonomicke-subjekty-v-be/rest/ekonomicke-subjekty/vyhledat'
    
    # Parameters are now sent as JSON in the body of the request
    call = {
        'start': 0, 
        'pocet': 10, 
    }

    if ico:
        call['ico'] = [ico]

    if firma:
        call['obchodniJmeno'] = firma

    payload = json.dumps(call)

    # Specify the content type as JSON
    headers = {'Content-Type': 'application/json'}

    # Make a POST request
    response = requests.post(URL, data=payload, headers=headers)
    data = response.json()

    info = []

    try:
      if data["pocetCelkem"] == 0:
          return "False"
      
      elif data["pocetCelkem"] == 1:
          info.append(data["ekonomickeSubjekty"][0]["obchodniJmeno"])
          return info
      
      else:
          for firma in data["ekonomickeSubjekty"]:
              info.append(firma["obchodniJmeno"])
        
      return info

    except:
       return "False"