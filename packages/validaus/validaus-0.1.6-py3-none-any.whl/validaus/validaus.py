import requests
import json

API_VERSION = 1

validausAPIMethods = {
  "publishFact": {
    "action": 'POST',
    "endpoint": 'publish'
  },
  "getFacts": {
    "action": 'GET',
    "endpoint": 'facts'
  },
  "validateFacts": {
    "action": 'POST',
    "endpoint": 'validate'
  }
}

class Validaus:
    def __init__(
        self, 
        validausURL: str,
        app: str,
        apiKey: str
    ):
        self.validausURL = validausURL
        self.app = app
        self.apiKey = apiKey

    def constructEndpointURL(self, endpoint: str) -> str:
        return "{}/api/v{}/{}".format(self.validausURL, API_VERSION, endpoint)

    def makeGQLRequest(self, apiMethod: object, body: object):
        endpointURL = self.constructEndpointURL(apiMethod['endpoint'])
        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'x-validaus-api-key': self.apiKey
        }

        action = apiMethod['action']

        if action == 'POST':
            resp = requests.post(
                endpointURL,
                headers = headers,
                data = json.dumps(body)
            )
        elif action == 'GET':
            resp = requests.get(
                endpointURL,
                headers = headers,
                params = body
            )
        else:
            raise Exception('Invalid action: {}'.format(action))
        return json.loads(resp.content)

    def publishFact(self, metric: str, fact: object):
        try:
            publishFactObj = {
                "app": self.app,
                "metric": metric,
                "fact": fact
            }
            return self.makeGQLRequest(validausAPIMethods['publishFact'], publishFactObj)
        except:
            print('Validaus:publishFact() -> Error occurred.')

    def getFacts(self, metric: str):
        try:
            getFactsObj = {
                "app": self.app,
                "metric": metric,
            }
            return self.makeGQLRequest(validausAPIMethods['getFacts'], getFactsObj)
        except:
            print('Validaus:getFacts() -> Error occurred.')

    def validateFacts(self, metric: str, facts: list):
        try:
            validateFactsObj = {
                "app": self.app,
                "metric": metric,
                "facts": facts
            }
            return self.makeGQLRequest(validausAPIMethods['validateFacts'], validateFactsObj)
        except:
            print('Validaus:validateFacts() -> Error occurred.')
