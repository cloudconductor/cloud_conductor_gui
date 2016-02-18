# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from ..forms import cloudForm
from ..forms import baseImageForm
from ..utils import CloudUtil
from ..utils import StringUtil
from ..utils.PathUtil import Path
from ..utils.PathUtil import Html
from ..enum.CloudType import CloudType
from ..enum.OSVersion import OSVersion
from ..enum.FunctionCode import FuncCode
from ..logs import log


def cloudCreate(request):
    try:
        if request.method == "GET":
            param = {
                'auth_token': request.session['auth_token'],
                'project_id': request.session['project_id'],
            }

            cloud = request.session.get('w_cl_select')
            if StringUtil.isNotEmpty(cloud):
                param.update(cloud)

            return render(request, Html.cloudregist_cloudCreate,
                          {"cloud": param, 'cloudType': list(CloudType),
                           'message': '', 'create': True})
        elif request.method == "POST":
            param = request.POST

            # -- Validate check
            form = cloudForm(param)
            if not form.is_valid():
                cloud = param.copy()

                return render(request, Html.cloudregist_cloudCreate,
                              {"cloud": cloud, 'cloudType': list(CloudType),
                               'form': form, 'create': True})

            # -- Session add
            cloud = cloudPut(param)
            request.session['w_cl_select'] = cloud

            return redirect(Path.cloudregist_baseimageCreate)
    except Exception as ex:
        log.error(FuncCode.cloudReg_cloud.value, None, ex)

        return render(request, Html.cloudregist_cloudCreate,
                      {"cloud": request.POST, 'cloudType': list(CloudType),
                       'message': str(ex), 'create': True})


def baseimageCreate(request):
    try:
        if request.method == "GET":
            param = {
                'auth_token': request.session['auth_token']
            }

            baseimage = request.session.get('w_bi_create')
            if StringUtil.isNotEmpty(baseimage):
                param.update(baseimage)

            return render(request, Html.cloudregist_baseimageCreate,
                          {"baseImage": param, 'osversion': list(OSVersion),
                           'message': ''})
        elif request.method == "POST":
            param = request.POST

            # -- Validate check
            form = baseImageForm(param)
            if not form.is_valid():
                baseimage = param.copy()

                return render(request, Html.cloudregist_baseimageCreate,
                              {"baseImage": baseimage,
                               'osversion': list(OSVersion), 'form': form})

            baseimage = baseimagePut(request.POST)
            request.session['w_bi_create'] = baseimage

            return redirect(Path.cloudregist_confirm)
    except Exception as ex:
        log.error(FuncCode.cloudReg_baseimage.value, None, ex)

        return render(request, Html.cloudregist_baseimageCreate, {
            "baseimage": request.POST, 'message': str(ex),
            'wizard': True})


def confirm(request):
    cl_session = ''
    bi_session = ''
    try:
        session = request.session
        cl_session = session.get('w_cl_select')
        bi_session = session.get('w_bi_create')

        if request.method == "GET":

            return render(request, Html.cloudregist_confirm,
                          {'cloud': cl_session, 'baseImage': bi_session,
                           'message': ''})
        elif request.method == "POST":
            session = request.session
            code = FuncCode.cloudReg_confirm.value
            token = session.get('auth_token')
            project_id = request.session.get('project_id')

            # -- cloud Create
            cloud = CloudUtil.create_cloud2(code, token,
                                            project_id, cl_session)

            # -- baseimage Create
            bi_session['cloud_id'] = cloud.get('id')

            # -- session delete
            sessionDelete(session)

            return redirect(Path.cloudList)
    except Exception as ex:
        log.error(FuncCode.patternList.value, None, ex)
        session = request.session

        return render(request, Html.cloudregist_confirm,
                      {'cloud': cl_session, 'baseImage': bi_session,
                       'message': str(ex)})


def projectPut(req):
    if StringUtil.isEmpty(req):
        return None

    project = {
        'name': req.get('name'),
        'description': req.get('description'),
    }
    return project


def cloudPut(req):
    if StringUtil.isEmpty(req):
        return None

    cloud = {
        'name': req.get('name'),
        'type': req.get('type'),
        'key': req.get('key'),
        'secret': req.get('secret'),
        'entry_point': req.get('entry_point'),
        'description': req.get('description'),
        'tenant_name': req.get('tenant_name'),
    }
    return cloud


def baseimagePut(req):
    if StringUtil.isEmpty(req):
        return None

    baseimage = {
        'os_version': req.get('os_version'),
        'source_image': req.get('source_image'),
        'ssh_username': req.get('ssh_username'),
    }
    return baseimage


def sessionDelete(session):
    if 'w_cl_select' in session:
        del session['w_cl_select']

    if 'w_bi_create' in session:
        del session['w_bi_create']
