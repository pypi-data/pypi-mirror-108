import argparse
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
        if self.model == 1:
            return CustomImageLoader(self.config.TEST_FILE_PATH, data_transforms=data_tranforms['Test'])
        if self.model == 3:
            test_data = MyDataset(txt_path=self.data_path)
            print(len(test_data))
            return test_data

    def predictBatch(self):
        if self.model == 1:
            testloader = torch.utils.data.DataLoader(self.test_data, batch_size=self.config.batch_size,
                                                     shuffle=False, num_workers=self.config.num_workers)
            dataset_size = len(self.test_data)

            correct = 0
            total = 0
            self.y_pred = []
            self.y_score = []
            with torch.no_grad():
                img_cnt = 0
                for data in testloader:
                    images, labels = data
                    img_cnt += images.size(0)
                    print('Testing image {:d}/{:d}'.format(img_cnt, dataset_size))
                    images = images.to(self.device)
                    labels = torch.from_numpy(np.array(data[1])).to(self.device)
                    outputs = self.Net(images)
                    score, predicted = torch.max(torch.softmax(outputs, 0), 1)
                    # classes[predicted[j]] for j in range(batch_size))
                    total += labels.size(0)
                    correct += (predicted == labels).sum().item()
                    self.y_pred.extend(predicted.cpu().numpy())
                    self.y_score.extend(score.cpu().numpy())
        if self.model == 2:
            with open(self.test_path, 'r') as annotation_file:
                i = 0
                path_array = []
                self.pre_resout = []
                for num, line in enumerate(annotation_file):
                    annotation = line.strip().split()
                    image_path = annotation[0]
                    image_name = image_path.split('/')[-1]
                    print("path******", image_path)
                    path_array.append(image_path)
                    i += 1
                    if i == self.batch_size:
                        # 新预测执行
                        dict, _ = self.Net._preprocess(
                            path_array,
                            '')
                        for k, v in dict.items():
                            if k == "data":
                                input_array = v
                            else:
                                pass_param = v
                        input_file_matrix = self.Net._concatenate_matrix(matrix_list=input_array)
                        output_matrix = self.Net._inference(input_file_matrix)
                        if self.Net.framework == Framework.tensorflow.value:
                            output_matrix = tensorflow_utils.split_matrix(output_matrix)
                        else:
                            output_matrix = pytorch_utils.split_matrix(output_matrix)
                        for index, param in enumerate(pass_param):
                            a = self.Net._postprocess(self.Net._get_single_result(output_matrix, index), param)
                            self.pre_resout.append(a)
                        # 预测结束
                        print("One batch OK!")
                        i = 0
                        path_array = []
                if i != 0:
                    dict, _ = self.Net._preprocess(
                        path_array,
                        '')
                    for k, v in dict.items():
                        if k == "data":
                            input_array = v
                        else:
                            pass_param = v
                    input_file_matrix = self.Net._concatenate_matrix(matrix_list=input_array)
                    output_matrix = self.Net._inference(input_file_matrix)
                    if self.Net.framework == Framework.tensorflow.value:
                        output_matrix = tensorflow_utils.split_matrix(output_matrix)
                    else:
                        output_matrix = pytorch_utils.split_matrix(output_matrix)
                    for index, param in enumerate(pass_param):
                        a = self.Net._postprocess(self.Net._get_single_result(output_matrix, index), param)
                        self.pre_resout.append(a)
        if self.model == 3:
            device = torch.device('cuda:0')
            self.Net.to(device)
            self.Net.load_state_dict(torch.load(self.weights))
            self.Net.eval()

            test_loader = Data.DataLoader(self.test_data, batch_size=self.batch_size, shuffle=True)

            self.pre = []
            self.gt = []

            i = 1
            for step, (t_x, t_y) in enumerate(test_loader):
                t_x, t_y = t_x.to(device), t_y.to(device)
                output = self.Net(t_x)
                output = output.argmax(dim=1)
                self.pre.append(output.cpu().numpy())
                self.gt.append(t_y.cpu().numpy())
                print(i)
                i += 1


    def setCalParam(self):
        print("setCalParam")

    def calcluateMetrics(self):
        print("cacluateMetrics")

    def saveResult(self):
        print("saveResult")

    def evaluate(self):
        self.loadConfig()
        self.test_data = self.loadTestData()
        self.predictBatch()

        self.setCalParam()

        self.saveResult()
        print("TEST OK")





