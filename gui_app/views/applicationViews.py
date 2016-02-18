# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect, render_to_response
from ..forms import applicationForm
from ..forms import applicationForm2
from ..forms import applicationHistoryForm
from ..utils import ApiUtil
from ..utils import ApplicationUtil
from ..utils import SystemUtil
from ..utils import ApplicationHistoryUtil
from ..utils.PathUtil import Path
from ..utils.PathUtil import Html
from ..utils.ApiUtil import Url
from ..utils import SessionUtil
from ..enum.FunctionCode import FuncCode
from ..enum.ApplicationType import ApplicaionType
from ..enum.ProtocolType import ProtocolType
from ..logs import log


def applicationList(request):
    apps = None
    try:
        if not SessionUtil.check_login(request):
            return redirect(Path.logout)
        if not SessionUtil.check_permission(request,
                                            'application', 'list'):
            return render_to_response(Html.error_403)

        # -- Get a application list, API call
        url = Url.applicationList

        data = {
            'auth_token': request.session['auth_token'],
            'project_id': request.session['project_id']
        }
        apps = ApiUtil.requestGet(url, FuncCode.applicationList.value, data)

        for app in apps:
            system = SystemUtil.get_system_detail(
                FuncCode.applicationList.value,
                request.session['auth_token'], app.get("system_id"))
            app["system_name"] = system.get("name")

        return render(request, Html.applicationList,
                      {'apps': apps, 'message': ''})
    except Exception as ex:
        log.error(FuncCode.applicationList.value, None, ex)

        return render(request, Html.applicationList,
                      {"application": apps, 'message': str(ex)})


def applicationDetail(request, id):
    code = FuncCode.applicationDetail.value
    app = None
    history_list = None
    try:
        if not SessionUtil.check_login(request):
            return redirect(Path.logout)
        if not SessionUtil.check_permission(request, 'application', 'read'):
            return render_to_response(Html.error_403)

        # -- application DetailAPI call, get a response
        token = request.session['auth_token']
        app = ApplicationUtil.get_application_detail(code, token, id)
        system = SystemUtil.get_system_detail(
            FuncCode.applicationList.value,
            request.session['auth_token'], app.get("system_id"))
        app["system_name"] = system.get("name")

        history_list = ApplicationHistoryUtil.get_history_list(code, token, id)

        return render(request, Html.applicationDetail,
                      {'app': app, 'history_list': history_list,
                       'message': ''})
    except Exception as ex:
        log.error(FuncCode.applicationDetail.value, None, ex)

        return render(request, Html.applicationDetail,
                      {'app': app, 'history_list': history_list,
                       'message': str(ex)})


def applicationCreate(request):
    code = FuncCode.applicationCreate.value
    apptype = list(ApplicaionType)
    protocol = list(ProtocolType)
    systems = None
    try:
        if not SessionUtil.check_login(request):
            return redirect(Path.logout)
        if not SessionUtil.check_permission(request, 'application', 'create'):
            return render_to_response(Html.error_403)

        token = request.session['auth_token']
        project_id = request.session['project_id']

        systems = SystemUtil.get_system_list2(code, token, project_id)

        if request.method == "GET":

            return render(request, Html.applicationCreate,
                          {'app': '', 'history': '', 'apptype': apptype,
                           'protocol': protocol, 'message': '',
                           'systems': systems, 'save': True})
        else:
            # -- Get a value from a form
            p = request.POST
            cpPost = p.copy()

            # -- Validate check
            form = applicationForm(p)
            form.full_clean()
            if not form.is_valid():

                return render(request, Html.applicationCreate,
                              {'app': cpPost, 'history': cpPost,
                               'apptype': apptype,
                               'protocol': protocol, 'form': form,
                               'message': '', 'systems': systems,
                               'save': True})

            # -- 1.Create a application, api call
            app = ApplicationUtil.create_application(code, token, form.data)

            # -- 2.Create a applicationhistory, api call
            ApplicationHistoryUtil.create_history(
                code, token, app.get('id'), form.data)

            return redirect(Path.applicationList)
    except Exception as ex:
        log.error(FuncCode.applicationCreate.value, None, ex)

        return render(request, Html.applicationCreate,
                      {'app': request.POST, 'history': request.POST,
                       'apptype': apptype,
                       'protocol': protocol, 'form': '',
                       'systems': systems, 'message': str(ex), 'save': True})


def applicationEdit(request, id):
    code = FuncCode.applicationEdit.value
    systems = None
    app = None

    try:
        if not SessionUtil.check_login(request):
            return redirect(Path.logout)
        if not SessionUtil.check_permission(request, 'application', 'update'):
            return render_to_response(Html.error_403)

        token = request.session['auth_token']
        project_id = request.session['project_id']
        systems = SystemUtil.get_system_list(code, token, project_id)

        if request.method == "GET":
            app = ApplicationUtil.get_application_detail(code, token, id)

            return render(request, Html.applicationEdit,
                          {'app': app, 'form': '', 'message': '',
                           'systems': systems, 'save': True})
        else:
            # -- Get a value from a form
            p = request.POST
            # -- Validate check
            form = applicationForm2(p)
            form.full_clean()
            if not form.is_valid():

                return render(request, Html.applicationEdit,
                              {'app': p, 'form': form, 'message': '',
                               'systems': systems, 'save': True})
            # -- 1.Edit a application, api call
            app = ApplicationUtil.edit_application(code, token, id, form.data)

            return redirect(Path.applicationList)
    except Exception as ex:
        log.error(FuncCode.applicationEdit.value, None, ex)

        return render(request, Html.applicationEdit,
                      {'app': request.POST, 'form': '', 'message': str(ex),
                       'systems': systems, 'save': True})


