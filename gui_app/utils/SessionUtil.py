from ..utils import RoleUtil
from ..utils import StringUtil
from ..utils import ProjectUtil
from ..utils import PermissionUtil


def edit_project_session(code, token, session, id=None, name=None):

    project_list = ''

    if session.get('account_admin'):
        project_list = ProjectUtil.get_project_list_admin(
            code, token, session.get('account_id'))
    else:
        project_list = ProjectUtil.get_project_list(code, token)

    session['project_list'] = project_list

    if session.get('project_id') == id:

        if not name:
            session['project_id'] = ''
            session['project_name'] = ''
        else:
            session['project_id'] = id
            session['project_name'] = name


def edit_role_session(code, session, id):
    token = session.get('auth_token')
    account_id = session.get('account_id')
    project_id = session.get('project_id')

    if StringUtil.isEmpty(token):
        return None

    if StringUtil.isEmpty(account_id):
        return None

    if StringUtil.isEmpty(project_id):
        return None

    role = RoleUtil.get_account_role(code, token, project_id, account_id)

    if StringUtil.isEmpty(role):
        return None

    if id == str(role.get('id')):
        # -- PermissionListAPI call, get a response
        permissions = PermissionUtil.get_permission_list(
            code, token, role.get('id'))

        if not permissions:
            return None

        RoleUtil.delete_session_role(session)
        RoleUtil.add_session_role(session, role, permissions)


def check_login(request):
    if request.session.get('auth_token') is (u"" or None):
        return False
    else:
        return True


def check_permission(request, model, action, account_id=None):

    permission = False
    model_action = request.session.get(model)
    if action == 'list' or action == 'read':
        if model_action.get('manage') is True or \
           model_action.get('read') is True or \
           model_action.get('create') is True or \
           model_action.get('update') is True or \
           model_action.get('destroy') is True:
            permission = True

    elif action == 'create':
        if model_action.get('manage') is True or \
           model_action.get('create') is True:
            permission = True

    elif action == 'update':
        if model_action.get('manage') is True or \
           model_action.get('update') is True:
            if StringUtil.isEmpty(account_id):
                permission = True
            else:
                if request.session.get('account_admin') or \
                   request.session.get('account_id') == int(account_id):
                    permission = True

    elif action == 'destroy':
        if model_action.get('manage') is True or \
           model_action.get('destroy') is True:
            permission = True

    return permission
