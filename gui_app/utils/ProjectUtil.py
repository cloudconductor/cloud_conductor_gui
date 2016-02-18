from ..utils import ApiUtil
from ..utils import RoleUtil
from ..utils import StringUtil
from ..utils.ApiUtil import Url


def get_project_list(code, token):

    if StringUtil.isEmpty(code):
        return None

    if StringUtil.isEmpty(token):
        return None

    url = Url.projectList
    data = {'auth_token': token}
    list = ApiUtil.requestGet(url, code, data)

    return list


def get_project_list2(code, token):

    projects = get_project_list(code, token)

    if StringUtil.isNotEmpty(projects):
        dic = {}
        list = []
        for project in projects:
            dic['project_id'] = project.get('id')
            dic['project_name'] = project.get('name')
            list.append(dic.copy())

        return list

    else:
        return None


def get_project_list3(code, token):

    projects = get_project_list(code, token)

    if StringUtil.isNotEmpty(projects):
        dic = {}
        list = []
        for project in projects:
            dic['id'] = project.get('id')
            dic['name'] = project.get('name')
            list.append(dic.copy())

        return list

    else:
        return None


def get_project_list_admin(code, token, account_id):

    project_list = []

    if StringUtil.isEmpty(account_id):
        return None

    projects = get_project_list(code, token)

    if StringUtil.isEmpty(projects):
        return None

    for pj in projects:
        role_pj = RoleUtil.get_account_role(code, token,
                                            pj.get('id'), account_id)
        if role_pj:
            project_list.append(pj)

    return project_list


def get_project_detail(code, token, id):

    if StringUtil.isEmpty(code):
        return None

    if StringUtil.isEmpty(token):
        return None

    if StringUtil.isEmpty(id):
        return None

    url = Url.projectDetail(id, Url.url)
    data = {
        'auth_token': token,
        'id': id,
    }
    project = ApiUtil.requestGet(url, code, data)

    return StringUtil.deleteNullDict(project)


def create_project(code, token, name, description):
    # -- Create a project, api call
    url = Url.projectCreate
    data = {
        'auth_token': token,
        'name': name,
        'description': description
    }
    data = StringUtil.deleteNullDict(data)
    # -- API call, get a response
    project = ApiUtil.requestPost(url, code, data)

    return project


def edit_project(code, token, id, name, description):
    # -- Create a project, api call
    url = Url.projectEdit(id, Url.url)
    data = {
        'auth_token': token,
        'name': name,
        'description': description
    }
    data = StringUtil.deleteNullDict(data)
    # -- API call, get a response
    project = ApiUtil.requestPut(url, code, data)

    return project


def delete_project(code, token, id):
    if StringUtil.isEmpty(id):
        return None

    if StringUtil.isEmpty(token):
        return None

    url = Url.projectDelete(id, Url.url)
    data = {'auth_token': token}
    ApiUtil.requestDelete(url, code, data)
