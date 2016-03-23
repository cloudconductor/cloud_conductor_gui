# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect, render_to_response
import ast
from ..forms import environmentForm
from ..forms import edit_environmentForm
from ..utils import ApiUtil
from ..utils import BlueprintUtil
from ..utils import BlueprintHistoryUtil
from ..utils import EnvironmentUtil
from ..utils import SessionUtil
from ..utils import SystemUtil
from ..utils.PathUtil import Path
from ..utils.PathUtil import Html
from ..utils.ApiUtil import Url
from ..utils.BlueprintUtil import get_blueprint_version
from ..api_models.systems import *
from ..api_models.blueprints import *
from ..api_models.environments import *
from ..enum.FunctionCode import FuncCode
from ..logs import log
PATRITION = '/'


def environmentList(request):
    try:
        if not SessionUtil.check_login(request):
            return redirect(Path.logout)
        if not SessionUtil.check_permission(request, 'environment', 'list'):
            return render_to_response(Html.error_403)

        code = FuncCode.environmentList.value
        auth_token = request.session['auth_token']
        project_id = request.session['project_id']

        envs = Environments(code, auth_token, project_id)
        blueprints = Blueprints(code, auth_token, project_id)
        systems = Systems(code, auth_token, project_id)
        blueprint_histories = blueprints.get_all_blueprint_histories()

        for env in envs:
            for blueprint_history in blueprint_histories:
                if env['blueprint_history_id'] == blueprint_history['id']:
                    blueprint_id = blueprint_history['blueprint_id']
                    blueprint = blueprints.get_blueprint(blueprint_id)
                    system = systems.get_system(env['system_id'])
                    env['bp_name'] = blueprint['name']
                    env['system_name'] = system['name']
                    break

        return render(request, Html.environmentList,
                      {'envs': envs, 'message': ''})
    except Exception as ex:
        log.error(FuncCode.environmentList.value, None, ex)

        return render(request, Html.environmentList,
                      {"environment": '', 'message': str(ex)})


def environmentDetail(request, id):
    code = FuncCode.environmentDetail.value
    env = None
    try:
        if not SessionUtil.check_login(request):
            return redirect(Path.logout)
        if not SessionUtil.check_permission(request, 'environment', 'read'):
            return render_to_response(Html.error_403)

        # -- environment DetailAPI call, get a response
        token = request.session['auth_token']
        env = EnvironmentUtil.get_environment_detail(code, token, id)
        system = SystemUtil.get_system_detail(
            code, request.session['auth_token'], env.get("system_id"))
        bp = BlueprintHistoryUtil.get_blueprint_history_list_id(
            FuncCode.environmentList.value, request.session['auth_token'],
            request.session['project_id'], env.get("blueprint_history_id"))
        env["system_name"] = system.get("name")
        env["bp_name"] = bp.get("name")

        return render(request, Html.environmentDetail,
                      {'env': env, 'message': ''})
    except Exception as ex:
        log.error(FuncCode.environmentDetail.value, None, ex)

        return render(request, Html.environmentDetail,
                      {'env': env, 'message': str(ex)})


def environmentCreate(request):
    clouds = None
    systems = None
    blueprints = None
    code = None
    try:
        if not SessionUtil.check_login(request):
            return redirect(Path.logout)
        if not SessionUtil.check_permission(request, 'environment', 'create'):
            return render_to_response(Html.error_403)

        p = request.POST
        code = FuncCode.environmentCreate.value
        token = request.session['auth_token']
        project_id = request.session['project_id']
        data = {
            'auth_token': token,
            'project_id': project_id
        }

        clouds = ApiUtil.requestGet(Url.cloudList, code, data)
        systems = ApiUtil.requestGet(Url.systemList, code, data)
        blueprints = get_blueprint_version(code, data)

        if request.method == "GET":
            return render(request, Html.environmentCreate,
                          {'env': data, 'clouds': clouds, 'systems': systems,
                           'blueprints': blueprints, 'message': '',
                           'create': True, 'save': True})
        else:
            # -- Get a value from a form
            p = request.POST
            # -- Validate check
            cpPost = p.copy()
            bp = putBlueprint(cpPost)
            param = BlueprintHistoryUtil.get_blueprint_parameters(
                                                            code,
                                                            token,
                                                            bp['blueprint_id'],
                                                            bp['version'])
            form = environmentForm(bp)
            form.full_clean()
            if not form.is_valid():
                return render(request, Html.environmentCreate,
                              {'env': cpPost, 'clouds': clouds,
                               'systems': systems, 'blueprints': blueprints,
                               'form': form, 'message': '', 'create': True,
                               'save': True})

            EnvironmentUtil.create_environment(code, cpPost, request.session)

            return redirect(Path.environmentList)
    except Exception as ex:
        log.error(FuncCode.environmentCreate.value, None, ex)

        return render(request, Html.environmentCreate,
                      {'env': request.POST, 'clouds': clouds,
                       'systems': systems, 'blueprints': blueprints,
                       'form': '', 'message': str(ex), 'create': True,
                       'save': True})


