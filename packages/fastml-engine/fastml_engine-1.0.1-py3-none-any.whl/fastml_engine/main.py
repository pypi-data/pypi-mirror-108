#!/usr/bin/env python
# -*- coding: utf-8 -*-
from gevent import monkey

monkey.patch_all()

import base64
import six
import numpy as np
import traceback
import json
import time
import collections
import io
import os
import logging
import tempfile
from flask import Flask, request, jsonify
from fastml_engine.core import ServiceEngine
from flasgger import Swagger
from flasgger.utils import swag_from

logger = logging.getLogger(__name__)
app = Flask(__name__)
Swagger(app)


@app.route('/health', methods=['GET'])
@swag_from('docs/health.yaml')
def health():
    return engine.instance.health()

@app.route('/infer', methods=['POST'])
@swag_from('docs/predict.yaml')
def infer():
    try:
        start_time = time.time()
        input_data = preprocess()
        output_data = engine.invoke(input_data)
        duration = time.time() * 1000 - start_time * 1000
        result = postprocess(output_data, duration)
    except Exception as e:
        if hasattr(e, 'error_type'):
            error_type = e.error_type
        else:
            error_type = 'InferError'
        result = json.dumps({
            'status': False,
            'data': {
                'message': str(e),
                'stacktrace': traceback.format_exc(),
                'error_type': error_type
            }
        }, ensure_ascii=False)
        logger.error("[Exception] %s", result)
    return result


def preprocess():
    content_type = request.content_type
    logger.info("request contentType: %s ,content_length: %d", content_type, request.content_length)
    if content_type.startswith("application/json"):
        data = request.get_json()
    elif content_type.startswith('text/plain'):
        if is_binary(request.get_data()):
            data = request.get_data().decode('utf-8')
        else:
            data = request.get_data()
    elif content_type == 'application/octet-stream' or content_type == 'binary':
        data = bytes(request.data)
    elif request.form or request.files:
        form = request.form
        files = request.files
        data = {}
        for k, v in form.items():
            data[k] = v
        for k, file in files.items():
            list = files.getlist(k)
            filename_dict = collections.OrderedDict()
            for one in list:
                if isinstance(one.stream, tempfile.SpooledTemporaryFile):
                    filename_dict[one.filename] = io.BytesIO(one.stream.read())
                elif isinstance(one.stream, io.BytesIO):
                    filename_dict[one.filename] = one.stream
                else:
                    logger.error('receive file not recognized!')
                    raise Exception

            data[k] = filename_dict
    else:
        raise Exception("Invalid content_type: {}".format(content_type))
    return data


def postprocess(data, duration):
    if is_binary(data):
        content_type = 'binary'
        data = base64.b64encode(data)
        if not isinstance(data, six.string_types):
            data = str(data, 'utf-8')
    elif isinstance(data, six.string_types) or isinstance(data, six.text_type):
        content_type = 'string'
    else:
        content_type = 'json'
    response_string = json.dumps({
        'status': True,
        'data': data,
        'metadata': {
            'duration': duration,
            'content_type': content_type
        }
    }, ensure_ascii=False, cls=NumpyEncoder)
    return response_string

def is_binary(arg):
    return isinstance(arg, base64.bytes_types)


# np array转json
class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, bytes):
            return str(obj, encoding='utf-8')
        return json.JSONEncoder.default(self, obj)


service_path = os.getenv('SERVICE_PATH')

def start(host='0.0.0.0', port=5000):
    app.run(host, port, debug=False, threaded=True)

if __name__ == '__main__':
    engine = ServiceEngine(service_path='D:\\fastml\\inference-template-python')
    start()


