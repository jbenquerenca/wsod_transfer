from PIL import Image
from collections import defaultdict
from maskrcnn_benchmark.structures.bounding_box import BoxList
import torch, torch.utils.data, os, json

class PedestrianDataset(torch.utils.data.Dataset):

    def __init__(self, data_dir, split, transforms=None, remove_images_without_annotations=True):
        self.root = data_dir
        self.image_set = split
        self._anno_path = os.path.join(self.root, "annotations", f"{self.image_set}.json")
        self._anno_file = json.load(open(self._anno_path))
        self._imgpath = os.path.join(self.root, "images")
        self.ids = sorted([im["id"] for im in self._anno_file["images"]])
        self.imgToAnns, self.imgs = defaultdict(list), dict()
        for ann in self._anno_file["annotations"]: self.imgToAnns[ann["image_id"]].append(ann)
        for img in self._anno_file["images"]: self.imgs[img["id"]] = img
        self.json_category_id_to_contiguous_id = {v: i + 1 for i, v in enumerate([cat["id"] for cat in self._anno_file["categories"]])}
        self.contiguous_category_id_to_json_id = {v: k for k, v in self.json_category_id_to_contiguous_id.items()}
        # filter images without detection annotations (for training the frcnn only)
        if remove_images_without_annotations:
            ids = list()
            for img_id in self.ids:
                anns = self.imgToAnns[img_id]
                if len(anns) == 0: continue
                valid = False
                for ann in anns:
                    if ann["iscrowd"] == 0 and ann["ignore"] == 0: valid = True
                if valid: ids.append(img_id)
            self.ids = ids
        self.id_to_img_map = {k: v for k, v in enumerate(self.ids)}
        self._transforms = transforms
        self.categories = {cat['id']: cat['name'] for cat in self._anno_file["categories"]}

    def __len__(self): return len(self.ids)
    
    def get_img_info(self, index): return self.imgs[self.ids[index]]
    
    def _load_image(self, file_name): return Image.open(os.path.join(self._imgpath, file_name)).convert("RGB")

    def _load_target(self, anns): 
        targets = list()
        for ann in anns:
            if ann["iscrowd"] == 0 and ann["ignore"] == 0: targets.append(ann)
        return targets

    def __getitem__(self, idx):
        img_id = self.ids[idx]
        img_file_name = self.imgs[img_id]["file_name"]
        img, anno = self._load_image(img_file_name), self._load_target(self.imgToAnns[img_id])
        if len(anno) == 0: print(img); exit()
        boxes = [obj["bbox"] for obj in anno]
        boxes = torch.as_tensor(boxes).reshape(-1, 4)
        target = BoxList(boxes, img.size, mode="xywh").convert("xyxy")
        classes = [obj["category_id"] for obj in anno]
        classes = [self.json_category_id_to_contiguous_id[c] for c in classes]
        classes = torch.tensor(classes)
        target.add_field("labels", classes)
        target = target.clip_to_image(remove_empty=False)
        if self._transforms is not None: img, target = self._transforms(img, target)
        return img, target, idx