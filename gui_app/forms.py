# -*- coding: utf-8 -*-
from django import forms
from .enum.MessageCode import Error
from .enum.CloudType import CloudType
from .utils import StringUtil


class loginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(max_length=64, min_length=8)
    rePassword = forms.CharField(
        max_length=500, min_length=8, widget=forms.PasswordInput,
        required=False)


class projectForm(forms.Form):
    id = forms.IntegerField(required=False)
    name = forms.CharField(max_length=500)
    description = forms.CharField(required=False, max_length=500)


class cloudForm(forms.Form):
    name = forms.CharField(max_length=500)
    type = forms.CharField(max_length=500)
    key = forms.CharField(max_length=500)
    secret = forms.CharField(max_length=500)
    entry_point = forms.CharField(max_length=500)
    description = forms.CharField(required=False, max_length=500)
    tenant_name = forms.CharField(required=False, max_length=500)

    def clean_tenant_name(self):
        tenant_name = self.cleaned_data['tenant_name']
        type = self.cleaned_data.get('type')
        if StringUtil.isNotEmpty(type) and CloudType.openstack.name == type:
            if StringUtil.isEmpty(tenant_name):
                raise forms.ValidationError(Error.Required.value)

        return tenant_name

class BaseCloudForm(forms.Form):
    name = forms.CharField(max_length=500)
    type = forms.CharField(max_length=500)
    key = forms.CharField(max_length=500)
    secret = forms.CharField(max_length=500)
    entry_point = forms.CharField(max_length=500)
    description = forms.CharField(required=False, max_length=500)
    tenant_name = forms.CharField(required=False, max_length=500)

    def clean_tenant_name(self):
        tenant_name = self.cleaned_data['tenant_name']
        type = self.cleaned_data.get('type')
        if StringUtil.isNotEmpty(type) and CloudType.openstack.name == type:
            if StringUtil.isEmpty(tenant_name):
                raise forms.ValidationError(Error.Required.value)

        return tenant_name

class WakameCloudForm(forms.Form):
    name = forms.CharField(max_length=500)
    type = forms.CharField(max_length=500)
    key = forms.CharField(max_length=500)
    secret = forms.CharField(required=False, max_length=500)
    entry_point = forms.CharField(max_length=500)
    description = forms.CharField(required=False, max_length=500)
    tenant_name = forms.CharField(required=False, max_length=500)

    def clean_tenant_name(self):
        tenant_name = self.cleaned_data['tenant_name']
        type = self.cleaned_data.get('type')
        if StringUtil.isNotEmpty(type) and CloudType.openstack.name == type:
            if StringUtil.isEmpty(tenant_name):
                raise forms.ValidationError(Error.Required.value)

        return tenant_name

class cloudForm2(forms.Form):
    name = forms.CharField(required=False, max_length=500)
    type = forms.CharField(required=False, max_length=500)
    key = forms.CharField(required=False, max_length=500)
    secret = forms.CharField(required=False, max_length=500)
    entry_point = forms.CharField(required=False, max_length=500)
    description = forms.CharField(required=False, max_length=500)
    tenant_name = forms.CharField(required=False, max_length=500)


class baseImageForm(forms.Form):
    project_id = forms.CharField(required=False)
    id = forms.IntegerField(required=False)
    ssh_username = forms.CharField(max_length=500)
    source_image = forms.CharField(max_length=500)
    platform = forms.CharField(max_length=500)
    platform_version = forms.CharField(max_length=500)


class systemForm(forms.Form):
    id = forms.IntegerField(required=False)
    name = forms.CharField(max_length=500)
    description = forms.CharField(required=False, max_length=500)
    domain = forms.CharField(required=False, max_length=500)
    environment = forms.CharField(required=False, max_length=500)


class systemSelectForm(forms.Form):
    id = forms.CharField()


class environmentSelectForm(forms.Form):
    id = forms.CharField()


class environmentForm(forms.Form):
    id = forms.IntegerField(required=False)
    system_id = forms.CharField()
    blueprint_id = forms.CharField()
    version = forms.CharField(required=False)
    name = forms.CharField(max_length=500)
    description = forms.CharField(required=False, max_length=500)
    template_parameters = forms.CharField(required=False)
    user_attributes = forms.CharField(required=False)
    candidates_attributes_1 = forms.CharField(max_length=500)
    candidates_attributes_2 = forms.CharField(required=False, max_length=500)
    candidates_attributes_3 = forms.CharField(required=False, max_length=500)

    def clean(self):
        candidates_attributes_1 = self.cleaned_data.get(
            'candidates_attributes_1', None)
        candidates_attributes_2 = self.cleaned_data.get(
            'candidates_attributes_2', None)
        candidates_attributes_3 = self.cleaned_data.get(
            'candidates_attributes_3', None)

        if candidates_attributes_2:
            if candidates_attributes_1 == candidates_attributes_2:
                raise forms.ValidationError(Error.DuplicationCloud.value)

        if candidates_attributes_3:
            if candidates_attributes_2 == candidates_attributes_3:
                raise forms.ValidationError(Error.DuplicationCloud.value)

            if candidates_attributes_1 == candidates_attributes_3:
                raise forms.ValidationError(Error.DuplicationCloud.value)

        return self.cleaned_data


class edit_environmentForm(forms.Form):
    id = forms.IntegerField(required=False)
    name = forms.CharField(max_length=500)
    description = forms.CharField(required=False, max_length=500)
    template_parameters = forms.CharField(required=False)
    user_attributes = forms.CharField(required=False)


