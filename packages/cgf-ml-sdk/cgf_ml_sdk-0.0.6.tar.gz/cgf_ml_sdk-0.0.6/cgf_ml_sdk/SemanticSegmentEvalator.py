import json
import numpy as np
from .Evaluator import *

class SemanticSegmentEvalator(Evaluator):
    """
    gt_image: numpy矩阵数据的真实标签 n*H*W n为数量 标签为 0~(n-1) (带背景)
    pre_image: numpy矩阵与gt_image对应的预测结果，同为 n*H*W n为数量 标签为 0~(n-1) (带背景)
    num_class: 类别数量
    class_name: 类别名 字典结构 {int（0-（n-1））：String，int：String}
    save_path: json文件存储路径
    """
    # 初始化数据
    def setCalParam(self, gt, pre_resout, num_class, class_name, save_path):
        gt_image = None
        pre_image = None
        for i in range(len(pre_resout)):
            if i == 0:
                pre_image = pre_resout[i]
                gt_image = gt[i]
            else:
                pre_image = np.concatenate((pre_image,pre_resout[i]),axis=0)
                    # torch.cat((pre_image, pre[i]), 0)
                gt_image = np.concatenate((gt_image,gt[i]),axis=0)
                    # torch.cat((gt_image, gt[i]), 0)
        self.gt_image = gt_image
        self.pre_image = pre_image
        self.num_class = num_class
        self.class_name = class_name
        self.save_path = save_path


    def calcluateMetrics(self, gt_image, pre_image, num_class):
        cal = SemanticSegmentCal(num_class)
        cal.set_confusion(gt_image, pre_image)

        PA = cal.Pixel_Accuracy()

        MPA_all = cal.Pixel_Accuracy_Class()
        # print(MPA_all)
        MPA = np.nanmean(MPA_all)

        MIou_all = cal.Mean_Intersection_Over_Union()
        # print(MIou_all)
        MIou = np.nanmean(MIou_all)

        FWIou = cal.Frequency_Weighted_Intersection_Over_Union()

        self.dict["PA"] = PA
        self.dict["MPA_all"] = MPA_all
        self.dict["MPA"] = MPA
        self.dict["MIou_all"] = MIou_all
        self.dict["MIou"] = MIou
        self.dict["FWIou"] = FWIou
        # self.PA = PA
        # self.MPA_all = MPA_all
        # self.MPA = MPA
        # self.MIou_all = MIou_all
        # self.MIou = MIou
        # self.FWIou = FWIou

    def predictBatch(self):
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

    # def saveResult(self):
    #     self.calcluateMetrics(self.gt_image, self.pre_image, self.num_class)
    #
    #     jsonpath = self.save_path
    #     jsonobj = open(jsonpath, 'w')
    #     contjson = {}
    #     contjson["tables"] = []
    #     table = {}
    #     table["tableName"] = "像素准确率；平均像素准确率；平均交并比；频权交并比"
    #     table["all_class"] = {"PA": self.dict["PA"], "MPA": self.dict["MPA"], "MIou": self.dict["MIou"], "FWIou": self.dict["FWIou"]}
    #     for i in range(len(self.dict["MPA_all"])):
    #         table[self.class_name[i]] = {"PA": self.dict["MPA_all"][i], "MPA": None, "MIou": self.dict["MIou_all"][i], "FWIou": None}
    #     contjson["tables"].append(table)
    #     json.dump(contjson, jsonobj)

    def evaluate(self):
        self.loadConfig()
        self.test_data = self.loadTestData()
        self.predictBatch()

        self.setCalParam(
            self.gt,
            self.pre,
            self.class_num,
            self.class_dict,
            self.save_path
        )

        self.saveResult()
        print("TEST OK")



class SemanticSegmentCal(object):
    # 初始化数据
    def __init__(self, num_class):
        self.num_class = num_class
        self.confusion = np.zeros((self.num_class,) * 2)

    # 计算像素准确率（PA）
    # acc = (TP + TN) / (TP + TN + FP + TN)
    def Pixel_Accuracy(self):
        PA = np.diag(self.confusion).sum() / \
              self.confusion.sum()
        return PA

    # 计算平均像素准确率（MPA）
    # acc = (TP) / TP + FP
    def Pixel_Accuracy_Class(self):
        MPA_all = np.diag(self.confusion) / \
              self.confusion.sum(axis=1)
        # MPA = np.nanmean(MPA_all)
        return MPA_all

    # 计算平均交并比（MIou）
    # Iou = TP / (TP + FP + FN)
    def Mean_Intersection_Over_Union(self):
        MIou_all = np.diag(self.confusion) / (
                np.sum(self.confusion, axis=1) + np.sum(self.confusion, axis=0) -
                np.diag(self.confusion))
        # MIou = np.nanmean(MIou_all)
        return MIou_all

    # 计算频权交并比（FWIou）
    # FWIou = [(TP + FN)/(TP + FP + TN + FN)] * [TP / (TP + FP + FN)]
    def Frequency_Weighted_Intersection_Over_Union(self):
        freq = np.sum(self.confusion, axis=1) / \
               np.sum(self.confusion)
        iu = np.diag(self.confusion) / (
                np.sum(self.confusion, axis=1) + np.sum(self.confusion, axis=0) -
                np.diag(self.confusion))

        FWIou = (freq[freq > 0] * iu[freq > 0]).sum()
        return FWIou

    # 生成矩阵
    def generate_matrix(self, gt_image, pre_image):
        mask = (gt_image >= 0) & (gt_image < self.num_class)
        label = self.num_class * gt_image[mask].astype('int') + pre_image[mask]

        label = label.astype(int)

        count = np.bincount(label, minlength=self.num_class ** 2)
        confusion = count.reshape(self.num_class, self.num_class)
        return confusion

    # 设置混淆矩阵
    def set_confusion(self, gt_image, pre_image):
        assert gt_image.shape == pre_image.shape
        self.confusion += self.generate_matrix(gt_image, pre_image)
