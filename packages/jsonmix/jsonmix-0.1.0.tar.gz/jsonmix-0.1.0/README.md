[![Python Package](https://github.com/Suspir0n/jsonmix/actions/workflows/github-actions-demo.yml/badge.svg)](https://github.com/Suspir0n/jsonmix/actions/workflows/github-actions-demo.yml)
[![PyPI version fury.io](https://badge.fury.io/py/jsonmix.svg)](https://pypi.python.org/pypi/jsonmix/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/jsonmix.svg)](https://pypi.python.org/pypi/jsonmix/)
[![GitHub license](https://img.shields.io/github/license/Suspir0n/jsonmix.svg)](https://github.com/Suspir0n/jsonmix/blob/main/LICENSE)
[![GitHub tag](https://img.shields.io/github/tag/Suspir0n/jsonmix.svg)](https://github.com/Suspir0n/jsonmix/tags)


# Json Mix

A Python library for validate json. In this `0.1.0` version of jsonmix, it allows you to validate the json that you this awaiting.

## Installation

The latest stable version [is available on PyPI](https://pypi.org/project/jsonmix/). Either add `jsonmix` to your `requirements.txt` file or install with pip:

    pip install jsonmix

## Description

This project is to help other types of projects that need a json validation, and with this lib, you can validate fields, validate the types of fields or if it is necessary to validate both together.

## Steps

### Step 0:

In this lib we use the decorator, so for you to use it would be through a function or class, so it would start by importing the lib:

    import jsonmix

To be more specific and save space in memory, it could also import this way:

    from jsonmix.validate import validate_json

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

Notice that I pass 4 parameters that are them:

1. receive_json: The json you receive from an API or elsewhere.
2. model_json: The model json you created to be the basis of your validations
3. response_json_field: Your error response if the error is in the json keys
4. response_json_field_type: Your error response if the error is in the json types

### Step 2:

We have a test example of each of the parameter passages

* receive_json
```
    example_json_receive = {
        'uid': 1,
        'Name': 'Json Mix',
        'Version': '0.1.0',
        'message': 'A library for validate in python'
    }
```   

* model_json
```
    example_json_model = {
        'uid': int,
        'Name': str,
        'Version': str,
        'message': str
    }
```  

* response_json_field
```
  example_json_custom_error_response_field = {
        "code": "JMERR-001",
        "data": {
            "error": "inconsistency on JSON structure",
            "message": "Missing required JSON field"
        },
        "date": str(datetime.now().timestamp())
  }
```  

* response_json_field_type
```
    example_json_custom_error_response_field_type = {
        "code": "JMERR-002",
        "data": {
            "error": "inconsistency on JSON structure",
            "message": "JSON field type is incorrect"
        },
        "date": str(datetime.now().timestamp())
    }
```  

Now that I have shown you the examples of possible json of each parameter that `validate_json` receives and I have shown an example of use.

### Step 3:

Let's suppose that you set up your json model, to be able to validate with the json that is coming, and this was your model json:

```
    example_json_model = {
        'uid': int,
        'Name': str,
        'Version': str,
        'message': str
    }
``` 

With that there are some malicious people who want to invade or damage your website, app or some software of your own in some way and start editing your receiving json like changing the names of the keys, changing the types or even adding a new key to your json , see these examples of possible json that a malicious person could pass on to you.

```
    example_json_model = {
        'uid': int,
        'Name': str,
        'Version': str,
        'message': str
    }
``` 

```
    example_json_model = {
        'uid': int,
        'Name': str,
        'Version': str,
        'message': str
    }
```

```
    example_json_model = {
        'uid': int,
        'Name': str,
        'Version': str,
        'message': str
    }
``` 

Soon you realize that in the first example you receive a json with the wrong type, in this case your key 'uid' you defined as int and is receiving it as a string, in the second example we can see that an extra key was assigned in your json that would be the 'add_field' that is not in your json model, in the third example you receive a json with the invalid key, in which case your key for the json model is 'Name' and what you received is 'Na'. So these are the possible invalid json that can be received.
