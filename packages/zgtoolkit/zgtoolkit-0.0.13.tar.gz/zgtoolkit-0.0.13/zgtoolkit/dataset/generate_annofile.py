from pathlib import Path
import numpy as np
from shutil import rmtree
from glob import glob
import os
import random
from ..utils import track_iter_progress
from .parse import parse_label


def write_oneline(path, annofile, label_suffix, classes):
    path = Path(path)

    base_name = path.parent
    stem = path.stem
    anno_path = base_name / Path(stem + label_suffix)
    annofile.write(str(path))

    if 'xml' in label_suffix:
        objs = parse_label(anno_path, label_suffix, classes)

    for obj in objs:
        annofile.write(' ')
        annofile.write(','.join([str(x) for x in obj]))
    annofile.write('\n')


def generate_annofile(root, label_suffix, classes, image_format='jpg'):
    if Path('anno').exists():
        rmtree('anno')
    os.mkdir('anno')

    train_anno = open('anno/train.txt', 'w', encoding='utf-8')
    test_anno = open('anno/test.txt', 'w', encoding='utf-8')

    if not isinstance(root, list):
        root = [root]
    image_paths = [glob(os.path.join(x, f'*.{image_format}')) for x in root]
    image_paths = np.concatenate(image_paths).tolist()
    random.shuffle(image_paths)

    total = len(image_paths)
    default_train = int(len(image_paths) * 0.8)
    default_test = total - default_train
    print(f'total: {total}, default_train: {default_train}, '
          f'default_test: {default_test}')
    test_num = input('input test_num:')
    if test_num is '':
        test_num = default_test

    test_image_paths = random.sample(image_paths, int(test_num))
    train_image_paths = list(set(image_paths) - set(test_image_paths))

    for train_image_path in track_iter_progress(train_image_paths):
        write_oneline(train_image_path, train_anno, label_suffix, classes)

    for test_image_path in track_iter_progress(test_image_paths):
        write_oneline(test_image_path, test_anno, label_suffix, classes)

    train_anno.close()
    test_anno.close()
