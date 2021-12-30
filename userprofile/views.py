from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.core import serializers
from userprofile.forms import UserLoginForm, User
from userprofile.models import UserProfile
try:
    from utils.smmsapi import initsmms
except Exception as e:
    print(f"init smmsApi failed, please check!!! reason: {e}")
import json
import logging
dlogger = logging.getLogger('defaultlogger')

def user_login(request):
    if request.method == 'POST':
        user_login_form = UserLoginForm(data=request.POST)
        if user_login_form.is_valid():
            data = user_login_form.cleaned_data
            u = data.get('username')
            user = authenticate(username=data.get('username'), password=data.get('password'))
            if user:
                login(request, user)
                # return redirect("userprofile:home", id=user.id)
                return redirect("userprofile:home")
            else:
                return HttpResponse("账号或密码输入错误，请重新输入！")
        else:
            return HttpResponse("账号或密码输入不合法！！！")
    elif request.method == 'GET':
        user_login_form = UserLoginForm()
        context = {'form': user_login_form}
        return render(request, 'userprofile/login.html', context)
    else:
        return HttpResponse(status='400', reason='Request method not allowed, Please check...')

def user_logout(request):
    logout(request)
    return redirect("userprofile:home")

def home(request):
    try:
        # 数据库取出用户数据
        loginid = request.session['_auth_user_id']
        username = User.objects.get(id=loginid).username
        account_object = UserProfile.objects.filter(username=username)
        account_info = account_object.get()
        authheader = {'Authorization': account_info.token}

        # 默认调用数据库返回数据
        if True:
            select_result = serializers.serialize('json', account_object)
            data = json.loads(select_result)[0]['fields']
            return_data = {'data': data}
            return_data['data']['token'] = authheader['Authorization']
        # 调用smms 接口获取用户数据并更新数据库
        else:
            smmsApi = initsmms('smmsapi', '/profile', authheader)
            return_data = smmsApi.get_userprofile()
            return_data['data']['token'] = authheader['Authorization']

            account_info.disk_usage = return_data['data']['disk_usage']
            account_info.disk_usage_raw = return_data['data']['disk_usage_raw']
            account_info.disk_limit = return_data['data']['disk_limit']
            account_info.disk_limit_raw = return_data['data']['disk_limit_raw']
            account_info.last_requestid = return_data['RequestId']
            account_info.save()
    except Exception as e:
        return_data = None
        dlogger.error(f"Request userprofile failed, reason：{e}")
    finally:
        return render(request, 'userprofile/index.html', {'rd': return_data})


def usage_overview(request):
    try:
        # 数据库取出用户数据
        loginid = request.session['_auth_user_id']
        username = User.objects.get(id=loginid).username
        account_object = UserProfile.objects.filter(username=username)
        account_info = account_object.get()
        authheader = {'Authorization': account_info.token}

        # 默认调用数据库返回数据
        if True:
            select_result = serializers.serialize('json', account_object)
            data = json.loads(select_result)[0]['fields']
            return_data = {'data': data}
        # 调用smms 接口获取用户数据并更新数据库
        else:
            smmsApi = initsmms('smmsapi', '/profile', authheader)
            return_data = smmsApi.get_userprofile()
            return_data['data']['token'] = authheader['Authorization']
            # 计算使用百分比
            disk_usage = return_data['data']['disk_usage']
            disk_limit = return_data['data']['disk_limit']
            dtotal = int(disk_usage.split('.')[0]) if 'KB' in disk_usage.split('.')[1] else int(disk_usage.split('.')[0]) * 1024
            ltotal = int(disk_limit.split('.')[0]) if 'KB' in disk_limit.split('.')[1] else int(disk_limit.split('.')[0]) * 1024 * 1024
            usage_percent = str('%.1f' % (dtotal / ltotal * 100))
            return_data['data']['usage_percent'] = usage_percent

            account_info.disk_usage = disk_usage
            account_info.disk_usage_raw = return_data['data']['disk_usage_raw']
            account_info.disk_limit = disk_limit
            account_info.disk_limit_raw = return_data['data']['disk_limit_raw']
            account_info.last_requestid = return_data['RequestId']
            account_info.usage_percent = usage_percent
            account_info.save()
    except Exception as e:
        return_data = None
        dlogger.error(f"Request userprofile failed, reason：{e}")
    finally:
        return render(request, 'userprofile/usage-overview.html', {'rd': return_data})
