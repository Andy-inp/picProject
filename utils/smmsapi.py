import requests
import json
from getlogger import GetLogger
smmslog = GetLogger().get_logger('smmslogger')

__all__ = [
    'SmmsApi',
]

class _ApiBase(object):
    def __init__(self, api_host, endpoint, auth_header):
        self.api_host = api_host
        self.endpoint = endpoint
        self.auth_header = auth_header

    def _do(self, method, relative_path=None, **kwargs):
        """
        Parameters
        ----------
        kwargs: dict --> like data=dict({'arg1': 'a', 'arg2': 'b'})
        """
        try:
            url = self.api_host + self.endpoint + (relative_path if relative_path else "")
            res = requests.request(method,
                                   url,
                                   headers=self.auth_header,
                                   **kwargs)
            success_return = getattr(res, 'json', None)
            # smmslog.info(f"请求 {url} 成功，返回信息：{success_return()}")
            return success_return()
        except Exception as e:
            error_return = dict()
            error_return['code'] = 111
            error_return['msg'] = f"请求 {url} 失败，检查网络或参数！"
            smmslog.error(f"请求 {url} 失败，检查网络或参数！")
            return error_return

    # @property
    # def method(self):
    #     return self._method
    # @method.setter
    # def method(self, mt: str="PUT|GET|POST|DELETE") -> str:
    #     self._method = mt

    @property
    def relative_path(self):
        return self._relative_path
    @relative_path.setter
    def relative_path(self, rp: str="extra url, like /delete/:hash") -> str:
        self._relative_path = rp

    @property
    def endpoint(self):
        return self._endpoint
    @endpoint.setter
    def endpoint(self, ep: str="like /token or /userprofile") -> str:
        self._endpoint = ep

    @property
    def auth_header(self):
        return self._auth_header
    @auth_header.setter
    def auth_header(self, ah: dict) -> dict:
        self._auth_header = ah


class SmmsApi(_ApiBase):
    def __init__(self, api_host=None, endpoint=None, auth_header=None):
        """
        Parameters
        ----------
        api_host: str --> url hostname
        endpoint: str --> request url endpoint
        auth_header: dict  -->  request header
            default: {'Content-Type': 'multipart/form-data', 'Authorization': 'yW47L4kjQK3yeLHYNj7vNjBq3RpEG3Tg'}
        """
        super(SmmsApi, self).__init__(api_host, endpoint=None, auth_header=None)

    def get_token(self, username, password):
        data = {
            'username': username,
            'password': password,
        }
        resp = self._do('POST', data=data)
        return resp

    def get_userprofile(self):
        resp = self._do('POST')
        return resp

    def clear4ip_upload_history(self, format='json'):
        data = {'format': format}
        resp = self._do('GET', data=data)
        return resp

    def upload4ip_history(self, format='json'):
        data = {'format': format}
        resp = self._do('GET', data=data)
        return resp

    def delete_image(self, del_hash, format='json'):
        """
        Parameters
        ----------
        del_hash:  str --> image hash value
        """
        data = {'format': format}
        resp = self._do('GET', relative_path=f"/{del_hash}", data=data)
        return resp

    def upload_history(self, page=None):
        data = {'page': page}
        resp = self._do('GET') if not page else self._do('GET', data=data)
        return resp

    def upload_image(self, smfile, format='json'):
        """
        Parameters
        ----------
        smfile:  binary --> image file object of binary
        """
        files = smfile
        # files = {
        #     "field1" : ("filename1", open("filePath1", "rb")),
        #     "field2" : ("filename2", open("filePath2", "rb"), "image/jpeg"),
        #     "field3" : ("filename3", open("filePath3", "rb"), "image/jpeg", {"refer" : "localhost"})
        # }
        resp = self._do('POST', files=files)
        return resp

if __name__ == '__main__':
    # pass
    ah = {'Authorization': 'yW47L4kjQK3yeLHYNj7vNjBq3RpEG3Tg'}
    s = SmmsApi('https://sm.ms/api/v2')
    s.endpoint = '/upload_history'
    s.auth_header = ah
    result = s.upload_history()
    print(result)
