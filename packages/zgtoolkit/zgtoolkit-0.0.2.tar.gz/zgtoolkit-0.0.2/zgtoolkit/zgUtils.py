import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np
from .zgDataset import parse_annofile
from copy import deepcopy
from PIL import Image


def statistic_area(root, suffix, dst_shape=None, bins=10):
    root = Path(root)
    image_paths = root.glob('*.jpg')

    bboxes = []
    for image_path in image_paths:
        image = Image.open(image_path)
        shape = np.array(image.size, dtype=int)
        anno_path = image_path.with_suffix(suffix)
        annos = parse_annofile(anno_path, suffix)

        if dst_shape is not None:
            dst_shape = np.array(dst_shape, dtype=int)
            ratio = dst_shape / shape
            ratio = np.reshape([ratio, ratio], (-1, 4))
            annos = annos.astype(float)
            annos[:, 0:4] = annos[:, 0:4] * ratio
        bboxes.append(annos)
    bboxes = np.concatenate(bboxes, 0)

    whs = bboxes[:, 2:4] - bboxes[:, 0:2]

    areas = whs[:, 0] * whs[:, 1]
    average_wh = np.sqrt(areas)
    nums, bins, patches = plt.hist(average_wh, bins=bins, edgecolor='k')
    b_bins = deepcopy(bins[1:])
    a_bins = deepcopy(bins[0:-1])

    center = (a_bins + b_bins) / 2
    plt.xticks(center, [f'{x:.1f}' for x in center])

    for num, bin in zip(nums, bins):
        plt.annotate(f'{int(num)}', xy=(bin, num), xytext=(bin, num + 0.5))
    plt.show()


if __name__ == '__main__':
    statistic_area('/home/zg/资料/项目/铅封/样本/第二批-zk',
                   '.xml',
                   bins=50)
