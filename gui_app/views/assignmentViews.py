# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from ..utils import ApiUtil
from ..utils import AccountUtil
from ..utils import SessionUtil
from ..utils.PathUtil import Path
from ..utils.PathUtil import Html
from ..utils.ApiUtil import Url
from ..enum.FunctionCode import FuncCode
from ..enum.MessageCode import Error
from ..logs import log


def assignmentList(request):
    try:

        projects = None
        # -- Get a project list, API call
        url = Url.projectList
        data = {'auth_token': request.session['auth_token']}
        projects = ApiUtil.requestGet(url, FuncCode.projectList.value, data)

        return render(request, Html.projectList, {'projects': projects,
                                                  'message': ''})
    except Exception as ex:
        log.error(FuncCode.projectList.value, None, ex)

        return render(request, Html.projectList,
                      {"projects": '', 'message': str(ex)})


def assignmentAdd(request, id=None):
    code = FuncCode.projectDetail.value
    try:
        token = request.session['auth_token']
        if request.method == "GET":

            url = Url.accountList
            data = {
                'auth_token': token,
            }
            accounts = ApiUtil.requestGet(
                url, code, data)
            data = {
                'auth_token': token,
                'project_id': id,
            }
            accountsByProject = ApiUtil.requestGet(
                url, code, data)

            for account in accountsByProject:
                accounts.remove(account)

            if request.session.get('select_account'):
                for account in request.session['select_account']:
                    accounts.remove(account)

            return render(request, Html.assignmentAdd,
                          {'accounts': accounts, 'project_id': id,
                           'message': '', 'save': True})
        else:
            # -- Get a value from a form
            p = request.POST

            # -- Create a project, api call
            url = Url.assignmentAdd
            accounts = []
            for param in p:
                if 'chk-' in param:
                    account = AccountUtil.get_account_detail(
                        code, token, param.split('-')[1])
                    accounts.append(account)

            if request.session.get('select_account'):
                for account in request.session['select_account']:
                    accounts.append(account)
                    request.session['select_account'] = accounts
            else:
                request.session['select_account'] = accounts

            return redirect(Path.assignmentEdit(id))
    except Exception as ex:
        log.error(FuncCode.projectCreate.value, None, ex)

        return render(request, Html.assignmentAdd,
                      {'accounts': None, 'project_id': id,
                       "message": str(ex), 'save': True})


