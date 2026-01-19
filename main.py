from typing import Union

from fastapi import FastAPI

import mysql.connector
from mysql.connector import pooling
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
try:
    pool = mysql.connector.pooling.MySQLConnectionPool(
        pool_name="mypool",
        pool_size=5,
        host="34.44.150.229",
        user="zan",
        password=">tnitm&+NqgoA=q6",
        database="RSOAdminVozila",
        autocommit=True
    )
except Exception as e:
    print("Error: ",e)
    
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins (dev only!)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Kraj(BaseModel):
    naziv: str
    longitude: str
    latitude: str
    uniqueid: str

class Kraj1(BaseModel):
    idkraj: str
    naziv: str
    longitude: str
    latitude: str
    uniqueid: str

@app.get("/")
def read_root():
    return {"Mikrostoritev": "AdminVozila"}

@app.get("/items/")
def read_items():
    return {"Tu": "So izdelki"}

@app.get("/key/")
def return_key():
    return {"Public key": "Kljuc"}

@app.post("/dodajkraj/")
def dodajKraj(kraj: Kraj):
    userid = kraj.uniqueid
    try:
        conn = pool.get_connection()
        # Create a cursor
        cursor = conn.cursor()

        query = "INSERT INTO Kraj(NazivKraja,Longitude,Latitude) VALUES (%s,%s,%s)"
        cursor.execute(query,(kraj.naziv,kraj.longitude,kraj.latitude))
        return {"Kraji": "passed"}
  
    except Exception as e:
        print("Error: ", e)
        return {"Kraji": "failed"}
    finally:
        cursor.close()
        conn.close() 
    return {"Kraji": "unknown"}    
    
    
@app.get("/kraji/")
def get_kraji():
    try:
        conn = pool.get_connection()
        # Create a cursor
        cursor = conn.cursor()

        # Run a SELECT query
        query = "SELECT * FROM Kraj"
        cursor.execute(query)

        # Fetch all rows
        rows = cursor.fetchall()

        result = {row['id']: row for row in rows}
        return result
 
    except Exception as e:
        print("Error: ", e)
        return {"Kraji": "failed", "Error":, e}
    finally:
        cursor.close()
        conn.close() 
    return {"Kraji": "failed"}    

@app.get("/kraj/{krajid}")
def get_kraj(krajid: int):
    
    try:
        conn = pool.get_connection()
        # Create a cursor
        cursor = conn.cursor()

        # Run a SELECT query
        query = "SELECT * FROM Kraj where IDKraj = %s"
        cursor.execute(query,(krajid,))

        row = cursor.fetchone()

        if row is not None:
            print(row)
            return {"IDKraj": row[0], "NazivKraja": row[1], "Longitude": row[2], "Latitude": row[3]}
 
    except Exception as e:
        print("Error: ", e)
    finally:
        cursor.close()
        conn.close() 
    return {"Kraji": "failed"}

@app.put("/posodobikraj/")
def posodobi_kraj(kraj: Kraj1):
    userid = kraj.uniqueid
    try:
        conn = pool.get_connection()
        # Create a cursor
        cursor = conn.cursor()

        query = "UPDATE Kraj SET NazivKraja = %s, Longitude = %s, Latitude = %s WHERE IDKraj = %s"
        cursor.execute(query,(kraj.naziv,kraj.longitude,kraj.latitude,kraj.idkraj))
        return {"Kraji": "passed"}
  
    except Exception as e:
        print("Error: ", e)
        return {"Kraji": "failed"}
    finally:
        cursor.close()
        conn.close() 
    return {"Kraji": "unknown"}    



@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
    
