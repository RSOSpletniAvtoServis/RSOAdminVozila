from typing import Union

from fastapi import FastAPI
from fastapi import HTTPException
import mysql.connector
from mysql.connector import pooling
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

def validate_identifier(name: str) -> str:
    if not re.fullmatch(r"[A-Za-z0-9_]{1,64}", name):
        raise ValueError("Invalid database name")
    return name


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

# Za storitve začetek

class Storitev(BaseModel):
    naziv: str
    uniqueid: str

class Storitev1(BaseModel):
    idstoritev: str
    naziv: str
    aktiven: str
    uniqueid: str

@app.post("/dodajstoritev/")
def dodajStoritev(storitev: Storitev):
    userid = storitev.uniqueid
    try:
        conn = pool.get_connection()
        # Create a cursor
        cursor = conn.cursor()

        query = "INSERT INTO Storitev(NazivStoritve,Aktiven) VALUES (%s,%s)"
        cursor.execute(query,(storitev.naziv,1))
        return {"Storitev": "passed"}
  
    except Exception as e:
        print("Error: ", e)
        return {"Storitev": "failed"}
    finally:
        cursor.close()
        conn.close() 
    return {"Storitev": "unknown"}   

@app.get("/storitve/")
def get_storitve():
    try:
        with pool.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT IDStoritev, NazivStoritve, Aktiven FROM Storitev"
                )
                rows = cursor.fetchall()
        # Fixed columns → no need to read cursor.description
        return [
            {"IDStoritev": row[0], "NazivStoritve": row[1], "Aktiven": row[2]}
            for row in rows
        ]
    except Exception as e:
        print("DB error:", e)
        raise HTTPException(status_code=500, detail="Database error")
    return {"Storitev": "failed"}    


@app.get("/storitev/{storitevid}")
def get_storitev(storitevid: int):
    try:
        with pool.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT IDStoritev, NazivStoritve, Aktiven FROM Storitev WHERE IDStoritev = %s",
                    (storitevid,)
                )

                row = cursor.fetchone()

                if row is None:
                    raise HTTPException(status_code=404, detail="Znamka not found")

                return {"IDStoritev": row[0], "NazivStoritve": row[1], "Aktiven": row[2]}

    except HTTPException:
        raise
    except Exception as e:
        print("DB error:", e)
        raise HTTPException(status_code=500, detail="Database error")
    return {"Storitev": "undefined"}


@app.put("/posodobistoritev/")
def posodobi_storitev(storitev: Storitev1):
    userid = storitev.uniqueid
    try:
        conn = pool.get_connection()
        # Create a cursor
        cursor = conn.cursor()

        query = "UPDATE Storitev SET NazivStoritve = %s, Aktiven = %s WHERE IDStoritev = %s"
        cursor.execute(query,(storitev.naziv,storitev.aktiven,storitev.idstoritev))
        return {"Storitev": "passed"}
  
    except Exception as e:
        print("Error: ", e)
        return {"Storitev": "failed"}
    finally:
        cursor.close()
        conn.close() 
    return {"Storitev": "unknown"}


# Za storitve konec 

# Za statuse zacetek 

class Status(BaseModel):
    naziv: str
    uniqueid: str

class Status1(BaseModel):
    idstatus: str
    naziv: str
    uniqueid: str

@app.post("/dodajstatus/")
def dodajStatus(status: Status):
    userid = status.uniqueid
    try:
        conn = pool.get_connection()
        # Create a cursor
        cursor = conn.cursor()

        query = "INSERT INTO Status(NazivStatusa) VALUES (%s)"
        cursor.execute(query,(status.naziv,))
        return {"Status": "passed"}
  
    except Exception as e:
        print("Error: ", e)
        return {"Status": "failed"}
    finally:
        cursor.close()
        conn.close() 
    return {"Status": "unknown"}   

@app.get("/statusi/")
def get_statusi():
    try:
        with pool.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT IDStatus, NazivStatusa FROM Status"
                )
                rows = cursor.fetchall()
        # Fixed columns → no need to read cursor.description
        return [
            {"IDStatus": row[0], "NazivStatusa": row[1]}
            for row in rows
        ]
    except Exception as e:
        print("DB error:", e)
        raise HTTPException(status_code=500, detail="Database error")
    return {"Status": "failed"}    


@app.get("/status/{statusid}")
def get_status(statusid: int):
    try:
        with pool.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT IDStatus, NazivStatusa FROM Status WHERE IDStatus = %s",
                    (statusid,)
                )

                row = cursor.fetchone()

                if row is None:
                    raise HTTPException(status_code=404, detail="Znamka not found")

                return {"IDStatus": row[0], "NazivStatusa": row[1]}

    except HTTPException:
        raise
    except Exception as e:
        print("DB error:", e)
        raise HTTPException(status_code=500, detail="Database error")
    return {"Status": "undefined"}


