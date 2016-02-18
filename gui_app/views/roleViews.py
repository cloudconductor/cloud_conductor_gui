# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect, render_to_response
from ..forms import roleForm
from ..utils import RoleUtil
from ..enum.MessageCode import Error
from ..utils.PathUtil import Path
from ..utils.PathUtil import Html
from ..utils import SessionUtil
from ..enum.FunctionCode import FuncCode
from ..logs import log


def roleList(request):
    try:
        if not SessionUtil.check_login(request):
            return redirect(Path.logout)
        if not SessionUtil.check_permission(request, 'role', 'list'):
            return render_to_response(Html.error_403)

        roles = None
        # -- Get a project list, API call
        code = FuncCode.roleList.value
        token = request.session['auth_token']
        project_id = request.session['project_id']

        roles = RoleUtil.get_role_list(code, token, project_id)

        return render(request, Html.roleList, {'roles': roles, 'message': ''})
    except Exception as ex:
        log.error(FuncCode.roleList.value, None, ex)

        return render(request, Html.roleList, {"role": '', 'message': str(ex)})


def roleDetail(request, id):
    try:
        if not SessionUtil.check_login(request):
            return redirect(Path.logout)
        if not SessionUtil.check_permission(request, 'role', 'read'):
            return render_to_response(Html.error_403)

        return render(request, Html.roleDetail, {'role': '', 'message': ''})
    except Exception as ex:
        log.error(FuncCode.roleDetail.value, None, ex)

        return render(request, Html.roleDetail, {'role': '',
                                                 'message': str(ex)})


def roleCreate(request):
    if not SessionUtil.check_login(request):
        return redirect(Path.logout)
    if not SessionUtil.check_permission(request, 'role', 'create'):
        return render_to_response(Html.error_403)

    check_items = []
    check_items.append({"no": "1", "name": "Project", "m": "manage",
                        "r": "read", "c": "create", "u": "update",
                        "d": "destroy", "item_name": "project", "read": True})
    check_items.append({"no": "2", "name": "Assignment", "m": "manage",
                        "r": "read", "c": "create", "u": "update",
                        "d": "destroy", "item_name": "assignment"})
    check_items.append({"no": "3", "name": "Cloud", "m": "manage",
                        "r": "read", "c": "create", "u": "update",
                        "d": "destroy", "item_name": "cloud"})
    check_items.append({"no": "4", "name": "BaseImage", "m": "manage",
                        "r": "read", "c": "create", "u": "update",
                        "d": "destroy", "item_name": "base_image"})
    check_items.append({"no": "5", "name": "System", "m": "manage",
                        "r": "read", "c": "create", "u": "update",
                        "d": "destroy", "item_name": "system"})
    check_items.append({"no": "6", "name": "Environment", "m": "manage",
                        "r": "read", "c": "create", "u": "update",
                        "d": "destroy", "item_name": "environment",
                        "read": True})
    check_items.append({"no": "7", "name": "Application", "m": "manage",
                        "r": "read", "c": "create", "u": "update",
                        "d": "destroy", "item_name": "application"})
    check_items.append({"no": "8", "name": "Application History",
                        "m": "manage", "r": "read", "c": "create",
                        "u": "update", "d": "destroy",
                        "item_name": "application_history"})
    check_items.append({"no": "9", "name": "Deployment", "m": "manage",
                        "r": "read", "c": "create", "u": "update",
                        "d": "destroy", "item_name": "deployment"})
    check_items.append({"no": "10", "name": "Blueprint", "m": "manage",
                        "r": "read", "c": "create", "u": "update",
                        "d": "destroy", "item_name": "blueprint"})
    check_items.append({"no": "11", "name": "Blueprint Pattern",
                        "m": "manage", "r": "read", "c": "create",
                        "u": "update", "d": "destroy",
                        "item_name": "blueprint_pattern"})
    check_items.append({"no": "12", "name": "Blueprint History",
                        "m": "manage", "r": "read", "c": "create",
                        "u": "update", "d": "destroy",
                        "item_name": "blueprint_history"})
    check_items.append({"no": "13", "name": "Pattern", "m": "manage",
                        "r": "read", "c": "create", "u": "update",
                        "d": "destroy", "item_name": "pattern"})
    check_items.append({"no": "14", "name": "Account", "m": "manage",
                        "r": "read", "c": "create", "u": "update",
                        "d": "destroy", "item_name": "account"})
    check_items.append({"no": "15", "name": "Role", "m": "manage",
                        "r": "read", "c": "create", "u": "update",
                        "d": "destroy", "item_name": "role", "read": True})
    check_items.append({"no": "16", "name": "Permission", "m": "manage",
                        "r": "read", "c": "create", "u": "update",
                        "d": "destroy", "item_name": "permission"})

    try:
        code = FuncCode.roleCreate.value
        token = request.session['auth_token']
        project_id = request.session['project_id']

        if request.method == "GET":

            return render(request, Html.roleCreate,
                          {'message': '',
                           'role': {"token": token, 'project': project_id},
                           'items': check_items, 'save': True})
        else:
            # -- Get a value from a form
            p = request.POST

            form = roleForm(request.POST)
            if not form.is_valid():
                return render(request, Html.roleCreate,
                              {'role': p, 'form': form, 'items': check_items,
                               'save': True})

            checkbox = False
            for param in request.POST:
                if '-' in param:
                    if param.split('-')[1] in \
                       ['manage', 'create', 'read', 'update', 'destroy']:
                        checkbox = True
                        break

            if not checkbox:
                return render(request, Html.roleCreate,
                              {'role': p,
                               'message': Error.CheckboxNotSelected.value,
                               'items': check_items, 'save': True})

            # -- API call, get a response
            RoleUtil.create_role(
                code, token, project_id, p.get('name'),
                p.get('description'), p)

            # -- Validate check

            return redirect(Path.roleList)
    except Exception as ex:
        log.error(FuncCode.roleCreate.value, None, ex)
        return render(request, Html.roleCreate,
                      {'message': str(ex), 'role': request.POST,
                       'items': check_items, 'save': True},)


