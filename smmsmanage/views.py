from django.shortcuts import render, HttpResponse, redirect
from homeapp.models import UserProfile
import logging
dlogger = logging.getLogger('defaultlogger')
import json

# 查询条件
accountInfo = UserProfile.objects.filter(id=1).first()
acToken = accountInfo.token
authHeader = {'Authorization': acToken}

def initsmms(service: str="yaml service",
            endpoint: str="request endpoint",
            authheader: str="request header") -> "smms class":
    # 获取配置
    from utils.getconfig import GetYamlConfig
    from utils.smmsapi import SmmsApi
    cfg = GetYamlConfig()
    apihost = cfg.get_config(service)['smmsApiHost']
    # 初始化smms接口
    smmsApi = SmmsApi(apihost)
    smmsApi.endpoint = endpoint
    smmsApi.auth_header = authheader
    return smmsApi

def upload(request):
    if request.method == 'GET':
        return render(request, 'smmsmanage/upload.html')
    elif request.method == 'POST':
        try:
            ah = authHeader
            smmsApi = initsmms('smmsapi', '/upload', ah)
            # 开始调用smms上传接口并记录
            uploadResult = []
            fileList = request.FILES.getlist('file-input')
            for file in fileList:
                smfile = {
                    "smfile": (file.name, file)
                }
                upload_to_smms = smmsApi.upload_image(smfile)
                uploadResult.append(upload_to_smms)
                dlogger.info(f" 上传图片：{file.name}，上传结果：{upload_to_smms}")
            # upload_result = {
            #   "success": "True",
            #   "code": "success",
            #   "message": "Upload success.",
            #   "data": {
            #     "file_id": 0,
            #     "width": 474,
            #     "height": 296,
            #     "filename": "2.jpg",
            #     "storename": "sLu5VUOq3wz2vin.jpg",
            #     "size": 19027,
            #     "path": "/2021/12/14/sLu5VUOq3wz2vin.jpg",
            #     "hash": "wMPLoDsR28W69nAj1fetEZrFXc",
            #     "url": "https://s2.loli.net/2021/12/14/sLu5VUOq3wz2vin.jpg",
            #     "delete": "https://sm.ms/delete/wMPLoDsR28W69nAj1fetEZrFXc",
            #     "page": "https://sm.ms/image/sLu5VUOq3wz2vin"
            #   },
            #   "RequestId": "9FE079A1-397B-40D8-9DA2-67D7DB15BDBD"
            # }
            return_data = {'success': True, 'upload_result': uploadResult}
            return HttpResponse(json.dumps(return_data))
        except:
            return HttpResponse(json.dumps({'error': 'upload error...'}))
    else:
        return HttpResponse(status='400', reason='Request method not allowed, Please check...')

def img_list(request):
    # smmsapi.endpoint = '/upload_history'

    return render(request, 'smmsmanage/img-list.html')