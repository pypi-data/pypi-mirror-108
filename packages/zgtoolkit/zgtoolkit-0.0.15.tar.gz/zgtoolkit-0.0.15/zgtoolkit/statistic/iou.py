import numpy as np


def iou(preds, targets, threshold=0.1):
    """

    :param preds: [N, 4]
    :param targets: [M, 4]
    :param threshold: 0.1
    :return:
    """
    N = preds.shape[0]
    M = targets.shape[0]
    preds = np.tile(np.expand_dims(preds, 1), [1, M, 1])
    targets = np.tile(np.expand_dims(targets, 0), [N, 1, 1])

    overlap_tl = np.maximum(preds[..., 0:2], targets[..., 0:2])
    overlap_rb = np.minimum(preds[..., 2:], targets[..., 2:])
    overlap_wh = np.maximum(overlap_rb - overlap_tl, 0.)
    overlap_area = overlap_wh[..., 0] * overlap_wh[..., 1]

    preds_wh = preds[..., 2:] - preds[..., 0:2]
    preds_area = preds_wh[..., 0] * preds_wh[..., 1]

    targets_wh = targets[..., 2:] - targets[..., 0:2]
    targets_area = targets_wh[..., 0] * targets_wh[..., 1]

    iou = overlap_area / (preds_area + targets_area - overlap_area)
    return iou[iou > threshold]
