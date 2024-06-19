import sqlite3
from storage import Inventory, Object

def init_db():
    conn = sqlite3.connect('game_data.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS inventory (
        id INTEGER PRIMARY KEY,
        status INTEGER NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS objects (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        img TEXT NOT NULL,
        inventory_id INTEGER,
        FOREIGN KEY (inventory_id) REFERENCES inventory(id)
    )
    ''')

    conn.commit()
    conn.close()

def add_inventory(status: int) -> Inventory:
    conn = sqlite3.connect('game_data.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO inventory (status) VALUES (?)', (status,))
    conn.commit()


    inventory_id = cursor.lastrowid
    cursor.execute('SELECT * FROM inventory WHERE id = ?', (inventory_id,))
    inv = cursor.fetchone()
    conn.close()
    
    return Inventory(inv[0],[],inv[1])

def get_inventory(id: int) -> Inventory:
    conn = sqlite3.connect('game_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM inventory WHERE id = ?', (id,))
    inventory = cursor.fetchone()
    conn.close()
    
    objects = get_objects_by_inv(inventory[0])
    
    return Inventory(inventory[0], objects, inventory[1])

def get_all_inventories() -> list[Inventory]:
    conn = sqlite3.connect('game_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM inventory')
    inventories_fetch = cursor.fetchall()
    
    inventories = []
    for inventory in inventories_fetch:
        objects = get_objects_by_inv(inventory[0])
        inventories.append(Inventory(inventory[0], objects, inventory[1]))
    
    conn.close()
    return inventories

def update_inventory(id: int, status: int):
    conn = sqlite3.connect('game_data.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE inventory SET status = ? WHERE id = ?', (status, id))
    conn.commit()
    conn.close()
    
def delete_inventory(id: int):
    conn = sqlite3.connect('game_data.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM inventory WHERE id = ?', (id,))
    conn.commit()
    conn.close()

def any_inventory_exists() -> bool:
    conn = sqlite3.connect('game_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM inventory')
    inventory = cursor.fetchone()
    conn.close()
    return inventory is not None

def add_object(name: str, img: str, inventory_id: int) -> Object:
    conn = sqlite3.connect('game_data.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO objects (name, img, inventory_id) VALUES (?, ?, ?)', (name, img, inventory_id))
    conn.commit()

    object_id = cursor.lastrowid
    cursor.execute('SELECT * FROM objects WHERE id = ?', (object_id,))
    obj = cursor.fetchone()
    conn.close()
    
    return Object(obj[0], obj[1], obj[2], obj[3])

def get_all_objects() -> list[Object]:
    conn = sqlite3.connect('game_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM objects')
    objs = cursor.fetchall()
    
    objects = []
    
    for obj in objs:
        objects.append(Object(obj[0], obj[1], obj[2], obj[3]))
    conn.close()
    
    return objects

def get_objects_by_inv(inventory_id: int) -> list[Object]:
    conn = sqlite3.connect('game_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM objects WHERE inventory_id = ?', (inventory_id,))
    objs = cursor.fetchall()
    conn.close()
    
    objects = []
    for obj in objs:
        objects.append(Object(obj[0], obj[1], obj[2], obj[3]))
    
    return objects

def get_object(id: int) -> Object:
    conn = sqlite3.connect('game_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM objects WHERE id = ?', (id,))
    obj = cursor.fetchone()
    conn.close()
    
    return Object(obj[0], obj[1], obj[2], obj[3])
    
def delete_object(id: int):
    conn = sqlite3.connect('game_data.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM objects WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    