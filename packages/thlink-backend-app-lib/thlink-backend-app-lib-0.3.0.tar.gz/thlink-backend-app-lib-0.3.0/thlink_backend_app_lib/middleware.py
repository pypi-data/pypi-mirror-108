from typing import Union, Dict
import os
import logging
from aws_lambda_powertools.middleware_factory import lambda_handler_decorator
from aws_lambda_powertools import Logger
from aws_lambda_powertools.utilities.parser import ValidationError
from . import BaseModel


class BadOperationUserError(Exception):
    pass


class EntityDoesNotExistUserError(Exception):
    pass


class AppErrorModel(BaseModel):
    type: str
    message: Union[str, Dict]


class AppErrorResponseModel(BaseModel):
    app_error: AppErrorModel = None


env_service_name = os.environ.get("Service")
if env_service_name is None:
    raise ValueError("'Service' env var not set (service name)")
env_logging_level = os.environ.get("Service")
if env_logging_level is None:
    env_logging_level = logging.INFO
else:
    env_logging_level = int(env_logging_level)

logger = Logger(service=env_service_name, level=env_logging_level)


def error(type_: str, message: Union[str, Dict]):
    return AppErrorResponseModel(app_error=AppErrorModel(type=type_, message=message)).dict()


@lambda_handler_decorator
def middleware(handler, event, context):
    handler = logger.inject_lambda_context(log_event=logger.level == logging.DEBUG)(handler)
    try:
        response = handler(event, context)
        logger.debug("Handler Response", extra=response)
        return response
    except ValidationError as e:
        logger.info("EventValidationUserError")
        return error("EventValidationUserError", e.json())
    except BadOperationUserError as e:
        logger.info("BadOperationUserError")
        return error("BadOperationUserError", str(e))
    except EntityDoesNotExistUserError as e:
        logger.info("EntityDoesNotExistUserError")
        return error("EntityDoesNotExistUserError", str(e))
    except:
        logger.exception("InternalError")
        return error("InternalError", "Oh no!")


@lambda_handler_decorator
def middleware_mock(handler, event, context):
    response = handler(event, context)
    return response
