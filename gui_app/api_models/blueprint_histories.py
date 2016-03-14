from ..utils import ApiUtil
from ..utils.ApiUtil import Url


class BlueprintHistories:
    def __init__(self, code, auth_token, blueprint_id):
        self.code = code
        self.auth_token = auth_token
        self.blueprint_id = blueprint_id
        url = Url.blueprintHistoriesList(self.blueprint_id, Url.url)
        data = {
                'auth_token': self.auth_token,
               }
        self.blueprint_histories = ApiUtil.requestGet(url, self.code, data)

    def get_blueprint_history(self, id):
        for blueprint_history in self:
            if blueprint_history['id'] == id:
                return blueprint_history

    def __iter__(self):
        for blueprint_history in self.blueprint_histories:
            yield(blueprint_history)
