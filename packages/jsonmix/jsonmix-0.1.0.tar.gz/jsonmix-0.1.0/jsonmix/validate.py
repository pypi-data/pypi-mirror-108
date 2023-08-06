from functools import wraps


def _validate_fields(receive:dict, model:dict, response:dict) -> dict:
    """
    This method valid the fields of json receive through of model json passed,
    beyond of pass the receive json and model json, it receives a custom json response.
    :param receive: get the json that comes from outside
    :param model: get the model json
    :param response: get the response customized
    :return: the response customized
    """
    missing = list()
    for key in receive.keys():
        if isinstance(receive[key], dict):
            for i in receive[key].keys():
                if i not in model[key]:
                    missing.append(i)
        if key not in model:
            missing.append(key)
    if missing:
        response.update({'aux': missing})
        return response
    else:
        return None


def _validate_fields_types(receive:dict, model:dict, response:dict) -> dict:
    """
    This method valid the fields types of json receive through of model json passed,
    beyond of pass the receive json and model json, it receives a custom json response.
    :param receive: get the json that comes from outside
    :param model: get the model json
    :param response: get the response customized
    :return: the response customized
    """
    wrong_types = list()
    for type_field in receive.keys():
        if isinstance(receive[type_field], dict):
            for i in receive[type_field].keys():
                if type(receive[type_field][i]) != model[type_field][i]:
                    wrong_types.append(i)
        elif type(receive[type_field]) != model[type_field]:
            wrong_types.append(type_field)
    if wrong_types:
        response.update({'aux': {k: str(v) for k, v in model.items()}})
        return response
    else:
        return None


def validate_json(receive:dict, model:dict, response_field=dict, response_field_type=dict, operation='default') -> dict:
    """
    This method validates json completely, it can only validate fields,
    fields types or both. it receives a json from outside, a valid json
    model and the answer that it will have to have and the type of
    operation, if nothing is passed in the operation parameter, it will
    understand that it has to validate both fields and types, if passing
    "fields" it validates only the fields, if passing "types" it validates
    only the types of the fields, if you pass 'decorator' as the name says,
    you will be able to validate both the fields and the field types, more
    not as a method but as a decorator.

    examples of how to use:

        * operation receiving fields
            def hello():
                receive_json = {
                    'uid': 1,
                    'Name': 'Json Mix',
                    'Version': '0.1.0',
                    'message': 'A library for validate in python'
                }
                model_json = {
                    'uid': int,
                    'Name': str,
                    'Version': str,
                    'message': str
                }
                response = {
                    "code": "JMERR-001",
                    "data": {
                        "error": "inconsistency on JSON structure",
                        "message": "Missing required JSON field"
                    },
                    "date": str(datetime.now().timestamp()),
                }
                return validate_json(receive=receive_json, model=model_json, response_field=response, operation='fields')

        * operation receiving fields types
            def hello():
                receive_json = {
                    'uid': 1,
                    'Name': 'Json Mix',
                    'Version': '0.1.0',
                    'message': 'A library for validate in python'
                }
                model_json = {
                    'uid': int,
                    'Name': str,
                    'Version': str,
                    'message': str
                }
                response = {
                    "code": "JMERR-002",
                    "data": {
                        "error": "inconsistency on JSON structure",
                        "message": "JSON field type is incorrect"
                    },
                    "date": str(datetime.now().timestamp())
                }
                return validate_json(receive=receive_json, model=model_json, response_field=response, operation='types')

        * operation receiving decorator
            receive_json = {
                    'uid': 1,
                    'Name': 'Json Mix',
                    'Version': '0.1.0',
                    'message': 'A library for validate in python'
                }
            model_json = {
                'uid': int,
                'Name': str,
                'Version': str,
                'message': str
            }
            response_fields = {
                "code": "JMERR-001",
                "data": {
                    "error": "inconsistency on JSON structure",
                    "message": "Missing required JSON field"
                },
                "date": str(datetime.now().timestamp()),
            }
            response_types = {
                "code": "JMERR-002",
                "data": {
                    "error": "inconsistency on JSON structure",
                    "message": "JSON field type is incorrect"
                },
                "date": str(datetime.now().timestamp())
            }

            @validate_json(receive=receive_json, model=model_json, response_field=response_fields, response_field_types=response_types, operation='decorator')
            def hello():
                return 'Hello Word'

        * operation receiving default
            def hello():
                receive_json = {
                        'uid': 1,
                        'Name': 'Json Mix',
                        'Version': '0.1.0',
                        'message': 'A library for validate in python'
                    }
                model_json = {
                    'uid': int,
                    'Name': str,
                    'Version': str,
                    'message': str
                }
                response_fields = {
                    "code": "JMERR-001",
                    "data": {
                        "error": "inconsistency on JSON structure",
                        "message": "Missing required JSON field"
                    },
                    "date": str(datetime.now().timestamp()),
                }
                response_types = {
                    "code": "JMERR-002",
                    "data": {
                        "error": "inconsistency on JSON structure",
                        "message": "JSON field type is incorrect"
                    },
                    "date": str(datetime.now().timestamp())
                }
                return validate_json(receive=receive_json, model=model_json, response_field=response_fields, response_field_types=response_types, operation='decorator')


    :param receive: get the json that comes from outside
    :param model: get the model json
    :param response_field: get the response customized for errors in fields
    :param response_field_type: get the response customized for errors in fields types
    :param operation: initialized as 'default', more can get 'fields', 'types' or 'decorator'
    :return: the response customized
    """
    try:
        if operation == 'fields':
            if response_field != '':
                return _validate_fields(receive, model, response_field)
        elif operation == 'types':
            if response_field_type != '':
                return _validate_fields_types(receive, model, response_field_type)
        elif operation == 'decorator':
            def decorator(fn):
                @wraps(fn)
                def wrapper(*args, **kwargs):
                    if response_field != '':
                        missing = _validate_fields(receive, model, response_field)
                        if missing != None:
                            return missing
                    if response_field_type != '':
                        wrong_types = _validate_fields_types(receive, model, response_field_type)
                        if wrong_types != None:
                            return wrong_types
                    return fn(*args, **kwargs)
                return wrapper
            return decorator
        elif operation == 'default':
            if response_field != '':
                missing = _validate_fields(receive, model, response_field)
                if missing != None:
                    return missing
            if response_field_type != '':
                wrong_types = _validate_fields_types(receive, model, response_field_type)
                if wrong_types != None:
                    return wrong_types
    except Exception as error:
        raise Exception(f'The key you passed in the operation parameter is invalid, it only receives "fields", "types" or "decorator". error {error}')


