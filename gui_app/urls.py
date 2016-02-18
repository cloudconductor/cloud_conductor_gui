from django.conf.urls import url
from .views import projectViews
from .views import cloudViews
from .views import baseImageViews
from .views import loginViews
from .views import accountViews
from .views import roleViews
from .views import systemViews
from .views import environmentViews
from .views import assignmentViews
from .views import applicationViews
from .views import blueprintViews
from .views import patternViews
from .views import cloudRegistrationViews
from .views import makeApplicationViews
from .views import applicationEnvironmentViews
from .views import applicationDeployViews


urlpatterns = [

    url('^login/', loginViews.login, name="login"),
    url('^logout/', loginViews.logout, name="logout"),
    url(r"^$", environmentViews.environmentList, name="top"),

    url('^project/list', projectViews.projectList, name="projectList"),
    url('^project/create', projectViews.projectCreate, name="projectCreate"),
    url('^project/(?P<id>\d+)/detail/',
        projectViews.projectDetail, name="projectDetail"),
    url('^project/(?P<id>\d+)/delete/',
        projectViews.projectDelete, name="projectDelete"),
    url('^project/add/$', projectViews.projectEdit, name="projectAdd"),
    url('^project/(?P<id>\d+)/edit/$',
        projectViews.projectEdit, name="projectEdit"),
    url('^project/(?P<id>\d+)/project/change/$',
        projectViews.projectChange, name="projectChange"),

    url('^assignment/(?P<id>\d+)/edit/$',
        assignmentViews.assignmentEdit, name="assignmentEdit"),
    url('^assignment/(?P<id>\d+)/add/$',
        assignmentViews.assignmentAdd, name="assignmentAdd"),

    url('^cloud/list', cloudViews.cloudList, name="cloudList"),
    url('^cloud/(?P<id>\d+)/detail/',
        cloudViews.cloudDetail, name="cloudDetail"),
    url('^cloud/create', cloudViews.cloudCreate, name="cloudCreate"),
    url('^cloud/(?P<id>\d+)/edit/$', cloudViews.cloudEdit, name="cloudEdit"),
    url('^cloud/(?P<id>\d+)/delete/',
        cloudViews.cloudDelete, name="cloudDelete"),

    url('^baseimage/(?P<id>\d+)/detail/',
        baseImageViews.baseImageDetail, name="baseImageDetail"),
    url('^cloud/(?P<cid>\d+)/baseimage/create',
        baseImageViews.baseImageCreate, name="baseImageCreate"),
    url('^baseimage/(?P<id>\d+)/edit/$',
        baseImageViews.baseImageEdit, name="baseImageEdit"),
    url('^baseimage/(?P<id>\d+)/delete/',
        baseImageViews.baseImageDelete, name="baseImageDelete"),

    url('^system/list', systemViews.systemList, name="systemList"),
    url('^system/(?P<id>\d+)/detail/',
        systemViews.systemDetail, name="systemDetail"),
    url('^system/create', systemViews.systemCreate, name="systemCreate"),
    url('^system/(?P<id>\d+)/edit/$',
        systemViews.systemEdit, name="systemEdit"),
    url('^system/(?P<id>\d+)/delete/',
        systemViews.systemDelete, name="systemDelete"),

    url('^environment/list', environmentViews.environmentList,
        name="environmentList"),
    url('^environment/(?P<id>\d+)/detail/',
        environmentViews.environmentDetail, name="environmentDetail"),
    url('^environment/create', environmentViews.environmentCreate,
        name="environmentCreate"),
    url('^environment/ajax', environmentViews.environmentAjaxBlueprint,
        name="environmentAjaxBlueprint"),
    url('^environment/(?P<id>\d+)/edit/$',
        environmentViews.environmentEdit, name="environmentEdit"),
    url('^environment/(?P<id>\d+)/delete/',
        environmentViews.environmentDelete, name="environmentDelete"),

    url('^application/list', applicationViews.applicationList,
        name="applicationList"),
    url('^application/(?P<id>\d+)/detail/',
        applicationViews.applicationDetail, name="applicationDetail"),
    url('^application/create', applicationViews.applicationCreate,
        name="applicationCreate"),
    url('^application/(?P<id>\d+)/edit/$',
        applicationViews.applicationEdit, name="applicationEdit"),
    url('^application/(?P<id>\d+)/delete/',
        applicationViews.applicationDelete, name="applicationDelete"),

    url('^application/(?P<id>\d+)/history/(?P<hid>\d+)/detail/',
        applicationViews.applicationHistoryDetail,
        name="applicationHistoryDetail"),
    url('^application/(?P<id>\d+)/history/create',
        applicationViews.applicationHistoryCreate,
        name="applicationHistoryCreate"),
    url('^application/(?P<id>\d+)/history/(?P<hid>\d+)/edit/',
        applicationViews.applicationHistoryEdit,
        name="applicationHistoryEdit"),

    url('^blueprint/list', blueprintViews.blueprintList,
        name="blueprintList"),
    url('^blueprint/(?P<id>\d+)/detail/',
        blueprintViews.blueprintDetail, name="blueprintDetail"),
    url('^blueprint/create', blueprintViews.blueprintCreate,
        name="blueprintCreate"),
    url('^blueprint/(?P<id>\d+)/edit/$',
        blueprintViews.blueprintEdit, name="blueprintEdit"),
    url('^blueprint/(?P<id>\d+)/delete/',
        blueprintViews.blueprintDelete, name="blueprintDelete"),

    url('^blueprint/(?P<id>\d+)/build', blueprintViews.blueprintBuild,
        name="blueprintBuild"),
    url('^blueprint/(?P<id>\d+)/history/(?P<ver>\d+)/detail/',
        blueprintViews.blueprintHistoryDetail,
        name="blueprintHistoryDetail"),

    url('^pattern/list', patternViews.patternList, name="patternList"),
    url('^pattern/(?P<id>\d+)/detail/',
        patternViews.patternDetail, name="patternDetail"),
    url('^pattern/create', patternViews.patternCreate, name="patternCreate"),
    url('^pattern/(?P<id>\d+)/edit/$',
        patternViews.patternEdit, name="patternEdit"),
    url('^pattern/(?P<id>\d+)/delete/',
        patternViews.patternDelete, name="patternDelete"),

    url('^account/list', accountViews.accountList, name="accountList"),
    url('^account/(?P<id>\d+)/detail/',
        accountViews.accountDetail, name="accountDetail"),
    url('^account/create/', accountViews.accountCreate, name="accountCreate"),
    url('^account/(?P<id>\d+)/edit/',
        accountViews.accountEdit, name="accountEdit"),
    url('^account/(?P<id>\d+)/delete/',
        accountViews.accountDelete, name="accountDelete"),

    url('^role/list', roleViews.roleList, name="roleList"),
    url('^role/(?P<id>\d+)/detail/', roleViews.roleDetail, name="roleDetail"),
    url('^role/create/', roleViews.roleCreate, name="roleCreate"),
    url('^role/(?P<id>\d+)/edit/', roleViews.roleEdit, name="roleEdit"),
    url('^role/(?P<id>\d+)/delete/', roleViews.roleDelete, name="roleDelete"),

    url('^role/create/', roleViews.roleCreate, name="roleCreate"),

    url('^cloudregist/cloud/create/',
        cloudRegistrationViews.cloudCreate, name="cloudregistCloud"),
    url('^cloudregist/baseimage/create/',
        cloudRegistrationViews.baseimageCreate, name="cloudregistBaseimage"),
    url('^cloudregist/confirm/', cloudRegistrationViews.confirm,
        name="cloudregistConfirm"),

    url('^newapp/system/select/', makeApplicationViews.systemSelect,
        name="mkappSystemSelect"),
    url('^newapp/system/create/', makeApplicationViews.systemCreate,
        name="mkappSystemCreate"),
    url('^newapp/application/create/',
        makeApplicationViews.applicationCreate,
        name="mkappApplicationCreate"),
    url('^newapp/environment/select/',
        makeApplicationViews.environmentSelect,
        name="mkappEnvironmentSelect"),
    url('^newapp/environment/create/',
        makeApplicationViews.environmentCreate,
        name="mkappEnvironmentCreate"),
    url('^newapp/confirm/', makeApplicationViews.confirm,
        name="mkappConfirm"),

    url('^envapp/system/select/', applicationEnvironmentViews.systemSelect,
        name="envapp_systemSelect"),
    url('^envapp/system/create/', applicationEnvironmentViews.systemCreate,
        name="envapp_systemCreate"),
    url('^envapp/blueprint/select/',
        applicationEnvironmentViews.blueprintSelect,
        name="envapp_bluprintSelect"),
    url('^envapp/blueprint/create',
        applicationEnvironmentViews.blueprintCreate,
        name="envapp_blueprintCreate"),
    url('^envapp/environment/create/',
        applicationEnvironmentViews.environmentCreate,
        name="envapp_environmentCreate"),
    url('^envapp/confirm/', applicationEnvironmentViews.confirm,
        name="envapp_confirm"),

    url('^appdeploy/application/select/',
        applicationDeployViews.applicationSelect,
        name="appdeployApplicationSelect"),
    url('^appdeploy/application/create/',
        applicationDeployViews.applicationCreate,
        name="appdeployApplicationCreate"),
    url('^appdeploy/environment/select/',
        applicationDeployViews.environmentSelect,
        name="appdeployEnvironmentSelect"),
    url('^appdeploy/confirm/', applicationDeployViews.confirm,
        name="appdeployConfirm"),

]
