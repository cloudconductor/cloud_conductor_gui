# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from ..forms import loginForm
from ..enum.FunctionCode import FuncCode
from ..enum.MessageCode import Error
from ..utils.PathUtil import Path
from ..utils.PathUtil import Html
from ..utils import ValiUtil
from ..utils import TokenUtil
from ..utils import AccountUtil
from ..utils import ProjectUtil
from ..utils import RoleUtil
from ..utils import PermissionUtil
from ..utils import StringUtil
from ..logs import log

# Create your views here.


def login(request):
    try:
        if request.method == "GET":
            return render(request, Html.login, {'message': ''})
        else:
            # -- Get a value from a form
            code = FuncCode.login.value
            session = request.session
            msg = ''
            p = request.POST
            # -- Validate check
            form = loginForm(p)
            form.full_clean()

            if not form.is_valid():
                msg = ValiUtil.valiCheck(form)
                return render(request, Html.login, {'message': msg})

            # -- TokenAPI call, get a response
            password = p.get('password')
            email = p.get('email')
            tokens = TokenUtil.get_token(code, email, password)

            if tokens:
                token = tokens.get('auth_token')
            else:
                raise Exception(Error.Authentication.value)

            # -- AccountApi call, get a response
            account = AccountUtil.get_account(code, token, email)
            if not account:
                raise Exception(Error.Authentication.value)

            # -- ProjectListAPI call, get a response
            project_list = ''

            if account.get('admin'):
                project_list = ProjectUtil.get_project_list_admin(
                    code, token, account.get('id'))
            else:
                project_list = ProjectUtil.get_project_list(code, token)

            project = StringUtil.list_to_record(project_list)
            if not project:
                raise Exception(Error.NoAssginment.value)

            # -- RoleListAPI call, get a response
            role = RoleUtil.get_account_role(
                code, token, project.get('id'), account.get('id'))
            if not role:
                raise Exception(Error.NoRole.value)

            # -- PermissionListAPI call, get a response
            permissions = PermissionUtil.get_permission_list(
                code, token, role.get('id'))

            if not permissions:
                raise Exception(Error.NoPermission.value)

            # -- Add to session
            addLoginSession(token, account, project_list, project,
                            session, role, permissions)

            return redirect(Path.top)

    except Exception as ex:
        log.error(code, None, ex)

        return render(request, Html.login, {"message": str(ex)})


def addLoginSession(token, account, project_list, project,
                    session, role, permissions):
        # -- token
    session['auth_token'] = token

    # -- account
    session['account_id'] = account.get('id')
    session['account_name'] = account.get('name')
    session['account_admin'] = account.get('admin')

    # -- projects
    session['project_list'] = project_list
    session['project_id'] = project.get('id')
    session['project_name'] = project.get('name')

    # -- Role and role_id and menu
    RoleUtil.add_session_role(session, role, permissions)


def logout(request):
    # session delete
    request.session.clear()
    return render(request, Html.login, {'message': ''})