def applicationDelete(request, id):
    code = FuncCode.applicationDelete.value
    app = None
    try:
        if not SessionUtil.check_login(request):
            return redirect(Path.logout)
        if not SessionUtil.check_permission(request, 'application', 'destroy'):
            return render_to_response(Html.error_403)

        # -- URL and data set
        token = request.session['auth_token']
        app = ApplicationUtil.get_application_detail(code, token, id)

        ApplicationUtil.delete_application(code, token, id)

        return redirect(Path.applicationList)
    except Exception as ex:
        log.error(code, None, ex)

        return render(request, Html.applicationDetail,
                      {'app': app, 'message': ex})


def applicationHistoryDetail(request, id, hid):
    code = FuncCode.applicationHistoryDetail.value
    app = None
    history_list = None
    try:
        if not SessionUtil.check_login(request):
            return redirect(Path.logout)
        if not SessionUtil.check_permission(request, 'application', 'read'):
            return render_to_response(Html.error_403)

        # -- application DetailAPI call, get a response
        token = request.session['auth_token']
        history = ApplicationHistoryUtil.get_history_detail(code, token,
                                                            id, hid)

        return render(request, Html.applicationHistoryDetail,
                      {'history': history, 'message': ''})
    except Exception as ex:
        log.error(FuncCode.applicationDetail.value, None, ex)

        return render(request, Html.applicationHistoryDetail,
                      {'app': app, 'history_list': history_list,
                       'message': str(ex)})


def applicationDeploy(request, id):
    code = FuncCode.applicationDeploy.value
    blueprint = None
    pattern = None
    history_list = None
    try:
        if not SessionUtil.check_login(request):
            return redirect(Path.logout)
        if not SessionUtil.check_permission(request, 'blueprint', 'create'):
            return render_to_response(Html.error_403)

        token = request.session['auth_token']

        # -- URL and data set
        ApplicationUtil.create_bluepritn_build(code, token, id)

        return redirect(Path.blueprintDetail(id))
    except Exception as ex:
        log.error(code, None, ex)

        return render(request, Html.blueprintDetail,
                      {'blueprint': blueprint, 'pattern': pattern,
                       'history_list': history_list, 'message': ex})


def applicationHistoryCreate(request, id):
    code = FuncCode.applicationHistoryEdit.value
    apptype = list(ApplicaionType)
    protocol = list(ProtocolType)

    try:
        if not SessionUtil.check_login(request):
            return redirect(Path.logout)
        if not SessionUtil.check_permission(request, 'application', 'create'):
            return render_to_response(Html.error_403)

        token = request.session['auth_token']

        if request.method == "GET":
            data = {'application_id': id}

            return render(request, Html.applicationHistoryCreate,
                          {'history': data, 'form': '', 'apptype': apptype,
                           'protocol': protocol, 'message': ''})
        else:
            # -- Get a value from a form
            p = request.POST
            # -- Validate check
            form = applicationHistoryForm(p)
            form.full_clean()
            if not form.is_valid():

                return render(request, Html.applicationHistoryCreate,
                              {'history': p, 'apptype': apptype,
                               'protocol': protocol, 'form': form,
                               'message': ''})

            # -- 1.Edit a applicationhistory, api call
            ApplicationHistoryUtil.create_history(
                code, token, id, form.data)

            return redirect(Path.applicationDetail(id))
    except Exception as ex:
        log.error(code, None, ex)

        return render(request, Html.applicationHistoryCreate,
                      {'history': request.POST, 'apptype': apptype,
                       'protocol': protocol, 'form': '', 'message': str(ex)})


def applicationHistoryEdit(request, id, hid):
    code = FuncCode.applicationHistoryEdit.value
    apptype = list(ApplicaionType)
    protocol = list(ProtocolType)
    history = None

    try:
        if not SessionUtil.check_login(request):
            return redirect(Path.logout)
        if not SessionUtil.check_permission(request, 'application', 'update'):
            return render_to_response(Html.error_403)

        token = request.session['auth_token']

        if request.method == "GET":
            history = ApplicationHistoryUtil.get_history_detail(
                code, token, id, hid)
            return render(request, Html.applicationHistoryEdit,
                          {'history': history, 'form': '', 'apptype': apptype,
                           'protocol': protocol, 'message': '', 'save': True})
        else:
            # -- Get a value from a form
            p = request.POST
            # -- Validate check
            form = applicationHistoryForm(p)
            form.full_clean()
            if not form.is_valid():

                return render(request, Html.applicationHistoryEdit,
                              {'history': p, 'apptype': apptype,
                               'protocol': protocol, 'form': form,
                               'message': '', 'save': True})

            # -- 1.Edit a applicationhistory, api call
            ApplicationHistoryUtil.edit_history(
                code, token, id, hid, form.data)

            return redirect(Path.applicationDetail(id))
    except Exception as ex:
        log.error(FuncCode.applicationEdit.value, None, ex)

        return render(request, Html.applicationHistoryEdit,
                      {'history': request.POST, 'apptype': apptype,
                       'protocol': protocol, 'form': '', 'message': str(ex),
                       'save': True})
