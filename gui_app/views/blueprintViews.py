# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect, render_to_response
from ..forms import blueprintForm
from ..utils import PatternUtil
from ..utils import BlueprintUtil
from ..utils import BlueprintPatternUtil
from ..utils import BlueprintHistoryUtil
from ..utils import SessionUtil
from ..utils.PathUtil import Path
from ..utils.PathUtil import Html
from ..enum.FunctionCode import FuncCode
from ..enum.OSVersion import OSVersion
from ..enum.MessageCode import Error
from ..logs import log


def blueprintList(request):
    blueprints = None
    try:
        if not SessionUtil.check_login(request):
            return redirect(Path.logout)
        if not SessionUtil.check_permission(request, 'blueprint', 'list'):
            return render_to_response(Html.error_403)

        # -- Get a blueprint list, API call
        project_id = request.session['project_id']
        token = request.session['auth_token']
        blueprints = BlueprintUtil.get_blueprint_list(
            FuncCode.blueprintList.value, token, project_id)

        return render(request, Html.blueprintList,
                      {'blueprints': blueprints, 'message': ''})
    except Exception as ex:
        log.error(FuncCode.blueprintList.value, None, ex)

        return render(request, Html.blueprintList,
                      {"blueprints": '', 'message': str(ex)})


def blueprintDetail(request, id):
    code = FuncCode.blueprintDetail.value
    blueprint = None
    history_list = None
    pattern = None
    try:
        if not SessionUtil.check_login(request):
            return redirect(Path.logout)
        if not SessionUtil.check_permission(request, 'blueprint', 'read'):
            return render_to_response(Html.error_403)

        token = request.session['auth_token']
        project_id = request.session['project_id']

        # -- blueprint DetailAPI call, get a response
        blueprint = BlueprintUtil.get_blueprint_detail(code, token, id)
        history_list = BlueprintHistoryUtil.get_blueprint_history_list(
            code, token, id)
        pattern = BlueprintUtil.get_pattern_list(code, id, token, project_id)

        return render(request, Html.blueprintDetail,
                      {'blueprint': blueprint, 'history_list': history_list,
                       'pattern': pattern, 'message': ''})
    except Exception as ex:
        log.error(FuncCode.blueprintDetail.value, None, ex)

        return render(request, Html.blueprintDetail,
                      {'blueprint': blueprint, 'pattern': pattern,
                       'history_list': history_list, 'message': str(ex)})


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

            return render(request, Html.blueprintCreate,
                          {'blueprint': '', 'patterns': patterns,
                           'osversion': osversion, 'form': '', 'message': ''})
        else:
            # -- Get a value from a form
            p = request.POST
            my_pattern = BlueprintPatternUtil.dic_pattern_list(
                p.getlist('os_version'), p.getlist('pattern_id'))
            # -- Validate check
            form = blueprintForm(p)
            if not form.is_valid():

                return render(request, Html.blueprintCreate,
                              {'blueprint': p, 'patterns': patterns,
                               'my_pattern': my_pattern,
                               'osversion': osversion,
                               'form': form, 'message': ''})

            checkbox = False
            if request.POST.get('pattern_id'):
                checkbox = True

            if not checkbox:
                return render(request, Html.blueprintCreate,
                              {'blueprint': p, 'patterns': patterns,
                               'my_pattern': my_pattern,
                               'osversion': osversion, 'form': form,
                               'message': Error.PatternRequired.value})

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

            return redirect(Path.blueprintList)
    except Exception as ex:
        log.error(code, None, ex)

        return render(request, Html.blueprintCreate,
                      {'blueprint': request.POST, 'patterns': patterns,
                       'my_pattern': my_pattern, 'osversion': osversion,
                       'form': '', 'message': str(ex)})


