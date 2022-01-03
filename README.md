[![Python Version](https://img.shields.io/badge/python-3.9.7-red)](https://img.shields.io/badge/python-3.9.7-red)
[![Python Version](https://img.shields.io/badge/Django-3.2.9-blue)](https://img.shields.io/badge/Django-3.2.9-blue)

### 前言
- 使用图床接口地址为 [SMMS](https://sm.ms/) 网站
- 网站旨在个人学习使用，如有侵权请联系删除
- 当前实现功能：
   - 登录注册页
   - 用户信息查看功能
   - 上传图片
   - 已上传图片地址查看、删除、批量删除（待完成）
   - 上传信息当前已保存入数据库信息为准，后续增加同步远程接口按钮（待完成）

​

### 示例页面
#### 登录注册页

- 支持登录、注册（跳转SMMS 官网自行注册， 注册后信息需自行存入user_profile 表中）
+ userprofile 表：
```python
# python manage.py shell
from userprofile.models import User, UserProfile
# username、password、token 手动更新注册信息
UserProfile.objects.create(username='yakir111', password='passwd123', token='xxxxxxx') 
```
+ auth_user 表：
```python
# python manage.py shell
from django.contrib.auth.models import User
User.objects.create_user('Username', 'Password')   # 将用户名与密码注册入User 表
```
![image.png](https://s2.loli.net/2022/01/03/oqfGJIYeUEd3Fsg.png)


#### 首页-用户操作-用户信息

- 默认从DB获取数据

![image.png](https://cdn.nlark.com/yuque/0/2022/png/21806976/1641196361630-3750e6cf-80e2-4013-9c8e-89b7bac8af1f.png#clientId=u30fa0fc3-033c-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=763&id=PUepG&margin=%5Bobject%20Object%5D&name=image.png&originHeight=1526&originWidth=2878&originalType=binary&ratio=1&rotation=0&showTitle=false&size=167224&status=done&style=none&taskId=u724f3df4-da77-4ae7-a732-1818a2ac5f5&title=&width=1439)


#### 首页-用户操作-使用概览

- 默认从DB 获取数据，

![image.png](https://cdn.nlark.com/yuque/0/2021/png/21806976/1640878669504-8f58cf38-9c55-48ab-b185-14f302008647.png#clientId=uf9c6d1ec-15e1-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=631&id=bMYU9&margin=%5Bobject%20Object%5D&name=image.png&originHeight=1262&originWidth=2856&originalType=binary&ratio=1&rotation=0&showTitle=false&size=139922&status=done&style=none&taskId=u4e145533-fee7-488d-b92d-dd66d0655c9&title=&width=1428)


#### 图床管理-上传图片

- 可多选图片同时上传（最多支持图片数量以及图片大小可通过upload.html 页面中参数进行修改）

![image.png](https://cdn.nlark.com/yuque/0/2022/png/21806976/1641198808925-76ccb54d-f737-4914-bc6c-cae98537f71e.png#clientId=u30fa0fc3-033c-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=764&id=iO2cO&margin=%5Bobject%20Object%5D&name=image.png&originHeight=1528&originWidth=2876&originalType=binary&ratio=1&rotation=0&showTitle=false&size=669162&status=done&style=none&taskId=u54a4fe54-1d7a-47af-a4bd-b1040919a67&title=&width=1438)


#### 图床管理-图床地址

- 已上传图片地址查看管理（默认从DB 获取）

![image.png](https://cdn.nlark.com/yuque/0/2022/png/21806976/1641196497138-dfbd8f89-2e45-4087-9d1a-f6140074ce86.png#clientId=u30fa0fc3-033c-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=766&id=jDt4k&margin=%5Bobject%20Object%5D&name=image.png&originHeight=1532&originWidth=2880&originalType=binary&ratio=1&rotation=0&showTitle=false&size=318049&status=done&style=none&taskId=u1c886c2c-6a10-4843-a0da-200e8c612e9&title=&width=1440)

- 从远端同步数据更新图片列表按钮（待完成）

​

​


- 删除图片操作

![image.png](https://cdn.nlark.com/yuque/0/2022/png/21806976/1641198097405-2e89a81c-325b-4d4d-b7db-be7dc10a6917.png#clientId=u30fa0fc3-033c-4&crop=0&crop=0&crop=1&crop=1&from=paste&height=689&id=ga5TH&margin=%5Bobject%20Object%5D&name=image.png&originHeight=1378&originWidth=2784&originalType=binary&ratio=1&rotation=0&showTitle=false&size=310716&status=done&style=none&taskId=uf083291f-d426-4b74-a36f-79588f40d43&title=&width=1392)

- 批量删除图片（待完成）
