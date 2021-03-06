#!/bin/bash

# Copyright 2020 The FedLearner Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

set -ex
export CUDA_VISIBLE_DEVICES=
export LD_LIBRARY_PATH=${HADOOP_HOME}/lib/native:${JAVA_HOME}/jre/lib/amd64/server:${LD_LIBRARY_PATH}
export CLASSPATH=.:$CLASSPATH:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar:$($HADOOP_HOME/bin/hadoop classpath --glob)

python -m fedlearner.data_join.rsa_psi.rsa_psi_signer \
    --listen_port=50051 \
    --rsa_private_key_path=$RSA_PRIVATE_KEY_PATH \
    --rsa_privet_key_pem=$RSA_KEY_PEM \
    --offload_processor_number=$OFFLOAD_PROCSSOR_NUMBER
