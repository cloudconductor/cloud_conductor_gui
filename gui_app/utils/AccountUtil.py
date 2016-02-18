from ..utils import ApiUtil
from ..utils import StringUtil
from ..utils.ApiUtil import Url


def get_account_list(code, token, project_id=None):
    if StringUtil.isEmpty(code):
        return None

    if StringUtil.isEmpty(token):
        return None

    data = {
        'auth_token': token,
    }

    if StringUtil.isNotEmpty(project_id):
        data['project_id'] = project_id

    url = Url.accountList
    list = ApiUtil.requestGet(url, code, data)
    return list


def get_account(code, token, email):

    if StringUtil.isEmpty(email):
        return None

    list = get_account_list(code, token)

    dic = {}
    for account in list:
        if account.get('email') == email:
            dic['id'] = account.get('id')
            dic['name'] = account.get('name')
            dic['admin'] = account.get('admin')
            dic['email'] = email

            return dic

    return None


def get_account_detail(code, token, id):
    if StringUtil.isEmpty(code):
        return None

    if StringUtil.isEmpty(token):
        return None

    if StringUtil.isEmpty(id):
        return None

    data = {
        'auth_token': token,
    }

    url = Url.accountDetail(id, Url.url)
    account = ApiUtil.requestGet(url, code, data)

    return account


def get_account_create(code, token, name, email, password, repassword, admin):
    # -- URL set
    url = Url.accountCreate

    # -- Set the value to the form
    data = {
        'auth_token': token,
        'name': name,
        'email': email,
        'password': password,
        'password_confirmation': repassword,
        'admin': int(admin),
    }
    # -- API call, get a response
    response = ApiUtil.requestPost(url, code, data)

    return StringUtil.deleteNullDict(response)


def get_assginment_account(code, token, id):

    if StringUtil.isEmpty(token):
        return None

    if StringUtil.isEmpty(id):
        return None

    url2 = Url.accountList
    data = {
        'auth_token': token,
        'project_id': id,
    }
    accounts = ApiUtil.requestGet(url2, code, data)

    if StringUtil.isEmpty(accounts):
        return None

    accountList = []
    for account in accounts:
        url2 = Url.roleList
        data = {
            'auth_token': token,
            'project_id': id,
            'account_id': account["id"]
        }
        assignments = ApiUtil.requestGet(url2, code, data)
        role = ""
        for assignment in assignments:
            role = assignment["name"]

        accountList.append({'id': account["id"],
                            'name': account["name"],
                            'role': role,
                            'admin': account["admin"],
                            'email': account["email"],
                            })

    return accountList


def delete_account(code, token, id):
    if StringUtil.isEmpty(id):
        return None

    if StringUtil.isEmpty(token):
        return None

    url = Url.accountDelete(id, Url.url)
    data = {'auth_token': token}
    ApiUtil.requestDelete(url, code, data)
