#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import traceback
import time
from fastml_engine.log import Logger
from fastml_engine.exception.infer_exception import InferException
from fastml_engine.exception.load_exception import LoadException
import os


class ServiceEngine:

    def __init__(self, service_path=None):

        if service_path and os.path.exists(service_path):
            logger = Logger(log_path=service_path + "/logs").getLogger(__name__)
            logger.info('service_path: %s', service_path)
        else:
            raise LoadException('service_path is none, terminated')
        try:
            logger.info("starting...")
            init_start_time = time.time()
            sys.path.append(service_path + "/src")
            script_name = 'inference'
            class_name = 'Inference'
            logger.info('import inference module')
            ext_module = __import__(script_name)
            cls = getattr(ext_module, class_name)
            self.instance = cls()
            logger.info(dir(ext_module))
            duration = time.time() - init_start_time
            logger.info('finished cost:%s s', duration)
        except Exception as e:
            logger.warn("Failed to start ,please check error log")
            logger.error("errmsg: %s , %s", str(e), traceback.format_exc())
            raise LoadException(message='start error' + str(e))

    def invoke(self, data):
        if self.instance:
            output = self.instance.infer(data)
        else:
            raise InferException(message='infer instance is none')
        return output
