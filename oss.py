import os
import urllib.request
import urllib.parse

class OSS():
    def __init__(self, ak, sk):
        self.auth = (ak, sk)
        self.endpoint = 'https://oss-cn-shanghai.aliyuncs.com'
        self.bucketName = 'picture-faceid'
        self.bucketUrl = f'https://{self.bucketName}.oss-cn-shanghai.aliyuncs.com'
        self.bucket = self.get_bucket()

    def get_bucket(self):
        url = f'{self.endpoint}/?{urllib.parse.urlencode({"prefix": ""})}'
        req = urllib.request.Request(url=url)
        req.add_header("Authorization", self.get_auth_header("GET", url))
        with urllib.request.urlopen(req) as f:
            body = f.read().decode('utf-8')
        bucket_names = [line.split(">")[1].split("<")[0] for line in body.splitlines() if "<Name>" in line]
        if self.bucketName not in bucket_names:
            raise ValueError(f'Bucket {self.bucketName} does not exist')
        return self.bucketUrl

    def get_auth_header(self, method, url):
        date = self.get_gmt_time()
        auth_string = f'{method}\n\n\n{date}\n/{self.bucketName}/'
        auth_header = f"OSS {self.auth[0]}:{self.get_signature(auth_string)}"
        return auth_header

    def get_gmt_time(self):
        from datetime import datetime
        from email.utils import formatdate
        now = datetime.utcnow()
        return formatdate(timeval=now.timestamp(), localtime=False, usegmt=True)

    def get_signature(self, auth_string):
        import hmac
        import base64
        signature = base64.b64encode(hmac.new(self.auth[1].encode(), auth_string.encode(), 'sha1').digest()).decode()
        return signature

    def uploadFile(self, fileUrl, key):
        self.listObj(prefix='总目录')
        key = key.replace('\\', '/')
        if key[0] == '/':
            key = key[1:]
        with open(fileUrl, 'rb') as f:
            data = f.read()
            headers = {'Content-Type': 'application/octet-stream'}
            url = f'{self.bucket}/{urllib.parse.quote(key)}'
            req = urllib.request.Request(url, data=data, headers=headers, method='PUT')
            req.add_header('Authorization', self.get_auth_header('PUT', url))
            with urllib.request.urlopen(req) as f:
                response = f.read().decode('utf-8')
        return f'{self.bucket}/{urllib.parse.quote(key)}'

    def listObj(self, prefix):
        url = f'{self.bucket}/?{urllib.parse.urlencode({"prefix": prefix})}'
        req = urllib.request.Request(url=url)
        req.add_header("Authorization", self.get_auth_header("GET", url))
        with urllib.request.urlopen(req) as f:
            body = f.read().decode('utf-8')
        objects = [line.split(">")[1].split("<")[0] for line in body.splitlines() if "<Key>" in line]
        for obj in objects:
            print('file: ' + obj)

    def uploadUrl(self, url):
        suffix = os.path.splitext(url)[1].lstrip('.')
        tmp = os.path.split(url)[1]
        key = os.path.join('总目录', tmp)
        req = urllib.request.Request(url=url)
        with urllib.request.urlopen(req) as f:
            data = f
