import os
from pathlib import Path
from glob import glob
import numpy as np
from ..utils import track_iter_progress
from .generate_annofile import parse_annofile


def modify_annocls(anno_path, root, classes, suffix, image_format='.jpg'):
    assert '.' in image_format
    assert '.' in suffix
    if not isinstance(root, list):
        root = [root]

    label_paths = [glob(os.path.join(x, f'*{suffix}')) for x in root]
    label_paths = np.concatenate(label_paths).tolist()
    label_names = ['/'.join(Path(x).parts[-2:]) for x in label_paths]
    with open(anno_path, 'r') as f:
        datas = f.readlines()
        new_datas = []
        for line in track_iter_progress(datas):
            annos = line.split(' ')
            image_path = annos[0]
            if '\\' in image_path:
                image_path = image_path.replace('\\', '/')

            label_path = Path(image_path).with_suffix(suffix)
            name = '/'.join(Path(label_path).parts[-2:])
            if name in label_names:
                index = label_names.index(name)
                label_path = label_paths[index]
                objs = parse_annofile(label_path, suffix, classes)
                objs = objs.astype(str)
                annos[1:] = [','.join(x) for x in objs]
            line = ' '.join(annos)
            new_datas.append(line)
    with open(anno_path, 'w') as f:
        f.writelines(new_datas)
