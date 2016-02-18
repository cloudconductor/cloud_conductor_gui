from ..utils import ApiUtil
from ..utils import StringUtil
from ..utils.ApiUtil import Url
from ..enum.StatusCode import Blueprint


def get_blueprint_list(code, token, project_id=None):

    if StringUtil.isEmpty(code):
        return None

    if StringUtil.isEmpty(token):
        return None

    if StringUtil.isEmpty(project_id):
        return None

    data = {
        'auth_token': token,
        'project_id': project_id,
    }
    url = Url.blueprintList
    list = ApiUtil.requestGet(url, code, data)

    return list


def get_blueprint_list2(code, token, project_id=None):

    blueprints = get_blueprint_list(code, token, project_id)

    if StringUtil.isEmpty(blueprints):
        return None

    dic = {}
    list = []
    for bp in blueprints:
        dic['id'] = str(bp.get('id'))
        dic['name'] = bp.get('name')
        list.append(dic.copy())

    return list


def get_blueprint_detail(code, token, id):

    if StringUtil.isEmpty(token):
        return None

    if StringUtil.isEmpty(id):
        return None

    url = Url.blueprintDetail(id, Url.url)
    data = {
        'auth_token': token,
        'id': id,
    }
    blueprint = ApiUtil.requestGet(url, code, data)

    return StringUtil.deleteNullDict(blueprint)


def create_blueprint(code, token, project_id, form):

    if StringUtil.isEmpty(code):
        return None

    if StringUtil.isEmpty(token):
        return None

    if StringUtil.isEmpty(project_id):
        return None

    data = {
        'auth_token': token,
        'project_id': project_id,
        'name': form.get('name'),
        'description': form.get('description'),
    }
    url = Url.blueprintCreate
    bp = ApiUtil.requestPost(url, code, StringUtil.deleteNullDict(data))

    return bp


def edit_blueprint(code, token, id, form):

    if StringUtil.isEmpty(token):
        return None

    if StringUtil.isEmpty(id):
        return None

    data = {
        'auth_token': token,
        'name': form.get('name'),
        'description': form.get('description'),
    }

    url = Url.blueprintEdit(id, Url.url)
    bp = ApiUtil.requestPut(url, code, StringUtil.deleteNullDict(data))

    return bp


def get_blueprint_version(code, data):

    if code is None or data is None:
        return None

    # Get a Blueprint List
    url = Url.blueprintList
    blueprints = ApiUtil.requestGet(url, code, data)

    if blueprints is None:
        return None

    # Create a custom blueprint list
    dic = {}
    list = []
    for bp in blueprints:
        bpid = bp.get('id')
        # Get a Blueprint History
        url = Url.blueprintHistoriesList(bpid, Url.url)
        histories = ApiUtil.requestGet(url, code, data)

        if histories is not None:

            for history in histories:
                if history.get('status') == Blueprint.CREATE_COMPLETE.value:
                    dic['id'] = bpid
                    dic['name'] = bp.get('name')
                    dic['version'] = history.get('version')
                    list.append(dic.copy())

    return list


def get_blueprint_pattern_list(code, id, token):

    if StringUtil.isEmpty(code):
        return None

    if StringUtil.isEmpty(id):
        return None

    if StringUtil.isEmpty(token):
        return None

    data = {
        'auth_token': token,
    }

    url = Url.blueprintPattrnList(id, Url.url)
    list = ApiUtil.requestGet(url, code, data)

    if StringUtil.isEmpty(list):
        return None
    else:
        return list


def get_pattern_list(code, id, token, pjid):

    if StringUtil.isEmpty(code):
        return None

    if StringUtil.isEmpty(id):
        return None

    if StringUtil.isEmpty(token):
        return None

    data = {
        'auth_token': token,
        'project_id': pjid,
    }

    bpptternList = get_blueprint_pattern_list(code, id, token)
    if StringUtil.isEmpty(bpptternList):
        return None

    url = Url.patternList
    patternList = ApiUtil.requestGet(url, code, data)
    if StringUtil.isEmpty(patternList):
        return None

    dic = {}
    list = []
    for bpt in bpptternList:

        for pt in patternList:

            if pt.get('id') == bpt.get('pattern_id'):

                dic['id'] = pt.get('id')
                dic['name'] = pt.get('name')
                dic['revision'] = pt.get('revision')
                dic['protocol'] = pt.get('protocol')
                list.append(dic.copy())

    return list


def create_bluepritn_build(code, token, id):

    if StringUtil.isEmpty(code):
        return None

    if StringUtil.isEmpty(token):
        return None

    if StringUtil.isEmpty(id):
        return None

    url = Url.blueprintBuild(id, Url.url)
    data = {
        'auth_token': token,
    }
    blueprint = ApiUtil.requestPost(url, code, data)

    return blueprint


def delete_bluepritn_build(code, token, id):
    if StringUtil.isEmpty(id):
        return None

    if StringUtil.isEmpty(token):
        return None

    # -- URL set
    url = Url.blueprintDelete(id, Url.url)

    # -- Set the value to the form
    data = {'auth_token': token}
    # -- API call, get a response
    ApiUtil.requestDelete(url, code, data)
