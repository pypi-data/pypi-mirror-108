import argparse
import json
import sys
import os
# from core import cfg
# from model_service.framework import pytorch_utils, tensorflow_utils
# from model_service.entity.predict_entity import Framework
# from Service import Service

sys.path.append(os.path.join(os.getcwd(),"yolov3/model_service"))
os.environ["CUDA_VISIBLE_DEVICES"] = "0"


from model import *

import numpy as np
# from core import ResNet
# from core import CustomImageLoader, data_tranforms

class Evaluator(object):
    def __init__(self, model, data_path, config):
        self.Net = model
        self.data_path = data_path
        self.config = config

        self.model = 3

        self.dict = {}

    def loadConfig(self):
        dic = vars(self.config)
        if "class_num" in dic:
            self.class_num = dic["class_num"]
        if "batch_size" in dic:
            self.batch_size = dic["batch_size"]
        if "test_path" in dic:
            self.test_path = dic["test_path"]
        if "weights" in dic:
            self.weights = dic["weights"]
        if "save_path" in dic:
            self.save_path = dic["save_path"]
        if "model_path" in dic:
            self.model_path = dic["model_path"]
        if "class_dict" in dic:
            self.class_dict = dic["class_dict"]
        if "classes" in dic:
            self.classes = dic["classes"].strip().split(',')


    def loadTestData(self):
        return MyDataset(txt_path=self.data_path)

    def predictBatch(self):
        device = torch.device('cuda:0')
        self.Net.load_state_dict(torch.load(self.weights))
        self.Net.eval()

        test_loader = Data.DataLoader(self.test_data, batch_size=self.batch_size, shuffle=True)
        self.pre_resout = []
        self.gt = []
        i = 1
        for step, (t_x, t_y) in enumerate(test_loader):
            t_x, t_y = t_x.to(device), t_y.to(device)
            output = self.Net(t_x)
            output = output.argmax(dim=1)
            self.pre_resout.append(output.cpu().numpy())
            self.gt.append(t_y.cpu().numpy())
            i += 1


    def setCalParam(self, pre_resout, test_path, class_name, save_path):
        self.pre_resout = pre_resout
        self.test_path = test_path
        self.class_name = class_name
        self.save_path = save_path

    def calcluateMetrics(self):
        print("cacluateMetrics")

    def saveResult(self):

        jsonpath = self.save_path
        jsonobj = open(jsonpath, 'w')
        contjson = {}
        contjson["tables"] = []
        table = {}
        tableName = ""
        dictSon = {}
        for son in dict:
            tableName += son
            dictSon[son] = self.dict[son]
        table["tableName"] = tableName
        table["index"] = dictSon
        contjson["tables"].append(table)
        json.dump(contjson, jsonobj)

    def evaluate(self):
        self.loadConfig()
        self.test_data = self.loadTestData()
        self.predictBatch()
        self.setCalParam()
        self.calcluateMetrics()
        self.saveResult()
        print("TEST OK")





