import xml.etree.ElementTree as ET
from glob import glob
import os

from ..utils import track_iter_progress


def print_label(root, suffix):
    assert '.' in suffix
    anno_paths = glob(os.path.join(root, f'*{suffix}'))

    labels = []
    for anno_path in track_iter_progress(anno_paths):
        if 'xml' in suffix:
            datas = ET.parse(str(anno_path))
            for name in datas.iter('name'):
                labels.append(name.text)

    print(set(labels))
