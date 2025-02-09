# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#

from iotdb.mlnode.algorithm.factory import create_forecast_model
from iotdb.mlnode.constant import TSStatusCode
from iotdb.mlnode.data_access.factory import create_forecast_dataset
from iotdb.mlnode.log import logger
from iotdb.mlnode.parser import parse_training_request
from iotdb.mlnode.util import get_status
from iotdb.thrift.mlnode import IMLNodeRPCService
from iotdb.thrift.mlnode.ttypes import (TCreateTrainingTaskReq,
                                        TDeleteModelReq, TForecastReq,
                                        TForecastResp)


class MLNodeRPCServiceHandler(IMLNodeRPCService.Iface):
    def __init__(self):
        pass

    def deleteModel(self, req: TDeleteModelReq):
        return get_status(TSStatusCode.SUCCESS_STATUS, "")

    def createTrainingTask(self, req: TCreateTrainingTaskReq):
        # parse request stage (check required config and config type)
        data_config, model_config, task_config = parse_training_request(req)

        # create model stage (check model config legitimacy)
        try:
            model, model_config = create_forecast_model(**model_config)
        except Exception as e:  # Create model failed
            return get_status(TSStatusCode.FAIL_STATUS, str(e))
        logger.info('model config: ' + str(model_config))

        # create data stage (check data config legitimacy)
        try:
            dataset, data_config = create_forecast_dataset(**data_config)
        except Exception as e:  # Create data failed
            return get_status(TSStatusCode.FAIL_STATUS, str(e))
        logger.info('data config: ' + str(data_config))

        # create task stage (check task config legitimacy)

        # submit task stage (check resource and decide pending/start)

        return get_status(TSStatusCode.SUCCESS_STATUS, 'Successfully create training task')

    def forecast(self, req: TForecastReq):
        status = get_status(TSStatusCode.SUCCESS_STATUS, "")
        forecast_result = b'forecast result'
        return TForecastResp(status, forecast_result)
