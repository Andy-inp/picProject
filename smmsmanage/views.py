from django.shortcuts import render, HttpResponse, redirect
from homeapp.models import UserProfile
import logging
dlogger = logging.getLogger('defaultlogger')
import json
import time

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
            return_data = {'success': True, 'upload_result': uploadResult}
            return HttpResponse(json.dumps(return_data))
            # 测试返回数据
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
        except Exception as e:
            return HttpResponse(json.dumps({'error': f"upload error, error reason {e}"}))
    else:
        return HttpResponse(status='400', reason='Request method not allowed, Please check...')

def img_list(request):
    return render(request, 'smmsmanage/img-list.html')

def imglist_json(request, imglist):
    try:
        # 测试数据
        with open('/Users/yakir/yakir_code/tmp_save/tmp.json', 'r') as f:
            return_data = f.read()

        # ah = authHeader
        # smmsApi = initsmms('smmsapi', '/upload_history', ah)
        # result = smmsApi.upload_history()
        # assert result['success'], f"Get upload history failed!!!"
        # return_data = list()
        # for result_temp in result['data']:
        #     tmp_dict = {}
        #     tmp_dict['filename'] = result_temp['filename']
        #     tmp_dict['preview'] = result_temp['url']
        #     tmp_dict['size'] = str(round(result_temp['size'] / 1024, 2)) + "KB"
        #     tmp_dict['width'] = result_temp['width']
        #     tmp_dict['height'] = result_temp['height']
        #     tmp_dict['upload_date'] =  time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(result_temp['created_at']))
        #     tmp_dict['operations'] = result_temp['delete']
        #     return_data.append(tmp_dict)
        # return_data = json.dumps(return_data)
    except Exception as e:
        return_data = None
        dlogger.error(f"Request upload history failed, reason：{e}")
    finally:
        return HttpResponse(return_data)

def delimg(request):
    try:
        # 测试数据
        del_result = {
            # 'success': True,
            # 'code': 'success',
            # 'message': 'File delete success',
            'success': False,
            'code': 'error',
            'message': 'failed reason: xxxxxx.',
            'data': [],
            'RequestId': '16789D65-C375-44AB-8D33-AFB859265472'
        }
        # 获取到需要删除的 hash 值
        # params = request.GET.get('v')
        # imghash = params.split('/')[-1]
        # # 调用接口删除文件
        # ah = authHeader
        # smmsApi = initsmms('smmsapi', '/delete', ah)
        # del_result = smmsApi.delete_image(imghash)
        # assert del_result['success'], f"delete image failed!!!"
        return_data = json.dumps(del_result)
    except Exception as e:
        return_data = None
        dlogger.error(f"Delete image failed, reason：{e}")
    finally:
        return HttpResponse(return_data)