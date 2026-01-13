from typing import Union

from fastapi import FastAPI

import mysql.connector

app = FastAPI()


@app.get("/")
def read_root():
    return {"Mikrostoritev": "AdminVozila"}

@app.get("/items/")
def read_items():
    return {"Tu": "So izdelki"}

@app.get("/key/")
def return_key():
    return {"Public key": "Kljuc"}

@app.get("/kraji/")
def get_kraji():
    conn = mysql.connector.connect(
        host="34.44.150.229",
        user="zan",
        password=">tnitm&+NqgoA=q6",
        database="RSOAdminVozila"
    )

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
    return {"Kraji": "kraj"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
    
