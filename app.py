from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3

app = FastAPI()

# Modelo de datos
class Item(BaseModel):
    name: str
    description: str | None = None

# Inicializar DB
def init_db():
    conn = sqlite3.connect("items.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

# Endpoints CRUD
@app.post("/items/")
def create_item(item: Item):
    conn = sqlite3.connect("items.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO items (name, description) VALUES (?, ?)", (item.name, item.description))
    conn.commit()
    item_id = cursor.lastrowid
    conn.close()
    return {"id": item_id, "name": item.name, "description": item.description}

@app.get("/items/{item_id}")
def read_item(item_id: int):
    conn = sqlite3.connect("items.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, description FROM items WHERE id=?", (item_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {"id": row[0], "name": row[1], "description": row[2]}
    else:
        raise HTTPException(status_code=404, detail="Item not found")

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    conn = sqlite3.connect("items.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE items SET name=?, description=? WHERE id=?", (item.name, item.description, item_id))
    conn.commit()
    updated = cursor.rowcount
    conn.close()
    if updated:
        return {"id": item_id, "name": item.name, "description": item.description}
    else:
        raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    conn = sqlite3.connect("items.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM items WHERE id=?", (item_id,))
    conn.commit()
    deleted = cursor.rowcount
    conn.close()
    if deleted:
        return {"message": "Item deleted"}
    else:
        raise HTTPException(status_code=404, detail="Item not found")
