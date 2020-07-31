import requests

def addEcomail (email):
  header = {'key': '80a87e5f1f0b486fa0314a6df1f5aa6f','Content-Type': 'application/json'}

  values = '''
  {
  "subscriber_data": {
    "email": "'''+ email +'''",
    "tags": [
      "Zakladac_testing"
    ]
  },
  "trigger_autoresponders": true,
  "update_existing": true,
  "resubscribe": false
  }
  '''
  r = requests.post('http://api2.ecomailapp.cz/lists/75/subscribe', headers=header, data=values)
  
  return