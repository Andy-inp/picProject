from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from django.core import serializers
from userprofile.models import User, UserProfile
from smmsmanage.models import ImageList
try:
    from utils.smmsapi import initsmms
except Exception as ec:
    print(f"init smmsApi failed, please check!!! reason: {ec}")
import json
import time
import logging
dlogger = logging.getLogger('defaultlogger')


@login_required(login_url='/login/')
def upload(request):
    if request.method == 'GET':
        return render(request, 'smmsmanage/upload.html')
    elif request.method == 'POST':
        try:
            # 数据库取出用户数据
            current_uid = request.session['_auth_user_id']
            username = User.objects.get(id=current_uid).username
            account_object = UserProfile.objects.get(username=username)
            authheader = {'Authorization': account_object.token}
            # 调用smms 上传接口并记录
            smmsApi = initsmms('smmsapi', '/upload', authheader)
            uploadResult = []
            fileList = request.FILES.getlist('file-input')
            for file in fileList:
                smfile = {
                    "smfile": (file.name, file)
                }
                upload_to_smms = smmsApi.upload_image(smfile)
                uploadResult.append(upload_to_smms)
                dlogger.info(f" 上传图片：{file.name}，上传结果：{upload_to_smms}")
                # 上传结果保存入库
                upload_result2db = {}
                upload_result2db['filename'] = upload_to_smms['data']['filename']
                upload_result2db['imgurl'] = upload_to_smms['data']['url']
                upload_result2db['size'] = str(round(upload_to_smms['data']['size'] / 1024, 2)) + "KB"
                upload_result2db['width'] = upload_to_smms['data']['width']
                upload_result2db['height'] = upload_to_smms['data']['height']
                upload_result2db['imghash'] = upload_to_smms['data']['hash']
                upload_result2db['deleteurl'] = upload_to_smms['data']['delete']
                upload_result2db['last_requestid'] = upload_to_smms['RequestId']
                upload_result2db['belong_user'] = account_object
                ImageList.objects.create(**upload_result2db)
            return_data = {'success': True, 'upload_result': uploadResult}
            return HttpResponse(json.dumps(return_data))
        except Exception as ec:
            return HttpResponse(json.dumps({'error': f"upload error, error reason {ec}"}))
    else:
        return HttpResponse(status='400', reason='Request method not allowed, Please check...')

@login_required(login_url='/login/')
def img_list(request):
    return render(request, 'smmsmanage/img-list.html')

@login_required(login_url='/login/')
def imglist_json(request, imglist):
    try:
        # 数据库取出用户数据
        current_uid = request.session['_auth_user_id']
        username = User.objects.get(id=current_uid).username
        account_object = UserProfile.objects.get(username=username)
        img_db_object = account_object.imagelist_set.all()
        authheader = {'Authorization': account_object.token}
        # 默认调用数据库返回数据
        if False:
            select_result = serializers.serialize('json', img_db_object)
            select_result = json.loads(select_result)
            img_list = list()
            for sr in select_result:
                tmp_dict = {}
                tmp_data = sr['fields']
                tmp_dict['filename'] = tmp_data['filename']
                tmp_dict['imgurl'] = tmp_data['imgurl']
                tmp_dict['size'] = tmp_data['size']
                tmp_dict['width'] = tmp_data['width']
                tmp_dict['height'] = tmp_data['height']
                tmp_dict['uploaddate'] = tmp_data['uploaddate']
                tmp_dict['deleteurl'] = tmp_data['deleteurl']
                img_list.append(tmp_dict)
            return_data = json.dumps(img_list)
        # 调用smms 接口获取用户数据
        else:
            smmsApi = initsmms('smmsapi', '/upload_history', authheader)
            result = smmsApi.upload_history()
            assert result['success'], f"Get upload history failed!!!"
            img_list = list()
            img_db_object.delete()
            for result_temp in result['data']:
                tmp_dict = {}
                tmp_dict['filename'] = result_temp['filename']
                tmp_dict['imgurl'] = result_temp['url']
                tmp_dict['imghash'] = result_temp['hash']
                tmp_dict['size'] = str(round(result_temp['size'] / 1024, 2)) + "KB"
                tmp_dict['width'] = result_temp['width']
                tmp_dict['height'] = result_temp['height']
                tmp_dict['deleteurl'] = result_temp['delete']
                tmp_dict['last_requestid'] = result['RequestId']
                tmp_dict['belong_user'] = account_object
                tmp_dict['uploaddate'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(result_temp['created_at']))
                img_db_object.create(**tmp_dict)
                # 保存信息入库后，修改返回信息到前端
                del tmp_dict['belong_user']
                img_list.append(tmp_dict)
            return_data = json.dumps(img_list)
    except Exception as ec:
        return_data = None
        dlogger.error(f"Request upload history failed, reason：{ec}")
    finally:
        return HttpResponse(return_data)

@login_required(login_url='/login/')
def singeldel(request):
    try:
        # 测试数据
        del_result = {
            'success': True,
            'code': 'success',
            'message': 'File delete success',
            # 'success': False,
            # 'code': 'error',
            # 'message': 'failed reason: xxxxxx.',
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
    except Exception as ec:
        return_data = None
        dlogger.error(f"Delete image failed, reason：{ec}")
    finally:
        return HttpResponse(return_data)

@login_required(login_url='/login/')
def batchdelimg(request):
    try:
        if request.method == 'POST':
            # 提交批量删除操作
            imginfo = {}
            del_result = {}
            print('此处为批量删除操作')
            return_data = json.dumps(del_result)
            return redirect('/smmsmanage/batchdel')
        else:
            pass
    except Exception as ec:
        return_data = None
        dlogger.error(f"Delete image failed, reason：{ec}")
    finally:
        return HttpResponse(return_data)
