from ..utils import ApiUtil
from ..utils import StringUtil
from ..utils.ApiUtil import Url
from ..utils import ApplicationHistoryUtil


def get_application_list(code, token, project_id=None):
    if StringUtil.isEmpty(code):
        return None

    if StringUtil.isEmpty(token):
        return None

    data = {
        'auth_token': token,
        'project_id': project_id,
    }

    url = Url.applicationList
    list = ApiUtil.requestGet(url, code, data)
    return list


def get_application_version(code, token, project_id=None):

    if StringUtil.isEmpty(code):
        return None

    if StringUtil.isEmpty(token):
        return None

    data = {
        'auth_token': token,
        'project_id': project_id,
    }

    # Get a Blueprint List
    url = Url.applicationList
    applications = ApiUtil.requestGet(url, code, data)

    if applications is None:
        return None

    # Create a custom blueprint list
    dic = {}
    list = []
    for app in applications:

        histories = ApplicationHistoryUtil.get_history_list(code, token,
                                                            app.get('id'))

        if histories is not None:
            for history in histories:
                dic['id'] = app.get('id')
                dic['name'] = app.get('name')
                dic['version'] = history.get('version')
                dic['system_id'] = app.get('system_id')
                dic['description'] = app.get('description')
                dic['domain'] = app.get('domain')
                list.append(dic.copy())

    return list


def get_application_list2(code, token, project_id=None):

    apps = get_application_list(code, token, project_id)

    if StringUtil.isEmpty(apps):
        return None

    dic = {}
    list = []
    for app in apps:
        dic['id'] = str(app.get('id'))
        dic['name'] = app.get('name')
        list.append(dic.copy())

    return list


def get_application_detail(code, token, id):
    if StringUtil.isEmpty(code):
        return None

    if StringUtil.isEmpty(token):
        return None

    data = {
        'auth_token': token,
    }

    url = Url.applicationDetail(id, Url.url)
    list = ApiUtil.requestGet(url, code, data)
    return StringUtil.deleteNullDict(list)


def create_application(code, token, form):

    if StringUtil.isEmpty(token):
        return None

    if StringUtil.isEmpty(form):
        return None

    # -- URL set
    url = Url.applicationCreate
    # -- Set the value to the form
    data = put_application(token, form)
    # -- API call, get a response
    response = ApiUtil.requestPost(url, code, StringUtil.deleteNullDict(data))

    return response


def edit_application(code, token, id, form):
    if StringUtil.isEmpty(id):
        return None

    if StringUtil.isEmpty(token):
        return None

    if StringUtil.isEmpty(form):
        return None

    # -- URL set
    url = Url.applicationEdit(id, Url.url)

    # -- Set the value to the form
    data = put_application(token, form)
    # -- API call, get a response
    response = ApiUtil.requestPut(url, code, StringUtil.deleteNullDict(data))

    return response


def delete_application(code, token, id):
    if StringUtil.isEmpty(id):
        return None

    if StringUtil.isEmpty(token):
        return None

    # -- URL set
    url = Url.applicationDelete(id, Url.url)

    # -- Set the value to the form
    data = {'auth_token': token}
    # -- API call, get a response
    ApiUtil.requestDelete(url, code, data)


def put_application(token, form):

    data = {}
    # -- Set the value to the form
    data = {
        'auth_token': token,
        'system_id': form.get('system_id', ''),
        'name': form.get('name', ''),
        'description': form.get('description', ''),
        'domain': form.get('domain', ''),
    }

    return data


def deploy_application(code, token, environment_id, application_id,
                       application_history_id=None):
    # -- URL set
    url = Url.applicationDeploy(application_id, Url.url)

    # -- Set the value to the form
    data = {
        'auth_token': token,
        'environment_id': environment_id,
        'application_history_id': application_history_id,
    }
    # -- API call, get a response
    response = ApiUtil.requestPost(url, code, data)

    return response
