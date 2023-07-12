from flask import Flask, render_template, request,jsonify
import json
import json
import numpy as np
app = Flask(__name__)
from object_detection.ditod.mytrainer import DefaultPredictor
from PIL import Image
import io
from detectron2.structures import BoxMode

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
    boxes = instances.pred_boxes.tensor.cpu().numpy() # bug fix 需要区分是否cuda模式下
    boxes = BoxMode.convert(boxes, BoxMode.XYXY_ABS, BoxMode.XYWH_ABS)
    boxes = boxes.tolist()
    scores = instances.scores.tolist()
    classes = instances.pred_classes.tolist()
    results=[]
    for k in range(num_instance):
        print(classes[k])
        
        #output_label=self.category_id_maping[classes[k]]["name"]
        output_label=category_id_maping[classes[k]]["name"]
        bbox=boxes[k]
        x, y, width, heigh = bbox[:4]
        result = {
            'from_name': "label",
            'to_name': "image",
            'type': 'rectanglelabels',
            "value":{
                "origin_bbox": bbox[:4],
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

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)
@app.route("/",methods = ['GET', 'POST'])
def hello_world():
    if request.method =="POST":
      model_predictor=globals()['lv3_predictor']
      image_bytes = request.files['file'].read()
      print(image_bytes)
      original_image=Image.open(io.BytesIO(image_bytes))
      image = np.asarray(original_image)
      res=model_predictor(image)
      return jsonify(json.loads(json.dumps(parser_instance(res["instances"],original_image.width,original_image.height),cls=NpEncoder)))
    html="""
    <html>
    <body>
      <form action = "/" method = "POST" 
         enctype = "multipart/form-data">
         <input type = "file" name = "file" />
         <input type = "submit"/>
      </form>   
    </body>
    </html>
    """
    return html
if __name__ == "__main__":
    from _wsgi import setup_obejct_detection_config
    from detectron2.engine import default_argument_parser
    parser = default_argument_parser()
    args = parser.parse_args()
    cfg = setup_obejct_detection_config(args)
    globals()['lv3_predictor']=DefaultPredictor(cfg)
    app.run()