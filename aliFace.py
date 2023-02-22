#!/usr/bin/env python
# coding=utf-8

from aliyunsdkfacebody.request.v20191230.FaceFilterRequest import FaceFilterRequest
from aliyunsdkfacebody.request.v20191230.FaceBeautyRequest import FaceBeautyRequest
from aliyunsdkfacebody.request.v20191230.DeleteFaceImageTemplateRequest import DeleteFaceImageTemplateRequest
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.auth.credentials import AccessKeyCredential
from aliyunsdkfacebody.request.v20191230.MergeImageFaceRequest import MergeImageFaceRequest
from aliyunsdkfacebody.request.v20191230.QueryFaceImageTemplateRequest import QueryFaceImageTemplateRequest
from aliyunsdkfacebody.request.v20191230.AddFaceImageTemplateRequest import AddFaceImageTemplateRequest
from aliyunsdkvideoenhan.request.v20200320.MergeVideoFaceRequest import MergeVideoFaceRequest
from aliyunsdkvideoenhan.request.v20200320.GetAsyncJobResultRequest import GetAsyncJobResultRequest as getMergeVieoResult
from aliyunsdkimageseg.request.v20191230.SegmentHDCommonImageRequest import SegmentHDCommonImageRequest
from aliyunsdkimageseg.request.v20191230.SegmentBodyRequest import SegmentBodyRequest
from aliyunsdkfacebody.request.v20191230.FaceMakeupRequest import FaceMakeupRequest
from aliyunsdkimageseg.request.v20191230.GetAsyncJobResultRequest import GetAsyncJobResultRequest as getSegmentHDResult

import json


class Aliface():

    def setAkSk(self, ak, sk):
        self.credentials = AccessKeyCredential(ak, sk)
        self.client = AcsClient(region_id='cn-shanghai', credential=self.credentials)

    def __init__(self, ak, sk):
        self.credentials = AccessKeyCredential(ak, sk)
        self.client = AcsClient(region_id='cn-shanghai', credential=self.credentials)

    def MergeImageFace(self, TemplateId, ImageURL):
        request = MergeImageFaceRequest()
        request.set_TemplateId(TemplateId)
        request.set_ImageURL(ImageURL)
        request.set_accept_format('json')
        response = self.client.do_action_with_exception(request)
        return str(response, encoding='utf-8')

    def AddFaceImageTemplate(self, ImageURL):
        request = AddFaceImageTemplateRequest()
        request.set_ImageURL(ImageURL)
        request.set_accept_format('json')
        response = self.client.do_action_with_exception(request)
        obj = json.loads(response)
        return obj['Data']['TemplateId']

    def QueryFaceImageTemplate(self, TemplateId=''):
        request = QueryFaceImageTemplateRequest()
        request.set_UserId()
        request.set_TemplateId(TemplateId)
        request.set_accept_format('json')
        response = self.client.do_action_with_exception(request)
        return str(response, encoding='utf-8')

    def DeleteFaceImageTemplate(self, TemplateId):
        request = DeleteFaceImageTemplateRequest()
        request.set_TemplateId(TemplateId)
        request.set_accept_format('json')
        response = self.client.do_action_with_exception(request)
        return str(response, encoding='utf-8')

    def MergeVideoFace(self, VideoURL,  ReferenceURL):
        request = MergeVideoFaceRequest()
        request.set_ReferenceURL(ReferenceURL)
        request.set_VideoURL(VideoURL)
        request.set_accept_format('json')
        response = self.client.do_action_with_exception(request)
        obj=json.loads(response)
        RequestId = obj['RequestId']
        return RequestId

    def getMergeVieoResult(self, JobId):
        '''QUEUING：任务排队中
PROCESSING ：异步处理中
PROCESS_SUCCESS ：处理成功
PROCESS_FAILED ：处理失败
TIMEOUT_FAILED ：任务超时未处理完成
LIMIT_RETRY_FAILED ：超过最大重试次数'''
        request = getMergeVieoResult()
        request.set_accept_format('json')
        request.set_JobId(JobId)
        response = self.client.do_action_with_exception(request)
        obj = json.loads(response)
        Status = obj['Data']['Status']
        # python2:  print(response)
        if Status == 'PROCESS_SUCCESS':
            tmp = obj['Data']['Result']
            obj=json.loads(tmp)
            VideoUrl = obj['videoUrl']
            return 'PROCESS_SUCCESS',VideoUrl
        else:
            return Status,''

    def SegmentHDCommonImageRequest(self, ImageUrl):
        '''高清人体分割'''
        request = SegmentHDCommonImageRequest()
        request.set_ImageUrl(ImageUrl)
        request.set_accept_format('json')
        response = self.client.do_action_with_exception(request)
        obj = json.loads(response)
        RequestId = obj['RequestId']
        return RequestId

    def getSegmentHDResult(self,JobId):
        request = getSegmentHDResult()
        request.set_accept_format('json')
        request.set_JobId(JobId)
        response = self.client.do_action_with_exception(request)
        obj = json.loads(response)
        Status = obj['Data']['Status']
        if Status == 'PROCESS_SUCCESS':
            tmp = obj['Data']['Result']
            obj = json.loads(tmp)
            VideoUrl = obj['imageUrl']
            return 'PROCESS_SUCCESS', VideoUrl
        else:
            return Status, ''

    def SegmentBodyRequest(self, ImageUrl):
        '''人体分割'''
        request = SegmentBodyRequest()
        request.set_ImageURL(ImageUrl)
        request.set_accept_format('json')
        response = self.client.do_action_with_exception(request)
        obj = json.loads(response)
        url = obj["Data"]['ImageURL']
        return url

    def FaceBeautyRequest(self, ImageURL:str, Sharp: float, Smooth: float, White: float):
        '''人脸美颜'''
        request = FaceBeautyRequest()
        request.set_accept_format('json')
        request.set_Sharp(Sharp)
        request.set_Smooth(Smooth)
        request.set_White(White)
        request.set_ImageURL(ImageURL)
        response = self.client.do_action_with_exception(request)
        obj = json.loads(response)
        url = obj["Data"]['ImageURL']
        return url

    def FaceMakeupRequest(self, ImageURL, ResourceType:str,Strength:float):
        '''人脸美妆
        美妆类型，当前支持whole（整妆）。
        美妆使用的风格，具体包括：0（whole）、1（基础妆）、2（少女妆）、3（活力妆）、4（优雅妆）、5（魅惑妆）、6（梅子妆）。
        美妆强度，取值范围0～1。float
        '''
        request = FaceMakeupRequest()
        request.set_accept_format('json')

        request.set_ImageURL(ImageURL)
        request.set_MakeupType("whole")
        request.set_ResourceType(ResourceType)
        request.set_Strength(Strength)
        response = self.client.do_action_with_exception(request)
        obj = json.loads(response)
        url = obj["Data"]['ImageURL']
        return url

    def FaceFilterRequest(self, ImageURL, ResourceType, Strength):
        request = FaceFilterRequest()
        request.set_accept_format('json')
        request.set_ImageURL(ImageURL)
        request.set_ResourceType(ResourceType)
        request.set_Strength(Strength)
        response = self.client.do_action_with_exception(request)
        obj = json.loads(response)
        url = obj["Data"]['ImageURL']
        return url
