# -*- coding: utf-8 -*-

"""
MS Teams / Email Logger for AWS
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

AWS Teams Logger is a Python library that forwards errors (failures) and log
messages to a MS Teams channel and an optional list of Developer Emails who may
need to be notified -- adds HTML formatting originally designed for MS Outlook.

Simple Usage for an AWS Lambda function:

    >>> from aws_teams_logger import LambdaLogger
    >>> from logging import getLogger
    >>>
    >>> log = getLogger()
    >>>
    >>> # Note: this is a simplified example, and assumes you define the required
    >>> # environment variables. Otherwise, you'd need to pass the parameters
    >>> # to the decorator class like `@LambdaLogger(teams_email='my-teams-email')
    >>> # in this case.
    >>>
    >>> @LambdaLogger
    >>> def my_lambda_handler(event, context):
    >>>   # This message can be sent to Teams, depending on the enabled log lvl
    >>>   log.info('Hello world!')
    >>>   # This will forward the error to Teams, and notify any Devs via email
    >>>   result = 1 / 0


Please see the docs for additional examples and some important how-to's.

"""
__all__ = [
    'LambdaLogger',
    'TaskLogger',
    'set_account_name',
    'upload_templates',
    'delete_templates'
]


from .loggers import *
from .utils.aws.ses.templates import *
