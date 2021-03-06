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

# coding: utf-8

import argparse
import logging
import os
from trainer_master import TrainerMaster
from fedlearner.trainer_master.data.data_block_queue import DataBlockQueue
from fedlearner.data_join.data_block_visitor import DataBlockVisitor

ETCD_NAME = os.environ.get('ETCD_NAME', None)
ETCD_ADDR = os.environ.get('ETCD_ADDR', None)
ETCD_BASE_DIR = os.environ.get('ETCD_BASE_DIR', None)


class LeaderTrainerMaster(TrainerMaster):
    def __init__(self, application_id, data_source,
                 start_time, end_time, online_training):
        super(LeaderTrainerMaster, self).__init__(application_id,
                                                  None, online_training)
        self._data_block_queue = DataBlockQueue()
        self._data_block_visitor = DataBlockVisitor(
            data_source, ETCD_NAME, ETCD_BASE_DIR, ETCD_ADDR)
        self._start_time = start_time
        self._end_time = end_time

    def _load_data(self):
        checkpoint = self._get_checkpoint()
        # pylint: disable=line-too-long
        for block_id, block_item in self._data_block_visitor.LoadDataBlockRepByTimeFrame(
                self._start_time, self._end_time).items():
            if block_id not in checkpoint:
                logging.debug('load data block id %s path %s',
                              block_id, block_item.data_block_fpath)
                self._data_block_queue.put(block_item)

    def _alloc_data_block(self, block_id=None):
        # block_id is unused in leader role
        data_blocks_resp = None
        if not self._data_block_queue.empty():
            data_blocks_resp = self._data_block_queue.get()
        return data_blocks_resp


if __name__ == '__main__':
    logging.getLogger().setLevel(logging.DEBUG)
    parser = argparse.ArgumentParser('leader trainer master cmd.')
    parser.add_argument('-p', '--port', type=int, default=50001,
                        help='Listen port of leader trainer master')
    parser.add_argument('-app_id', '--application_id',
                        required=True, help='application_id')
    parser.add_argument('-data_source', '--data_source',
                        required=False, help='training example data source')
    parser.add_argument('-start_date', '--start_date',
                        default=None, help='training data start date')
    parser.add_argument('-end_date', '--end_date',
                        default=None, help='training data end date')
    parser.add_argument('--online_training', action='store_true',
                        help='the train master run for online training')
    FLAGS = parser.parse_args()

    leader_tm = LeaderTrainerMaster(FLAGS.application_id, FLAGS.data_source,
                                    int(FLAGS.start_date), int(FLAGS.end_date),
                                    FLAGS.online_training)
    leader_tm.run(listen_port=FLAGS.port)
