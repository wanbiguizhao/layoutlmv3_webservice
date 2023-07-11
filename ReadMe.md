# 安装
## 创建环境
conda create -n lv3_ws  python=3.9   不要随意切换Python版本
conda activate lv3_ws
git clone https://github.com/heartexlabs/label-studio-ml-backend  
cd label-studio-ml-backend && pip install -U -e .


## layoutlm3 
pip install -r lv3req.txt
### torch and cuda 
#pip install torch==1.10.0+cu111 torchvision==0.11.1+cu111 -f https://download.pytorch.org/whl/torch_stable.html # 以前的链接失效了
pip install torch==1.12.0+cu113 torchvision==0.11.1+cu113 -f https://download.pytorch.org/whl/torch_stable.html # 以前的链接失效了


### detectron2
pip install detectron2 -f https://dl.fbaipublicfiles.com/detectron2/wheels/cu111/torch1.10/index.html


## 年报摘要

pip install -r apps/nbzy/requestments.txt