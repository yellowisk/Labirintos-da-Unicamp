import sqlite3
from storage import Inventario, Objetos

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
        inventory_id INTEGER,
        FOREIGN KEY (inventory_id) REFERENCES inventory(id)
    )
    ''')

    conn.commit()
    conn.close()

def add_inventory(status):
    conn = sqlite3.connect('game_data.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO inventory (status) VALUES (?)', (status,))
    conn.commit()


    inventory_id = cursor.lastrowid
    cursor.execute('SELECT * FROM inventory WHERE id = ?', (inventory_id,))
    new_inventory = cursor.fetchone()

    conn.close()
    return Inventario(new_inventory[0],[],new_inventory[1])

def get_inventory(id):
    conn = sqlite3.connect('game_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM inventory WHERE id = ?', (id,))
    inventory = cursor.fetchone()
    conn.close()
    
    objects = get_objects_by_inventory(inventory[0])
    
    return Inventario(inventory[0], objects, inventory[1])

def get_all_inventories():
    conn = sqlite3.connect('game_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM inventory')
    inventories_fetch = cursor.fetchall()
    
    inventories = []
    for inventory in inventories_fetch:
        objects = get_objects_by_inventory(inventory[0])
        inventories.append(Inventario(inventory[0], objects, inventory[1]))
    
    conn.close()
    return inventories

def update_inventory(id, status):
    conn = sqlite3.connect('game_data.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE inventory SET status = ? WHERE id = ?', (status, id))
    conn.commit()
    conn.close()
    
def delete_inventory(id):
    conn = sqlite3.connect('game_data.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM inventory WHERE id = ?', (id,))
    conn.commit()
    conn.close()

def any_inventory_exists():
    conn = sqlite3.connect('game_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM inventory')
    inventory = cursor.fetchone()
    conn.close()
    return inventory is not None

def add_object(name, img, inventory_id):
    conn = sqlite3.connect('game_data.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO objects (name, inventory_id) VALUES (?, ?)', (name, img, inventory_id))
    conn.commit()

    object_id = cursor.lastrowid
    cursor.execute('SELECT * FROM objects WHERE id = ?', (object_id,))
    object = cursor.fetchone()

    conn.close()
    return Objetos(object[0], object[1], object[2], object[3])

def get_all_objects():
    conn = sqlite3.connect('game_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM objects')
    objects_fetch = cursor.fetchall()
    
    objects = []
    
    for object in objects_fetch:
        objects.append(Objetos(object[0], object[1], object[2], object[3]))
    
    conn.close()
    return objects

def get_objects_by_inventory(inventory_id):
    conn = sqlite3.connect('game_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM objects WHERE inventory_id = ?', (inventory_id,))
    objects_fetch = cursor.fetchall()
    conn.close()
    
    objects = []
    for object in objects_fetch:
        objects.append(Objetos(object[0], object[1], object[2], object[3]))
    
    return objects

def get_object(id):
    conn = sqlite3.connect('game_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM objects WHERE id = ?', (id,))
    object = cursor.fetchone()
    conn.close()
    return Objetos(object[0], object[1], object[2], object[3])
    
def delete_object(id):
    conn = sqlite3.connect('game_data.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM objects WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    