# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect, render_to_response
from ..forms import baseImageForm
from ..enum.FunctionCode import FuncCode
from ..enum.OSVersion import OSVersion
from ..utils import ApiUtil
from ..utils.PathUtil import Path
from ..utils.PathUtil import Html
from ..utils.ApiUtil import Url
from ..utils import SessionUtil
from ..utils import BaseimageUtil
from ..logs import log


# Create your views here.
def baseImageDetail(request, id):
    code = FuncCode.baseImageDetail.value
    baseimage = None
    try:
        if not SessionUtil.check_login(request):
            return redirect(Path.logout)
        if not SessionUtil.check_permission(request, 'base_image', 'read'):
            return render_to_response(Html.error_403)
        token = request.session.get('auth_token')
        # -- baseImage DetailAPI call, get a response
        baseimage = BaseimageUtil.get_baseimage_detail(code, token, id)

        return render(request, Html.baseImageDetail,
                      {'baseImage': baseimage, 'message': ''})
    except Exception as ex:
        log.error(FuncCode.baseImageDetail.value, None, ex)

        return render(request, Html.baseImageDetail,
                      {'baseImage': baseimage, 'message': str(ex)})


def baseImageCreate(request, cid):
    code = FuncCode.baseImageCreate.value
    osversion = list(OSVersion)
    try:
        if not SessionUtil.check_login(request):
            return redirect(Path.logout)
        if not SessionUtil.check_permission(request, 'base_image', 'create'):
            return render_to_response(Html.error_403)

        token = request.session.get('auth_token')
        if request.method == "GET":

            p = {
                'cloud_id': cid,
            }
            return render(request, Html.baseImageCreate,
                          {'baseImage': p, 'osversion': osversion,
                           'form': '', 'message': '', 'save': True})
        else:
            # -- Get a value from a form
            p = request.POST
            # -- Validate check
            form = baseImageForm(p)
            if not form.is_valid():
                cpPost = p.copy()

                return render(request, Html.baseImageCreate,
                              {'baseImage': cpPost, 'osversion': osversion,
                               'form': form, 'message': '', 'save': True})

            # -- Create a project, api call
            BaseimageUtil.create_baseimage(code, token, form.data)

            return redirect(Path.cloudDetail(cid))
    except Exception as ex:
        log.error(FuncCode.baseImageCreate.value, None, ex)

        return render(request, Html.baseImageCreate,
                      {'baseImage': request.POST, 'osversion': osversion,
                       'form': '', "message": str(ex), 'save': True})


def baseImageEdit(request, id):
    osversion = list(OSVersion)
    baseimage = None
    try:
        if not SessionUtil.check_login(request):
            return redirect(Path.logout)
        if not SessionUtil.check_permission(request, 'base_image', 'update'):
            return render_to_response(Html.error_403)

        code = FuncCode.baseImageEdit.value
        token = request.session.get('auth_token')

        if request.method == "GET":
            baseimage = BaseimageUtil.get_baseimage_detail(code, token, id)

            return render(request, Html.baseImageEdit,
                          {'baseImage': baseimage, 'osversion': osversion,
                           'form': '', 'message': '', 'save': True})
        else:
            # -- Get a value from a form
            p = request.POST
            # -- Validate check
            form = baseImageForm(request.POST)
            if not form.is_valid():

                return render(request, Html.baseImageEdit,
                              {'baseImage': p, 'osversion': osversion,
                               'form': form, 'message': '', 'save': True})

            # -- URL set
            url = Url.baseImageEdit(id, Url.url)
            # -- Set the value to the form
            data = {
                'auth_token': request.session['auth_token'],
                'cloud_id': p['cloud_id'],
                'source_image': p['source_image'],
                'ssh_username': p['ssh_username'],
                'os_version': p['os_version']
            }
            # -- API call, get a response
            ApiUtil.requestPut(url, FuncCode.baseImageEdit.value, data)

            return redirect(Path.cloudDetail(p['cloud_id']))
    except Exception as ex:
        log.error(FuncCode.baseImageEdit.value, None, ex)

        return render(request, Html.baseImageEdit,
                      {'baseImage': request.POST, 'osversion': osversion,
                       'form': '', 'message': ex, 'save': True})


def baseImageDelete(request, id):
    code = FuncCode.baseImageDelete.value
    baseimage = None
    cloud_id = None
    try:
        if not SessionUtil.check_login(request):
            return redirect(Path.logout)
        if not SessionUtil.check_permission(request, 'base_image', 'destroy'):
            return render_to_response(Html.error_403)

        token = request.session.get('auth_token')
        # -- Get a baseImage, api call
        baseimage = BaseimageUtil.get_baseimage_detail(code, token, id)
        cloud_id = baseimage.get('cloud_id')

        # -- Delete a baseImage, api call
        BaseimageUtil.delete_baseimage(code, token, id)

        return redirect(Path.cloudDetail(cloud_id))
    except Exception as ex:
        log.error(FuncCode.baseImageDelete.value, None, ex)

        return render(request, Html.baseImageDetail,
                      {'baseImage': baseimage, 'message': ex})
