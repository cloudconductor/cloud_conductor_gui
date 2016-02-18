# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect, render_to_response
from ..forms import projectForm
from ..utils import RoleUtil
from ..utils import ProjectUtil
from ..utils import AccountUtil
from ..utils import ApiUtil
from ..utils import PermissionUtil
from ..utils import SessionUtil
from ..enum.MessageCode import Error
from ..utils.PathUtil import Path
from ..utils.PathUtil import Html
from ..utils.ApiUtil import Url
from ..enum.FunctionCode import FuncCode
from ..logs import log


def projectList(request):
    try:
        if not SessionUtil.check_login(request):
            return redirect(Path.logout)
        if not SessionUtil.check_permission(request, 'project', 'list'):
            return render_to_response(Html.error_403)

        projects = None
        # -- Get a project list, API call
        code = FuncCode.projectList.value
        token = request.session['auth_token']
        projects = ProjectUtil.get_project_list(code, token)

        return render(request, Html.projectList,
                      {'projects': projects, 'message': ''})
    except Exception as ex:
        log.error(FuncCode.projectList.value, None, ex)

        return render(request, Html.projectList,
                      {"projects": '', 'message': str(ex)})


def projectCreate(request):
    try:
        if not SessionUtil.check_login(request):
            return redirect(Path.logout)
        if not SessionUtil.check_permission(request, 'project', 'create'):
            return render_to_response(Html.error_403)

        code = FuncCode.projectCreate.value
        token = request.session['auth_token']

        if request.method == "GET":
            return render(request, Html.projectCreate,
                          {'project': '', 'form': '', 'message': '',
                           'save': True})
        else:
            # -- Get a value from a form
            msg = ''
            p = request.POST
            # -- Validate check
            form = projectForm(p)
            if not form.is_valid():

                return render(request, Html.projectCreate,
                              {'project': p, 'form': form, 'message': msg,
                               'save': True})

            # -- Create a project, api call
            url = Url.projectCreate
            data = {
                'auth_token': token,
                'name': p['name'],
                'description': p['description']
            }
            # -- API call, get a response
            ApiUtil.requestPost(url, code, data)

            SessionUtil.edit_project_session(code, token, request.session)

            return redirect(Path.projectList)
    except Exception as ex:
        log.error(FuncCode.projectCreate.value, None, ex)

        return render(request, Html.projectCreate,
                      {'project': request.POST, 'form': '',
                       'message': str(ex), 'save': True})


def projectEdit(request, id):
    try:
        if not SessionUtil.check_login(request):
            return redirect(Path.logout)
        if not SessionUtil.check_permission(request, 'project', 'update'):
            return render_to_response(Html.error_403)

        code = FuncCode.projectEdit.value
        token = request.session['auth_token']

        if request.method == "GET":

            p = ProjectUtil.get_project_detail(code, token, id)

            return render(request, Html.projectEdit,
                          {'project': p, 'form': '', 'message': '',
                           'save': True})
        else:
            # -- Get a value from a form
            p = request.POST
            # -- Validate check
            form = projectForm(request.POST)
            form.full_clean()
            if not form.is_valid():

                return render(request, Html.projectEdit,
                              {'project': p, 'form': form, 'message': '',
                               'save': True})

            # -- API call, get a response
            project = ProjectUtil.edit_project(
                code, token, id, p.get('name'), p.get('description'))
            SessionUtil.edit_project_session(
                code, token, request.session, id, project.get('name'))

            return redirect(Path.projectList)
    except Exception as ex:
        log.error(FuncCode.projectEdit.value, None, ex)

        return render(request, Html.projectEdit,
                      {'project': request.POST, 'form': '', 'message': str(ex),
                       'save': True})


def projectDetail(request, id):
    accountList = None
    project = None
    try:
        if not SessionUtil.check_login(request):
            return redirect(Path.logout)
        if not SessionUtil.check_permission(request, 'project', 'read'):
            return render_to_response(Html.error_403)

        if request.session.get('select_account'):
            del request.session['select_account']

        code = FuncCode.projectDetail.value
        token = request.session['auth_token']

        # -- project DetailAPI call, get a response
        project = ProjectUtil.get_project_detail(code, token, id)

        # -- AccountAPI call, get a response
        accountList = AccountUtil.get_assginment_account(code, token, id)

        return render(request, Html.projectDetail,
                      {'project': project, 'accounts': accountList,
                       'message': ''})
    except Exception as ex:
        log.error(FuncCode.projectDetail.value, None, ex)

        return render(request, Html.projectDetail,
                      {'project': project, 'accounts': accountList,
                       'message': str(ex)})


def projectDelete(request, id):
    code = FuncCode.projectDelete.value
    project = None
    accountList = None
    try:
        if not SessionUtil.check_login(request):
            return redirect(Path.logout)
        if not SessionUtil.check_permission(request, 'project', 'destroy'):
            return render_to_response(Html.error_403)

        # -- URL and data set
        session = request.session
        token = session['auth_token']
        project = ProjectUtil.get_project_detail(code, token, id)
        accountList = AccountUtil.get_assginment_account(code, token, id)

        ProjectUtil.delete_project(code, token, id)

        SessionUtil.edit_project_session(code, token, session, id)

        return redirect(Path.logout)
    except Exception as ex:
        log.error(FuncCode.projectDelete.value, None, ex)

        return render(request, Html.projectDetail,
                      {'project': project, 'accounts': accountList,
                       'message': str(ex)})


def projectChange(request, id):
    try:
        session = request.session
        code = FuncCode.projectChange.value
        token = session['auth_token']
        account_id = session['account_id']

        # -- ProjectAPI call, get a response
        project = ProjectUtil.get_project_detail(code, token, id)

        # -- RoleListAPI call, get a response
        role = RoleUtil.get_account_role(code, token, id, account_id)

        if not role:
            raise(Error.Authentication.value)
        # -- PermissionListAPI call, get a response
        permissions = PermissionUtil.get_permission_list(
            code, token, role.get('id'))

        if not permissions:
            raise(Error.Authentication.value)

        session['project_id'] = id
        session['project_name'] = project['name']

        RoleUtil.delete_session_role(session)
        RoleUtil.add_session_role(session, role, permissions)

        return redirect(Path.top)
    except Exception as ex:
        log.error(FuncCode.projectDelete.value, None, ex)

        request.session.clear()

        return render(request, Html.login, {'message': str(ex)})
