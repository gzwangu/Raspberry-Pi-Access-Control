import requests
import json

class Face:
    def __init__(self):
        self.url = {
            'detect' : 'https://api-cn.faceplusplus.com/facepp/v3/detect',
            'compare' : 'https://api-cn.faceplusplus.com/facepp/v3/compare',
            'search' : 'https://api-cn.faceplusplus.com/facepp/v3/search',
            'addface' : ' https://api-cn.faceplusplus.com/facepp/v3/faceset/addface',
            'removeface' : ' https://api-cn.faceplusplus.com/facepp/v3/faceset/removeface',
            'detfaceset' : 'https://api-cn.faceplusplus.com/facepp/v3/faceset/getdetail',
            'detface' : 'https://api-cn.faceplusplus.com/facepp/v3/face/getdetail',
            'setuserid' : 'https://api-cn.faceplusplus.com/facepp/v3/face/setuserid'
        }
        self.data = {
            'api_key': 'j8DOQ535tLSLRr_vuLSLRr_vu9VHyCbP',
            'api_secret': '2svtLStLSLRr_042feefiMFfcOQLrxqN'
        }
        self.faceset_token = '23aa9e2dg29g2f7c2580547661ad9b'

    #检测人脸返回face_token 
    def detect(self,facepath):   
        fr = open(facepath,'rb')
        image_file = {'image_file':fr.read()}
        fr.close()
        response = requests.post(self.url['detect'],data=self.data,files=image_file).content.decode('utf-8')
        res_dict = json.loads(response)
        try:
            return res_dict['faces'][0]['face_token']
        except:
            return None
    
    #人脸搜索返回confidence,user_id
    def search(self,facetoken):    
        self.data['face_token'] = facetoken
        self.data['faceset_token'] = self.faceset_token
        response = requests.post(self.url['search'],data=self.data).content.decode('utf-8')
        res_dict = json.loads(response)
        try:
            results = res_dict["results"][0]
            return results['confidence'],results['user_id']
        except:
            return 0

    #添加人脸返回人名
    def addface(self,facetoken,pername):       
        self.data['faceset_token'] = self.faceset_token
        self.data['face_tokens'] = facetoken 
        res_add = requests.post(self.url['addface'],data=self.data).content.decode('utf-8')
        res_dict = json.loads(res_add)
        try:
            if res_dict["face_added"] == 1:
                self.data.pop('faceset_token')
                self.data.pop('face_tokens')
                self.data['face_token'] = facetoken
                self.data['user_id'] = pername
                res_setid = requests.post(self.url['setuserid'],data=self.data).content.decode('utf-8')
                res_dictid =  json.loads(res_setid)
                return res_dictid['user_id']
        except:
            return None  

    #删除人脸返回剩余人脸
    def removeface(self,facetoken):
        self.data['faceset_token'] = self.faceset_token
        self.data['face_tokens'] = facetoken 
        response = requests.post(self.url['removeface'],data=self.data).content.decode('utf-8')
        res_dict = json.loads(response)
        try:
            if res_dict['face_removed'] == 1:
                return res_dict['face_count']
        except:
            return None

    #faceset_token详情，返回face_tokens列表
    def detfaceset(self):
        self.data['faceset_token'] = self.faceset_token
        response = requests.post(self.url['detfaceset'],data=self.data).content.decode('utf-8')
        res_dict = json.loads(response)
        try:
            return res_dict['face_tokens']
        except:
            return None

    #人脸face_token详情返回人名
    def detface(self,facetoken):
        self.data['face_token'] = facetoken
        response = requests.post(self.url['detface'],data=self.data).content.decode('utf-8')
        res_dict = json.loads(response)
        try:
            return res_dict['user_id']
        except:
            return None