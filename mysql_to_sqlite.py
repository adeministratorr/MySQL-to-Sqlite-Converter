import pymysql
import sqlite3
import re

# Bu kısmı kendine göre düzenlemeyi unutma
MYSQL_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'sample_database',
    'port': 3306,
    'charset': 'utf8mb4'
}
# Sqlite veritabanı adını değiştirebilirsin.
SQLITE_DB = 'output.db'

TYPE_MAP = {
    'int': 'INTEGER',
    'tinyint': 'INTEGER',
    'smallint': 'INTEGER',
    'mediumint': 'INTEGER',
    'bigint': 'INTEGER',
    'float': 'REAL',
    'double': 'REAL',
    'decimal': 'REAL',
    'char': 'TEXT',
    'varchar': 'TEXT',
    'text': 'TEXT',
    'mediumtext': 'TEXT',
    'longtext': 'TEXT',
    'date': 'TEXT',
    'datetime': 'TEXT',
    'timestamp': 'TEXT',
    'enum': 'TEXT'
}

def get_columns(mysql_conn, table_name):
    """MySQL'den sütun bilgilerini doğru sırayla al"""
    with mysql_conn.cursor() as cursor:
        cursor.execute(f"""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = '{table_name}'
            AND table_schema = '{MYSQL_CONFIG['database']}'
            ORDER BY ordinal_position
        """)
        return cursor.fetchall()

def create_sqlite_table(sqlite_conn, table_name, columns):
    """SQLite'da tabloyu yeniden oluştur"""
    # Önce mevcut tabloyu sil
    sqlite_conn.execute(f"DROP TABLE IF EXISTS \"{table_name}\"")
    
    columns_def = []
    for col_name, col_type in columns:
        # Tüm sütun isimlerini tırnak içine al
        quoted_name = f'"{col_name}"'
        # Veri tipi dönüşümü
        sqlite_type = TYPE_MAP.get(col_type.lower(), 'TEXT')
        columns_def.append(f"{quoted_name} {sqlite_type}")
    
    create_sql = f"CREATE TABLE \"{table_name}\" (\n"
    create_sql += ",\n".join(columns_def)
    create_sql += "\n)"
    
    try:
        sqlite_conn.execute(create_sql)
        return True
    except Exception as e:
        print(f"Tablo oluşturma hatası ({table_name}): {str(e)}")
        print(f"Oluşturma SQL'i:\n{create_sql}")
        return False

def migrate_data(mysql_conn, sqlite_conn, table_name, columns):
    """Verileri güvenli bir şekilde aktar"""
    with mysql_conn.cursor() as cursor:
        cursor.execute(f"SELECT * FROM `{table_name}`")
        col_names = [f'"{col[0]}"' for col in columns]
        placeholders = ','.join(['?'] * len(col_names))
        
        insert_sql = f"INSERT INTO \"{table_name}\" ({','.join(col_names)}) VALUES ({placeholders})"
        
        total = 0
        while True:
            rows = cursor.fetchmany(100)
            if not rows:
                break
            
            # Veri dönüşümü
            converted = []
            for row in rows:
                row = list(row)
                for i, val in enumerate(row):
                    if isinstance(val, bytes):
                        row[i] = val.decode('utf-8', 'replace')
                converted.append(tuple(row))
            
            try:
                sqlite_conn.executemany(insert_sql, converted)
                total += len(converted)
            except Exception as e:
                print(f"Veri aktarım hatası ({table_name}): {str(e)}")
                print(f"Örnek veri: {converted[0] if converted else 'N/A'}")
                break
        
        print(f"{table_name}: {total} satır aktarıldı")
        return total > 0

def main():
    mysql_conn = pymysql.connect(**MYSQL_CONFIG)
    sqlite_conn = sqlite3.connect(SQLITE_DB)
    
    # SQLite optimizasyonları
    sqlite_conn.execute("PRAGMA journal_mode = MEMORY")
    sqlite_conn.execute("PRAGMA synchronous = OFF")
    
    try:
        with mysql_conn.cursor() as cursor:
            cursor.execute("SHOW TABLES")
            tables = [row[0] for row in cursor.fetchall()]
        
        for table in tables:
            print(f"\nİşleniyor: {table}")
            
            # 1. Sütun bilgilerini al
            columns = get_columns(mysql_conn, table)
            print("Sütunlar:", [col[0] for col in columns])
            
            # 2. SQLite tablosunu oluştur
            if not create_sqlite_table(sqlite_conn, table, columns):
                continue
                
            # 3. Verileri aktar
            if migrate_data(mysql_conn, sqlite_conn, table, columns):
                sqlite_conn.commit()
        
        print("\n✔ Tüm dönüşümler tamamlandı!")
        print(f"Çıktı dosyası: {SQLITE_DB}")
    
    finally:
        mysql_conn.close()
        sqlite_conn.close()

if __name__ == '__main__':
    main()
