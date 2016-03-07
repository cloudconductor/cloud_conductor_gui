from ..utils import ApiUtil
from ..utils.ApiUtil import Url


class Environments:
    def __init__(self, code, auth_token, project_id):
        self.code = code
        self.auth_token = auth_token
        self.project_id = project_id
        url = Url.environmentList
        data = {
                'auth_token': self.auth_token,
                'project_id': self.project_id,
               }
        self.environments = ApiUtil.requestGet(url, self.code, data)

    def get_environment(self, id):
        for system in self:
            if system['id'] == id:
                return system

    def __iter__(self):
        for environment in self.environments:
            yield(environment)
