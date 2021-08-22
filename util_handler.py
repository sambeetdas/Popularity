import pyodbc
import base64
from datetime import datetime, timedelta
import pandas as pd

con_str = 'DRIVER={SQL Server};SERVER=DESKTOP-JROCJVQ;DATABASE=Popularity;UID=sa;PWD=Sambeet@123;Trusted_Connection=Yes'


class util_handler(object):

    def execute(self, query, is_dml):
        conn = pyodbc.connect(con_str)
        #result = pd.read_sql_query(query, con=conn)

        cursor = conn.cursor()
        cursor.execute(query)        
         
        row = cursor.fetchall()
        
        if(is_dml):
            conn.commit()
       
        cursor.close()
        conn.close()
        return row

    def convert_data_to_json(self, rows): 

        result = []
        counter = 0
        for item in rows:
            index = 0
            subresult = {}
            for val in item:
                subresult.update( {str(item.cursor_description[index][0]).strip() : str(item[index]).strip()} )
                index += 1
            result.append(subresult)
            counter += 1
        return result

    def Encode(self, data):
        encodedBytes = base64.b64encode(data.encode("utf-8"))
        encodedStr = str(encodedBytes, "utf-8")
        return encodedStr

    def Decode(self, data):
        decodedBytes = base64.b64decode(data.encode("utf-8"))
        decodedStr = str(decodedBytes, "utf-8")
        return decodedStr

    def GetAuthToken(self, username, password, valid_for):
        now = datetime.now()
        con_str = username +'||'+ password + '||' + str(now) + '||' + str(now + timedelta(minutes=int(valid_for)))
        token = self.Encode(con_str)
        return token

    def GetCredential(self,token):
        result = self.ExtractAuthToken(token)
        return result

    def ExtractAuthToken(self, token):
        con_str = self.Decode(token)
        list_credentials = con_str.split('||')
        return list_credentials

    def DateValidation(self, exp_date):
        now = datetime.now()
        if(now <= datetime.fromisoformat(exp_date)):
            return True
        else:
            return False
        



