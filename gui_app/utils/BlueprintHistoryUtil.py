from ..utils import ApiUtil
from ..utils import StringUtil
from ..utils import BlueprintUtil
from ..utils.ApiUtil import Url


def get_blueprint_history_list(code, token, id):

    if StringUtil.isEmpty(token):
        return None

    if StringUtil.isEmpty(id):
        return None

    data = {
        'auth_token': token,
    }
    url = Url.blueprintHistoriesList(id, Url.url)
    list = ApiUtil.requestGet(url, code, data)

    return list


def get_new_blueprint_history(code, token, id):

    if StringUtil.isEmpty(token):
        return None

    if StringUtil.isEmpty(id):
        return None

    list = get_blueprint_history_list(code, token, id)

    new_his = {}
    for his in list:
        if new_his.get('version', 0) < his.get('version'):
            new_his = his

    return new_his


def get_blueprint_parameters(code, token, blueprint_id, version):

    if StringUtil.isEmpty(token):
        return None

    if StringUtil.isEmpty(blueprint_id):
        return None

    if StringUtil.isEmpty(version):
        return None

    data = {
        'auth_token': token,
    }
    url = Url.blueprintHistoriesParameters(blueprint_id, version, Url.url)
    param = ApiUtil.requestGet(url, code, data)

    return param


def get_blueprint_history_parameters(code, token, blueprint_id, history_id):
    # -- Later modifications
    if StringUtil.isEmpty(token):
        return None

    if StringUtil.isEmpty(blueprint_id):
        return None

    if StringUtil.isEmpty(history_id):
        return None

    list = get_blueprint_history_list(code, token, blueprint_id)

    history = None
    for his in list:
        if his.get('id') == history_id:
            history = his
            break

    data = {
        'auth_token': token,
    }
    url = Url.blueprintHistoriesParameters(history.get('blueprint_id'),
                                           history.get('version'), Url.url)
    param = ApiUtil.requestGet(url, code, data)

    return param


def get_blueprint_history_detail(code, token, blueprint_id, version):
    if StringUtil.isEmpty(token):
        return None

    if StringUtil.isEmpty(blueprint_id):
        return None

    if StringUtil.isEmpty(version):
        return None

    data = {
        'auth_token': token,
    }

    url = Url.blueprintHistoriesDetail(blueprint_id, version, Url.url)
    history = ApiUtil.requestGet(url, code, data)

    return history


def get_blueprint_history_detail2(code, token, blueprint_id, version):
    if StringUtil.isEmpty(token):
        return None

    if StringUtil.isEmpty(blueprint_id):
        return None

    if StringUtil.isEmpty(version):
        return None

    history = None

    history = get_blueprint_history_detail(code, token, blueprint_id, version)

    blueprint = BlueprintUtil.get_blueprint_detail(code, token, blueprint_id)

    history['blueprint_name'] = blueprint.get('name')

    return history


def get_blueprint_history_list_id(code, token, project_id, history_id):

    if StringUtil.isEmpty(token):
        return None

    if StringUtil.isEmpty(project_id):
        return None

    if StringUtil.isEmpty(history_id):
        return None

    bplist = BlueprintUtil.get_blueprint_list(code, token, project_id)
    if StringUtil.isEmpty(bplist):
        return None

    list = None
    history = None
    get_bp = False
    for bp in bplist:
        list = []
        list = get_blueprint_history_list(code, token, bp.get('id'))
        for his in list:
            if his.get('id') == history_id:
                history = his
                history.update(bp)
                get_bp = True

        if get_bp:
            break

    return history
