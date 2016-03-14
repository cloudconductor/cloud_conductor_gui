from ..utils import ApiUtil
from ..utils.ApiUtil import Url
from ..api_models.blueprint_histories import *


class Blueprints:
    def __init__(self, code, auth_token, project_id):
        self.code = code
        self.auth_token = auth_token
        self.project_id = project_id
        url = Url.blueprintList
        data = {
                'auth_token': self.auth_token,
                'project_id': project_id
               }
        self.blueprints = ApiUtil.requestGet(url, self.code, data)

    def get_blueprint(self, id):
        for blueprint in self:
            if blueprint['id'] == id:
                return blueprint

    def get_all_blueprint_histories(self):
        result = []
        for blueprint in self:
            blueprint_histories = BlueprintHistories(self.code,
                                                     self.auth_token,
                                                     blueprint['id'])

            for blueprint_history in blueprint_histories:
                result.append(blueprint_history)

        return result

    def __iter__(self):
        for blueprint in self.blueprints:
            yield(blueprint)
