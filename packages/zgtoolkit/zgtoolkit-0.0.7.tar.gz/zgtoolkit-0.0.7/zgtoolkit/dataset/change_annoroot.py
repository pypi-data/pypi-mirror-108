import os
from pathlib import Path
from glob import glob
import numpy as np
from zgtoolkit.utils import track_iter_progress


def change_annoroot(anno_path, root, image_format='.jpg'):
    assert '.' in image_format
    if not isinstance(root, list):
        root = [root]

    image_paths = [glob(os.path.join(x, f'*{image_format}')) for x in root]
    image_paths = np.concatenate(image_paths).tolist()
    image_names = [Path(x).name for x in image_paths]
    with open(anno_path, 'r', encoding='utf-8') as f:
        datas = f.readlines()
        new_datas = []
        for line in track_iter_progress(datas):
            annos = line.split(' ')
            image_path = annos[0]
            image_path = image_path.replace('\\', '/')
            name = Path(image_path).name
            if name in image_names:
                index = image_names.index(name)
                image_path = image_paths[index]
                annos[0] = image_path
            line = ' '.join(annos)
            new_datas.append(line)
    with open(anno_path, 'w', encoding='utf-8') as f:
        f.writelines(new_datas)


if __name__ == '__main__':
    change_annoroot('/home/zg/项目/铅封/工程/detection-classification/detection/train.txt',
                    ['/home/zg/资料/项目/铅封/样本/原始样本-多目标+分类',
                     '/home/zg/资料/项目/铅封/样本/第二批-zk',
                     '/home/zg/资料/项目/铅封/样本/第二批-lh'])
