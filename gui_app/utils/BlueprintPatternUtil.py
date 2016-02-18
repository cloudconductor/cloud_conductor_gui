from ..utils import ApiUtil
from ..utils import StringUtil
from ..utils.ApiUtil import Url


def get_blueprint_pattern_list(code, token, blueprint_id):

    if StringUtil.isEmpty(token):
        return None

    if StringUtil.isEmpty(blueprint_id):
        return None

    data = {
        'auth_token': token,
    }
    url = Url.blueprintPattrnList(blueprint_id, Url.url)
    list = ApiUtil.requestGet(url, code, data)

    return list


def get_blueprint_pattern_list2(code, token, id):

    if StringUtil.isEmpty(token):
        return None

    if StringUtil.isEmpty(id):
        return None

    blueprints = get_blueprint_pattern_list(code, token, id)
    if StringUtil.isEmpty(blueprints):
        return None

    list = []
    for bp in blueprints:
        dic = {}
        dic['id'] = bp['pattern_id']
        dic['os_version'] = bp['os_version']
        list.append(dic)

    return list


def get_blueprint_pattern_list3(code, token, id):

    if StringUtil.isEmpty(token):
        return None

    if StringUtil.isEmpty(id):
        return None

    blueprints = get_blueprint_pattern_list(code, token, id)
    if StringUtil.isEmpty(blueprints):
        return None

    list = []
    for bp in blueprints:
        list.append(str(bp['pattern_id']))

    return list


def add_blueprint_pattern(code, token, id, pattern_id, revison, os_version):
    if StringUtil.isEmpty(id):
        return None

    if StringUtil.isEmpty(pattern_id):
        return None

    url = Url.blueprintPattrnCreate(id, Url.url)
    data = {
        'auth_token': token,
        'pattern_id': pattern_id,
        'revison': revison,
        'os_version': os_version,
    }

    bp = ApiUtil.requestPost(url, code, StringUtil.deleteNullDict(data))

    return bp


def delete_blueprint_pattern(code, token, id, pattern_id):
    if StringUtil.isEmpty(id):
        return None

    if StringUtil.isEmpty(pattern_id):
        return None

    url = Url.blueprintPattrnDelete(id, pattern_id, Url.url)
    data = {
        'auth_token': token,
    }

    ApiUtil.requestDelete(url, code, data)


def add_blueprint_pattern_list(code, token, id, pt_list, id_list):
    if StringUtil.isEmpty(id):
        return None

    if StringUtil.isEmpty(pt_list):
        return None

    if StringUtil.isEmpty(id_list):
        return None

    pt_list = dic_pattern_list(pt_list, id_list)
    for pt in pt_list:
        add_blueprint_pattern(code, token, id, pt.get('id'),
                              pt.get('revison'), pt.get('os_version'))


def delete_blueprint_pattern_list(code, token, id, pt_list, id_list):
    if StringUtil.isEmpty(id):
        return None

    if StringUtil.isEmpty(pt_list):
        return None

    if StringUtil.isEmpty(id_list):
        return None

    pt_list = dic_pattern_list(pt_list, id_list)
    for pt in pt_list:
        delete_blueprint_pattern(code, token, id, pt.get('id'))


def dic_pattern_list(patterns, ids):
    if StringUtil.isEmpty(patterns):
        return None

    if StringUtil.isEmpty(ids):
        return None

    pt_list = StringUtil.stringToDictList(patterns)

    lists = []
    for pt in pt_list:
        if str(pt.get('id')) in ids:
            lists.append(pt)

    return lists
