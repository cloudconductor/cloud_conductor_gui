import json
import requests
from ..logs import log
from django.conf import settings
from ..utils import StringUtil
from ..enum.ResponseType import Response
from ..enum.LogType import Message
from ..utils.ErrorUtil import ApiError


class Url():
    url = settings.CLOUDCONDUCTOR_URL
    token = url + 'tokens'

    projectList = url + 'projects'
    projectCreate = url + 'projects'

    def projectEdit(id, id2):
        return id2 + 'projects/{0}'.format(id)

    def projectDetail(id, id2):
        return id2 + 'projects/{0}'.format(id)

    def projectDelete(id, id2):
        return id2 + 'projects/{0}'.format(id)

    cloudList = url + 'clouds'
    cloudCreate = url + 'clouds'

    def cloudEdit(id, id2):
        return id2 + 'clouds/{0}'.format(id)

    def cloudDetail(id, id2):
        return id2 + 'clouds/{0}'.format(id)

    def cloudDelete(id, id2):
        return id2 + 'clouds/{0}'.format(id)

    baseImageList = url + 'base_images'
    baseImageCreate = url + 'base_images'

    def baseImageEdit(id, id2):
        return id2 + 'base_images/{0}'.format(id)

    def baseImageDetail(id, id2):
        return id2 + 'base_images/{0}'.format(id)

    def baseImageDelete(id, id2):
        return id2 + 'base_images/{0}'.format(id)

    systemList = url + 'systems'
    systemCreate = url + 'systems'

    def systemEdit(id, id2):
        return id2 + 'systems/{0}'.format(id)

    def systemDetail(id, id2):
        return id2 + 'systems/{0}'.format(id)

    def systemDelete(id, id2):
        return id2 + 'systems/{0}'.format(id)

    applicationList = url + 'applications'
    applicationCreate = url + 'applications'

    def applicationEdit(id, id2):
        return id2 + 'applications/{0}'.format(id)

    def applicationDetail(id, id2):
        return id2 + 'applications/{0}'.format(id)

    def applicationDelete(id, id2):
        return id2 + 'applications/{0}'.format(id)

    def applicationDeploy(id, id2):
        return id2 + 'applications/{0}/deploy'.format(id)

    def applicationHistoryList(id, id2):
        return id2 + 'applications/{0}/histories'.format(id)

    def applicationHistoryDetail(id, id2, id3):
        return id3 + 'applications/{0}/histories/{1}'.format(id, id2)

    def applicationHistoryCreate(id, id2):
        return id2 + 'applications/{0}/histories'.format(id)

    def applicationHistoryEdit(id, id2, id3):
        return id3 + 'applications/{0}/histories/{1}'.format(id, id2)

    def applicationHistoryDelete(id, id2, id3):
        return id3 + 'applications/{0}/histories/{1}'.format(id, id2)

    environmentList = url + 'environments'
    environmentCreate = url + 'environments'

    def environmentEdit(id, id2):
        return id2 + 'environments/{0}'.format(id)

    def environmentDetail(id, id2):
        return id2 + 'environments/{0}'.format(id)

    def environmentDelete(id, id2):
        return id2 + 'environments/{0}'.format(id)

    blueprintList = url + 'blueprints'
    blueprintCreate = url + 'blueprints'

    def blueprintEdit(id, id2):
        return id2 + 'blueprints/{0}'.format(id)

    def blueprintDetail(id, id2):
        return id2 + 'blueprints/{0}'.format(id)

    def blueprintDelete(id, id2):
        return id2 + 'blueprints/{0}'.format(id)

    def blueprintBuild(id, id2):
        return id2 + 'blueprints/{0}/build'.format(id)

    def blueprintPattrnList(id, id2):
        return id2 + 'blueprints/{0}/patterns'.format(id)

    def blueprintPattrnDetail(id, id2, id3):
        return id3 + 'blueprints/{0}/patterns/{1}'.format(id, id2)

    def blueprintPattrnCreate(id, id2):
        return id2 + 'blueprints/{0}/patterns'.format(id)

    def blueprintPattrnEdit(id, id2, id3):
        return id3 + 'blueprints/{0}/patterns/{1}'.format(id, id2)

    def blueprintPattrnDelete(id, id2, id3):
        return id3 + 'blueprints/{0}/patterns/{1}'.format(id, id2)

    def blueprintHistoriesList(id, id2):
        return id2 + 'blueprints/{0}/histories'.format(id)

    def blueprintHistoriesParameters(id, id2, id3):
        return id3 + 'blueprints/{0}/histories/{1}/parameters'.format(id, id2)

    def blueprintHistoriesDetail(id, id2, id3):
        return id3 + 'blueprints/{0}/histories/{1}'.format(id, id2)

    patternList = url + 'patterns'
    patternCreate = url + 'patterns/'

    def patternEdit(id, id2):
        return id2 + 'patterns/{0}'.format(id)

    def patternDetail(id, id2):
        return id2 + 'patterns/{0}'.format(id)

    def patternDelete(id, id2):
        return id2 + 'patterns/{0}'.format(id)

    accountList = url + 'accounts'
    accountCreate = url + 'accounts'

    def accountEdit(id, id2):
        return id2 + 'accounts/{0}'.format(id)

    def accountDetail(id, id2):
        return id2 + 'accounts/{0}'.format(id)

    def accountDelete(id, id2):
        return id2 + 'accounts/{0}'.format(id)

    roleList = url + 'roles'
    roleCreate = url + 'roles'

    def roleEdit(id, id2):
        return id2 + 'roles/{0}'.format(id)

    def roleDetail(id, id2):
        return id2 + 'roles/{0}'.format(id)

    def roleDelete(id, id2):
        return id2 + 'roles/{0}'.format(id)

    def permissionList(id, id2):
        return id2 + 'roles/{0}/permissions'.format(id)

    def permissionDetail(id, id2, id3):
        return id3 + 'roles/{0}/permissions/{1}'.format(id, id2)

    def permissionCreate(id, id2):
        return id2 + 'roles/{0}/permissions'.format(id)

    def permissionDelete(id, id2, id3):
        return id3 + 'roles/{0}/permissions/{1}'.format(id, id2)

    assignmentEdit = url + 'assignments'
    assignmentList = url + 'assignments'
    assignmentAdd = url + 'assignments'

    def assignmentDelete(id, id2):
        return id2 + 'assignments/{0}'.format(id)

    def assignmentRoleList(id, id2):
        return id2 + 'assignments/{0}/roles'.format(id)

    def assignmentRoleAdd(id, id2):
        return id2 + 'assignments/{0}/roles'.format(id)

    def assignmentRoleDelete(id, id2, id3):
        return id3 + 'assignments/{0}/roles/{1}'.format(id, id2)

    def assignmentRoleDetail(id, id2, id3):
        return id3 + 'assignments/{0}/roles/{1}'.format(id, id2)

    def assignmentRoleCreate(id, id2):
        return id2 + 'assignments/{0}/roles'.format(id)


