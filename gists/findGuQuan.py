# 找到股权结构图的图片。
# 找到有picture的图片，然后再找到对应的图片。 然后再进行
import os
import tqdm
import json
import shutil
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


if __name__=="__main__":
    collect_image_from_ocr(
        "/media/liukun/7764-4284/cninfo/CnInfoReports/pdfs/ndbg_zy_ocrs",
        "/media/liukun/7764-4284/cninfo/CnInfoReports/pdfs/ndbg_zy_images",
        "/media/liukun/7764-4284/cninfo/CnInfoReports/pdfs/ndbg_guquan_images"
    )
    #find_gu_quan_jie_guo_tu_from_ocr("/media/liukun/7764-4284/cninfo/CnInfoReports/pdfs/ndbg_zy_ocrs")