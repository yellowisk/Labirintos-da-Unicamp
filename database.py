import sqlite3
from storage import Inventory, Object
from maze import Maze
from individual import Individual, Player, Enemy, Colleague

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
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS mazes (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        background TEXT NOT NULL,
        path TEXT NOT NULL
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS individuals (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        pos_x INTEGER NOT NULL,
        pos_y INTEGER NOT NULL,
        imgs TEXT NOT NULL,
        maze_id INTEGER
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS players (
        id INTEGER PRIMARY KEY,
        lives INTEGER NOT NULL,
        time INTEGER NOT NULL,
        points INTEGER NOT NULL,
        individual_id INTEGER,
        FOREIGN KEY (individual_id) REFERENCES individuals(id)
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS enemies (
        id INTEGER PRIMARY KEY,
        speed INTEGER NOT NULL,
        individual_id INTEGER,
        FOREIGN KEY (individual_id) REFERENCES individuals(id)
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS colleagues (
        id INTEGER PRIMARY KEY,
        is_statue INTEGER NOT NULL,
        individual_id INTEGER,
        FOREIGN KEY (individual_id) REFERENCES individuals(id)
    )
    ''')

    conn.commit()
    conn.close()

# ----------------------------
# ******** INVENTORY *********
# ----------------------------

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

# ----------------------------
# ******** OBJECTS ***********
# ----------------------------

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

# ----------------------------
# ******** MAZES *************
# ----------------------------

def add_maze(name: str, background: str, matrix: list[list[int]]):
    path = ''
    for row in matrix:
        path += ''.join(map(str, row)) + '\n'
    conn = sqlite3.connect('game_data.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO mazes (name, background, path) VALUES (?, ?, ?)', (name, background, path))
    conn.commit()
    conn.close()
    
    id = cursor.lastrowid
    
    return Maze(id, name, background, matrix)
    
def get_maze(id: int) -> tuple[str, str, list[list[int]]]:
    conn = sqlite3.connect('game_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM mazes WHERE id = ?', (id,))
    maze = cursor.fetchone()
    conn.close()
    
    matrix = []
    for row in maze[3].split('\n'):
        matrix.append(list(map(int, row)))
    
    return Maze(maze[0], maze[1], matrix[2], matrix)

def get_all_mazes() -> list[Maze]:
    conn = sqlite3.connect('game_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM mazes')
    mazes = cursor.fetchall()
    conn.close()
    
    mazes_list = []
    for maze in mazes:
        matrix = []
        for row in maze[3].split('\n'):
            matrix.append(list(map(int, row)))
        mazes_list.append(Maze(maze[0], maze[1], maze[2], matrix))
    
    return mazes_list

def update_maze(id: int, matrix: list[list[int]]):
    path = ''
    for row in matrix:
        path += ''.join(map(str, row)) + '\n'
    conn = sqlite3.connect('game_data.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE mazes SET path = ? WHERE id = ?', (path, id))
    conn.commit()
    conn.close()

def delete_maze(id: int):
    conn = sqlite3.connect('game_data.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM mazes WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    
# ----------------------------
# ******** INDIVIDUALS *******
# ----------------------------

def add_individual(name: str, pos_x: int, pos_y: int, imgs: list[str], maze_id: int) -> Individual:
    conn = sqlite3.connect('game_data.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO individuals (name, pos_x, pos_y, imgs, maze_id) VALUES (?, ?, ?, ?, ?)', (name, pos_x, pos_y, ';'.join(imgs), maze_id))
    conn.commit()
    id = cursor.lastrowid
    conn.close()
    
    return Individual(id, (pos_x, pos_y), imgs, maze_id)

def get_individual(id: int) -> Individual:
    conn = sqlite3.connect('game_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM individuals WHERE id = ?', (id,))
    ind = cursor.fetchone()
    conn.close()
    
    return Individual(ind[0], ind[1], (ind[2], ind[3]), ind[4].split(';'), ind[5])

def get_all_individuals() -> list[Individual]:
    conn = sqlite3.connect('game_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM individuals')
    inds = cursor.fetchall()
    conn.close()
    
    individuals = []
    for ind in inds:
        individuals.append(ind[0], ind[1], (ind[2], ind[3]), ind[4].split(';'), ind[5])
    
    return individuals

def get_individuals_by_maze(maze_id: int) -> list[Individual]:
    conn = sqlite3.connect('game_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM individuals WHERE maze_id = ?', (maze_id,))
    inds = cursor.fetchall()
    conn.close()
    
    individuals = []
    for ind in inds:
        individuals.append(Individual(ind[0], ind[1], (ind[2], ind[3]), ind[4].split(';'), ind[5]))
    
    return individuals

def update_ind_maze(id: int, maze_id: int):
    conn = sqlite3.connect('game_data.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE individuals SET maze_id = ? WHERE id = ?', (maze_id, id))
    conn.commit()
    conn.close()
    
def update_ind_pos(id: int, x: int, y: int):
    conn = sqlite3.connect('game_data.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE individuals SET pos_x = ?, pos_y = ? WHERE id = ?', (x, y, id))
    conn.commit()
    conn.close()

def delete_individual(id: int):
    conn = sqlite3.connect('game_data.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM individuals WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    
# ----------------------------
# ******** PLAYERS **********
# ----------------------------

def add_player(name: str, pos_x: int, pos_y: int, imgs: list[str], maze_id: int) -> Player:
    add_individual(name, pos_x, pos_y, imgs, maze_id)
    conn = sqlite3.connect('game_data.db')
    cursor = conn.cursor()
    ind_d = cursor.lastrowid
    cursor.execute('INSERT INTO players (lives, time, points, individual_id) VALUES (?, ?, ?, ?)', (3, 0, 0, id))
    player_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return Player(player_id, name, (pos_x, pos_y), imgs, maze_id, ind_d)

def get_player(id: int) -> Player:
    conn = sqlite3.connect('game_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM players WHERE id = ?', (id,))
    player = cursor.fetchone()
    conn.close()
    
    ind = get_individual(player[4])
    player = Player(player[0], ind.name, ind.position, ind.imgs, ind.maze_id, player[4])
    player.lives = player[1]
    player.time = player[2]
    player.points = player[3]
    
    return player

def player_by_ind(ind_id: int) -> Player:
    conn = sqlite3.connect('game_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM players WHERE individual_id = ?', (ind_id,))
    player = cursor.fetchone()
    conn.close()
    
    ind = get_individual(player[4])
    player = Player(player[0], ind.name, ind.position, ind.imgs, ind.maze_id, player[4])
    player.lives = player[1]
    player.time = player[2]
    player.points = player[3]
    
    return player

def player_by_maze(maze_id: int) -> list[Player]:
    conn = sqlite3.connect('game_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM players WHERE maze_id = ?', (maze_id,))
    players = cursor.fetchall()
    conn.close()
    
    players_list = []
    for player in players:
        ind = get_individual(player[4])
        players_list.append(Player(player[0], ind.name, ind.position, ind.imgs, ind.maze_id, player[4]))
    
    return players_list

def update_life(id: int, lives: int):
    conn = sqlite3.connect('game_data.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE players SET lives = ? WHERE id = ?', (lives, id))
    conn.commit()
    conn.close()
    
def update_time(id: int, time: int):
    conn = sqlite3.connect('game_data.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE players SET time = ? WHERE id = ?', (time, id))
    conn.commit()
    conn.close()
    
def update_points(id: int, points: int):
    conn = sqlite3.connect('game_data.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE players SET points = ? WHERE id = ?', (points, id))
    conn.commit()
    conn.close()
    
def delete_player(id: int):
    conn = sqlite3.connect('game_data.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM players WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    
# ----------------------------
# ******** ENEMIES **********
# ----------------------------

def add_enemy(speed: int, name: str, pos_x: int, pos_y: int, imgs: list[str], maze_id: int) -> Enemy:
    add_individual(name, pos_x, pos_y, imgs, maze_id)
    conn = sqlite3.connect('game_data.db')
    cursor = conn.cursor()
    ind_id = cursor.lastrowid
    cursor.execute('INSERT INTO enemies (speed, individual_id) VALUES (?, ?)', (speed, ind_id))
    enemy_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return Enemy(enemy_id, speed, name, (pos_x, pos_y), imgs, maze_id, ind_id)

def get_enemy(id: int) -> Enemy:
    conn = sqlite3.connect('game_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM enemies WHERE id = ?', (id,))
    enemy = cursor.fetchone()
    conn.close()
    
    ind = get_individual(enemy[3])
    enemy = Enemy(enemy[0], enemy[1], ind.name, ind.position, ind.imgs, ind.maze_id, enemy[3])
    
    return enemy

def enemy_by_ind(ind_id: int) -> Enemy:
    conn = sqlite3.connect('game_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM enemies WHERE individual_id = ?', (ind_id,))
    enemy = cursor.fetchone()
    conn.close()
    
    ind = get_individual(enemy[3])
    enemy = Enemy(enemy[0], enemy[1], ind.name, ind.position, ind.imgs, ind.maze_id, enemy[3])
    
    return enemy

def enemy_by_maze(maze_id: int) -> list[Enemy]:
    conn = sqlite3.connect('game_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM enemies WHERE maze_id = ?', (maze_id,))
    enemies = cursor.fetchall()
    conn.close()
    
    enemies_list = []
    for enemy in enemies:
        ind = get_individual(enemy[3])
        enemies_list.append(Enemy(enemy[0], enemy[1], ind.name, ind.position, ind.imgs, ind.maze_id, enemy[3]))
    
    return enemies_list

def update_speed(id: int, speed: int):
    conn = sqlite3.connect('game_data.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE enemies SET speed = ? WHERE id = ?', (speed, id))
    conn.commit()
    conn.close()
    
def delete_enemy(id: int):
    conn = sqlite3.connect('game_data.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM enemies WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    
# ----------------------------
# ******** COLLEAGUES ********
# ----------------------------

def add_colleague(name: str, pos_x: int, pos_y: int, imgs: list[str], maze_id: int) -> Colleague:
    add_individual(name, pos_x, pos_y, imgs, maze_id)
    conn = sqlite3.connect('game_data.db')
    cursor = conn.cursor()
    ind_id = cursor.lastrowid
    cursor.execute('INSERT INTO colleagues (is_statue, individual_id) VALUES (?, ?)', (0, ind_id))
    colleague_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return Colleague(colleague_id, name, (pos_x, pos_y), imgs, maze_id, ind_id)

def get_colleague(id: int) -> Colleague:
    conn = sqlite3.connect('game_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM colleagues WHERE id = ?', (id,))
    colleague = cursor.fetchone()
    conn.close()
    
    ind = get_individual(colleague[2])
    colleague = Colleague(colleague[0], ind.name, ind.position, ind.imgs, ind.maze_id, colleague[2])
    colleague.is_statue = colleague[1]
    
    return colleague

def colleague_by_ind(ind_id: int) -> Colleague:
    conn = sqlite3.connect('game_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM colleagues WHERE individual_id = ?', (ind_id,))
    colleague = cursor.fetchone()
    conn.close()
    
    ind = get_individual(colleague[2])
    colleague = Colleague(colleague[0], ind.name, ind.position, ind.imgs, ind.maze_id, colleague[2])
    colleague.is_statue = colleague[1]
    
    return colleague

def colleague_by_maze(maze_id: int) -> list[Colleague]:
    conn = sqlite3.connect('game_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM colleagues WHERE maze_id = ?', (maze_id,))
    colleagues = cursor.fetchall()
    conn.close()
    
    colleagues_list = []
    for colleague in colleagues:
        ind = get_individual(colleague[2])
        colleagues_list.append(Colleague(colleague[0], ind.name, ind.position, ind.imgs, ind.maze_id, colleague[2]))
    
    return colleagues_list

def update_statue(id: int, is_statue: int):
    conn = sqlite3.connect('game_data.db')
    cursor = conn.cursor()
    cursor.execute('UPDATE colleagues SET is_statue = ? WHERE id = ?', (is_statue, id))
    conn.commit()
    conn.close()
    
def delete_colleague(id: int):
    conn = sqlite3.connect('game_data.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM colleagues WHERE id = ?', (id,))
    conn.commit()
    conn.close()