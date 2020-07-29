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
import json
import numpy as np


class MyEncoder(json.JSONEncoder):
    # 调整json文件存储形式
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(MyEncoder, self).default(obj)


def split_coco_dataset(dataset_dir, val_percent, test_percent):
    if not osp.exists(osp.join(dataset_dir, "annotations.json")):
        raise ValueError("\'annotations.json\' is not found in {}!".format(
            dataset_dir))
    try:
        from pycocotools.coco import COCO
    except:
        print(
            "pycococotools is not installed, follow this doc install pycocotools: https://paddlex.readthedocs.io/zh_CN/develop/install.html#pycocotools"
        )
        return
    annotation_file = osp.join(dataset_dir, "annotations.json")
    coco = COCO(annotation_file)
    img_ids = coco.getImgIds()
    cat_ids = coco.getCatIds()
    anno_ids = coco.getAnnIds()

    val_num = int(len(img_ids) * val_percent)
    test_num = int(len(img_ids) * test_percent)
    train_num = len(img_ids) - val_num - test_num

    random.shuffle(img_ids)
    train_files_ids = img_ids[:train_num]
    val_files_ids = img_ids[train_num:train_num + val_num]
    test_files_ids = img_ids[train_num + val_num:]

    for img_id_list in [train_files_ids, val_files_ids, test_files_ids]:
        img_anno_ids = coco.getAnnIds(imgIds=img_id_list, iscrowd=0)
        imgs = coco.loadImgs(img_id_list)
        instances = coco.loadAnns(img_anno_ids)
        categories = coco.loadCats(cat_ids)
        img_dict = {
            "annotations": instances,
            "images": imgs,
            "categories": categories
        }

        if img_id_list == train_files_ids:
            json_file = open(osp.join(dataset_dir, 'train.json'), 'w+')
            json.dump(img_dict, json_file, cls=MyEncoder)
        elif img_id_list == val_files_ids:
            json_file = open(osp.join(dataset_dir, 'val.json'), 'w+')
            json.dump(img_dict, json_file, cls=MyEncoder)
        elif img_id_list == test_files_ids:
            json_file = open(osp.join(dataset_dir, 'test.json'), 'w+')
            json.dump(img_dict, json_file, cls=MyEncoder)
    print("COCO Split Done")
    print("Train samples: {}".format(train_num))
    print("Eval samples: {}".format(val_num))
    print("Test samples: {}".format(test_num))
    print("Split json(train.json, val.json, test.json) saved in {}".format(
        dataset_dir))
