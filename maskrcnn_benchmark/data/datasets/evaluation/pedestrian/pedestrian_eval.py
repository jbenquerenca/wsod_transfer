import json, os, logging
from .coco import COCO
from .eval_MR_multisetup import COCOeval

def validate(dataset, detections, output_folder=None):
    logger = logging.getLogger("maskrcnn_benchmark.inference")
    MRs, my_id_setup = list(), list()
    cocoRes = prepare_coco_results(detections, dataset)
    if output_folder: json.dump(cocoRes, open(os.path.join(output_folder, "coco_results.json"), "w"))
    for id_setup in range(0, 4):
        cocoGt = COCO(dataset._anno_path)
        cocoDt = cocoGt.loadRes(cocoRes)
        imgIds = sorted(cocoGt.getImgIds())
        cocoEval = COCOeval(cocoGt, cocoDt, 'bbox')
        cocoEval.params.imgIds = imgIds
        cocoEval.evaluate(id_setup)
        cocoEval.accumulate()
        MRs.append(cocoEval.summarize_nofile(id_setup))
        my_id_setup.append(id_setup)
    logger.info('[Reasonable: %.2f%%], [Reasonable_Small: %.2f%%], [Heavy: %.2f%%], [All: %.2f%%]'%(MRs[0] * 100, MRs[1] * 100, MRs[2] * 100, MRs[3] * 100))
    return MRs

def prepare_coco_results(predictions, dataset):
    coco_results = list()
    for image_id, prediction in enumerate(predictions):
        if len(prediction.bbox) == 0: continue
        original_id = dataset.id_to_img_map[image_id]
        img_info = dataset.get_img_info(image_id)
        image_width = img_info["width"]
        image_height = img_info["height"]
        prediction = prediction.resize((image_width, image_height))
        prediction = prediction.convert("xywh")
        boxes = prediction.bbox.tolist()
        scores = prediction.get_field("scores").tolist()
        labels = prediction.get_field("labels").tolist()
        # TODO: Hacky way to solve this problem where I consider all predictions from the model as 1
        mapped_labels = [1 for i in labels] # [dataset.contiguous_category_id_to_json_id[i] for i in labels]
        coco_results.extend([{"image_id": original_id, "category_id": mapped_labels[k], "bbox": box, "score": scores[k]} for k, box in enumerate(boxes)])
    return coco_results