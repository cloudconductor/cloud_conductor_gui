# -*- coding: utf-8 -*-
from django.shortcuts import redirect
from ..enum.FunctionCode import FuncCode
from ..utils.PathUtil import Path
from ..logs import log


def top(request):
    code = FuncCode.top.value
    log.info(code, None, None, '')
    return redirect(Path.environmentList)
