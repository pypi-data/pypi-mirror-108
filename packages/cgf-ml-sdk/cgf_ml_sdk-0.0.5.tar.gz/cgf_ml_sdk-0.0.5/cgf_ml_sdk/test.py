import argparse
import sys
import os
# from core import cfg
# from model_service.framework import pytorch_utils, tensorflow_utils
# from model_service.entity.predict_entity import Framework
# from Service import Service

sys.path.append(os.path.join(os.getcwd(), "yolov3/model_service"))
os.environ["CUDA_VISIBLE_DEVICES"] = "0"

from config import *
from model import *

import numpy as np
# from core import ResNet
# from core import CustomImageLoader, data_tranforms
from SemanticSegmentEvalator import *
# 模型 数据集 配置


#     device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
#     print('device:' + str(device))
#     net = ResNet(num_classes=2, pretrained=False)
#     net.load_state_dict(torch.load('resnet_model.pth'))
#     net.eval()
#     net.to(device)
#     model = net

#     service = Service('YOLOv3Model', cfg.TEST.MODEL_PATH, '0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15')
#     service.get_model("0")
#     model = service




model = SegNet(3, 2)
data_path = "test.txt"
config = semantic_segmentation_cfg()

a = SemanticSegmentEvalator(model, data_path, config)
a.evaluate()


