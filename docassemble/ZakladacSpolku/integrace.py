import requests
from docassemble.base.util import get_config

def addEcomail (email):
  ecomailKey = get_config('ecomailKey')

  header = {'key': ecomailKey,'Content-Type': 'application/json'}

  values = '''
  {
  "subscriber_data": {
    "email": "'''+ email +'''",
    "tags": [
      "OBČAN 2.0",
      "Zakladac"
    ]
  },
  "trigger_autoresponders": true,
  "update_existing": true,
  "resubscribe": true
  }
  '''
  r = requests.post('http://api2.ecomailapp.cz/lists/96/subscribe', headers=header, data=values)

  return
