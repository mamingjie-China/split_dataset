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

from six import text_type as _text_type
import argparse
import sys
import os.path as osp
from coco_split import split_coco_dataset
from voc_split import split_voc_dataset
from seg_split import split_seg_dataset
from imagenet_split import split_imagenet_dataset


def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--form",
        "-f",
        type=_text_type,
        default=None,
        help="the type of dataset(COCO, ImageNet, VOC, Seg)")
    parser.add_argument(
        "--split_dataset",
        "-d",
        type=_text_type,
        default=None,
        help="the path of dataset to be splited")
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
        default=0.0,
        help="test set percent number(for example 0.1)")
    parser.add_argument(
        "--save_dir",
        "-s",
        type=_text_type,
        default=None,
        help="the path of saved file")

    return parser


def check_input(dataset_type, dataset_dir, val_percent, test_percent,
                save_dir):
    # 输入校验
    if not dataset_type in ["coco", "imagenet", "voc", "seg"]:
        raise ValueError(
            "--type is not correct defined(support COCO/ImageNet/VOC/Seg)")
    if not osp.exists(dataset_dir):
        raise ValueError("File {} is not exist!".format(dataset_dir))
    if val_percent <= 0 or val_percent >= 1 or test_percent < 0 or test_percent >= 1 or val_percent + test_percent >= 1:
        raise ValueError("Please input correct split percent")
    if not osp.exists(save_dir):
        raise ValueError("Please input correct save dir")

    return True


def main():
    if len(sys.argv) < 7:
        print(
            "Usage: python split.py --form COCO --split_dataset dataset_path --val_percent 0.2 --test_percent 0.1"
        )
        return

    parser = arg_parser()
    args = parser.parse_args()

    dataset_type = args.form.lower()
    dataset_dir = args.split_dataset
    val_percent = float(args.val_percent)
    test_percent = float(args.test_percent)
    if args.save_dir is None:
        save_dir = dataset_dir
    else:
        save_dir = args.save_dir

    if check_input(dataset_type, dataset_dir, val_percent, test_percent,
                   save_dir):
        if dataset_type == "coco":
            train_num, val_num, test_num = split_coco_dataset(
                dataset_dir, val_percent, test_percent, save_dir)
        elif dataset_type == "voc":
            train_num, val_num, test_num = split_voc_dataset(
                dataset_dir, val_percent, test_percent, save_dir)
        elif dataset_type == "seg":
            train_num, val_num, test_num = split_seg_dataset(
                dataset_dir, val_percent, test_percent, save_dir)
        else:
            print("The type {} is not supported now".format(dataset_type))
            return
        # elif dataset_type == "imagenet":
        #     split_imagenet_dataset(dataset_dir, val_percent, test_percent)

    print("Dataset Split Done.")
    print("Train samples: {}".format(train_num))
    print("Eval samples: {}".format(val_num))
    print("Test samples: {}".format(test_num))
    print("Split file saved in {}".format(save_dir))


if __name__ == "__main__":
    main()
