from typing import Union

from fastapi import FastAPI
from fastapi import HTTPException
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
        with pool.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT IDKraj, NazivKraja, Longitude, Latitude FROM Kraj"
                )

                cols = [c[0] for c in cursor.description]
                rows = cursor.fetchall()   # ⬅️ important

        return [dict(zip(cols, row)) for row in rows]

    except Exception as e:
        print("DB error:", e)
        raise HTTPException(status_code=500, detail="Database error")
    return {"Kraji": "failed"}    


@app.get("/kraj/{krajid}")
def get_kraj(krajid: int):

    try:
        with pool.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT IDKraj, NazivKraja, Longitude, Latitude "
                    "FROM Kraj WHERE IDKraj = %s",
                    (krajid,)
                )

                row = cursor.fetchone()

                if row is None:
                    raise HTTPException(status_code=404, detail="Kraj not found")

                return {
                    "IDKraj": row[0],
                    "NazivKraja": row[1],
                    "Longitude": row[2],
                    "Latitude": row[3],
                }

    except HTTPException:
        raise
    except Exception as e:
        print("DB error:", e)
        raise HTTPException(status_code=500, detail="Database error")
    return {"Kraji": "undefined"}

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



# Za Znamke zacetek

class Znamka(BaseModel):
    naziv: str
    uniqueid: str

class Znamka1(BaseModel):
    idznamka: str
    naziv: str
    uniqueid: str
    
@app.post("/dodajznamko/")
def dodajZnamko(znamka: Znamka):
    userid = znamka.uniqueid
    try:
        conn = pool.get_connection()
        # Create a cursor
        cursor = conn.cursor()

        query = "INSERT INTO Znamka(NazivZnamke) VALUES (%s)"
        cursor.execute(query,(znamka.naziv,))
        return {"Znamka": "passed"}
  
    except Exception as e:
        print("Error: ", e)
        return {"Znamka": "failed"}
    finally:
        cursor.close()
        conn.close() 
    return {"Znamka": "unknown"}    
    
    
@app.get("/znamke/")
def get_znamke():
    try:
        with pool.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT IDZnamka, NazivZnamke FROM Znamka"
                )
                rows = cursor.fetchall()
        # Fixed columns → no need to read cursor.description
        return [
            {"IDZnamka": row[0], "NazivZnamke": row[1]}
            for row in rows
        ]
    except Exception as e:
        print("DB error:", e)
        raise HTTPException(status_code=500, detail="Database error")
    return {"Znamka": "failed"}    


@app.get("/znamka/{znamkaid}")
def get_znamka(znamkaid: int):
    try:
        with pool.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT IDZnamka, NazivZnamke FROM Znamka WHERE IDZnamka = %s",
                    (znamkaid,)
                )

                row = cursor.fetchone()

                if row is None:
                    raise HTTPException(status_code=404, detail="Znamka not found")

                return {"IDZnamka": row[0], "NazivZnamke": row[1]}

    except HTTPException:
        raise
    except Exception as e:
        print("DB error:", e)
        raise HTTPException(status_code=500, detail="Database error")
    return {"Znamke": "undefined"}

@app.put("/posodobiznamko/")
def posodobi_znamko(znamka: Znamka1):
    userid = znamka.uniqueid
    try:
        conn = pool.get_connection()
        # Create a cursor
        cursor = conn.cursor()

        query = "UPDATE Znamka SET NazivZnamke = %s WHERE IDZnamka = %s"
        cursor.execute(query,(znamka.naziv,znamka.idznamka))
        return {"Znamke": "passed"}
  
    except Exception as e:
        print("Error: ", e)
        return {"Znamke": "failed"}
    finally:
        cursor.close()
        conn.close() 
    return {"Znamke": "unknown"}   
    
# Za znamke konec

# Za modele zacetek 

class Model(BaseModel):
    naziv: str
    idznamka: str
    uniqueid: str

class Model1(BaseModel):
    idmodel: str
    naziv: str
    idznamka: str
    uniqueid: str

@app.post("/dodajmodel/")
def dodajModel(model: Model):
    userid = model.uniqueid
    try:
        conn = pool.get_connection()
        # Create a cursor
        cursor = conn.cursor()

        query = "INSERT INTO Model(NazivModel,IDZnamka) VALUES (%s,%s)"
        cursor.execute(query,(model.naziv,model.idznamka))
        return {"Model": "passed"}
  
    except Exception as e:
        print("Error: ", e)
        return {"Model": "failed"}
    finally:
        cursor.close()
        conn.close() 
    return {"Model": "unknown"}   

@app.get("/modeli/{idznamka}")
def get_modeli(idznamka: int):
    try:
        with pool.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT IDModel, NazivModel, IDZnamka FROM Model WHERE IDZnamka = %s",(idznamka,)
                )
                rows = cursor.fetchall()
        # Fixed columns → no need to read cursor.description
        return [
            {"IDModel": row[0], "NazivModel": row[1], "IDZnamka": row[2]}
            for row in rows
        ]
    except Exception as e:
        print("DB error:", e)
        raise HTTPException(status_code=500, detail="Database error")
    return {"Model": "failed"}    


@app.get("/model/{modelid}")
def get_model(modelid: int):
    try:
        with pool.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT IDModel, NazivModel, IDZnamka FROM Model WHERE IDModel = %s",
                    (modelid,)
                )

                row = cursor.fetchone()

                if row is None:
                    raise HTTPException(status_code=404, detail="Znamka not found")

                return {"IDModel": row[0], "NazivModel": row[1], "IDZnamka": row[2]}

    except HTTPException:
        raise
    except Exception as e:
        print("DB error:", e)
        raise HTTPException(status_code=500, detail="Database error")
    return {"Model": "undefined"}


@app.put("/posodobimodel/")
def posodobi_model(model: Model1):
    userid = model.uniqueid
    try:
        conn = pool.get_connection()
        # Create a cursor
        cursor = conn.cursor()

        query = "UPDATE Model SET NazivModel = %s, IDZnamka = %s WHERE IDModel = %s"
        cursor.execute(query,(model.naziv,model.idznamka,model.idmodel))
        return {"Model": "passed"}
  
    except Exception as e:
        print("Error: ", e)
        return {"Model": "failed"}
    finally:
        cursor.close()
        conn.close() 
    return {"Model": "unknown"}

# Za modele konec