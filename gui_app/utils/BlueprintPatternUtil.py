from ..utils import ApiUtil
from ..utils import StringUtil
from ..utils.ApiUtil import Url
from itertools import chain
from functools import reduce


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
        dic['platform'] = bp['platform']
        dic['platform_version'] = bp['platform_version']
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


def add_blueprint_pattern(code, token, id, pattern):
    url = Url.blueprintPatternCreate(id, Url.url)
    data = {
        'auth_token': token,
        'pattern_id': pattern['id'],
        'revision': pattern['revision'],
        'platform': pattern['platform'],
        'platform_version': pattern['platform_version']
    }

    return ApiUtil.requestPost(url, code, StringUtil.deleteNullDict(data))


def update_blueprint_pattern(code, token, id, pattern):
    url = Url.blueprintPatternUpdate(id, int(pattern['id']), Url.url)
    data = {
            'auth_token': token,
            'revision': pattern['revision'],
            'platform': pattern['platform'],
            'platform_version': pattern['platform_version']
    }

    return ApiUtil.requestPut(url, code, StringUtil.deleteNullDict(data))


def delete_blueprint_pattern(code, token, id, pattern_id):
    if StringUtil.isEmpty(id):
        return None

    if StringUtil.isEmpty(pattern_id):
        return None

    url = Url.blueprintPattrnDelete(id, int(pattern_id), Url.url)
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


def format_pattern(platforms, platform_versions, revisions, ids):
    dict_platforms = StringUtil.stringToDictList(platforms)
    dict_platform_versions = StringUtil.stringToDictList(platform_versions)
    dict_revisions = StringUtil.stringToDictList(revisions)

    zip_patterns = list(zip(
                    [x for x in dict_platforms if x['id'] in ids],
                    [x for x in dict_platform_versions if x['id'] in ids],
                    [x for x in dict_revisions if x['id'] in ids]))

    def dict_merge(x, y): return dict(chain(x.items(), y.items()))
    result = []
    for id in ids:
        select_pattern = []
        for platform, platform_version, revision in zip_patterns:
            if id == platform['id']:
                select_pattern.append(platform)
            if id == platform_version['id']:
                select_pattern.append(platform_version)
            if id == revision['id']:
                select_pattern.append(revision)

        if len(select_pattern) != 0:
            result.append(reduce(dict_merge, select_pattern))

    return result
