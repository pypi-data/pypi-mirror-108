# -*- coding:utf-8 -*-
__author__ = 'shichao'


import numpy as np
import json
import argparse


def parse_json(json_pred_data,json_gt_data):
    pred_data_list = []
    gt_data_list = []
    path_list = []
    for img_path,pred_img_infos in json_pred_data.items():
        try:
            gt_img_infos = json_gt_data[img_path]
            gt_data_list.append(gt_img_infos)
            pred_data_list.append(pred_img_infos)
            path_list.append(img_path)
        except:
            print(img_path)
            continue
    return pred_data_list,gt_data_list,path_list


def flue_det_metric(pred,gt):
    nd = len(pred)
    positive = 0
    negative = 0
    tp = 0
    fp = 0
    fn = 0
    for i in range(nd):
        pred_info = pred[i]
        gt_info = gt[i]

        if len(gt_info) == 1:
            positive += 1
            if len(pred_info) == 1:
                tp += 1
            else:
                fn += 1
        else:
            negative += 1
            if len(pred_info) == 1:
                fp += 1
    prec = float(tp)/(tp+fp)
    recall = float(tp)/positive

    return prec,recall


def evaluation(pred_path,gt_path):
    with open(pred_path, 'r', encoding='utf8')as fp:
        pred_data = json.load(fp)
    with open(gt_path, 'r', encoding='utf8')as fp:
        gt_data = json.load(fp)
    pred_data_list, gt_data_list, path_list = parse_json(pred_data, gt_data)
    prec, recall = flue_det_metric(pred_data_list, gt_data_list)
    print(prec,recall)
    return prec,recall



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--gt', default='gt.json', help='json file of ground truth')
    parser.add_argument('--pred', default='pred.json', help='json file of prediction')
    args = parser.parse_args()
    gt_path = args.gt
    pred_path = args.pred
    prec,recall = evaluation(args.pred, args.gt)
    print(prec)
    print(recall)
