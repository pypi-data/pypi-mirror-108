from glob import glob
import xml.etree.ElementTree as ET
import os
from ..utils import track_iter_progress

def modify_label(root, suffix, old_label, new_label):
    assert '.' in suffix
    anno_paths = glob(os.path.join(root, f'*{suffix}'))

    for anno_path in track_iter_progress(anno_paths):
        if 'xml' in suffix:
            datas = ET.parse(str(anno_path))
            for name in datas.iter('name'):
                if name.text == old_label:
                    name.text = new_label
            datas.write(str(anno_path), encoding='utf-8')
