# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect, render_to_response
from ..forms import cloudForm
from ..forms import cloudForm2
from ..enum.CloudType import CloudType
from ..enum.FunctionCode import FuncCode
from ..utils import CloudUtil
from ..utils import BaseimageUtil
from ..utils import SessionUtil
from ..utils.PathUtil import Path
from ..utils.PathUtil import Html
from ..logs import log
clouds = None


# Create your views here.
def cloudList(request):
    try:

        if not SessionUtil.check_login(request):
            return redirect(Path.logout)
        if not SessionUtil.check_permission(request, 'cloud', 'list'):
            return render_to_response(Html.error_403)

        code = FuncCode.cloudList.value
        token = request.session['auth_token']
        project_id = request.session['project_id']
        # -- Get a cloud list, API call
        clouds = CloudUtil.get_cloud_list(code, token, project_id)

        return render(request, Html.cloudList,
                      {'cloud': clouds, 'message': ''})
    except Exception as ex:

        log.error(FuncCode.cloudList.value, None, ex)
        return render(request, Html.cloudList, {'cloud': '', 'message': ex})


def cloudDetail(request, id):
    cloud = None
    baseimages = None
    try:
        if not SessionUtil.check_login(request):
            return redirect(Path.logout)
        if not SessionUtil.check_permission(request, 'cloud', 'read'):
            return render_to_response(Html.error_403)

        code = FuncCode.cloudDetail.value
        token = request.session['auth_token']
        # -- Get a cloud list, API call
        cloud = CloudUtil.get_cloud_detail(code, token, id)

        # -- Get a baseImage list, API call
        baseimages = BaseimageUtil.get_baseimege_list(code, token, id)
        return render(request, Html.cloudDetail,
                      {'cloud': cloud, 'baseImage': baseimages,
                       'message': ''})
    except Exception as ex:

        log.error(FuncCode.cloudList.value, None, ex)
        return render(request, Html.cloudDetail,
                      {'cloud': cloud, 'baseImage': baseimages, 'message': ex})


def cloudCreate(request):
    cloudType = None
    try:
        if not SessionUtil.check_login(request):
            return redirect(Path.logout)
        if not SessionUtil.check_permission(request, 'cloud', 'create'):
            return render_to_response(Html.error_403)

        cloudType = list(CloudType)

        token = request.session['auth_token']
        code = FuncCode.cloudList.value
        project_id = request.session['project_id']

        if request.method == "GET":

            return render(request, Html.cloudCreate,
                          {'cloud': '', 'form': '', 'message': '',
                           'cloudType': cloudType, 'save': True,
                           'create': True})

        else:
            # -- Get a value from a form
            p = request.POST
            # -- Validate check
            form = cloudForm(p)
            form.full_clean()
            if not form.is_valid():

                return render(request, Html.cloudCreate,
                              {'cloud': p, 'form': form, 'message': '',
                               'cloudType': cloudType, 'save': True,
                               'create': True})
            # -- Create a cloud, api call
            CloudUtil.create_cloud2(code, token, project_id, form.data.copy())

            return redirect(Path.cloudList)

    except Exception as ex:
        log.error(FuncCode.cloudList.value, None, ex)

        return render(request, Html.cloudCreate,
                      {'cloud': request.POST, 'form': '', 'message': ex,
                       'cloudType': cloudType, 'save': True, 'create': True})


def cloudEdit(request, id):
    cloudType = list(CloudType)
    code = FuncCode.cloudEdit.value
    cloud = ''
    p = ''
    try:
        if not SessionUtil.check_login(request):
            return redirect(Path.logout)
        if not SessionUtil.check_permission(request, 'cloud', 'update'):
            return render_to_response(Html.error_403)

        token = request.session['auth_token']

        if request.method == "GET":
            cloud = CloudUtil.get_cloud_detail(code, token, id)

            return render(request, Html.cloudEdit,
                          {'cloud': cloud, 'form': '', 'message': '',
                           'cloudType': cloudType, 'save': True})
        elif request.method == "POST":
            # -- Get a value from a form
            p = request.POST
            # -- Validate check
            form = cloudForm2(request.POST)
            form.full_clean()
            if not form.is_valid():

                return render(request, Html.cloudEdit,
                              {'cloud': p, 'form': form, 'message': '',
                               'cloudType': cloudType, 'save': True})

            # -- API call, get a response
            cloud = CloudUtil.edit_cloud(code, token, id, form.data.copy())

            return redirect(Path.cloudList)
    except Exception as ex:
        log.error(code, None, ex)

        return render(request, Html.cloudEdit,
                      {'cloud': p, 'form': '', 'message': ex,
                       'cloudType': cloudType, 'save': True})


def cloudDelete(request, id):
    code = FuncCode.projectDelete.value
    cloud = None
    baseimages = None
    try:
        if not SessionUtil.check_login(request):
            return redirect(Path.logout)
        if not SessionUtil.check_permission(request, 'cloud', 'destroy'):
            return render_to_response(Html.error_403)

        token = request.session['auth_token']
        cloud = CloudUtil.get_cloud_detail(code, token, id)

        # -- Get a cloud list, API call
        cloud = CloudUtil.get_cloud_detail(code, token, id)
        # -- Get a baseImage list, API call
        baseimages = BaseimageUtil.get_baseimege_list(code, token, id)

        # -- URL and data set
        CloudUtil.delete_cloud(code, token, id)

        return redirect(Path.cloudList)
    except Exception as ex:
        log.error(FuncCode.cloudDelete.value, None, ex)

        return render(request, Html.cloudDetail,
                      {'cloud': cloud, 'baseImage': baseimages, 'message': ex})
