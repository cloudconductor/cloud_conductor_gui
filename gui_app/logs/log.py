from logging import getLogger
import json
# logger = getLogger(__name__)
logger = getLogger('app')


def info(scid, res, parm, msg):
    if res is not None:
        response = str(res.status_code) + ':' + res.reason
        url = ', ' + res.url
        logger.info(response + ', ' + scid + ', ' + msg + url)
    elif parm is not None:
        logger.info(scid + ', ' + msg + parm)
    else:
        logger.info(scid + ', ' + msg)


def debug(scid, msg, res, param):
    if param is not None:
        logger.debug(scid + ' Message:' + msg + ' Response:' + res, param)
    else:
        logger.error(scid + ' Message:' + msg)


def error(scid, res, ex):

    if res is not None and ex is not None:
        response = str(res.status_code) + ':' + res.reason

        logger.error(response + ', ' + scid + ', ' + str(ex))
    if res is not None and ex is None:
        response = str(res.status_code) + ':' + res.reason

        logger.error(response + ', ' + scid)
    else:
        logger.error(scid + ', ' + str(ex))


def errorMessage(res, ex):

    if not res and not ex:
        errormsg = apiErrorMessage(res)

        return errormsg + str(ex)

    elif not res and ex:

        errormsg = apiErrorMessage(res)
        return errormsg

    else:
        return str(ex)


def apiErrorMessage(res):
    response = json.loads(res.text)
    apimsg = response.get('error')
    errormsg = str(res.status_code) + ':' + res.reason + '  ' + apimsg

    return errormsg
