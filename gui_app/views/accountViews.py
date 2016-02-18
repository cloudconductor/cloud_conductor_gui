# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect, render_to_response
from ..forms import accountForm
from ..utils import AccountUtil
from ..utils import ApiUtil
from ..utils import SessionUtil
from ..utils.PathUtil import Path
from ..utils.PathUtil import Html
from ..utils.ApiUtil import Url
from ..enum.FunctionCode import FuncCode
from ..logs import log


def accountList(request):
    try:
        if not SessionUtil.check_login(request):
            return redirect(Path.logout)
        if not SessionUtil.check_permission(request, 'account', 'list'):
            return render_to_response(Html.error_403)

        code = FuncCode.accountList.value
        token = request.session.get('auth_token')

        # -- Get a  list, API call
        accounts = AccountUtil.get_account_list(code, token)

        return render(request, Html.accountList,
                      {'accounts': accounts, 'message': ''})

    except Exception as ex:
        log.error(FuncCode.accountList.value, None, ex)

        return render(request, Html.accountList,
                      {"accounts": '', 'message': str(ex)})


def accountDetail(request, id):
    account = None
    try:
        if not SessionUtil.check_login(request):
            return redirect(Path.logout)
        if not SessionUtil.check_permission(request, 'account', 'read'):
            return render_to_response(Html.error_403)

        # -- account DetailAPI call, get a response
        token = request.session['auth_token']
        code = FuncCode.accountDetail.value

        account = AccountUtil.get_account_detail(code, token, id)

        return render(request, Html.accountDetail,
                      {'account': account, 'message': ''})

    except Exception as ex:
        log.error(FuncCode.accountDetail.value, None, ex)

        return render(request, Html.accountDetail,
                      {'account': account, 'message': str(ex)})


def accountCreate(request):
    try:
        if not SessionUtil.check_login(request):
            return redirect(Path.logout)
        if not SessionUtil.check_permission(request, 'account', 'create'):
            return render_to_response(Html.error_403)

        token = request.session['auth_token']
        code = FuncCode.accountCreate.value

        if request.method == "GET":
            return render(request, Html.accountCreate,
                          {'account': '', 'form': '', 'message': ''})
        else:
            # -- Get a value from a form
            p = request.POST
            # -- Validate check
            form = accountForm(request.POST)
            form.full_clean()
            if not form.is_valid():
                return render(request, Html.accountCreate,
                              {'account': p, 'form': form, 'message': ''})

            # -- AccountCreateAPI call, get a response
            AccountUtil.get_account_create(code, token, p['name'], p['email'],
                                           p['password'], p['repassword'],
                                           p['admin'])

            return redirect(Path.accountList)

    except Exception as ex:
        log.error(FuncCode.accountCreate.value, None, ex)

        return render(request, Html.accountCreate,
                      {'account': request.POST, 'form': '',
                       'message': str(ex)})


def accountEdit(request, id):
    try:
        if not SessionUtil.check_login(request):
            return redirect(Path.logout)

        if not SessionUtil.check_permission(request, 'account', 'update', id):
            return render_to_response(Html.error_403)

        if request.method == "GET":
            token = request.session['auth_token']
            url = Url.accountDetail(id, Url.url)
            data = {
                'auth_token': token
            }
            p = ApiUtil.requestGet(url, FuncCode.accountEdit.value, data)
            p.update(data)

            return render(request, Html.accountEdit,
                          {'account': p, 'message': '', 'edit': True})

        else:
            # -- Get a value from a form
            p = request.POST
            # -- Validate check
            form = accountForm(request.POST)
            form.full_clean()
            if not form.is_valid():

                return render(request, Html.accountEdit,
                              {'account': p, 'form': form,
                               'message': '', 'edit': True})

            # -- URL set
            url = Url.accountEdit(id, Url.url)
            # -- Set the value to the form
            data = {
                'auth_token': request.session['auth_token'],
                'name': p['name'],
                'email': p['email'],
                'password': p['password'],
                'repassword': p['repassword'],
                'admin': p['admin'],
            }
            # -- API call, get a response
            ApiUtil.requestPut(url, FuncCode.accountEdit.value, data)

            return redirect(Path.accountList)
    except Exception as ex:
        log.error(FuncCode.accountEdit.value, None, ex)

        return render(request, Html.accountEdit,
                      {'account': request.POST, 'form': '',
                       'message': str(ex), 'edit': True})


def accountDelete(request, id):
    account = None
    code = FuncCode.accountDetail.value
    try:
        if not SessionUtil.check_login(request):
            return redirect(Path.logout)
        if not SessionUtil.check_permission(request, 'account', 'destroy'):
            return render_to_response(Html.error_403)

        token = request.session['auth_token']

        account = AccountUtil.get_account_detail(code, token, id)

        # -- accounDelte
        AccountUtil.delete_account(code, token, id)

        return redirect(Path.accountList)
    except Exception as ex:
        log.error(FuncCode.accountDetail.value, None, ex)

        return render(request, Html.accountDetail,
                      {'account': account, 'message': str(ex)})
