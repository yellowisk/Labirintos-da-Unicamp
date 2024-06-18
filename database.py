import sqlite3
from store import Inventario, Objetos

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
    return inventory

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
    

def add_object(name, img, inventory_id):
    conn = sqlite3.connect('game_data.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO objects (name, inventory_id) VALUES (?, ?)', (name, img, inventory_id))
    conn.commit()

    object_id = cursor.lastrowid
    cursor.execute('SELECT * FROM objects WHERE id = ?', (object_id,))
    new_object = cursor.fetchone()

    conn.close()
    return Objetos(object_id[0], object_id[1], object_id[2], object_id[3])

def get_objects():
    conn = sqlite3.connect('game_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM objects')
    objects = cursor.fetchall()
    conn.close()
    return objects

def get_objects_by_inventory(inventory_id):
    conn = sqlite3.connect('game_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM objects WHERE inventory_id = ?', (inventory_id,))
    objects = cursor.fetchall()
    conn.close()
    return objects
    
def delete_object(id):
    conn = sqlite3.connect('game_data.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM objects WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    