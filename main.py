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
        database="RSOUporabnikPrijava",
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
    logitude: str
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

        # Process results
        for row in rows:
            print(row)  # row is a tuple: (id, name, email)

        # Clean up
        cursor.close()
        conn.close()   
    except Exception as e:
        print("Error: ", e)
    finally:
        cursor.close()
        conn.close() 
    return {"Kraji": "kraj"}


@app.get("/flf/")
def read_root():
    return {"Dela": "In to hitrejs"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
    
