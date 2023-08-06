import mysql.connector
class Csdl:
    def __init__(self, host='192.168.100.220', port=8457, user='Tanquoc', passwd='t@nqu0c1', Db='DBS01'):
        self.host = host
        self.Mydb = mysql.connector.connect(
            host=self.host,
            port=port,
            user=user,
            passwd=passwd,
            database=Db
        )

    def Closed(self):
        self.Mydb.close()

    def CreateTable(self, tablestring):
        try:
            curser = self.Mydb.cursor()
            curser.execute(tablestring)
            print('Tạo Table thành công')
            curser.close()
        except Exception as e:
            print('Tạo bảng Không thành Công')
            curser.close()
            return None

    def GetData(self, query, Method=None):
        global cusor
        try:
            cusor = self.Mydb.cursor()
            cusor.execute(query,Method)
            mydta = cusor.fetchall()
            cusor.close()
            return mydta
        except Exception as e:
            print(str(e))
            cusor.close()
            return None
        pass

    def InsertData(self, query, lstValue):
        try:
            mycusor = self.Mydb.cursor()
            mycusor.execute(query, lstValue)
            self.Mydb.commit()
            print(mycusor.rowcount, 'Duoc insert vao bang')
            mycusor.close()
            return True
        except Exception as e:
            print(str(e))
            mycusor.close()
            return None
        pass

    def UpdateData(self):

        pass

    def Delete(self):

        pass
