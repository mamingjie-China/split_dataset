from six import text_type as _text_type
import argparse
import sys
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


def split_dataset(annotation_file, val_percent, test_percent):
    try:
        from pycocotools.coco import COCO
    except:
        print(
            "pycococotools is not installed, follow this doc install pycocotools: https://paddlex.readthedocs.io/zh_CN/develop/install.html#pycocotools"
        )
        return
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
            json_file = open('train.json', 'w+')
            json.dump(img_dict, json_file, cls=MyEncoder)
        elif img_id_list == val_files_ids:
            json_file = open('val.json', 'w+')
            json.dump(img_dict, json_file, cls=MyEncoder)
        elif img_id_list == test_files_ids:
            json_file = open('test.json', 'w+')
            json.dump(img_dict, json_file, cls=MyEncoder)
    print("COCO Split Done")
    print("Train samples: {}".format(train_num))
    print("Eval samples: {}".format(val_num))
    print("Test samples: {}".format(test_num))
    print("Split json saved in ./train.json  ./val.json ./test.json")


def main():
    if len(sys.argv) < 3:
        print(
            "Usage: python ins_seg_split.py --annotation ann.json --val_percent 0.2 --test_percent 0.1"
        )
        return
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--annotation",
        "-a",
        type=_text_type,
        default=None,
        help="COCO annotation file /'annotation.json/'")
    parser.add_argument(
        "--val_percent",
        "-vp",
        type=_text_type,
        default=None,
        help="validation set percent number(for example 0.2)")
    parser.add_argument(
        "--test_percent",
        "-tp",
        type=_text_type,
        default=None,
        help="test set percent number(for example 0.1)")

    args = parser.parse_args()

    annotation_file = args.annotation
    val_percent = float(args.val_percent)
    test_percent = float(args.test_percent)

    # 输入校验
    if not osp.exists(annotation_file):
        raise ValueError("File {} is not exist!".format(annotation_file))
    if val_percent <= 0 or val_percent >= 1 or test_percent < 0 or test_percent >= 1 or val_percent + test_percent >= 1 - 0.00001:
        raise ValueError("Please input correct split percent")

    split_dataset(annotation_file, val_percent, test_percent)


if __name__ == "__main__":
    main()
