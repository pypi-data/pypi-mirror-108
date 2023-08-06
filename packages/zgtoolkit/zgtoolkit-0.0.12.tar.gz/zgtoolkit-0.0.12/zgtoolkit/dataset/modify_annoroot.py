import os
from pathlib import Path
from glob import glob
import numpy as np
from ..utils import track_iter_progress


def modify_annoroot(anno_path, root, image_format='.jpg'):
    assert '.' in image_format
    if not isinstance(root, list):
        root = [root]

    image_paths = [glob(os.path.join(x, f'*{image_format}')) for x in root]
    image_paths = np.concatenate(image_paths).tolist()
    image_names = ['/'.join(Path(x).parts[-2:]) for x in image_paths]
    with open(anno_path, 'r') as f:
        datas = f.readlines()
        new_datas = []
        for line in track_iter_progress(datas):
            annos = line.split(' ')
            image_path = annos[0]
            if '\\' in image_path:
                image_path = image_path.replace('\\', '/')

            image_path = Path(image_path)
            name = '/'.join(Path(image_path).parts[-2:])
            if name in image_names:
                index = image_names.index(name)
                image_path = image_paths[index]
                annos[0] = image_path
            line = ' '.join(annos)
            new_datas.append(line)
    with open(anno_path, 'w') as f:
        f.writelines(new_datas)