def environmentEdit(request, id):
    code = FuncCode.environmentEdit.value
    env = None
    blueprints = None
    try:
        if not SessionUtil.check_login(request):
            return redirect(Path.logout)
        if not SessionUtil.check_permission(request, 'environment', 'update'):
            return render_to_response(Html.error_403)

        token = request.session['auth_token']
        project_id = request.session['project_id']
        env = EnvironmentUtil.get_environment_detail(code, token, id)
        env_template = BlueprintHistoryUtil.uniq_terraform_param(
                                        env['template_parameters'])
        env['template_parameters'] = env_template

        history = BlueprintHistoryUtil.get_blueprint_history_list_id(
            code, token, project_id, env.get('blueprint_history_id'))
        blueprints = BlueprintHistoryUtil.get_blueprint_parameters(
            code, token, history.get('blueprint_id'), history.get('version'))

        uniq_blueprints = BlueprintHistoryUtil.uniq_terraform_param(blueprints)

        if request.method == "GET":

            return render(request, Html.environmentEdit,
                          {'env': env,
                           'blueprints': uniq_blueprints,
                           'form': '',
                           'message': '',
                           'save': True})
        else:
            # -- Get a value from a for
            p = request.POST
            cpPost = p.copy()
            # -- Validate check
            form = edit_environmentForm(cpPost)
            if not form.is_valid():

                return render(request, Html.environmentEdit,
                              {'env': env,
                               'blueprints': uniq_blueprints,
                               'form': form,
                               'message': '',
                               'save': True})

            EnvironmentUtil.edit_environment(code,
                                             id,
                                             cpPost,
                                             request.session,
                                             blueprints)

            return redirect(Path.environmentList)
    except Exception as ex:
        log.error(code, None, ex)

        return render(request, Html.environmentEdit,
                      {'env': env,
                       'blueprints': uniq_blueprints,
                       'form': form,
                       'message': str(ex),
                       'save': True})


def environmentRebuild(request, id):
    code = FuncCode.environmentRebuild.value
    env = None
    blueprints = None
    try:
        if not SessionUtil.check_login(request):
            return redirect(Path.logout)
        if not SessionUtil.check_permission(request, 'environment', 'update'):
            return render_to_response(Html.error_403)

        token = request.session['auth_token']
        project_id = request.session['project_id']
        env = EnvironmentUtil.get_environment_detail(code, token, id)
        env_template = BlueprintHistoryUtil.uniq_terraform_param(
                                        env['template_parameters'])
        env['template_parameters'] = env_template

        history = BlueprintHistoryUtil.get_blueprint_history_list_id(
            code, token, project_id, env.get('blueprint_history_id'))
        blueprints = BlueprintHistoryUtil.get_blueprint_parameters(
            code, token, history.get('blueprint_id'), history.get('version'))

        uniq_blueprints = BlueprintHistoryUtil.uniq_terraform_param(blueprints)

        if request.method == "GET":

            return render(request, Html.environmentRebuild,
                          {'env': env,
                           'blueprints': uniq_blueprints,
                           'form': '',
                           'message': '',
                           'save': True})
        else:
            # -- Get a value from a for
            p = request.POST
            cpPost = p.copy()
            # -- Validate check
            form = edit_environmentForm(cpPost)
            if not form.is_valid():

                return render(request, Html.environmentRebuild,
                              {'env': env,
                               'blueprints': uniq_blueprints,
                               'form': form,
                               'message': '',
                               'save': True})

            EnvironmentUtil.rebuild_environment(code,
                                                id,
                                                cpPost,
                                                request.session,
                                                blueprints)

            return redirect(Path.environmentList)
    except Exception as ex:
        log.error(code, None, ex)

        return render(request, Html.environmentRebuild,
                      {'env': env,
                       'blueprints': uniq_blueprints,
                       'message': str(ex),
                       'save': True})


def environmentDelete(request, id):
    code = FuncCode.environmentDelete.value
    env = None
    try:
        if not SessionUtil.check_login(request):
            return redirect(Path.logout)
        if not SessionUtil.check_permission(request, 'environment', 'destroy'):
            return render_to_response(Html.error_403)

        token = request.session['auth_token']

        env = EnvironmentUtil.get_environment_detail(code, token, id)

        # -- URL and data set
        EnvironmentUtil.delete_system(code, token, id)

        return redirect(Path.environmentList)
    except Exception as ex:
        log.error(code, None, ex)

        return render(request, Html.environmentDetail,
                      {'env': env, 'message': ex})


def createForm(js, keyParent):
    ''' json to HTML input field '''

    PATRITION = '/'
    inpt = []

    if isinstance(js, dict):
        for k in js.keys():
            v = js[k]
            kk = keyParent + PATRITION + k
            if keyParent == '':
                kk = k
            inpt.extend(createForm(v, kk))
    else:
        inpt.append((keyParent, js))

    return inpt


def environmentAjaxBlueprint(request):
    try:
        p = request.GET
        bp = putBlueprint(p.copy())

        code = FuncCode.environmentCreate.value
        token = request.session['auth_token']
        param = BlueprintHistoryUtil.get_blueprint_parameters(
            code, token, bp['blueprint_id'], bp['version'])
        param = BlueprintHistoryUtil.uniq_terraform_param(param)
        key = param.keys()

        return render(request, Html.environmentAjaxBlueprint,
                      {'name': key, 'blueprints': param})

    except Exception as ex:
        log.error(code, None, ex)

        return render(request, Html.environmentAjaxBlueprint, {})


def putBlueprint(param):
    blueprint = param.get('blueprint', None)
    if blueprint is not None and blueprint != '':
        blueprint = ast.literal_eval(blueprint)

        param['blueprint_id'] = blueprint.get('id')
        param['version'] = blueprint.get('version')

    return param
