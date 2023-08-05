from .Evaluator import *

import core as utils
import json
import numpy as np
import cv2
import os

class ObjectDetectionEvaluator(Evaluator):
    """
    docstring
    """

    """
    传入testout的path，保存在此路径下
    file_path:最后保存的文件的地址
    annotation_path:标注文件的路径
    types:对应的类别,[swiming pool,car]
    """
    def setCalParam(self, annotation_path, bboxes, types, file_path):
        self.file_path = file_path
        self.annotation_path = annotation_path
        self.types = types
        self.bboxes = bboxes


    """
    保存annotation和预测之间的差异
    """

    def calcluateMetrics(self, file_path, threshold):
        #
        info = ObjectDetectionCal.save_result(self.annotation_path, self.file_path, self.types)

        annotation_data = {}
        predict_data = {}

        # 读入标注数据
        with open(self.annotation_path, 'r', encoding='utf-8') as f:
            # 对每个图片来处理
            for line in f:
                line = line.strip('\n').strip().split(' ')
                annotation = []
                for i, item in enumerate(line[1:]):
                    item = item.split(',')
                    annotation.append(item)
                annotation_data.update({line[0]: annotation})
                # print(annotation_data[line[0]])

        # 读入预测数据
        with open(self.file_path, 'r', encoding='utf-8') as f:
            # 对每个图像来处理
            for line in f:
                line = line.strip('\n').strip().split(' ')
                predict = []
                for i, item in enumerate(line[1:]):
                    item = item.split(',')
                    predict.append(item)
                predict_data.update({line[0]: predict})
                # print(predict_data[line[0]])

        json_data = {'tableName': '测试标注结果'}
        # 将两者数据进行求iou的共同区域>threshold=0.5 且种类相同则为正确预测
        for img_path in annotation_data:
            annotation = annotation_data[img_path]
            predict = predict_data[img_path]

            json_data.update({img_path: {}})
            json_data[img_path].update({'dataset_annot': {}})
            json_data[img_path].update({'evaluate_annot': {}})
            json_data[img_path].update({'error_annot': {}})

            json_data[img_path]['dataset_annot'].update({'num': len(annotation)})
            json_data[img_path]['dataset_annot'].update({'annotations': []})

            json_data[img_path]['evaluate_annot'].update({'num': len(predict)})
            json_data[img_path]['evaluate_annot'].update({'annotations': []})

            for j in enumerate(predict):
                json_data[img_path]['evaluate_annot']['annotations'].append({
                    'xmin': predict[j[0]][0],
                    'ymin': predict[j[0]][1],
                    'xmax': predict[j[0]][2],
                    'ymax': predict[j[0]][3],
                    'code': predict[j[0]][5],
                    'label': self.types[int(predict[j[0]][5])],
                    'confidence': predict[j[0]][4]
                })

            # 对一张图片的每一个标注
            ok_set = set()
            error_set = set()
            for i in enumerate(annotation):
                json_data[img_path]['dataset_annot']['annotations'].append({
                    'xmin': annotation[i[0]][0],
                    'ymin': annotation[i[0]][1],
                    'xmax': annotation[i[0]][2],
                    'ymax': annotation[i[0]][3],
                    'code': annotation[i[0]][4],
                    'label': self.types[int(annotation[i[0]][4])]
                })

                for j in enumerate(predict):
                    # 不满足条件则加入error_list
                    iou = utils.bboxes_iou(np.array([float(i) for i in annotation[i[0]][:4]]),
                                           np.array([float(i) for i in predict[j[0]][:4]]))
                    if iou > threshold and annotation[i[0]][4] == predict[j[0]][5]:
                        ok_set.add(j[0])
                    else:
                        error_set.add(j[0])
            for i in error_set.copy():
                if i in ok_set:
                    error_set.remove(i)
            json_data[img_path]['error_annot'].update({'num': len(error_set)})
            json_data[img_path]['error_annot'].update({'error_no': list(error_set)})

        info['tables'].append(json_data)
        # json_data.update(info)
        # 保存对比结果和混淆矩阵等信息
        with open(file_path, 'w')as f:
            json.dump(info, f)

    '''
    保存测试结果和结果相比标注的错误对比
    '''

    def saveResult(self, threshold=0.1):
        open(self.file_path, 'w').close()
        self.save_all_lines()
        self.calcluateMetrics(os.path.splitext(self.file_path)[0] + '.json', threshold)

    """
    设置类型信息
    """

    def set_img_path(self, img_path):
        self.img_path = img_path

    """
    设置单张图片预测结果
    """

    def set_data(self, data):
        self.data = data

    """
    将一张图片的所有标注信息单行存储
    """

    def save_one_line(self):
        with open(self.file_path, 'a', encoding='utf-8') as f:
            line = self.img_path
            for i, item in enumerate(self.data):
                # 开头路径
                # print(self.data[0],self.data[1])
                # print(item[0], item[1], item[2], item[3], item[4], item[5])
                line = line + ' ' + ','.join(
                    [str(item[0]), str(item[1]), str(item[2]), str(item[3]), str(item[4]), str(int(item[5]))])
            f.write(line + '\n')

    """
    传入预测的结果值bboxes，直接保存到result.json中
    """

    def save_all_lines(self):
        path_list = []
        with open(self.annotation_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip('\n').split(' ')
                path_list.append(line[0])

        # 保存所有图片的预测结果
        for i, img_path in enumerate(path_list):
            self.set_img_path(img_path)
            self.set_data(self.bboxes[i])
            self.save_one_line()

    """
    给出标注框选的可视化
    """

    def show_annotation(self):
        with open(self.annotation_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip('\n').split(' ')
                img_path = line[0]
                img = cv2.imread(img_path)
                for i, item in enumerate(line[1:]):
                    item = item.split(',')
                    red = (0, 0, 255)
                    cv2.rectangle(img, (int(float(item[0])), int(float(item[1]))),
                                  (int(float(item[2])), int(float(item[3]))), red)
                cv2.imwrite('annotation.png', img)
                img = cv2.imread(img_path)
                # cv2.waiteKey()

    """
    给出预测框选的可视化
    """

    def show_precit(self):
        with open(self.file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip('\n').split(' ')
                img_path = line[0]
                img = cv2.imread(img_path)
                for i, item in enumerate(line[1:]):
                    item = item.split(',')
                    red = (0, 0, 255)
                    cv2.rectangle(img, (int(float(item[0])), int(float(item[1]))),
                                  (int(float(item[2])), int(float(item[3]))), red)
                cv2.imwrite('./lziqi_test_show/' + img_path, img)
                img = cv2.imread(img_path)
                # cv2.waiteKey()
    def evaluate(self):
        self.loadConfig()
        self.test_data = self.loadTestData()
        self.predictBatch()

        self.setCalParam(
            self.test_path,
            self.pre_resout,
            self.classes,
            self.save_path
        )
        self.saveResult()
        print("TEST OK")

class ObjectDetectionCal(object):
    # 计算两矩形的IOU
    def IOU(self, boxes1, boxes2):
        boxes1 = np.array(boxes1)
        boxes2 = np.array(boxes2)

        boxes1_area = (boxes1[..., 2] - boxes1[..., 0]) * (boxes1[..., 3] - boxes1[..., 1])
        boxes2_area = (boxes2[..., 2] - boxes2[..., 0]) * (boxes2[..., 3] - boxes2[..., 1])

        left_up = np.maximum(boxes1[..., :2], boxes2[..., :2])
        right_down = np.minimum(boxes1[..., 2:], boxes2[..., 2:])

        inter_section = np.maximum(right_down - left_up, 0.0)
        inter_area = inter_section[..., 0] * inter_section[..., 1]
        union_area = boxes1_area + boxes2_area - inter_area
        ious = np.maximum(1.0 * inter_area / union_area, np.finfo(np.float32).eps)

        return ious

    # 计算混淆矩阵
    def confusion_matrix(self, real_ann_path, pred_ann_path, classes, iou=0.5):
        class_nums = len(classes)
        matrix = np.zeros((class_nums + 1, class_nums + 1))
        file_lists = [['' for _ in range(class_nums + 1)] for _ in range(class_nums + 1)]

        with open(real_ann_path, 'r') as real_annotation:
            with open(pred_ann_path, 'r') as pred_annotation:
                for num, line in enumerate(real_annotation):
                    real_line = line
                    annotation = real_line.strip().split()
                    image_path = annotation[0]
                    image_name = image_path.split('/')[-1]
                    image_name = image_name.split('\\')[-1]

                    real_bboxes = np.array([list(map(float, box.split(','))) for box in annotation[1:]])
                    # print("pred_annotation",pred_annotation)
                    pred_line = pred_annotation.readline()
                    # print(pred_line)
                    annotation = pred_line.strip().split()
                    # print(annotation)
                    pred_bboxes = np.array([list(map(float, box.split(','))) for box in annotation[1:]])
                    image_path = str(image_path).replace('/home/ml_space', '{workspace}')
                    if len(pred_bboxes) == 0:
                        # print(image_name, '图片预测失败，无匹配成功项')
                        for real_bbox in real_bboxes:
                            real_class = int(real_bbox[-1])
                            matrix[-1][real_class] += 1
                            file_lists[-1][real_class] += image_path + ' '
                        continue
                    # 预测的数组按置信度逆序后删除置信度列
                    pred_bboxes = pred_bboxes[np.argsort(pred_bboxes, axis=0)[:, 4]]
                    # 数据顺序颠倒
                    pred_bboxes = pred_bboxes[::-1]
                    pred_bboxes = np.delete(pred_bboxes, 4, axis=1)
                    pre_find = [0 for _ in range(len(pred_bboxes))]
                    for real_bbox in real_bboxes:
                        real_class = int(real_bbox[-1])
                        find = 0
                        index = 0
                        for pre_bbox in pred_bboxes:
                            pre_class = int(pre_bbox[-1])
                            if self.IOU(real_bbox[:-1], pre_bbox[:-1]) > iou:
                                find = 1
                                pre_find[index] += 1
                                matrix[pre_class][real_class] += 1
                                file_lists[pre_class][real_class] += image_path + ' '
                                # if pre_class != real_class:
                                #     print(image_name, '图片检测错误，将', real_bbox[:-1], '中的', classes[real_class],
                                #           '检测为了', classes[pre_class])
                            index += 1
                        if find == 0:
                            matrix[-1][real_class] += 1
                            file_lists[-1][real_class] += image_path + ' '
                            # print(image_name, '图片的', real_bbox[:-1], '区域的', classes[real_class], '检测失败，无匹配成功项')

                    for i in range(len(pre_find)):
                        pre_bbox = pred_bboxes[i]
                        pre_class = int(pre_bbox[-1])
                        if pre_find[i] == 0:
                            matrix[pre_class][-1] += 1
                            file_lists[pre_class][-1] += image_path + ' '
                            # print(image_name, '图片的', pre_bbox[:-1], '区域的', classes[pre_class], '检测错误，图中无此目标')

        return matrix, file_lists

    # 绘制混淆矩阵，计算指标，写入文本
    def save_result(self, real_ann_path, pred_ann_path, classes, IOU=0.5, beta=1):
        matrix, file_lists = self.confusion_matrix(real_ann_path, pred_ann_path, classes, IOU)
        tables = []
        table = {"tableName": "查准率，查全率，F1值，精确值，平均精度"}
        for index in range(len(classes)):
            label = classes[index]
            if matrix[index][index] == 0:
                precision = 0
                recall = 0
                f_beta = 0
                accuaracy = 0
                AP = 0
            else:
                precision = matrix[index][index] / sum(matrix[index])
                recall = matrix[index][index] / sum(matrix)[index]
                f_beta = (1 + beta * beta) * precision * recall / (beta * beta * precision + recall + 0.00001)
                accuaracy = matrix[index][index] / (sum(matrix[index]) + sum(matrix)[index] - matrix[index][index])
                AP = self.get_AP(real_ann_path, pred_ann_path, index, IOU)
            res_dic = {"precision": precision,
                       "recall": recall,
                       "F1_score": f_beta,
                       "accuaracy": accuaracy,
                       "AP": AP}
            table[label] = res_dic
        tables.append(table)
        # 混淆矩阵绘制
        table = {"tableName": "混淆矩阵"}
        i = 0
        for i in range(len(matrix)):
            row = matrix[i]
            if i >= len(classes):
                label = "none"
            else:
                label = classes[i]
            key = 'predict_' + label
            res_dic = {}
            for j in range(len(row)):
                num = row[j]
                if j >= len(classes):
                    label = "none"
                else:
                    label = classes[j]
                data = {'num': int(num), 'fileList': sorted(list(set(file_lists[i][j].split())))}
                res_dic['real_' + label] = data

            table[key] = res_dic
            i += 1
        tables.append(table)
        result = {"tables": tables}
        return result

    # 计算AP
    def get_AP(self, real_ann_path, pred_ann_path, label, iou=0.5):
        Q = []
        P = []
        M = N = 0
        with open(real_ann_path, 'r') as real_annotation:
            for num, line in enumerate(real_annotation):
                real_line = line
                annotation = real_line.strip().split()
                real_bboxes = np.array([list(map(float, box.split(','))) for box in annotation[1:]])
                for real_bbox in real_bboxes:
                    real_class = int(real_bbox[-1])
                    if real_class == label:
                        M += 1
        with open(real_ann_path, 'r') as real_annotation:
            with open(pred_ann_path, 'r') as pred_annotation:

                for num, line in enumerate(real_annotation):
                    real_line = line
                    annotation = real_line.strip().split()
                    real_bboxes = np.array([list(map(float, box.split(','))) for box in annotation[1:]])
                    pred_line = pred_annotation.readline()
                    annotation = pred_line.strip().split()
                    pred_bboxes = np.array([list(map(float, box.split(','))) for box in annotation[1:]])

                    for pred_bbox in pred_bboxes:
                        pred_class = int(pred_bbox[-1])
                        find = 0
                        if pred_class == label:
                            N += 1
                            for real_bbox in real_bboxes:
                                real_class = int(real_bbox[-1])
                                if real_class == label:
                                    if self.IOU(real_bbox[:-1], pred_bbox[:-2]) > iou:
                                        find = 1
                            P.append([float(pred_bbox[-2]), find])

        if len(P) > 0 and N != 0:
            P = np.array(P)
            P = P[np.lexsort(-P[:, ::-1].T)]
            TP = 0
            for index in range(len(P)):
                TP += P[index][1]
                Q.append([TP / M, TP / (index + 1)])

        if not Q:
            return 0
        Q = np.array(Q)
        recall = Q[:, 0]
        precision = Q[:, 1]
        AP = self.compute_ap(recall, precision)
        return AP

    # 根据recall和precision数组计算AP
    def compute_ap(self, recall, precision):
        mrec = np.concatenate(([0.0], recall, [1.0]))
        mpre = np.concatenate(([0.0], precision, [0.0]))

        # compute the precision envelope
        # 将小于某元素前面的所有元素置为该元素，如[11,3,5,8,6]，操作后为[11,  8,  8,  8,  6]
        # 原因是 对于每个recall值r，我们要计算出对应（r’ > r）的最大precision
        for i in range(mpre.size - 1, 0, -1):
            mpre[i - 1] = np.maximum(mpre[i - 1], mpre[i])

        # to calculate area under PR curve, look for points
        # where X axis (recall) changes value
        # recall_curve列表是有局部相等的，如[0,0.1,0.1,0.1,0.2,0.2,0.5,0.5],
        i = np.where(mrec[1:] != mrec[:-1])[0]

        # and sum (\Delta recall) * prec , 微积分定义方式求解，小矩形相加
        ap = np.sum((mrec[i + 1] - mrec[i]) * mpre[i + 1])
        return ap



