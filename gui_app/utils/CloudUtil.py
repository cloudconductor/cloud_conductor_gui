from ..utils import ApiUtil
from ..utils import StringUtil
from ..utils.ApiUtil import Url


def get_cloud_list(code, token, project_id=None):

    if StringUtil.isEmpty(code):
        return None

    if StringUtil.isEmpty(token):
        return None

    url = Url.cloudList
    data = {
        'auth_token': token,
        'project_id': project_id
    }
    list = ApiUtil.requestGet(url, code, data)

    return list


def get_cloud_detail(code, token, id):

    if StringUtil.isEmpty(code):
        return None

    if StringUtil.isEmpty(token):
        return None

    if StringUtil.isEmpty(id):
        return None

    url = Url.cloudDetail(id, Url.url)
    data = {
        'auth_token': token,
        'id': id,
    }
    cloud = ApiUtil.requestGet(url, code, data)
    del cloud['secret']

    return StringUtil.deleteNullDict(cloud)


def create_cloud2(code, token, project_id, form):

    # -- Create a cloud, api call
    url = Url.cloudCreate
    data = {
        'auth_token': token,
        'project_id': project_id,
    }
    form.update(data)
    # -- API call, get a response
    cloud = ApiUtil.requestPost(url, code, StringUtil.deleteNullDict(form))

    return cloud


def create_cloud(code, token, project_id, name, type, key, secret,
                 entry_point, tenant_name, description):

    # -- Create a cloud, api call
    url = Url.cloudCreate
    data = {
        'auth_token': token,
        'project_id': project_id,
        'name': name,
        'type': type,
        'key': key,
        'secret': secret,
        'entry_point': entry_point,
        'tenant_name': tenant_name,
        'description': description
    }
    # -- API call, get a response
    cloud = ApiUtil.requestPost(url, code, StringUtil.deleteNullDict(data))

    return cloud


def edit_cloud(code, token, id, form):
    if StringUtil.isEmpty(id):
        return None

    if StringUtil.isEmpty(token):
        return None

    if StringUtil.isEmpty(form):
        return None

    # -- URL set
    url = Url.cloudEdit(id, Url.url)

    # -- Set the value to the form
    data = {
        'auth_token': token,
        'name': form.get('name'),
        'type': form.get('type'),
        'key': form.get('key'),
        'secret': form.get('secret'),
        'entry_point': form.get('entry_point'),
        'tenant_name': form.get('tenant_name'),
        'description': form.get('description')
    }

#     data.update(form)
    # -- API call, get a response
    response = ApiUtil.requestPut(url, code, StringUtil.deleteNullDict(data))

    return response


def delete_cloud(code, token, id):
    if StringUtil.isEmpty(id):
        return None

    if StringUtil.isEmpty(token):
        return None

    url = Url.cloudDelete(id, Url.url)
    data = {'auth_token': token}
    ApiUtil.requestDelete(url, code, data)
