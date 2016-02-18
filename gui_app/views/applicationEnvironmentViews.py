# -*- coding: utf-8 -*-
import ast
import json
from django.shortcuts import render, redirect, render_to_response, HttpResponse
from ..enum.FunctionCode import FuncCode
from ..enum.MessageCode import Info
from ..enum.OSVersion import OSVersion
from ..enum.StatusCode import Blueprint
from ..forms import blueprintForm
from ..forms import blueprintSelectForm
from ..forms import systemForm
from ..forms import systemSelectForm
from ..forms import w_appenv_environmentForm
from ..logs import log
from ..utils import ApiUtil
from ..utils import BlueprintHistoryUtil
from ..utils import BlueprintPatternUtil
from ..utils import BlueprintUtil
from ..utils import EnvironmentUtil
from ..utils import PatternUtil
from ..utils import SessionUtil
from ..utils import StringUtil
from ..utils import SystemUtil
from ..utils.ApiUtil import Url
from ..utils.PathUtil import Html
from ..utils.PathUtil import Path


def systemSelect(request):
    try:
        session = request.session

        id = session.get('project_id')
        token = session.get('auth_token')
        code = FuncCode.appenv_system.value
        list = SystemUtil.get_system_list(code, token, id)

        if request.method == "GET":
            system = session.get('w_sys_select')

            return render(request, Html.envapp_systemSelect,
                          {"list": list, 'system': system, 'message': '',
                           'wizard_code': Info.WizardSystem.value})
        elif request.method == "POST":
            p = request.POST
            cpPost = p.copy()
            system = putSystem(cpPost)
            form = systemSelectForm(system)
            if not form.is_valid():

                return render(request, Html.envapp_systemSelect,
                              {"list": list, 'system': system,
                               'form': form,
                               'message': '',
                               'wizard_code': Info.WizardSystem.value})

            session['w_sys_select'] = system

            return redirect(Path.envapp_bluprintSelect)
    except Exception as ex:
        log.error(FuncCode.appenv_system.value, None, ex)

        return render(request, Html.envapp_systemSelect,
                      {"system": '', 'message': str(ex),
                       'wizard_code': Info.WizardSystem.value})


def systemCreate(request):
    try:
        code = FuncCode.newapp_system.value
        if request.method == "GET":

            return render(request, Html.envapp_systemCreate,
                          {'message': ''})
        elif request.method == "POST":
            param = request.POST

            # -- Validate check
            form = systemForm(param)
            if not form.is_valid():

                return render(request, Html.envapp_systemCreate,
                              {"system": param, 'form': form, 'message': ''})

            system = SystemUtil.create_system(code,
                                              request.session.get(
                                                  'auth_token'),
                                              request.session.get(
                                                  'project_id'),
                                              form.data)

            request.session['w_sys_select'] = {
                "id": system.get("id"), "name": system.get("name")}

            return redirect(Path.envapp_bluprintSelect)
    except Exception as ex:
        log.error(FuncCode.newapp_system.value, None, ex)

        return render(request, Html.envapp_systemCreate,
                      {"application": '', 'message': str(ex)})


def blueprintSelect(request):
    list = None
    blueprint = None
    try:
        code = FuncCode.appenv_blueprint.value
        session = request.session
        token = session['auth_token']
        project_id = session['project_id']

        data = {
            'auth_token': token,
            'project_id': project_id
        }
        list = BlueprintUtil.get_blueprint_version(code, data)

        if request.method == "GET":
            blueprint = session.get('w_bp_select')

            return render(request, Html.envapp_bluprintSelect,
                          {'list': list, 'blueprint': blueprint,
                           'message': '',
                           'wizard_code': Info.WizardSystem.value})
        elif request.method == "POST":
            p = request.POST
            cpPost = p.copy()
            blueprint = putBlueprint(cpPost)
            form = blueprintSelectForm(blueprint)
            if not form.is_valid():

                return render(request, Html.envapp_bluprintSelect,
                              {'list': list, 'blueprint': blueprint,
                               'form': form,
                               'wizard_code': Info.WizardSystem.value})

            request.session['w_bp_select'] = blueprint

            return redirect(Path.envapp_environmentCreate)
    except Exception as ex:
        log.error(FuncCode.appenv_blueprint.value, None, ex)

        return render(request, Html.envapp_bluprintSelect,
                      {'list': list, 'blueprint': blueprint,
                       'message': str(ex),
                       'wizard_code': Info.WizardSystem.value})


