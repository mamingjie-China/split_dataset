# copyright (c) 2020 PaddlePaddle Authors. All Rights Reserve.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os.path as osp
import random
from utils import list_files, is_pic, replace_ext


def split_seg_dataset(dataset_dir, val_percent, test_percent):
    if not osp.exists(osp.join(dataset_dir, "JPEGImages")):
        raise ValueError("\'JPEGImages\' is not found in {}!".format(
            dataset_dir))
    if not osp.exists(osp.join(dataset_dir, "Annotations")):
        raise ValueError("\'Annotations\' is not found in {}!".format(
            dataset_dir))

    all_image_files = list_files(osp.join(dataset_dir, "JPEGImages"))

    image_anno_list = list()
