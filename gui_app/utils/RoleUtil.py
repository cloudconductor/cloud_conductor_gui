from ..utils import ApiUtil
from ..utils import StringUtil
from ..utils.ApiUtil import Url


def get_role_list(code, token, project_id=None, account_id=None):

    if StringUtil.isEmpty(code):
        return None

    if StringUtil.isEmpty(token):
        return None

    url = Url.roleList
    data = {
        'auth_token': token,
    }
    if StringUtil.isNotEmpty(project_id):
        data['project_id'] = project_id
    elif StringUtil.isNotEmpty(project_id):
        data['account_id'] = account_id
    list = ApiUtil.requestGet(url, code, data)

    return list


def create_role(code, token, project_id, name, description, params):
    # -- Create a project, api call
    url = Url.roleCreate
    data = {
        'auth_token': token,
        'project_id': project_id,
        'name': name,
        'description': description
    }
    # -- API call, get a response
    role = ApiUtil.requestPost(url, code, data)

    for param in params:
        if '-' in param:
            if param.split('-')[1] in \
               ['manage', 'read', 'create', 'update', 'destroy']:
                url = Url.permissionCreate(role["id"], Url.url)
                data = {
                    'auth_token': token,
                    'action': param.split('-')[1],
                    'model': param.split('-')[0],
                }
                ApiUtil.requestPost(url, code, data)

    return role


def edit_role(code, token, id, name, description, params):
    # -- Create a project, api call
    url = Url.roleEdit(id, Url.url)
    data = {
        'auth_token': token,
        'name': name,
        'description': description
    }

    # -- API call, get a response
    role = ApiUtil.requestPut(url, code, data)

    url = Url.permissionList(id, Url.url)
    permissions = ApiUtil.requestGet(url, code, data)
    old_value = []
    for permission in permissions:
        old_value.append(permission["model"] + "-" + permission["action"])
        pass

    for param in params:
        if '-' in param:
            if param.split('-')[1] in \
               ['manage', 'read', 'create', 'update', 'destroy']:
                if param in old_value:
                    old_value.remove(param)
                    pass

                else:
                    url = Url.permissionCreate(role["id"], Url.url)
                    data = {
                        'auth_token': token,
                        'action': param.split('-')[1],
                        'model': param.split('-')[0],
                    }
                    permission = ApiUtil.requestPost(url, code, data)

    for permission in permissions:

        if permission["model"] + "-" + permission["action"] in old_value:
            url = Url.permissionDelete(id, permission["id"], Url.url)
            data = {'auth_token': token}
            ApiUtil.requestDelete(url, code, data)

    return role


def get_role_detail(code, token, id):

    if StringUtil.isEmpty(code):
        return None

    if StringUtil.isEmpty(token):
        return None

    if StringUtil.isEmpty(id):
        return None

    url = Url.roleDetail(id, Url.url)
    data = {'auth_token': token}
    role = ApiUtil.requestGet(url, code, data)

    url = Url.permissionList(id, Url.url)
    permissions = ApiUtil.requestGet(url, code, data)

    check_value = []
    for permission in permissions:
        check_value.append(permission["model"] + "-" + permission["action"])
        pass

    check_items = []
    actions = ["manage", "read", "create", "update", "destroy"]
    models = []
    models.append({"no": "1", "name": "Project", "item_name": "project"})
    models.append({"no": "2", "name": "Assignment",
                   "item_name": "assignment"})
    models.append({"no": "3", "name": "Cloud", "item_name": "cloud"})
    models.append({"no": "4", "name": "BaseImage",
                   "item_name": "base_image"})
    models.append({"no": "5", "name": "System", "item_name": "system"})
    models.append({"no": "6", "name": "Environment",
                   "item_name": "environment"})
    models.append({"no": "7", "name": "Application",
                   "item_name": "application"})
    models.append({"no": "8", "name": "Application History",
                   "item_name": "application_history"})
    models.append({"no": "9", "name": "Deployment",
                   "item_name": "deployment"})
    models.append({"no": "10", "name": "Blueprint",
                   "item_name": "blueprint"})
    models.append({"no": "11", "name": "Blueprint Pattern",
                   "item_name": "blueprint_pattern"})
    models.append({"no": "12", "name": "Blueprint History",
                   "item_name": "blueprint_history"})
    models.append({"no": "13", "name": "Pattern", "item_name": "pattern"})
    models.append({"no": "14", "name": "Account", "item_name": "account"})
    models.append({"no": "15", "name": "Role", "item_name": "role"})
    models.append(
        {"no": "16", "name": "Permission", "item_name": "permission"})

    for model in models:
        items = []
        for action in actions:
            if model["item_name"] + "-" + action in check_value:
                items.append(
                    {"item_name": model["item_name"] + "-" + action,
                     "checked": "checked"})
            else:
                items.append(
                    {"item_name": model["item_name"] + "-" + action,
                     "checked": ""})

        check_items.append(
            {"no": model["no"], "name": model["name"], "items": items})
        pass

    return {'role': role, 'check_items': check_items}