def roleEdit(request, id):
    try:
        if not SessionUtil.check_login(request):
            return redirect(Path.logout)
        if not SessionUtil.check_permission(request, 'role', 'update'):
            return render_to_response(Html.error_403)

        token = request.session.get('auth_token')
        code = FuncCode.roleEdit.value

        if request.method == "GET":
            role = RoleUtil.get_role_detail(code, token, id)

            return render(request, Html.roleEdit,
                          {'message': '', 'role': role["role"],
                           'items': role["check_items"], 'save': True},)
        else:
            p = request.POST
            checkbox = False
            for param in request.POST:
                if '-' in param:
                    if param.split('-')[1] in \
                       ['manage', 'create', 'read', 'update', 'destroy']:
                        checkbox = True
                        break

            if not checkbox:
                return render(request, Html.roleCreate,
                              {'role': p,
                               'message': Error.CheckboxNotSelected.value,
                               'items': role["check_items"], 'save': True})

            # -- Get a value from a form
            RoleUtil.edit_role(code, token, id,
                               request.POST.get('name'),
                               request.POST.get('description'), request.POST)

            SessionUtil.edit_role_session(code, request.session, id)

            return redirect(Path.roleList)

    except Exception as ex:
        log.error(code, None, ex)
        role = RoleUtil.get_role_detail(
            code, request.session['auth_token'], id)
        return render(request, Html.roleEdit,
                      {'message': str(ex), 'role': role["role"],
                       'items': role["check_items"], 'save': True})


def roleDelete(request, id):
    code = FuncCode.roleDelete.value
    roles = None
    try:
        if not SessionUtil.check_login(request):
            return redirect(Path.logout)
        if not SessionUtil.check_permission(request, 'role', 'destroy'):
            return render_to_response(Html.error_403)

        # -- URL and data set
        session = request.session
        token = session.get('auth_token')
        project_id = session.get('project_id')
        roles = RoleUtil.get_role_list(code, token, project_id)

        # -- Role delete
        RoleUtil.delete_role(code, token, id)

        return redirect(Path.roleList)
    except Exception as ex:
        log.error(code, None, ex)

        return render(request, Html.roleList,
                      {'roles': roles, 'message': str(ex)})
