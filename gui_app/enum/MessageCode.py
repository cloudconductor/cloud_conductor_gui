from enum import Enum


class Error(Enum):

    Authentication = 'Email address, or password is incorrect.'
    DuplicationCloud = 'Cloud priority should not be duplicated.'
    PasswordMismatch = 'Passwords do not match.'
    CheckboxNotSelected = 'Not selected'
    NoAssginment = 'This account is not assigned to the project.'
    NoRole = 'This account does not have Role is assigned.'
    NoPermission = 'Permission does not exist.'
    Required = 'This field is required.'
    PatternRequired = 'Please select one or more Patterns.'


class Info(Enum):
    WizardSystem = 'And transition to the new creation screen. is it OK??'