def get_account_role(code, token, project_id, account_id):

    if StringUtil.isEmpty(token):
        return None

    if StringUtil.isEmpty(project_id):
        return None

    if StringUtil.isEmpty(account_id):
        return None

    url = Url.roleList
    data = {
        'auth_token': token,
        'account_id': account_id,
        'project_id': project_id
    }
    roles = ApiUtil.requestGet(url, code, data)

    if not roles:
        return None

    role = None
    for r in roles:
        role = r
        break

    return role


def delete_role(code, token, id):

    if StringUtil.isEmpty(code):
        return None

    if StringUtil.isEmpty(token):
        return None

    url = Url.roleDelete(id, Url.url)
    data = {'auth_token': token}
    ApiUtil.requestDelete(url, code, data)


def add_session_role(session, role, permissions):
    session['role_id'] = role.get('id')

    for per in permissions:
        dic = {}
        if per.get('model') in session:
            dic[per.get('action')] = True
            session[per.get('model')].update(dic)
        else:
            dic[per.get('action')] = True
            dic['m_' + per.get('model')] = True
            session[per.get('model')] = dic

    # -- wizard
    if w_cloud_registrarion(session):
        session['w_cloud_registrarion'] = True

    if w_make_new_app(session):
        session['w_make_new_app'] = True

    if w_app_env(session):
        session['w_app_env'] = True

    if w_deploying_app(session):
        session['w_deploying_app'] = True


def w_cloud_registrarion(session):
    if 'cloud' not in session:
        return None

    if 'base_image' not in session:
        return None

    cloud = session.get('cloud')
    baseimage = session.get('base_image')

    if (cloud.get('manage') or cloud.get('create')) and\
            (baseimage.get('manage') or baseimage.get('create')):

        return True
    else:
        return False


def w_make_new_app(session):
    if 'system' not in session:
        return None

    if 'application' not in session:
        return None

    if 'application_history' not in session:
        return None

    if 'environment' not in session:
        return None

    system = session.get('system')
    application = session.get('application')
    app_his = session.get('application_history')
    environment = session.get('environment')

    if (system.get('manage') or system.get('read')) and\
            (application.get('manage') or application.get('create')) and\
            (app_his.get('manage') or app_his.get('create')) and\
            (environment.get('manage') or environment.get('read')):

        return True
    else:
        return False


def w_app_env(session):
    if 'system' not in session:
        return None

    if 'application' not in session:
        return None

    if 'application_history' not in session:
        return None

    if 'environment' not in session:
        return None

    if 'cloud' not in session:
        return None

    system = session.get('system')
    blueprint = session.get('blueprint')
    bp_his = session.get('blueprint_history')
    environment = session.get('environment')
    cloud = session.get('cloud')

    if (system.get('manage') or system.get('read')) and\
            (blueprint.get('manage') or blueprint.get('read')) and\
            (bp_his.get('manage') or bp_his.get('read')) and\
            (environment.get('manage') or environment.get('create')) and\
            (cloud.get('manage') or cloud.get('read')):

        return True
    else:
        return False


def w_deploying_app(session):

    if 'application' not in session:
        return None

    if 'application_history' not in session:
        return None

    if 'environment' not in session:
        return None

    if 'deployment' not in session:
        return None

    application = session.get('application')
    app_his = session.get('application_history')
    environment = session.get('environment')
    deployment = session.get('deployment')

    if (application.get('manage') or application.get('read')) and\
            (app_his.get('manage') or app_his.get('read')) and\
            (environment.get('manage') or environment.get('read')) and\
            (deployment.get('manage') or deployment.get('read')):

        return True
    else:
        return False


def delete_session_role(session):
    if 'project' in session:
        del session['project']

    if 'account' in session:
        del session['account']

    if 'assignment' in session:
        del session['assignment']

    if 'role' in session:
        del session['role']

    if 'cloud' in session:
        del session['cloud']

    if 'base_image' in session:
        del session['base_image']

    if 'pattern' in session:
        del session['pattern']

    if 'blueprint' in session:
        del session['blueprint']

    if 'blueprint_history' in session:
        del session['blueprint_history']

    if 'system' in session:
        del session['system']

    if 'environment' in session:
        del session['environment']

    if 'application' in session:
        del session['application']

    if 'application_history' in session:
        del session['application_history']

    if 'deployment' in session:
        del session['deployment']
