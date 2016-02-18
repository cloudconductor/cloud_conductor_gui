# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect, render_to_response
import ast
from ..forms import selecttForm
from ..forms import applicationForm
from ..utils import ApplicationUtil
from ..utils import ApplicationHistoryUtil
from ..utils import EnvironmentUtil
from ..utils import StringUtil
from ..utils.PathUtil import Path
from ..utils.PathUtil import Html
from ..enum.FunctionCode import FuncCode
from ..enum.ApplicationType import ApplicaionType
from ..enum.ProtocolType import ProtocolType
from ..utils import SessionUtil
from ..utils import SystemUtil
from ..logs import log


def applicationSelect(request):
    try:
        session = request.session
        code = FuncCode.appDep_application.value
        token = session.get('auth_token')
        project_id = session.get('project_id')
        application = ''
        list = ''

        list = ApplicationUtil.get_application_version(
            code, token, project_id)

        if request.method == "GET":
            application = request.session.get('w_app_select')

            return render(request, Html.appdeploy_applicationSelect,
                          {'list': list, 'application': application,
                           'message': ''})
        elif request.method == "POST":
            param = request.POST

            # -- Session add
            application = selectPut(param)
            form = selecttForm(application)
            if not form.is_valid():

                return render(request, Html.appdeploy_applicationSelect,
                              {'list': list, 'application': application,
                               'form': form, 'message': ''})

            request.session['w_app_select'] = application

            return redirect(Path.appdeploy_environmentSelect)
    except Exception as ex:
        log.error(FuncCode.appDep_application.value, None, ex)

        return render(request, Html.appdeploy_applicationSelect,
                      {'list': list, 'application': application,
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

            return render(request, Html.appdeploy_applicationCreate,
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

                return render(request, Html.appdeploy_applicationCreate,
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

            request.session['w_app_select'] = {"id": app.get("id"),
                                               "name": app.get("name")}

            return redirect(Path.appdeploy_environmentSelect)
    except Exception as ex:
        log.error(FuncCode.applicationCreate.value, None, ex)

        return render(request, Html.appdeploy_applicationCreate,
                      {'app': request.POST, 'history': request.POST,
                       'apptype': apptype,
                       'protocol': protocol, 'form': '',
                       'systems': systems, 'message': str(ex), 'save': True})


def environmentSelect(request):
    list = ''
    try:
        code = FuncCode.appDep_environment.value
        session = request.session
        environment = session.get('w_env_select')
        token = session['auth_token']
        project_id = session['project_id']

        app = ApplicationUtil.get_application_detail(
            code, token, session.get('w_app_select').get('id'))

        list = EnvironmentUtil.get_environment_list_system_id(
            code, token, project_id, app.get("system_id"))

        if request.method == "GET":
            return render(request, Html.appdeploy_environmentSelect,
                          {"list": list, 'environment': environment,
                           'message': ''})
        elif request.method == "POST":
            param = request.POST
            environment = selectPut(param)

            form = selecttForm(environment)
            if not form.is_valid():
                return render(request, Html.appdeploy_environmentSelect,
                              {"list": list, 'environment': environment,
                               'form': form,
                               'message': ''})

            request.session['w_env_select'] = environment

            return redirect(Path.appdeploy_confirm)
    except Exception as ex:
        log.error(FuncCode.appDep_environment.value, None, ex)

        return render(request, Html.appdeploy_environmentSelect,
                      {"list": '', 'environment': '', 'message': str(ex)})


def confirm(request):
    try:
        code = FuncCode.appDep_confirm.value
        session = request.session
        app_session = session.get('w_app_select')
        env_session = session.get('w_env_select')

        if request.method == "GET":
            return render(request, Html.appdeploy_confirm,
                          {'application': app_session,
                           'environment': env_session, 'message': ''})
        elif request.method == "POST":
            session = request.session
            code = FuncCode.newapp_confirm.value
            token = session.get('auth_token')
            env_id = env_session.get('id')
            app_id = app_session.get('id')

            # -- application deploy
            ApplicationUtil.deploy_application(code, token, env_id, app_id)

            # -- session delete
            sessionDelete(session)

            return redirect(Path.top)
    except Exception as ex:
        log.error(FuncCode.newapp_confirm.value, None, ex)
        session = request.session

        return render(request, Html.appdeploy_confirm,
                      {"application": session.get('application'),
                       'environment': session.get('environment'),
                       'message': str(ex)})


def selectPut(req):
    if StringUtil.isEmpty(req):
        return None

    select_param = req.get('id', None)
    if StringUtil.isNotEmpty(select_param):
        select_param = ast.literal_eval(select_param)

        param = {
            'id': str(select_param.get('id')),
            'name': select_param.get('name'),
        }
        return param
    else:
        return select_param


def putBlueprint(param):

    blueprint = param.get('blueprint', None)
    if not (blueprint is None) and not (blueprint == ''):
        blueprint = ast.literal_eval(blueprint)

        param['blueprint_id'] = blueprint.get('id')
        param['version'] = blueprint.get('version')

    return param


def sessionDelete(session):

    if 'w_env_select' in session:
        del session['w_env_select']

    if 'w_app_select' in session:
        del session['w_app_select']