def blueprintCreate(request):
    code = FuncCode.blueprintCreate.value
    osversion = list(OSVersion)
    patterns = ''
    my_pattern = ''
    try:
        if not SessionUtil.check_login(request):
            return redirect(Path.logout)
        if not SessionUtil.check_permission(request, 'blueprint', 'create'):
            return render_to_response(Html.error_403)

        project_id = request.session['project_id']
        token = request.session['auth_token']
        patterns = PatternUtil.get_pattern_list(code, token, project_id)

        if request.method == "GET":

            return render(request, Html.envapp_blueprintCreate,
                          {'blueprint': '', 'patterns': patterns,
                           'osversion': osversion, 'form': '', 'message': ''})
        else:
            # -- Get a value from a form
            p = request.POST
            my_pattern = BlueprintPatternUtil.dic_pattern_list(
                p.getlist('os_version'), p.getlist('pattern_id'))

            if p.get('blueprint_id'):
                bp = BlueprintHistoryUtil.get_new_blueprint_history(
                    FuncCode.newapp_environment.value,
                    request.session.get('auth_token'), p.get('blueprint_id'))
                ret = 0
                if bp['status'] == Blueprint.ERROR.value:
                    ret = 1
                elif bp['status'] == Blueprint.CREATE_COMPLETE.value:
                    ret = 2
                    bp = {'id': p.get('blueprint_id'),
                          'version': bp.get('version')}
                    request.session['w_bp_select'] = bp

                return HttpResponse(json.dumps({'ret': ret}),
                                    content_type='application/json')

            # -- Validate check
            form = blueprintForm(p)
            if not form.is_valid():

                return render(request, Html.envapp_blueprintCreate,
                              {'blueprint': p, 'patterns': patterns,
                               'my_pattern': my_pattern,
                               'osversion': osversion,
                               'form': form, 'message': ''})

            # -- 1.Create a blueprint, api call
            blueprint = BlueprintUtil.create_blueprint(
                code, token, project_id, form.data)

            # -- 2. Add a Pattern, api call
            BlueprintPatternUtil.add_blueprint_pattern_list(
                code, token, blueprint.get('id'),
                p.getlist('os_version'), p.getlist('pattern_id'))

            # -- 3. BlueprintBuild, api call
            BlueprintUtil.create_bluepritn_build(
                code, token, blueprint.get('id'))

            return render(request, Html.envapp_blueprintCreate,
                          {'blueprint': p, 'patterns': patterns,
                           'my_pattern': my_pattern,
                           'osversion': osversion,
                           'blueprint_id': blueprint.get("id"),
                           'form': form, 'message': ''})

            return redirect(Path.blueprintList)
    except Exception as ex:
        log.error(code, None, ex)

        return render(request, Html.envapp_blueprintCreate,
                      {'blueprint': request.POST, 'patterns': patterns,
                       'my_pattern': my_pattern, 'osversion': osversion,
                       'form': '', 'message': str(ex)})


