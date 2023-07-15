# 找到股权结构图的图片。
# 找到有picture的图片，然后再找到对应的图片。 然后再进行
import os
from tqdm import tqdm
import json
import shutil
from PIL import Image
from math import ceil # 下取整数
def load_json(json_path):
    data=[]
    with open(json_path,"r") as jf:
        data=json.load(jf)
    return data
def find_gu_quan_jie_guo_tu_from_ocr(ocr_dir):
    # 从OCR中找到一个包含方框图的东西
    LOC_INDEX=0
    TEXT_SCORE_Index=1
    TEXT_Index=0
    ans=[]
    for pdf_dir in os.listdir(ocr_dir):
        for ocr_json_path in os.listdir(f"{ocr_dir}/{pdf_dir}"):
            ocr_json=load_json(f"{ocr_dir}/{pdf_dir}/{ocr_json_path}")
            for ocr_span_data in ocr_json[0]:
                if "方框图" in ocr_span_data[TEXT_SCORE_Index][TEXT_Index]:
                    #print(f"{ocr_dir}/{pdf_dir}/{ocr_json_path}",ocr_span_data[TEXT_SCORE_Index][TEXT_Index])
                    ans.append(
                        f"{pdf_dir}/{ocr_json_path[:-5]}"
                    )
                    break
    print(len(ans))
    return ans
def collect_image_from_ocr(ocr_dir,image_dir,output_dir):
    # 把股权结构图放到指定的位置
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    image_path_list=find_gu_quan_jie_guo_tu_from_ocr(ocr_dir)
    for  image_path in image_path_list:
        pdf_name,png_name=image_path.split("/")

        abs_image_dir_path=f"{image_dir}/{pdf_name}"

        if os.path.exists(abs_image_dir_path):
            pg_no_name=png_name.split("-")[-1]
            for rel_image_path in os.listdir(abs_image_dir_path):
                if f"-{pg_no_name}.png" in rel_image_path:
                    shutil.copy2( f"{abs_image_dir_path}/{rel_image_path}"
                                 ,
                                 f"{output_dir}/{rel_image_path}")
def crop_capital_graph():
    """
    裁剪股权结构图
    """
    def find_layout(captital_picture_name):
        # 找到layout的文件
        if ".png" not in captital_picture_name:
            return []
        pure_name=captital_picture_name.replace(".png","")# 不打算兼容了
        stock_code=pure_name[:6]
        image_layout_path=f"{basic_capital_graph_layout_dir}/{stock_code}/{pure_name}.json"
        if not os.path.exists(image_layout_path):
            print(f"warning!!!  {image_layout_path} no layout file")
            return []
        json_data=load_json(image_layout_path)
        return json_data
    def crop_capital_picture(captital_picture_name,out_dir):
        json_data=find_layout(captital_picture_name)
        if not json_data :
            print(f"error:{captital_picture_name} 没有文件")
            return
        picture_coor_list=[]
        for row_data in json_data[0]["result"]:
            #data example {'from_name': 'label', 'to_name': 'image', 'type': 'rectanglelabels', 'value': {'rectanglelabels': [...], 'x': 14.595892466829937, 'y': 86.39342922489578, 'width': 14.544060556026583, 'height': 2.0294724391433308}, 'score': 0.9999479651451111}
            if "Picture" in row_data["value"]["rectanglelabels"]:
                #x,y,width,height=row_data["value"]["x"],row_data["value"]["y"],row_data["value"]["width"],row_data["value"]["height"]
                picture_coor_list.append(
                    row_data
                )
        if not picture_coor_list:
            return 
        image_path=f"{basic_capital_graph_dir}/{captital_picture_name}"
        img=Image.open(image_path)
        original_width,original_height=img.width,img.height
        X_Index,Y_Index,Width_Index,Height_Index=0,1,2,3
        picture_count=1
        pure_name=captital_picture_name.replace(".png","")
        for row_data in picture_coor_list:
            x,y=int(row_data["value"]["x"]*original_width*0.01),int(row_data["value"]["y"]*original_height*0.01)
            x=max(x-20,5)
            width,height=ceil(row_data["value"]["width"]*original_width*0.01+40),ceil(row_data["value"]["height"]*original_height*0.01)
            if width< 150 or height<150:
                # 临时的办法，删除一些识别错的
                continue 
            crop_img=img.crop([x,y,x+width,y+height])
        
            crop_img.save(f"{out_dir}/{pure_name}-{picture_count}.png",format='png')
            picture_count+=1
            
            


        
         
    basic_capital_graph_dir="/media/liukun/7764-4284/cninfo/CnInfoReports/pdfs/captial_graph"
    basic_capital_graph_layout_dir="/media/liukun/7764-4284/cninfo/CnInfoReports/pdfs/ndbg_zy_infer"
    basic_capital_graph_crop_dir="/media/liukun/7764-4284/cninfo/CnInfoReports/pdfs/captial_graph_crop"# 裁剪的图片
    for captital_picture_name in tqdm(os.listdir(basic_capital_graph_dir)):
        #layout_json=find_layout(captital_picture_name)
        crop_capital_picture(captital_picture_name,basic_capital_graph_crop_dir) 


if __name__=="__main__":
    # collect_image_from_ocr(
    #     "/media/liukun/7764-4284/cninfo/CnInfoReports/pdfs/ndbg_zy_ocrs",
    #     "/media/liukun/7764-4284/cninfo/CnInfoReports/pdfs/ndbg_zy_images",
    #     "/media/liukun/7764-4284/cninfo/CnInfoReports/pdfs/ndbg_guquan_images"
    # )
    #find_gu_quan_jie_guo_tu_from_ocr("/media/liukun/7764-4284/cninfo/CnInfoReports/pdfs/ndbg_zy_ocrs")
    crop_capital_graph()
    pass