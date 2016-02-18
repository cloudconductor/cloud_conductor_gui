
class Path():
    top = "/ccgui/"
    logout = "/ccgui/logout"
    projectList = "/ccgui/project/list/"
    projectCreate = "/ccgui/project/create/"

    def projectDetail(id):
        return "/ccgui/project/{0}/detail".format(id)

    def projectEdit(id):
        return "/ccgui/project/{0}/edit".format(id)

    def assignmentEdit(id):
        return "/ccgui/assignment/{0}/edit".format(id)

    def assignmentAdd(id):
        return "/ccgui/assignment/{0}/add".format(id)

    cloudList = "/ccgui/cloud/list/"
    cloudCreate = "/ccgui/cloud/create/"

    def cloudDetail(id):
        return "/ccgui/cloud/{0}/detail".format(id)

    def cloudEdit(id):
        return "/ccgui/cloud/{0}/edit".format(id)

    baseImageList = "/ccgui/baseImage/list/"
    baseImageCreate = "/ccgui/baseImage/create/"

    def baseImageDetail(id):
        return "/baseImage/project/{0}/".format(id)

    def baseImageEdit(id):
        return "/ccgui/baseImage/{0}/edit".format(id)

    systemList = "/ccgui/system/list/"
    systemCreate = "/ccgui/system/create/"

    def systemDetail(id):
        return "/ccgui/system/{0}/detail".format(id)

    def systemEdit(id):
        return "/ccgui/system/{0}/edit".format(id)

    environmentList = "/ccgui/environment/list/"
    environmentCreate = "/ccgui/environment/create/"

    def environmentDetail(id):
        return "/ccgui/environment/{0}/detail".format(id)

    def environmentEdit(id):
        return "/ccgui/environment/{0}/edit".format(id)

    applicationList = "/ccgui/application/list/"
    applicationCreate = "/ccgui/application/create/"

    def applicationDetail(id):
        return "/ccgui/application/{0}/detail".format(id)

    def applicationEdit(id):
        return "/ccgui/application/{0}/edit".format(id)

    def applicationHistoryDetail(id, his_id):
        return "/ccgui/application/{0}/history/{1}/detail".format(id, his_id)

    def applicationHistoryEdit(id, his_id):
        return "/ccgui/application/{0}/history/{1}/edit".format(id, his_id)

    blueprintList = "/ccgui/blueprint/list/"
    blueprintCreate = "/ccgui/blueprint/create/"

    def blueprintDetail(id):
        return "/ccgui/blueprint/{0}/detail".format(id)

    def blueprintEdit(id):
        return "/ccgui/blueprint/{0}/edit".format(id)

    def blueprintBuild(id):
        return "/ccgui/blueprint/{0}/build".format(id)

    def blueprintHistoryDetail(id, hid):
        return "/ccgui/blueprint/{0}/history/{1}/detail".format(id, hid)

    patternList = "/ccgui/pattern/list/"
    patternCreate = "/ccgui/pattern/create/"

    def patternDetail(id):
        return "/ccgui/pattern/{0}/detail".format(id)

    def patternEdit(id):
        return "/ccgui/pattern/{0}/edit".format(id)

    accountList = "/ccgui/account/list/"
    accountCreate = "/ccgui/account/create/"

    def accountDetail(id):
        return "/account/project/{0}/".format(id)

    def accountEdit(id):
        return "/ccgui/account/{0}/edit".format(id)

    roleList = "/ccgui/role/list/"
    roleCreate = "/ccgui/role/create/"

    def roleDetail(id):
        return "/role/project/{0}/".format(id)

    def roleEdit(id):
        return "/ccgui/role/{0}/edit".format(id)

    cloudregist_projectCreate = "/ccgui/cloudregist/project/create/"
    cloudregist_projectSelect = "/ccgui/cloudregist/project/select/"
    cloudregist_cloudCreate = "/ccgui/cloudregist/cloud/create/"
    cloudregist_baseimageCreate = "/ccgui/cloudregist/baseimage/create/"
    cloudregist_confirm = "/ccgui/cloudregist/confirm/"

    newapp_systemSelect = "/ccgui/newapp/system/select/"
    newapp_systemCreate = "/ccgui/newapp/system/create/"
    newapp_applicationCreate = "/ccgui/newapp/application/create/"
    newapp_environmentSelect = "/ccgui/newapp/environment/select/"
    newapp_environmentCreate = "/ccgui/newapp/environment/create/"
    newapp_confirm = "/ccgui/newapp/confirm/"

    envapp_systemSelect = "/ccgui/envapp/system/select/"
    envapp_systemCreate = "/ccgui/envapp/system/create/"
    envapp_bluprintSelect = "/ccgui/envapp/blueprint/select/"
    envapp_blueprintCreate = "/ccgui/envapp/blueprint/create/"
    envapp_environmentCreate = "/ccgui/envapp/environment/create/"
    envapp_confirm = "/ccgui/envapp/confirm/"

    appdeploy_applicationSelect = "/ccgui/appdeploy/application/select/"
    appdeploy_applicationCreate = "/ccgui/appdeploy/application/create/"
    appdeploy_environmentSelect = "/ccgui/appdeploy/environment/select/"
    appdeploy_confirm = "/ccgui/appdeploy/confirm/"


