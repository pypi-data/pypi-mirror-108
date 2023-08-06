'''
孕橙算法所需要的输入输出想
'''
import json
from .util import post_for_request
from .util_file import read_pic_to_base64
from .util_file import label_yc_line
import os
import requests
import cv2
# class Serialize():
#     def jsonTran(self):
#         return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
# class AlInput(Serialize):
#     def __init__(self,imdata,id):
#         self.imdata = imdata
#         self.id = id
#
# class AlOutput(Serialize):
#     def __init__(self, entries: dict = {}):
#         for k, v in entries.items():
#             if isinstance(v, dict):
#                 self.__dict__[k] = AlOutput(v)
#             else:
#                 self.__dict__[k] = v

def make_al_input(imdata,id):
    requestbody = {"file":imdata,"id":id}
    return requestbody


def ask_for_yuncheng_al(url,pics):
    '''

    :param url:
    :param pics:
    :return:
    '''
    session = requests.session()
    bodys = []
    for i in pics:
        try:
            imdata = read_pic_to_base64(i)
            id = i
            body = make_al_input(imdata,id)
            bodys.append(body)
        except Exception as e:
            print(e)

    results = []
    for i in bodys:
        try:
            result = post_for_request(url,i,session)
            results.append({
                'id':i['id'],
                'result':result
            })
        except Exception as e:
            print(e)
    return results

def show_yuncheng_result(results):

    for i in results:
        path = i['id']
        result = i['result']
        imdata =cv2.imread(path)
        label_yc_line(imdata[:,:,::-1],result)