def environmentCreate(request):
    clouds = None
    code = FuncCode.newapp_environment.value
    try:
        session = request.session
        data = {
            'auth_token': session.get('auth_token'),
            'project_id': session.get('project_id')
        }

        clouds = ApiUtil.requestGet(Url.cloudList, code, data)

        blueprints = BlueprintHistoryUtil.get_blueprint_parameters(
            code, session.get('auth_token'),
            request.session['w_bp_select'].get('id'),
            request.session['w_bp_select'].get('version'))

        if request.method == "GET":
            environment = request.session.get('w_env_create')

            return render(request, Html.envapp_environmentCreate,
                          {'clouds': clouds, 'systems': None,
                           'blueprints': blueprints,
                           'env': environment,
                           'message': '', 'create': True})
        elif request.method == "POST":
            param = request.POST
            # -- Validate check
            form = w_appenv_environmentForm(param)
            if not form.is_valid():

                return render(request, Html.envapp_environmentCreate,
                              {'clouds': clouds, 'systems': None,
                               'blueprints': blueprints, 'env': param,
                               'form': form, 'create': True})

            # -- Session add
            environment = EnvironmentUtil.put_environment(
                form.data, request.session)
            request.session['w_env_create'] = environment

            return redirect(Path.envapp_confirm)
    except Exception as ex:
        log.error(FuncCode.appenv_environment.value, None, ex)

        return render(request, Html.envapp_environmentCreate,
                      {'clouds': clouds, 'systems': None,
                       'blueprints': blueprints, 'env': request.POST,
                       'create': True, 'message': str(ex)})


def confirm(request):
    try:
        session = request.session
        sys_session = session.get('w_sys_select')
        bp_session = session.get('w_bp_select')
        env_session = session.get('w_env_create')

        if request.method == "GET":

            return render(request, Html.envapp_confirm,
                          {"system": sys_session, 'blueprint': bp_session,
                           'environment': env_session, 'message': ''})
        elif request.method == "POST":
            session = request.session
            code = FuncCode.appenv_confirm.value

            EnvironmentUtil.create_wizard_environment(code, env_session,
                                                      sys_session, bp_session)

            # -- session delete
            sessionDelete(session)

            return redirect(Path.top)
    except Exception as ex:
        log.error(FuncCode.appenv_confirm.value, None, ex)
        session = request.session

        return render(request, Html.envapp_confirm,
                      {'system': sys_session, 'blueprint': bp_session,
                       'environment': env_session,
                       'message': str(ex)})


def putBlueprint(param):

    blueprint = param.get('id', None)
    if blueprint is not None and blueprint != '':
        blueprint = ast.literal_eval(blueprint)

        param['id'] = str(blueprint.get('id'))
        param['version'] = blueprint.get('version')
        param['name'] = blueprint.get('name')

    return param


def putEnvironment(param):

    environment = param.get('id', None)
    if environment is not None and environment != '':
        environment = ast.literal_eval(environment)

        param['id'] = str(environment.get('id'))
        param['name'] = environment.get('name')

    return param


def putSystem(param):

    system = param.get('id', None)
    if system is not None and system != '':
        system = ast.literal_eval(system)

        param['id'] = str(system.get('id'))
        param['name'] = system.get('name')

    return param


def systemPut(req):
    if StringUtil.isEmpty(req):
        return None

    system = {
        'id': req.get('id'),
        'name': req.get('name'),
    }
    return system


def environmentPut(req):
    if StringUtil.isEmpty(req):
        return None

    environment = {
        'id': req.get('id'),
        'name': req.get('name'),
        'candidates_attributes_1': req.get('candidates_attributes_1'),
        'candidates_attributes_2': req.get('candidates_attributes_2'),
        'candidates_attributes_3': req.get('candidates_attributes_3'),
        'json/tomcat_pattern/SSHLocation':
            req.get('json/tomcat_pattern/SSHLocation'),
        'json/tomcat_pattern/WebInstanceType':
            req.get('json/tomcat_pattern/WebInstanceType'),
        'json/tomcat_pattern/DbInstanceType':
            req.get('json/tomcat_pattern/DbInstanceType'),
        'json/tomcat_pattern/CloudConductorLocation':
            req.get('json/tomcat_pattern/CloudConductorLocation'),
        'json/tomcat_pattern/KeyName':
            req.get('json/tomcat_pattern/KeyName'),
        'json/tomcat_pattern/ApInstanceType':
            req.get('json/tomcat_pattern/ApInstanceType'),
        'user_attributes': req.get('user_attributes'),
        'description': req.get('description'),
    }

    return environment


def sessionDelete(session):

    if 'w_sys_select' in session:
        del session['w_sys_select']

    if 'w_env_create' in session:
        del session['w_env_create']

    if 'w_bp_select' in session:
        del session['w_bp_select']
