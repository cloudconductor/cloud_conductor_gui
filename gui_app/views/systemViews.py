# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect, render_to_response
from ..forms import systemForm
from ..utils import ApiUtil
from ..utils import SystemUtil
from ..utils import SessionUtil
from ..utils.PathUtil import Path
from ..utils.PathUtil import Html
from ..utils.ApiUtil import Url
from ..enum.FunctionCode import FuncCode
from ..logs import log


def systemList(request):
    try:
        if not SessionUtil.check_login(request):
            return redirect(Path.logout)
        if not SessionUtil.check_permission(request, 'system', 'list'):
            return render_to_response(Html.error_403)

        systems = None
        # -- Get a system list, API call
        url = Url.systemList

        data = {
            'auth_token': request.session['auth_token'],
            'project_id': request.session['project_id']
        }
        systems = ApiUtil.requestGet(url, FuncCode.systemList.value, data)
#         systems = systems['lists']

        return render(request, Html.systemList,
                      {'system': systems, 'message': ''})
    except Exception as ex:
        log.error(FuncCode.systemList.value, None, ex)

        return render(request, Html.systemList,
                      {"system": '', 'message': str(ex)})

    return render(request, Html.systemList,
                  {'system': '', 'baseImage': '', 'message': ex})


def systemDetail(request, id):
    system = None
    try:
        if not SessionUtil.check_login(request):
            return redirect(Path.logout)
        if not SessionUtil.check_permission(request, 'system', 'read'):
            return render_to_response(Html.error_403)

        # -- system DetailAPI call, get a response
        token = request.session.get('auth_token')
        code = FuncCode.systemDetail.value
        system = SystemUtil.get_system_detail(code, token, id)

        return render(request, Html.systemDetail,
                      {'system': system, 'message': ''})
    except Exception as ex:
        log.error(FuncCode.systemDetail.value, None, ex)

        return render(request, Html.systemDetail,
                      {'system': system, 'message': str(ex)})


def systemCreate(request):
    try:
        if not SessionUtil.check_login(request):
            return redirect(Path.logout)
        if not SessionUtil.check_permission(request, 'system', 'create'):
            return render_to_response(Html.error_403)

        if request.method == "GET":

            return render(request, Html.systemCreate,
                          {'system': '', 'form': '',
                           'message': '', 'save': True})
        else:
            # -- Get a value from a form
            p = request.POST
            # -- Validate check
            form = systemForm(p)
            form.full_clean()
            if not form.is_valid():

                return render(request, Html.systemCreate,
                              {'system': p, 'form': form, 'message': '',
                               'save': True})

            code = FuncCode.systemCreate.value
            SystemUtil.create_system(code, request.session.get('auth_token'),
                                     request.session.get('project_id'),
                                     form.data)

            return redirect(Path.systemList)
    except Exception as ex:
        p = request.POST
        log.error(FuncCode.systemCreate.value, None, ex)

        return render(request, Html.systemCreate,
                      {'system': p, 'form': '',
                       "message": str(ex), 'save': True})


def systemEdit(request, id):
    try:
        if not SessionUtil.check_login(request):
            return redirect(Path.logout)
        if not SessionUtil.check_permission(request, 'system', 'update'):
            return render_to_response(Html.error_403)

        code = FuncCode.systemEdit.value
        token = request.session.get('auth_token')
        if request.method == "GET":
            system = SystemUtil.get_system_detail(code, token, id)

            return render(request, Html.systemEdit,
                          {'system': system, 'message': '', 'save': True})
        else:
            # -- Get a value from a form
            p = request.POST
            # -- Validate check
            form = systemForm(p)
            form.full_clean()
            if not form.is_valid():

                return render(request, Html.systemEdit,
                              {'system': p, 'form': form,
                               'message': '', 'save': True})

            # -- Edit a system, api call
            SystemUtil.edit_system(code, request.session.get('auth_token'),
                                   id, form.data)

            return redirect(Path.systemList)
    except Exception as ex:
        log.error(FuncCode.systemEdit.value, None, ex)

        return render(request, Html.systemEdit,
                      {'system': request.POST, "message": str(ex),
                       'save': True})


def systemDelete(request, id):
    code = FuncCode.systemDelete.value
    system = None
    try:
        if not SessionUtil.check_login(request):
            return redirect(Path.logout)
        if not SessionUtil.check_permission(request, 'system', 'destroy'):
            return render_to_response(Html.error_403)

        # -- URL and data set
        token = request.session.get('auth_token')
        system = SystemUtil.get_system_detail(code, token, id)

        SystemUtil.get_system_delete(code, token, id)

        return redirect(Path.systemList)
    except Exception as ex:
        log.error(FuncCode.systemDelete.value, None, ex)

        return render(request, Html.systemDetail,
                      {'system': system, 'message': ex})
