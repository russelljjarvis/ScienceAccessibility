import requests

from elife_api_validator.validators import JSONResponseValidator

response = requests.get('https://api.elifesciences.org/articles')
print(response.content)
#JSONResponseValidator.validate(response)
