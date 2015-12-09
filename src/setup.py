import json

from models.user import User
from models.survey import Survey
from config.config import application

class Setup:
    def init_data(self):
        with open('../schema/sampleSurvey.json', 'r') as f:
           data = json.loads(f.read())
           Survey().create_item(data)

        user = {'username': 'george'}
        user = {'': 'george'}
        User().create_item(user)

if __name__ == "__main__":
    main()
