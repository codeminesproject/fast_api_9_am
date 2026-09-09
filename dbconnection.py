
import pymysql
import config

def dbConnect():
    try:
        connection_response=pymysql.connect(host=config.db_host,database=config.db_name,
                                            user=config.db_username,password=config.db_password,port=config.db_port)

        if connection_response.open==True:
            return connection_response
    except Exception as e:
        return None