def assignmentEdit(request, id=None):
    code = FuncCode.projectEdit.value
    try:
        if not SessionUtil.check_login(request):
            return redirect('/ccgui/logout')

        token = request.session['auth_token']
        account_id = request.session['account_id']
        if request.method == "GET":

            url = Url.assignmentList
            data = {
                'auth_token': token,
                'project_id': id,
            }
            assignments = ApiUtil.requestGet(
                url, code, data)

            assignmentList = []
            for assignment in assignments:
                url = Url.roleList
                data = {
                    'auth_token': token,
                    'account_id': assignment["account_id"],
                    'project_id': id
                }
                roleList = ApiUtil.requestGet(
                    url, code, data)
                role = ""
                for item in roleList:
                    role = item["id"]

                url = Url.accountList
                data = {
                    'auth_token': token,
                }
                accountList = ApiUtil.requestGet(
                    url, code, data)
                accountName = ""
                email = ""
                admin = ""
                for item in accountList:
                    if item["id"] == assignment["account_id"]:
                        accountName = item["name"]
                        email = item["email"]
                        admin = item["admin"]
                        break

                assignmentList.append({
                    'id': assignment["id"],
                    'account_id': assignment["account_id"],
                    'name': accountName,
                    'email': email,
                    'admin': admin,
                    'role': role,
                })

            if request.session.get('select_account'):
                for account in request.session['select_account']:
                    assignmentList.append({
                        'id': "",
                        'account_id': account["id"],
                        'name': account["name"],
                        'email': account["email"],
                        'admin': account["admin"],
                        'role': "",
                    })

            url = Url.roleList
            data = {
                'auth_token': token,
                'project_id': id
            }
            roleList = ApiUtil.requestGet(
                url, code, data)

            return render(request, Html.assignmentEdit,
                          {'assignments': assignmentList, 'message': '',
                           'roleList': roleList, 'project_id': id,
                           'account_id': account_id, 'save': True})
        else:
            # -- Get a value from a form
            p = request.POST
            # -- Validate check

            url = Url.assignmentEdit
            data = {
                'auth_token': token,
                'project_id': id,
            }
            assignments = ApiUtil.requestGet(
                url, code, data)

            selected = True

            for assignment in assignments:
                if 'chk-' + str(assignment['id']) in p:
                    if p['sel-' + str(assignment['id'])] == '':
                        selected = False

            if not selected:

                assignmentList = []
                for assignment in assignments:
                    url = Url.roleList
                    data = {
                        'auth_token': token,
                        'account_id': assignment["account_id"],
                        'project_id': id
                    }
                    roleList = ApiUtil.requestGet(
                        url, code, data)
                    role = ""
                    for item in roleList:
                        role = item["id"]

                    url = Url.accountList
                    data = {
                        'auth_token': token,
                    }
                    accountList = ApiUtil.requestGet(
                        url, code, data)
                    accountName = ""
                    for item in accountList:
                        if item["id"] == assignment["account_id"]:
                            accountName = item["name"]
                            break

                    assignmentList.append({
                        'id': assignment["id"],
                        'account_id': assignment["account_id"],
                        'name': accountName,
                        'role': role,
                    })

                url = Url.roleList
                data = {
                    'auth_token': token,
                    'project_id': id
                }
                roleList = ApiUtil.requestGet(
                    url, code, data)

                return render(request, Html.assignmentEdit,
                              {'assignments': assignmentList,
                               'message': Error.CheckboxNotSelected.value,
                               'roleList': roleList, 'project_id': id,
                               'account_id': account_id, 'save': True})

            logout = False
            roleid = None

            for assignment in assignments:
                if 'chk-' + str(assignment['id']) in p:
                    if p['sel-' + str(assignment['id'])] != \
                       p['sel_old-' + str(assignment['id'])]:

                        if p['sel_old-' + str(assignment['id'])] == '':
                            url = Url.assignmentRoleAdd(
                                str(assignment['id']), Url.url)
                            data = {
                                'auth_token': token,
                                'role_id': p['sel-' + str(assignment['id'])],
                            }
                            ApiUtil.requestPost(
                                url, code, data)

                        else:

                            url = Url.assignmentRoleList(
                                str(assignment['id']), Url.url)
                            data = {
                                'auth_token': token,
                            }
                            assignmentRoleList = ApiUtil.requestGet(
                                url, code, data)

                            for assignmentRole in assignmentRoleList:
                                if p['sel_old-' + str(assignment['id'])] == \
                                   str(assignmentRole["role_id"]):
                                    url = Url.assignmentRoleDelete(
                                        str(assignment['id']),
                                        assignmentRole["id"], Url.url)
                                    data = {'auth_token': token}
                                    ApiUtil.requestDelete(
                                        url, code,
                                        {'auth_token': token})
                                    break

                            if p['sel-' + str(assignment['id'])] != '':
                                url = Url.assignmentRoleAdd(
                                    str(assignment['id']), Url.url)
                                data = {
                                    'auth_token': token,
                                    'role_id': p['sel-' +
                                                 str(assignment['id'])],
                                }
                                ApiUtil.requestPost(
                                    url, code, data)

                                if str(request.session["project_id"]) == id\
                                        and request.session["account_id"]\
                                        == assignment['account_id']:
                                    roleid = p['sel-' + str(assignment['id'])]

                else:
                    url = Url.assignmentDelete(assignment["id"], Url.url)
                    data = {
                        'auth_token': token,
                    }
                    ApiUtil.requestDelete(url, code, data)
                    if request.session["project_id"] == id and \
                            request.session["account_id"] == \
                            assignment['account_id']:
                        logout = True

            if request.session.get('select_account'):
                for account in request.session['select_account']:
                    if 'chk--' + str(account['id']) in p:
                        data = {
                            'auth_token': token,
                            'project_id': id,
                            'account_id': account["id"],
                        }
                        url = Url.assignmentAdd
                        assi = ApiUtil.requestPost(
                            url, code, data)

                        url = Url.assignmentRoleAdd(
                            str(assi['id']), Url.url)
                        data = {
                            'auth_token': token,
                            'role_id': p['sel--' + str(account['id'])],
                        }
                        ApiUtil.requestPost(
                            url, code, data)

                del request.session['select_account']

            # role session update
            if roleid:
                SessionUtil.edit_role_session(code, request.session, roleid)

            if logout:
                return redirect('/ccgui/logout')

            return redirect(Path.projectDetail(id))
    except Exception as ex:
        log.error(FuncCode.projectEdit.value, None, ex)
        if request.session.get('select_account'):
            del request.session['select_account']

        return render(request, Html.assignmentEdit, {'project': request.POST,
                                                     'project_id': id,
                                                     'message': str(ex),
                                                     'save': True})


def assignmentDelete(request, id):
    try:
        # -- URL and data set
        url = Url.projectDelete(id, Url.url)
        data = {'auth_token': request.session['auth_token']}
        ApiUtil.requestDelete(url, FuncCode.projectDelete.value, data)

        return redirect(Path.projectList)
    except Exception as ex:
        log.error(FuncCode.projectDelete.value, None, ex)

        return render(request, Html.projectDetail,
                      {'project': '', 'accounts': '', 'message': str(ex)})