class w_environmentForm(forms.Form):
    id = forms.IntegerField(required=False)
    blueprint_id = forms.CharField()
    version = forms.CharField(required=False)
    name = forms.CharField(max_length=500)
    description = forms.CharField(required=False, max_length=500)
    template_parameters = forms.CharField(required=False, max_length=500)
    user_attributes = forms.CharField(required=False, max_length=500)
    candidates_attributes_1 = forms.CharField(max_length=500)
    candidates_attributes_2 = forms.CharField(required=False, max_length=500)
    candidates_attributes_3 = forms.CharField(required=False, max_length=500)

    def clean(self):
        candidates_attributes_1 = self.cleaned_data.get(
            'candidates_attributes_1', None)
        candidates_attributes_2 = self.cleaned_data.get(
            'candidates_attributes_2', None)
        candidates_attributes_3 = self.cleaned_data.get(
            'candidates_attributes_3', None)

        if candidates_attributes_2:
            if candidates_attributes_1 == candidates_attributes_2:
                raise forms.ValidationError(Error.DuplicationCloud.value)

        if candidates_attributes_3:
            if candidates_attributes_2 == candidates_attributes_3:
                raise forms.ValidationError(Error.DuplicationCloud.value)

            if candidates_attributes_1 == candidates_attributes_3:
                raise forms.ValidationError(Error.DuplicationCloud.value)

        return self.cleaned_data


class w_appenv_environmentForm(forms.Form):
    id = forms.IntegerField(required=False)
    name = forms.CharField(max_length=500)
    description = forms.CharField(required=False, max_length=500)
    template_parameters = forms.CharField(required=False, max_length=500)
    user_attributes = forms.CharField(required=False, max_length=500)
    candidates_attributes_1 = forms.CharField(max_length=500)
    candidates_attributes_2 = forms.CharField(required=False, max_length=500)
    candidates_attributes_3 = forms.CharField(required=False, max_length=500)

    def clean(self):
        candidates_attributes_1 = self.cleaned_data.get(
            'candidates_attributes_1', None)
        candidates_attributes_2 = self.cleaned_data.get(
            'candidates_attributes_2', None)
        candidates_attributes_3 = self.cleaned_data.get(
            'candidates_attributes_3', None)

        if candidates_attributes_2:
            if candidates_attributes_1 == candidates_attributes_2:
                raise forms.ValidationError(Error.DuplicationCloud.value)

        if candidates_attributes_3:
            if candidates_attributes_2 == candidates_attributes_3:
                raise forms.ValidationError(Error.DuplicationCloud.value)

            if candidates_attributes_1 == candidates_attributes_3:
                raise forms.ValidationError(Error.DuplicationCloud.value)

        return self.cleaned_data


class applicationForm(forms.Form):
    id = forms.IntegerField(required=False)
    system_id = forms.CharField()
    name = forms.CharField(max_length=500)
    description = forms.CharField(required=False, max_length=500)
    domain = forms.CharField(required=False, max_length=500)
    url = forms.URLField(max_length=500)
    type = forms.CharField(max_length=500)
    protocol = forms.CharField(max_length=500)
    revision = forms.CharField(required=False, max_length=500)
    pre_deploy = forms.CharField(required=False, max_length=500)
    post_deploy = forms.CharField(required=False, max_length=500)
    parameters = forms.CharField(required=False, max_length=1500)


class applicationForm2(forms.Form):
    id = forms.IntegerField(required=False)
    system_id = forms.CharField()
    name = forms.CharField(max_length=500)
    description = forms.CharField(required=False, max_length=500)
    domain = forms.CharField(required=False, max_length=500)


class applicationHistoryForm(forms.Form):
    id = forms.IntegerField(required=False)
    url = forms.URLField(max_length=500)
    type = forms.CharField(max_length=500)
    protocol = forms.CharField(max_length=500)
    revision = forms.CharField(required=False, max_length=500)
    pre_deploy = forms.CharField(required=False, max_length=500)
    post_deploy = forms.CharField(required=False, max_length=500)
    parameters = forms.CharField(required=False, max_length=1500)


class w_applicationForm(forms.Form):
    name = forms.CharField(max_length=500)
    description = forms.CharField(required=False, max_length=500)
    domain = forms.URLField(required=False, max_length=500)
    url = forms.CharField(max_length=500)
    type = forms.CharField(required=False, max_length=500)
    protocol = forms.CharField(required=False, max_length=500)
    revision = forms.CharField(required=False, max_length=500)
    pre_deploy = forms.CharField(required=False, max_length=500)
    post_deploy = forms.CharField(required=False, max_length=500)
    parameters = forms.CharField(required=False, max_length=1500)


class blueprintForm(forms.Form):
    id = forms.IntegerField(required=False)
    project_id = forms.CharField(required=False)
    name = forms.CharField(max_length=500)
    description = forms.CharField(required=False, max_length=500)
    patterns_attributes = forms.CharField(required=False, max_length=500)


class blueprintSelectForm(forms.Form):
    id = forms.CharField()


class selecttForm(forms.Form):
    id = forms.CharField()
    name = forms.CharField()


class patternForm(forms.Form):
    url = forms.CharField(required=True, max_length=500)
    revision = forms.CharField(required=False, max_length=500)
    secret_key = forms.CharField(required=False, max_length=2000)


class accountForm(forms.Form):
    email = forms.EmailField(max_length=500)
    name = forms.CharField(max_length=500)
    password = forms.CharField(min_length=8, max_length=500)
    repassword = forms.CharField(min_length=8, max_length=500)
    admin = forms.CharField(max_length=500)

    def clean_repassword(self):
        repassword = self.cleaned_data['repassword']
        if self.cleaned_data['password'] != self.cleaned_data['repassword']:
            raise forms.ValidationError(Error.PasswordMismatch.value)

        return repassword


class roleForm(forms.Form):
    name = forms.CharField(max_length=500)
    description = forms.CharField(required=False, max_length=500)
