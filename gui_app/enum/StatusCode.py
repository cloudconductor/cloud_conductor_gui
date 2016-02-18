from enum import Enum


class Environment(Enum):
    CREATE_COMPLETE = 'CREATE_COMPLETE'
    PENDING = 'PENDING'
    ERROR = 'ERROR'


class Blueprint(Enum):
    CREATE_COMPLETE = 'CREATE_COMPLETE'
    PENDING = 'PENDING'
    ERROR = 'ERROR'