class Html():
    login = 'gui_app/login.html'
    top = "/ccgui/"

    error_403 = "403.html"

    projectList = "gui_app/project/projectList.html"
    projectCreate = "gui_app/project/projectCreate.html"
    projectDetail = "gui_app/project/projectDetail.html"
    projectEdit = "gui_app/project/projectEdit.html"
    projectDelete = "gui_app/project/projectDetail.html"
    addUser = "gui_app/project/projectAddUser.html"

    assignmentEdit = "gui_app/assignment/assignmentEdit.html"
    assignmentAdd = "gui_app/assignment/assignmentAdd.html"

    cloudList = "gui_app/cloud/cloudList.html"
    cloudDetail = "gui_app/cloud/cloudDetail.html"
    cloudCreate = "gui_app/cloud/cloudCreate.html"
    cloudEdit = "gui_app/cloud/cloudEdit.html"

    baseImageList = "gui_app/baseImage/baseImageList.html"
    baseImageDetail = "gui_app/baseImage/baseImageDetail.html"
    baseImageCreate = "gui_app/baseImage/baseImageCreate.html"
    baseImageEdit = "gui_app/baseImage/baseImageEdit.html"

    systemList = "gui_app/system/systemList.html"
    systemDetail = "gui_app/system/systemDetail.html"
    systemCreate = "gui_app/system/systemCreate.html"
    systemEdit = "gui_app/system/systemEdit.html"

    environmentList = "gui_app/environment/environmentList.html"
    environmentDetail = "gui_app/environment/environmentDetail.html"
    environmentCreate = "gui_app/environment/environmentCreate.html"
    environmentEdit = "gui_app/environment/environmentEdit.html"
    environmentAjaxBlueprint = "gui_app/environment/" + \
                               "environmentAjaxBlueprint.html"

    applicationList = "gui_app/application/applicationList.html"
    applicationDetail = "gui_app/application/applicationDetail.html"
    applicationHistoryCreate = "gui_app/" + \
                               "application/applicationHistoryCreate.html"
    applicationHistoryDetail = "gui_app/" + \
                               "application/applicationHistoryDetail.html"
    applicationHistoryEdit = "gui_app/" + \
                             "application/applicationHistoryEdit.html"
    applicationCreate = "gui_app/application/applicationCreate.html"
    applicationEdit = "gui_app/application/applicationEdit.html"

    blueprintList = "gui_app/blueprint/blueprintList.html"
    blueprintDetail = "gui_app/blueprint/blueprintDetail.html"
    blueprintCreate = "gui_app/blueprint/blueprintCreate.html"
    blueprintEdit = "gui_app/blueprint/blueprintEdit.html"

    blueprintHistoryDetail = "gui_app/blueprint/blueprintHistoryDetail.html"

    patternList = "gui_app/pattern/patternList.html"
    patternDetail = "gui_app/pattern/patternDetail.html"
    patternCreate = "gui_app/pattern/patternCreate.html"
    patternEdit = "gui_app/pattern/patternEdit.html"

    accountList = "gui_app/account/accountList.html"
    accountCreate = "gui_app/account/accountCreate.html"
    accountDetail = "gui_app/account/accountDetail.html"
    accountEdit = "gui_app/account/accountEdit.html"

    roleList = "gui_app/role/roleList.html"
    roleCreate = "gui_app/role/roleCreate.html"
    roleDetail = "gui_app/role/roleDetail.html"
    roleEdit = "gui_app/role/roleEdit.html"

    cloudregist_projectCreate = \
        "gui_app/cloudRegistration/projectCreate.html"
    cloudregist_projectSelect = \
        "gui_app/cloudRegistration/projectSelect.html"
    cloudregist_cloudCreate = "gui_app/cloudRegistration/cloudCreate.html"
    cloudregist_baseimageCreate = \
        "gui_app/cloudRegistration/baseImageCreate.html"
    cloudregist_confirm = "gui_app/cloudRegistration/confirm.html"

    newapp_systemSelect = "gui_app/makeApplication/systemSelect.html"
    newapp_systemCreate = "gui_app/makeApplication/systemCreate.html"
    newapp_applicationCreate = \
        "gui_app/makeApplication/applicationCreate.html"
    newapp_environmentSelect = \
        "gui_app/makeApplication/environmentSelect.html"
    newapp_environmentCreate = \
        "gui_app/makeApplication/environmentCreate.html"
    newapp_confirm = "gui_app/makeApplication/confirm.html"

    envapp_systemSelect = "gui_app/envApplication/systemSelect.html"
    envapp_systemCreate = "gui_app/envApplication/systemCreate.html"
    envapp_bluprintSelect = "gui_app/envApplication/blueprintSelect.html"
    envapp_blueprintCreate = "gui_app/envApplication/blueprintCreate.html"
    envapp_environmentCreate = "gui_app/envApplication/environmentCreate.html"
    envapp_confirm = "gui_app/envApplication/confirm.html"

    appdeploy_applicationSelect = \
        "gui_app/applicationDeploy/applicationSelect.html"
    appdeploy_applicationCreate = \
        "gui_app/applicationDeploy/applicationCreate.html"
    appdeploy_environmentSelect = \
        "gui_app/applicationDeploy/environmentSelect.html"
    appdeploy_confirm = "gui_app/applicationDeploy/confirm.html"
