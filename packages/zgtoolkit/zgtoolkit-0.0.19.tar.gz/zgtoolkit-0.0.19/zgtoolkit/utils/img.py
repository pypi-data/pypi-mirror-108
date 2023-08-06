import cv2 as cv
from PIL import Image
import numpy as np
import bbox_visualizer as bbv
from albumentations import PadIfNeeded


def imread(pathname):
    image = Image.open(pathname)
    image = cv.cvtColor(np.asarray(image, np.uint8), cv.COLOR_RGB2BGR)
    return image


def imwrite(pathname, image):
    image = Image.fromarray(cv.cvtColor(image, cv.COLOR_BGR2RGB))
    image.save(pathname)


def cv2pil(image):
    return Image.fromarray(cv.cvtColor(image, cv.COLOR_BGR2RGB))


def pil2cv(image):
    return cv.cvtColor(np.asarray(image, np.uint8), cv.COLOR_RGB2BGR)


def imshow(win_name: str,
           image,
           ratio,
           is_fixedsize=False,
           size=None):
    h, w, _ = image.shape

    if is_fixedsize:
        dst_w, dst_h = size
        ratio = min(dst_w / w, dst_h / h)
        w, h = int(ratio * w), int(ratio * h)

        img = cv.resize(image, (w, h))
        img = PadIfNeeded(dst_h, dst_w,
                          border_mode=cv.BORDER_CONSTANT,
                          value=(0, 0, 0),
                          always_apply=True)(image=img)['image']
    else:
        if ratio is not None:
            h = int(h * ratio)
            w = int(w * ratio)
        img = cv.resize(image, (w, h))

    cv.imshow(win_name, img)
    cv.waitKey()


def imshow_with_bbox(win_name: str,
                     image,
                     bboxes: np.ndarray,
                     classes,
                     is_show=True,
                     thickness=1,
                     is_opaque=False,
                     top=True):
    assert bboxes.shape[-1] == 5

    labels = bboxes[:, -1].tolist()
    labels = [classes[int(x)] for x in labels]
    image = bbv.draw_multiple_rectangles(image, bboxes[:, 0:4].tolist(), is_opaque=is_opaque, thickness=thickness)
    image = bbv.add_multiple_labels(image, labels, bboxes[:, 0:4].tolist(), top=top)

    if is_show:
        cv.imshow(win_name, image)
        cv.waitKey()

    return image
