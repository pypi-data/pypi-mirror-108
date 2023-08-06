from .iou import iou
from terminaltables import AsciiTable


def statistic_bbox_recall(preds, labels, score_thre, iou_thre, ignore_cls, classes):
    assert preds.ndim == 2 and preds.shape[-1] == 6
    assert labels.ndim == 2 and labels.shape[-1] == 5

    if ignore_cls is not None:
        ignore_cls = [ignore_cls] if not isinstance(ignore_cls, list) else ignore_cls

    tables = [['class', 'gts', 'dets', 'tps', 'fps', 'precious', 'recall']]
    total_dets = []
    total_tps = []
    total_gts = []
    for i, cls in enumerate(classes):
        if cls in ignore_cls:
            continue

        _preds = preds[preds[:, -1] == i]
        _preds = _preds[_preds[:, -2] > score_thre]
        _labels = labels[labels[:, -1] == i]

        iou_val = iou(_preds[:, 0:4], _labels[:, 0:4], iou_thre)
        gts = _labels.shape[0]
        dets = _preds.shape[0]
        tps = iou_val.shape[0]
        fps = dets - tps

        precious = tps / dets * 100
        recall = tps / gts * 100
        total_gts.append(gts)
        total_tps.append(tps)
        total_dets.append(dets)
        tables.append([cls, f'{gts}', f'{dets}', f'{tps}', f'{fps}', f'{precious:.2f}', f'{recall:.2f}'])

    total_gts = sum(total_gts)
    total_dets = sum(total_dets)
    total_tps = sum(total_tps)
    total_fps = total_dets - total_tps

    total_precious = total_tps / total_dets * 100
    total_recall = total_tps / total_gts * 100

    tables.append(['total', f'{total_gts}', f'{total_dets}', f'{total_tps}', f'{total_fps}',
                   f'{total_precious:.2f}', f'{total_recall:.2f}'])
    tables = AsciiTable(tables)
    tables.inner_footing_row_border = True

    print(tables)
