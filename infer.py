import json
import os
import logging.config

from object_detection.ditod.mytrainer import DefaultPredictor
from detectron2.data.detection_utils import read_image
from detectron2.structures import BoxMode
from tqdm import tqdm
def setup_obejct_detection_config(args):
    """
    Create configs and perform basic setups.
    """
    from object_detection.ditod.config import add_vit_config
    from detectron2.engine import  default_setup
    from detectron2.config import get_cfg
    cfg = get_cfg()
    # add_coat_config(cfg)
    add_vit_config(cfg)
    cfg.merge_from_file(args.config_file)
    cfg.merge_from_list(args.opts)
    cfg.freeze()
    default_setup(cfg, args)
    return cfg
def parser_instance(instances,img_width,img_height):
    category_id_maping=[
                {
                "id": 0,
                "name": "Caption"
                },
                {
                "id": 1,
                "name": "None"
                },
                {
                "id": 2,
                "name": "Page-footer"
                },
                {
                "id": 3,
                "name": "Page-header"
                },
                {
                "id": 4,
                "name": "Picture"
                },
                {
                "id": 5,
                "name": "Section-header"
                },
                {
                "id": 6,
                "name": "Text"
                },
                {
                "id": 7,
                "name": "Title"
                },
                {
                "id": 8,
                "name": "metainfo"
                },
                {
                "id": 9,
                "name": "note"
                },
                {
                "id": 10,
                "name": "table"
                }
            ]
    num_instance = len(instances)
    if num_instance == 0:
        return []
    boxes = instances.pred_boxes.tensor.cpu().numpy()
    boxes = BoxMode.convert(boxes, BoxMode.XYXY_ABS, BoxMode.XYWH_ABS)
    boxes = boxes.tolist()
    scores = instances.scores.tolist()
    classes = instances.pred_classes.tolist()
    results=[]
    for k in range(num_instance):
        output_label=category_id_maping[classes[k]]["name"]
        bbox=boxes[k]
        x, y, width, heigh = bbox[:4]
        result = {
            'from_name': "label",
            'to_name': "image",
            'type': 'rectanglelabels',
            "value":{
                'rectanglelabels': [output_label],
                'x': float(x) / img_width * 100,
                'y': float(y) / img_height * 100,
                'width': float(width) / img_width * 100,
                'height': float(heigh) / img_height * 100
            },
            "score": scores[k],
        }
        results.append(
            result
        )
    avg_score=sum(scores)/max(1.0,len(scores)) 
    return [{
            'result': results,
            'score': avg_score
        }]

# def main(cfg,input_dir):
#     tasks_data=[]
#     model = DefaultPredictor(cfg)
#     with open(f"{input_dir}/tasks.json","r") as tasks_file:
#         tasks_data=json.load(tasks_file)
#     for task in  tqdm(tasks_data):
#         image_name=task["data"]["image"].split("/")[-1]
#         image_path=f"{input_dir}/images/{image_name}"
#         img = read_image(image_path, format="BGR")
#         print(img.shape)
        
#         img_width,img_height=img.shape[1],img.shape[0]
#         res=model(img)
#         output_prediction=parser_instance(res["instances"],img_width,img_height)
#         task["predictions"]=output_prediction
#         #print(task)tqdm
#     with open(f"{input_dir}/prediction_tasks.json","w") as prediction_tasks_file:
#         json.dump(tasks_data,prediction_tasks_file,indent=2,ensure_ascii=False)
    
def main(cfg,input_dir):
    # 批量的推理图片
    def infer_images(images_dir):
        for image_png in os.listdir(f"{basic_image_dir}/{images_dir}"):
            image_path=f"{basic_image_dir}/{images_dir}/{image_png}"
            if "png" not in image_path:
                continue 
            try:
              img = read_image(image_path, format="BGR")
              img_width,img_height=img.shape[1],img.shape[0]
              res=model(img)
              output_prediction=parser_instance(res["instances"],img_width,img_height)
              os.makedirs(f"{infer_image_dir}/{images_dir}/",exist_ok=True)
              with open(f"{infer_image_dir}/{images_dir}/{image_png[:-4]}.json","w") as prediction_tasks_file:
                  json.dump(output_prediction,prediction_tasks_file,indent=2,ensure_ascii=False)
            except:
              print(image_path)
    model = DefaultPredictor(cfg)
    basic_image_dir=input_dir
    infer_image_dir=""
    for images_dir in tqdm(os.listdir(basic_image_dir)):
        infer_images(images_dir)
if __name__ == "__main__":
    from detectron2.engine import default_argument_parser
    parser = default_argument_parser()
    parser.add_argument(
        '-in', '--input-dir', dest='input_dir', type=str,
        help='input data dir ，it has tasks.json and images dir')
    args = parser.parse_args()
    print(args.input_dir)
    cfg = setup_obejct_detection_config(args)
    main(cfg,args.input_dir)
    

