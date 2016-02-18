from ..utils import ApiUtil
from ..utils import StringUtil
from ..utils.ApiUtil import Url


def get_baseimege_list(code, token, id=None):

    if StringUtil.isEmpty(code):
        return None

    if StringUtil.isEmpty(token):
        return None

    url = Url.baseImageList
    data = {
        'auth_token': token,
        'cloud_id': id
    }
    list = ApiUtil.requestGet(url, code, data)

    return list


def create_baseimage(code, token, form):

    if StringUtil.isEmpty(token):
        return None

    if StringUtil.isEmpty(form):
        return None

    # -- URL set
    url = Url.baseImageCreate
    # -- Set the value to the form
    data = put_baseimage(token, form)
    # -- API call, get a response
    response = ApiUtil.requestPost(url, code, data)

    return response


def get_baseimage_detail(code, token, id):

    if StringUtil.isEmpty(code):
        return None

    if StringUtil.isEmpty(token):
        return None

    if StringUtil.isEmpty(id):
        return None

    url = Url.baseImageDetail(id, Url.url)
    data = {
        'auth_token': token,
        'id': id,
    }
    baseimage = ApiUtil.requestGet(url, code, data)

    return StringUtil.deleteNullDict(baseimage)


def put_baseimage(token, form):

    data = {}
    # -- Set the value to the form

    data = {
        'auth_token': token,
        'cloud_id': form.get('cloud_id', ''),
        'ssh_username': form.get('ssh_username', ''),
        'source_image': form.get('source_image', ''),
        'os_version': form.get('os_version', ''),
    }

    return data


def delete_baseimage(code, token, id):
    if StringUtil.isEmpty(id):
        return None

    if StringUtil.isEmpty(token):
        return None

    # -- URL set
    url = Url.baseImageDelete(id, Url.url)

    # -- Set the value to the form
    data = {'auth_token': token}
    # -- API call, get a response
    ApiUtil.requestDelete(url, code, data)