@app.put("/posodobistatus/")
def posodobi_status(status: Status1):
    userid = status.uniqueid
    try:
        conn = pool.get_connection()
        # Create a cursor
        cursor = conn.cursor()

        query = "UPDATE Status SET NazivStatusa = %s WHERE IDStatus = %s"
        cursor.execute(query,(status.naziv,status.idstatus))
        return {"Status": "passed"}
  
    except Exception as e:
        print("Error: ", e)
        return {"Status": "failed"}
    finally:
        cursor.close()
        conn.close() 
    return {"Status": "unknown"}


# Za statuse konec

#Za tennante začetek

class Tennant(BaseModel):
    naziv: str
    uniqueid: str



@app.post("/dodajtennanta/")
def dodajTennanta(tennant: Tennant):
    userid = tennant.uniqueid
    try:
        db_name = tennant.naziv.replace(" ", "")
        db_name = validate_identifier(db_name)
        conn = pool.get_connection()
        
        conn.autocommit = False
        cursor = conn.cursor()
        # Create a cursor
        db_narocila = db_name + "Narocilo"
        db_poslovalnice = db_name + "Poslovalnica"
        #add record to tennantlookup
        query = "INSERT INTO TennantLookup(NazivTennanta,TennantDBNarocila,TennantDBPoslovalnice) VALUES (%s,%s,%s)"
        cursor.execute(query,(db_name,db_narocila,db_poslovalnice))
        # Create db narocila for tennant
        query = f"CREATE DATABASE `{db_narocila}`"
        cursor.execute(query)
 
        query = f"CREATE TABLE `{db_narocila}`.Narocilo LIKE RSOSceletonNarocila.Narocilo"
        cursor.execute(query)
        
        query = f"CREATE TABLE `{db_narocila}`.Komunikacija LIKE RSOSceletonNarocila.Komunikacija"
        cursor.execute(query)
        
        query = f"CREATE TABLE `{db_narocila}`.Ocena LIKE RSOSceletonNarocila.Ocena"
        cursor.execute(query)
        
        query = f"CREATE TABLE `{db_narocila}`.Sporocilo LIKE RSOSceletonNarocila.Sporocilo"
        cursor.execute(query)
 
        # Create db Poslovalnice for tennant
        query = f"CREATE DATABASE `{db_poslovalnice}`"
        cursor.execute(query)
        
        query = f"CREATE TABLE `{db_poslovalnice}`.AvtoServis LIKE RSOSceletonPoslovalnice.AvtoServis"
        cursor.execute(query)
        
        query = f"CREATE TABLE `{db_poslovalnice}`.Poslovalnica LIKE RSOSceletonPoslovalnice.Poslovalnica"
        cursor.execute(query)
        
        query = f"CREATE TABLE `{db_poslovalnice}`.Ponuja LIKE RSOSceletonPoslovalnice.Ponuja"
        cursor.execute(query)
        
        query = f"CREATE TABLE `{db_poslovalnice}`.Zaposleni LIKE RSOSceletonPoslovalnice.Zaposleni"
        cursor.execute(query)
        
        query = f"INSERT INTO `{db_poslovalnice}`.AvtoServis(NazivAvtoServis) VALUES (%s)"
        cursor.execute(query,(tennant.naziv,))
        
        conn.commit()
        return {"Tennant": "passed"}
  
    except Exception as e:
        conn.rollback()
        print("Error: ", e)
        return {"Tennant": "failed"}
    finally:
        conn.autocommit = True
        cursor.close()
        conn.close() 
    return {"Tennant": "unknown"}   

@app.get("/tennanti/")
def get_tennanti():
    try:
        with pool.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT IDTennant, NazivTennanta, TennantDBNarocila, TennantDBPoslovalnice FROM TennantLookup"
                )
                rows = cursor.fetchall()
        # Fixed columns → no need to read cursor.description
        return [
            {"IDTennant": row[0], "NazivTennanta": row[1], "TennantDBNarocila": row[2], "TennantDBPoslovalnice": row[3]}
            for row in rows
        ]
    except Exception as e:
        print("DB error:", e)
        raise HTTPException(status_code=500, detail="Database error")
    return {"Tennant": "failed"}    


@app.get("/tenant/{tennantid}")
def get_status(tennantid: int):
    try:
        with pool.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "SELECT IDTennant, NazivTennanta, TennantDBNarocila, TennantDBPoslovalnice FROM TennantLookup WHERE IDTennant = %s",
                    (tennantid,)
                )

                row = cursor.fetchone()

                if row is None:
                    raise HTTPException(status_code=404, detail="Znamka not found")

                return {"IDTennant": row[0], "NazivTennanta": row[1], "TennantDBNarocila": row[2], "TennantDBPoslovalnice": row[3]}

    except HTTPException:
        raise
    except Exception as e:
        print("DB error:", e)
        raise HTTPException(status_code=500, detail="Database error")
    return {"Tennant": "undefined"}



# Za tennante konec


