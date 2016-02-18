from ..utils import ApiUtil
from ..utils import StringUtil
from ..utils.ApiUtil import Url


def get_system_list(code, token, project_id=None):

    # -- Create a cloud, api call
    url = Url.systemList
    data = {
        'auth_token': token,
        'project_id': project_id,
    }
    # -- API call, get a response
    list = ApiUtil.requestGet(url, code, data)

    return list


def get_system_list2(code, token, project_id=None):

    systems = get_system_list(code, token, project_id)

    dic = {}
    list = []
    for sys in systems:

        dic['id'] = str(sys.get('id'))
        dic['name'] = sys.get('name')
        list.append(dic.copy())

    return list


def get_system_detail(code, token, id):

    if StringUtil.isEmpty(code):
        return None

    if StringUtil.isEmpty(token):
        return None

    if StringUtil.isEmpty(id):
        return None

    url = Url.systemDetail(id, Url.url)
    data = {
        'auth_token': token,
    }
    system = ApiUtil.requestGet(url, code, data)

    return StringUtil.deleteNullDict(system)


def create_system(code, token, project_id, form):
    # -- Create a system, api call
    url = Url.systemCreate
    form = StringUtil.deleteNullDict(form)

    form['auth_token'] = token
    form['project_id'] = project_id

    # -- API call, get a response
    system = ApiUtil.requestPost(url, code, StringUtil.deleteNullDict(form))

    return system


def edit_system(code, token, id, form):
    # -- Create a system, api call
    url = Url.systemEdit(id, Url.url)

    data = StringUtil.deleteNullDict(form)
    data['auth_token'] = token

    # -- API call, get a response
    system = ApiUtil.requestPut(url, code, data)

    return system


def get_system_delete(code, token, id):

    if StringUtil.isEmpty(code):
        return None

    if StringUtil.isEmpty(token):
        return None

    if StringUtil.isEmpty(id):
        return None

    url = Url.systemDelete(id, Url.url)
    data = {'auth_token': token}
    ApiUtil.requestDelete(url, code, data)
