import pymysql

class Mysql:
    def __init__(self):   
        self.host = '192.168.1.102'
        self.user = 'root'
        self.password = '666888'
        self.port = 3306
        self.db = 'acestem'
        self.conn = pymysql.connect(host=self.host,user=self.user,password=self.password,port=self.port,db=self.db)
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
               
    def __del__(self):
        # 关闭数据库连接
        self.cursor.close()
        self.conn.close()

    def insert(self,date_time,face_token,confidence,face_name,user_id):
        sql = "INSERT INTO acsrecord VALUES (%s,%s,%s,%s,%s)"
        try:
            self.cursor.execute(sql,(date_time,face_token,confidence,face_name,user_id))
            self.conn.commit()
        except:
            self.conn.rollback()

    def query(self):
        sql = "SELECT * FROM acsrecord ORDER BY date_time DESC"
        try:
            self.cursor.execute(sql)
            record = self.cursor.fetchall()
            return record
        except:
            self.conn.rollback()