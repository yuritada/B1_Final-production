import sqlite3

DB_PATH = 'travel.db'

def init_db(test):
    """データベースを初期化し、必要なテーブルを作成"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS travel_logs (
            log_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            user_id INTEGER NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(user_id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS spots (
            spot_id INTEGER PRIMARY KEY AUTOINCREMENT,
            spot_name TEXT NOT NULL,
            log_id INTEGER NOT NULL,
            itinerary_number INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            access_rating INTEGER,
            experience_rating INTEGER,
            price_rating INTEGER,
            latitude REAL,
            longitude REAL,
            FOREIGN KEY(log_id) REFERENCES travel_logs(log_id),
            FOREIGN KEY(user_id) REFERENCES users(user_id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS images (
            image_id INTEGER PRIMARY KEY AUTOINCREMENT,
            image_path TEXT NOT NULL,
            user_id INTEGER NOT NULL,
            log_id INTEGER NOT NULL,
            itinerary_number INTEGER NOT NULL,
            image_number INTEGER NOT NULL,
            FOREIGN KEY(user_id) REFERENCES users(user_id),
            FOREIGN KEY(log_id) REFERENCES travel_logs(log_id)
        )
    ''')
    if test == True:
        # テストデータを挿入
        cursor.execute('''
            INSERT INTO users (username, password) VALUES
            ('user1', 'password1'),
            ('user2', 'password2')
        ''')

        cursor.execute('''
            INSERT INTO travel_logs (title, user_id) VALUES ('旅行1', 1)
        ''')

        cursor.execute('''
            INSERT INTO spots (log_id ,spot_name ,itinerary_number, user_id, access_rating, experience_rating, price_rating, latitude, longitude)
            VALUES (1 ,'hoge', 3, 1, 5, 6, 7, 35.658034, 139.701636)
        ''')

        cursor.execute('''
            INSERT INTO images (image_path, user_id, log_id, itinerary_number, image_number)
            VALUES ('static/uploads/e_1114.png', 2, 1, 4, 5)
        ''')

    conn.commit()
    conn.close()
    print('データベース初期化完了')

def get_db_connection():
    """データベース接続を取得"""
    return sqlite3.connect(DB_PATH)

def get_db_connection():
    """データベース接続を作成"""
    try:
        conn = sqlite3.connect(DB_PATH)
        return conn
    except sqlite3.Error as e:
        print(f"データベース接続エラー: {e}")
        return None

def close_db_connection(conn):
    """データベース接続を閉じる"""
    if conn:
        conn.close()

def insert_into_table(table_name, data):
    """指定されたテーブルにデータを挿入"""
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()

        placeholders = ', '.join(['?'] * len(data))  # プレースホルダを生成
        columns = ', '.join(data.keys())  # カラム名を結合
        sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

        cursor.execute(sql, tuple(data.values()))
        conn.commit()  # データベースに反映
        last_id = cursor.lastrowid  # 挿入されたレコードのIDを取得
        close_db_connection(conn)
        return last_id

    return None

def select_from_table(table_name, condition=None):
    """指定されたテーブルからデータを取得"""
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor()
        
        # 条件が指定されていなければ、全件取得
        if condition:
            sql = f"SELECT * FROM {table_name} WHERE {condition}"
        else:
            sql = f"SELECT * FROM {table_name}"

        cursor.execute(sql)
        rows = cursor.fetchall()
        close_db_connection(conn)
        return rows

    return None

# ユーザー関連の操作
def insert_user(username, password):
    """新しいユーザーをデータベースに挿入"""
    data = {'username': username, 'password': password}
    return insert_into_table('users', data)

def get_user_by_username(username):
    """ユーザー名でユーザーを検索"""
    condition = f"username = '{username}'"
    return select_from_table('users', condition)

# 旅ログ関連の操作
def insert_travel_log(title, user_id):
    """新しい旅ログをデータベースに登録"""
    data = {'title': title, 'user_id': user_id}
    return insert_into_table('travel_logs', data)

def get_travel_logs_by_user(user_id):
    """特定のユーザーの旅ログを取得"""
    condition = f"user_id = {user_id}"
    return select_from_table('travel_logs', condition)

# スポット関連の操作
def insert_spot(log_id, spot_name, itinerary_number, user_id, access_rating, experience_rating, price_rating, latitude, longitude):
    """新しいスポットを登録"""
    data = {
        'log_id': log_id,
        'spot_name': spot_name,
        'itinerary_number': itinerary_number,
        'user_id': user_id,
        'access_rating': access_rating,
        'experience_rating': experience_rating,
        'price_rating': price_rating,
        'latitude': latitude,
        'longitude': longitude
    }
    return insert_into_table('spots', data)

def get_spots_by_log_id(log_id):
    """特定の旅ログに関連するスポットを取得"""
    condition = f"log_id = {log_id}"
    return select_from_table('spots', condition)

# 画像関連の操作
def insert_image(image_path, user_id, log_id, itinerary_number, image_number):
    """新しい画像を登録"""
    data = {
        'image_path': image_path,
        'user_id': user_id,
        'log_id': log_id,
        'itinerary_number': itinerary_number,
        'image_number': image_number
    }
    return insert_into_table('images', data)

def get_images_by_log_id(log_id):
    """特定の旅ログに関連する画像を取得"""
    condition = f"log_id = {log_id}"
    return select_from_table('images', condition)

if __name__ == '__main__':
    init_db(test=True)
    # print(get_user_by_username('user1'))
    # print(get_travel_logs_by_user(1))
    # print(get_spots_by_log_id(1))
    # print(get_images_by_log_id(1))
    # print(insert_user('user3', 'password3'))
    # print(insert_travel_log('旅行2', 1))
    # print(insert_spot(2, 1, 1, 4, 3, 2, 35.658034, 139.701636))
    # print(insert_image('static/uploads/e_1114.png.jpg', 1, 1, 1, 1)                       