from ..utils import ApiUtil
from ..utils import StringUtil
from ..utils.ApiUtil import Url


def get_pattern_list(code, token, project_id):

    if StringUtil.isEmpty(code):
        return None

    if StringUtil.isEmpty(token):
        return None

    if StringUtil.isEmpty(project_id):
        return None

    url = Url.patternList
    data = {
        'auth_token': token,
        'project_id': project_id
    }
    list = ApiUtil.requestGet(url, code, data)

    return list


def get_pattern_list2(code, token, project_id):

    patterns = get_pattern_list(code, token, project_id)

    if StringUtil.isNotEmpty(patterns):
        dic = {}
        list = []
        for pattern in patterns:
            dic['id'] = str(pattern.get('id'))
            dic['name'] = pattern.get('name')
            list.append(dic.copy())

        return list

    else:
        return None


def get_pattern_detail(code, token, id):

    if StringUtil.isEmpty(code):
        return None

    if StringUtil.isEmpty(token):
        return None

    if StringUtil.isEmpty(id):
        return None

    url = Url.patternDetail(id, Url.url)
    data = {
        'auth_token': token,
        'id': id,
    }
    pattern = ApiUtil.requestGet(url, code, data)

    return StringUtil.deleteNullDict(pattern)


def create_pattern(code, token, name, description):
    # -- Create a pattern, api call
    url = Url.patternCreate
    data = {
        'auth_token': token,
        'name': name,
        'description': description
    }

    data = StringUtil.deleteNullDict(data)
    # -- API call, get a response
    pattern = ApiUtil.requestPost(url, code, data)

    return pattern


def edit_pattern(code, token, id, name, description):
    # -- Create a pattern, api call
    url = Url.patternEdit(id, Url.url)
    data = {
        'auth_token': token,
        'name': name,
        'description': description
    }
    data = StringUtil.deleteNullDict(data)
    # -- API call, get a response
    pattern = ApiUtil.requestPut(url, code, data)

    return pattern


def delete_pattern(code, token, id):
    if StringUtil.isEmpty(id):
        return None

    if StringUtil.isEmpty(token):
        return None

    # -- URL set
    url = Url.patternDelete(id, Url.url)

    # -- Set the value to the form
    data = {'auth_token': token}
    # -- API call, get a response
    ApiUtil.requestDelete(url, code, data)
