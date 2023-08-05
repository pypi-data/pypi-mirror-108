import argparse

def image_classification_cfg():
    parser = argparse.ArgumentParser()
    parser.add_argument('--TEST_FILE_PATH', type=str, default='annotation/test.txt')
    parser.add_argument('--MODEL_FILE', type=str, default='resnet_model.pth')
    parser.add_argument('--classes', type=str)
    parser.add_argument('--batch_size', type=int, default=16)
    parser.add_argument('--num_workers', type=int, default=2)
    parser.add_argument('--RESULT_PATH', type=str, default='testResult.json')
    args = parser.parse_args()

    return args

def object_detection_cfg():
    parser = argparse.ArgumentParser()
    parser.add_argument("--annotation_path", type=int, default=2, help="注解路径")
    parser.add_argument("--result_file", type=int, default=3, help="评估结果存储路径")
    parser.add_argument("--model_path", type=str, default="test.txt", help="模型路径")
    parser.add_argument("--batch_size", type=str, default="weights/SegNet_weight1620281368.971498.pth", help="批处理大小")

    args = parser.parse_args()
    return args
    # self.test_path = cfg.TEST.ANNOT_PATH
    # self.save_path = cfg.TEST.RESULT_PATH
    # self.model_path = cfg.TEST.MODEL_PATH
    # self.batch_size = cfg.TEST.BATCH_SIZE

    # self.annotation_path = cfg.TEST.ANNOT_PATH
    # self.result_file = cfg.TEST.RESULT_PATH
    # self.model_path = cfg.TEST.MODEL_PATH
    # self.batch_size = cfg.TEST.BATCH_SIZE

def semantic_segmentation_cfg():
    parser = argparse.ArgumentParser()
    parser.add_argument("--class_num", type=int, default=2, help="评估的类别的种类")
    parser.add_argument("--batch_size", type=int, default=3, help="批评估大小")
    parser.add_argument("--test_path", type=str, default="test.txt", help="评估图片和标签的路径；test.txt文件每一行内容：评估图片路径 标注图片路径")
    parser.add_argument("--weights", type=str, default="weights/SegNet_weight1620281368.971498.pth", help="评估权重路径")
    parser.add_argument("--save_path", type=str, default="evaluate/evaluateRes.json", help="评估结果存储路径")
    parser.add_argument("--class_dict", type=dict, default={0: 'background', 1: 'target'}, help="类别名")

    args = parser.parse_args()
    print(type(args),"aaaaa")
    return args


