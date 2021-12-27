from django.shortcuts import render
# from django.http import HttpResponse
# from django.contrib.auth import authenticate, login, logout
from homeapp.models import UserProfile
import logging
dlogger = logging.getLogger('defaultlogger')

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

# 测试数据
rd_test = {
    'success': True,
    'code': 'success',
    'message': 'Get user profile success.',
    'data': {
        'username': 'Yakir',
        'email': 'xxxx@gmail.com',
        'role': 'user',
        'group_expire': '0000-00-00',
        'email_verified': 0,
        'disk_usage': '1000.29 MB',
        'disk_limit': '5.00 GB',
    },
    'RequestId': 'A8F67DE1-14BE-4FA2-8955-247BF5C4540B'
}

def home(request):
    try:
        # ah = authHeader
        # smmsApi = initsmms('smmsapi', '/profile', ah)
        # return_data = smmsApi.get_userprofile()
        return_data = rd_test
        return_data['actoken'] = acToken
    except Exception as e:
        return_data = None
        dlogger.error(f"Request userprofile failed, reason：{e}")
    finally:
        return render(request, 'userprofile/index.html', {'rd': return_data})


def usage_overview(request):
    try:
        # ah = authHeader
        # smmsApi = initsmms('smmsapi', '/profile', ah)
        # return_data = smmsApi.get_userprofile()
        return_data = rd_test
        # 计算使用百分比
        u = return_data['data']['disk_usage']
        l = return_data['data']['disk_limit']
        u1 = int(u.split('.')[0]) if 'KB' in u.split('.')[1] else int(u.split('.')[0]) * 1024
        l1 = int(l.split('.')[0]) if 'KB' in l.split('.')[1] else int(l.split('.')[0]) * 1024 * 1024
        usage_percent = str('%.1f' % (u1 / l1 * 100))
        print(u1, l1, usage_percent)
        return_data['usage_percent'] = usage_percent
    except Exception as e:
        return_data = None
        dlogger.error(f"Request userprofile failed, reason：{e}")
    finally:
        return render(request, 'userprofile/usage-overview.html', {'rd': return_data})
