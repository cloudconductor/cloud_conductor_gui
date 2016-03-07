from ..utils import ApiUtil
from ..utils.ApiUtil import Url


class Systems:
    def __init__(self, code, auth_token, project_id):
        self.code = code
        self.auth_token = auth_token
        self.project_id = project_id
        data = {
                'auth_token': self.auth_token,
                'project_id': self.project_id
               }
        self.systems = ApiUtil.requestGet(Url.systemList, self.code, data)

    def get_system(self, id):
        for system in self.systems:
            if system['id'] == id:
                return system

    def __iter__(self):
        for system in self.systems:
            yield(system)
