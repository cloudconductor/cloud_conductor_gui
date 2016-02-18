from ..utils import ApiUtil
from ..utils import StringUtil
from ..utils.ApiUtil import Url


def get_history_list(code, token, id):
    if StringUtil.isEmpty(id):
        return None

    if StringUtil.isEmpty(code):
        return None

    if StringUtil.isEmpty(token):
        return None

    data = {'auth_token': token}

    url = Url.applicationHistoryList(id, Url.url)
    list = ApiUtil.requestGet(url, code, data)
    return list


def get_history_list2(code, token, id):
    if StringUtil.isEmpty(id):
        return None

    if StringUtil.isEmpty(code):
        return None

    if StringUtil.isEmpty(token):
        return None

    apps = get_history_list(code, token, id)

    if StringUtil.isEmpty(apps):
        return None

    dic = {}
    list = []
    for app in apps:
        dic['id'] = str(app.get('id'))
        dic['version'] = app.get('version')
        dic['revision'] = app.get('revision')
        list.append(dic.copy())

    return list


def get_new_history(code, token, id):
    if StringUtil.isEmpty(id):
        return None

    if StringUtil.isEmpty(code):
        return None

    if StringUtil.isEmpty(token):
        return None

    apps = get_history_list(code, token, id)

    if StringUtil.isEmpty(apps):
        return None

    new_app = {}
    for app in apps:
        if int(new_app.get('id', 0)) < app.get('id'):
            new_app = app
    if new_app.get('parameters') == '{}':
        new_app['parameters'] = ''
    return StringUtil.deleteNullDict(new_app)


def get_history_detail(code, token, id, his_id):
    if StringUtil.isEmpty(code):
        return None

    if StringUtil.isEmpty(token):
        return None

    data = {
        'auth_token': token,
    }

    url = Url.applicationHistoryDetail(id, his_id, Url.url)
    detail = ApiUtil.requestGet(url, code, data)
    return StringUtil.deleteNullDict(detail)


def create_history(code, token, id, form):

    if StringUtil.isEmpty(id):
        return None

    if StringUtil.isEmpty(token):
        return None

    if StringUtil.isEmpty(form):
        return None

    # -- URL set
    url = Url.applicationHistoryCreate(id, Url.url)

    # -- Set the value to the form
    data = put_history(token, form)

    # -- API call, get a response
    response = ApiUtil.requestPost(url, code, StringUtil.deleteNullDict(data))

    return response


def edit_history(code, token, id, his_id, form):

    if StringUtil.isEmpty(token):
        return None

    if StringUtil.isEmpty(id):
        return None

    if StringUtil.isEmpty(his_id):
        return None

    if StringUtil.isEmpty(form):
        return None

    # -- URL set
    url = Url.applicationHistoryEdit(id, his_id, Url.url)

    # -- Set the value to the form
    data = put_history(token, form)

    # -- API call, get a response
    response = ApiUtil.requestPut(url, code, StringUtil.deleteNullDict(data))

    return response


def put_history(token, form):
    if StringUtil.isEmpty(form):
        return None
    data = {}
    # -- Set the value to the form
    data = {
        'auth_token': token,
        'url': form.get('url'),
        'type': form.get('type'),
        'protocol': form.get('protocol'),
        'revision': form.get('revision'),
        'pre_deploy': form.get('pre_deploy'),
        'post_deploy': form.get('post_deploy'),
    }

    parameters = form.get('parameters')
    if StringUtil.isNotEmpty(parameters):
        data['parameters'] = parameters

    return data