def requestGet(url, scid, payload):
    log.info(scid, None, None, url)
    if payload is not None:
        r = requests.get(url, params=payload)
    else:
        r = requests.get(url)
    log.info(scid, r, None, Message.api_url.value)

    if r.status_code == Response.OK.value:
        log.info(scid, None, r.text, Message.api_response.value)
        param = json.loads(r.text)
        return param
    else:
        raise ApiError(log.errorMessage(r, None))


def requestPost(url, scid, payload):  # -- change post
    if payload is not None:
        r = requests.post(url, data=json.dumps(payload))
    else:
        r = requests.post(url)
    log.info(scid, r, None, Message.api_url.value)

    if r.status_code == Response.Created.value or \
       r.status_code == Response.Accepted.value:
        log.info(scid, None, r.text, Message.api_response.value)
        param = json.loads(r.text)
        return param
    else:
        raise ApiError(log.errorMessage(r, None))


def requestPut(url, scid, payload):  # -- change post
    if payload is not None:
        r = requests.put(url, data=json.dumps(payload))
    else:
        r = requests.put(url)
    log.info(scid, r, None, Message.api_url.value)

    if r.status_code == Response.OK.value:
        log.info(scid, None, r.text, Message.api_response.value)
        param = json.loads(r.text)
        return param
    else:
        raise ApiError(log.errorMessage(r, None))


def requestDelete(url, scid, payload):  # -- change post
    if payload is not None:
        r = requests.delete(url, data=payload)
    else:
        r = requests.delete(url)
    log.info(scid, r, None, Message.api_url.value)

    if r.status_code == Response.No_Content.value:
        json = r.text
        log.info(scid, None, json, Message.api_response.value)

        param = ''
        if StringUtil.isNotEmpty(json):
            param = json.loads(r.text)

        return param
    else:
        raise ApiError(log.errorMessage(r, None))