def blueprintEdit(request, id):
    code = FuncCode.blueprintEdit.value
    osversion = list(OSVersion)
    blueprint = ''
    patterns = ''
    old_pattern = ''
    my_pattern = ''
    try:
        if not SessionUtil.check_login(request):
            return redirect(Path.logout)
        if not SessionUtil.check_permission(request, 'blueprint', 'update'):
            return render_to_response(Html.error_403)

        project_id = request.session['project_id']
        token = request.session['auth_token']

        blueprint = BlueprintUtil.get_blueprint_detail(code, token, id)
        patterns = PatternUtil.get_pattern_list(code, token, project_id)

        if request.method == "GET":
            old_pattern = BlueprintPatternUtil.get_blueprint_pattern_list2(
                code, token, id)

            return render(request, Html.blueprintEdit,
                          {'blueprint': blueprint, 'patterns': patterns,
                           'my_pattern': old_pattern, 'osversion': osversion,
                           'form': '', 'message': ''})
        else:
            # -- Get a value from a form
            p = request.POST
            my_pattern = BlueprintPatternUtil.dic_pattern_list(
                p.getlist('os_version'), p.getlist('pattern_id'))

            # -- Validate check
            form = blueprintForm(p)
            form.full_clean()
            if not form.is_valid():

                return render(request, Html.blueprintEdit,
                              {'blueprint': p, 'patterns': patterns,
                               'my_pattern': my_pattern,
                               'osversion': osversion, 'form': form,
                               'message': ''})

            checkbox = False
            if request.POST.get('pattern_id'):
                checkbox = True

            if not checkbox:
                return render(request, Html.blueprintEdit,
                              {'blueprint': p, 'patterns': patterns,
                               'my_pattern': my_pattern,
                               'osversion': osversion, 'form': form,
                               'message': Error.PatternRequired.value})

            # -- 1.Edit a blueprint, api call
            blueprint = BlueprintUtil.edit_blueprint(
                code, token, id, form.data)

            # -- 2. Add a Pattern, api call

            # --     get newList
            new_set = set(p.getlist('pattern_id'))
            # --     get oldlist
            old_set = set(BlueprintPatternUtil.get_blueprint_pattern_list3(
                code, token, id))

            delete_list = old_set.difference(new_set)
            add_list = new_set.difference(old_set)

            BlueprintPatternUtil.add_blueprint_pattern_list(
                code, token, id, p.getlist('os_version'), add_list)

            # -- 3. Delete a Pattern, api call
            BlueprintPatternUtil.delete_blueprint_pattern_list(
                code, token, id, p.getlist('os_version'), delete_list)

            return redirect(Path.blueprintList)
    except Exception as ex:
        log.error(FuncCode.blueprintEdit.value, None, ex)

        return render(request, Html.blueprintEdit,
                      {'blueprint': request.POST, 'patterns': patterns,
                       'my_pattern': my_pattern, 'osversion': osversion,
                       'form': '', 'message': str(ex)})


def blueprintDelete(request, id):
    code = FuncCode.blueprintDelete.value
    blueprint = None
    pattern = None
    try:
        if not SessionUtil.check_login(request):
            return redirect(Path.logout)
        if not SessionUtil.check_permission(request, 'blueprint', 'destroy'):
            return render_to_response(Html.error_403)

        token = request.session['auth_token']
        project_id = request.session['project_id']

        # -- blueprint DetailAPI call, get a response
        blueprint = BlueprintUtil.get_blueprint_detail(code, token, id)
        pattern = BlueprintUtil.get_pattern_list(code, id, token, project_id)
        history_list = BlueprintHistoryUtil.get_blueprint_history_list(
            code, token, id)

        # -- URL and data set
        BlueprintUtil.delete_bluepritn_build(code, token, id)

        return redirect(Path.blueprintList)
    except Exception as ex:
        log.error(FuncCode.blueprintDelete.value, None, ex)

        return render(request, Html.blueprintDetail,
                      {'blueprint': blueprint, 'pattern': pattern,
                       'history_list': history_list, 'message': ex})


def blueprintBuild(request, id):
    code = FuncCode.blueprintBuild.value
    blueprint = None
    pattern = None
    history_list = None
    try:
        if not SessionUtil.check_login(request):
            return redirect(Path.logout)
        if not SessionUtil.check_permission(request, 'blueprint', 'create'):
            return render_to_response(Html.error_403)

        token = request.session['auth_token']
        project_id = request.session['project_id']

        # -- blueprint DetailAPI call, get a response
        blueprint = BlueprintUtil.get_blueprint_detail(code, token, id)
        pattern = BlueprintUtil.get_pattern_list(code, id, token, project_id)
        history_list = BlueprintHistoryUtil.get_blueprint_history_list(
            code, token, id)

        # -- URL and data set
        BlueprintUtil.create_bluepritn_build(code, token, id)

        return redirect(Path.blueprintDetail(id))
    except Exception as ex:
        log.error(FuncCode.blueprintDelete.value, None, ex)

        return render(request, Html.blueprintDetail,
                      {'blueprint': blueprint, 'pattern': pattern,
                       'history_list': history_list, 'message': ex})


def blueprintHistoryDetail(request, id, ver):
    code = FuncCode.blueprintHistoryDetail.value
    history = None
    try:
        if not SessionUtil.check_login(request):
            return redirect(Path.logout)
        if not SessionUtil.check_permission(request, 'blueprint_history',
                                                     'read'):
            return render_to_response(Html.error_403)

        token = request.session['auth_token']

        # -- blueprint DetailAPI call, get a response
        history = BlueprintHistoryUtil.get_blueprint_history_detail2(
            code, token, id, ver)

        return render(request, Html.blueprintHistoryDetail,
                      {'history': history, 'message': ''})
    except Exception as ex:
        log.error(FuncCode.blueprintDetail.value, None, ex)

        return render(request, Html.blueprintHistoryDetail,
                      {'history': history, 'message': str(ex)})
