# -*- coding: utf-8 -*-
"""
File Name：     youyou
Author:        zj
date：          2021/5/24
Description :
"""

import os
import json
from PIL import Image
from torch.utils.data import Dataset

from .evaluator.general_evaluator import GeneralEvaluator


class YYDataset(Dataset):

    def __init__(self, root, transform=None, target_transform=None, top_k=(1, 5)):
        assert os.path.isfile(root)

        self.root = root
        self.transform = transform
        self.target_transform = target_transform
        self.top_k = top_k

        with open(self.root, 'r') as f:
            file_dict = json.load(f)

        class_label_dict = dict()
        for idx, class_name in enumerate(list(file_dict.keys()), 0):
            class_label_dict[class_name] = idx

        label_list = list()
        path_list = list()
        for k, v in file_dict.items():
            for path in v:
                label_list.append(class_label_dict[k])
                path_list.append(path)

        self.label_list = label_list
        self.path_list = path_list

        self.classes = list(file_dict.keys())
        self.length = len(self.label_list)

        self._update_evaluator(self.top_k)

    def __getitem__(self, index: int):
        # if not hasattr(self, 'length'):
        #     self.init_data()
        assert index < self.length

        img_path = self.path_list[index]
        image = Image.open(img_path)
        target = self.label_list[index]
        if self.transform is not None:
            image = self.transform(image)
        if self.target_transform is not None:
            target = self.target_transform(target)

        # print(image.shape, target, type(target))
        return image, target

    def __len__(self) -> int:
        # if not hasattr(self, 'length'):
        #     self.init_data()
        return self.length

    def _update_evaluator(self, top_k):
        self.evaluator = GeneralEvaluator(self.classes, top_k=top_k)

    def get_classes(self):
        # if not hasattr(self, 'classes'):
        #     self.init_data()
        return self.classes

    def __repr__(self):
        return self.__class__.__name__ + ' (' + self.root + ')'

    # def init_data(self):
    #     with open(self.root, 'r') as f:
    #         file_dict = json.load(f)
    #
    #     class_label_dict = dict()
    #     for idx, class_name in enumerate(file_dict.keys(), 0):
    #         class_label_dict[class_name] = idx
    #
    #     label_list = list()
    #     path_list = list()
    #     for k, v in file_dict.items():
    #         for path in v:
    #             label_list.append(class_label_dict[k])
    #             path_list.append(path)
    #
    #     self.label_list = label_list
    #     self.path_list = path_list
    #
    #     self.classes = file_dict.keys()
    #     self.length = len(self.label_list)
    #
    #     self._update_evaluator(self.top_k)
