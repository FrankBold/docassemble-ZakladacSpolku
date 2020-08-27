import requests
import keys

def addEcomail (email):
  header = {'key': keyEcomail,'Content-Type': 'application/json'}

  values = '''
  {
  "subscriber_data": {
    "email": "'''+ email +'''",
    "tags": [
      "Zakladac"
    ]
  },
  "trigger_autoresponders": true,
  "update_existing": true,
  "resubscribe": true
  }
  '''
  r = requests.post('http://api2.ecomailapp.cz/lists/75/subscribe', headers=header, data=values)

  return
