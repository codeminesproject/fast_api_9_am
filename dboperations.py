
from dbconnection import dbConnect

def insert(query):
    try:
        connect = dbConnect()
        if connect is not None:
            with connect.cursor() as cur:
                cur.execute(query)
                connect.commit()
                return True
        else:
            return None
    except Exception as e:
        error_details = {"error_type":type(e).__name__,"error_details":str(e)}
        return None


def update(query):
    try:
        connect = dbConnect()
        if connect is not None:
            with connect.cursor() as cur:
                cur.execute(query)
                connect.commit()
                return True
        else:
            return None
    except Exception as e:
        error_details = {"error_type":type(e).__name__,"error_details":str(e)}
        return None
    
def delete(query):
    try:
        connect = dbConnect()
        if connect is not None:
            with connect.cursor() as cur:
                cur.execute(query)
                connect.commit()
                return True
        else:
            return None
    except Exception as e:
        error_details = {"error_type":type(e).__name__,"error_details":str(e)}
        return None


def getSingleData(query):
    try:
        connect = dbConnect()
        if connect is not None:
            with connect.cursor() as cur:
                cur.execute(query)
                data = cur.fetchone()
                return data
        else:
            return None
    except Exception as e:
        error_details = {"error_type":type(e).__name__,"error_details":str(e)}
        return None

def getAllData(query):
    try:
        connect = dbConnect()
        if connect is not None:
            with connect.cursor() as cur:
                cur.execute(query)
                data = cur.fetchall()
                return data
        else:
            return None
    except Exception as e:
        error_details = {"error_type":type(e).__name__,"error_details":str(e)}
        return None
        
