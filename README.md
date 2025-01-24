**MySQL to SQLite Converter**  
**GitHub Repository Documentation**  

---

### 📌 **Project Description**  
This Python script is designed to convert MySQL databases to SQLite. Key features include:  
- Automatic table schema conversion  
- Data type adaptations (MySQL → SQLite)  
- Automatic quoting of reserved keywords  
- Optimization for large datasets  
- Error handling and detailed logging  

---

### 🚀 **Features**  
- **Schema Conversion:**  
  - Converts MySQL `CREATE TABLE` statements to SQLite-compatible syntax.  
  - Parses indexes, foreign keys, and custom constraints.  
  - Removes SQLite-unsupported clauses (`AUTO_INCREMENT`, `ENGINE`, `UNSIGNED`).  

- **Data Migration:**  
  - High-performance bulk inserts (`executemany`).  
  - UTF-8 encoding support.  
  - Automatic binary data conversion.  

- **Error Handling:**  
  - Detailed logging for table creation and data migration errors.  
  - Automatic table cleanup and recreation.  

---

### 📦 **Installation**  
1. **Requirements:**  
   ```bash
   pip install pymysql
   ```

2. **Clone the Repository:**  
   ```bash
   git clone https://github.com/adeministratorr/MySQL-to-Sqlite-Converter.git
   cd mysql-to-sqlite-converter
   ```

---

### ⚙️ **Configuration**  
Edit the following section in the script:  
```python
MYSQL_CONFIG = {
    'host': 'localhost',
    'user': 'your_user',
    'password': 'your_password',
    'database': 'your_database',
    'port': 3306,
    'charset': 'utf8mb4'
}

SQLITE_DB = 'output.db'  # SQLite output file
```

---

### 🛠 **Usage**  
```bash
python mysql_to_sqlite.py
```

**Output:**  
```
✅ All tables migrated successfully!
📂 SQLite file: output.db
```

---

### 🔧 **Technical Details**  
#### **Data Type Mapping**  
| MySQL          | SQLite       |
|----------------|--------------|
| INT, TINYINT   | INTEGER      |
| VARCHAR, TEXT  | TEXT         |
| FLOAT, DOUBLE  | REAL         |
| DATETIME       | TEXT         |

#### **Reserved Keywords**  
SQLite reserved keywords (e.g., `index`, `group`) are automatically quoted:  
```sql
CREATE TABLE "group" ("index" INTEGER, ...)
```

---

### 🐛 **Troubleshooting**  
1. **Common Errors:**  
   - **OperationalError: near "index": syntax error** → Quote column names.  
   - **Encoding Errors** → Use `charset='utf8mb4'` in the MySQL connection.  

2. **Error Logs:**  
   ```log
   [ERROR] Table creation failed (users): no such column: email
   [DEBUG] Faulty SQL: CREATE TABLE users (id INT, email VARCHAR(255))
   ```

---

### ⚡ **Optimization Tips**  
- **Memory Management:**  
  ```python
  sqlite_conn.execute("PRAGMA journal_mode = MEMORY")
  sqlite_conn.execute("PRAGMA synchronous = OFF")
  ```
- **Batch Size Adjustment:**  
  ```python
  rows = cursor.fetchmany(500)  # Adjust based on performance
  ```

---

### 📄 **License**  
MIT License.  

---

### ❓ **FAQ**  
**Q:** Foreign keys are not migrated.  
**A:** SQLite supports foreign keys. Add `PRAGMA foreign_keys = ON`.  

**Q:** Memory issues with large tables.  
**A:** Reduce `fetchmany(100)` size and commit frequently.  

**Q:** Corrupted non-English characters.  
**A:** Ensure `charset='utf8mb4'` in the MySQL connection.  

---

**✨ Example Workflow:**  
```bash
1. Edit MYSQL_CONFIG
2. Run python mysql_to_sqlite.py
3. Verify with sqlite3 output.db
```
---

**MySQL to SQLite Converter**  
**GitHub Repository Documentation**  

---

### 📌 **Proje Açıklaması**  
Bu Python betiği, MySQL veritabanlarını SQLite'a dönüştürmek için tasarlanmıştır. Özellikle şunları destekler:  
- Tablo şemalarının otomatik dönüşümü  
- Veri tipi uyarlamaları (MySQL → SQLite)  
- Rezerve kelimelerin otomatik tırnaklanması  
- Büyük veri setleri için optimizasyon  
- Hata yönetimi ve detaylı loglama  

---

### 🚀 **Özellikler**  
- **Şema Dönüşümü:**  
  - MySQL `CREATE TABLE` komutlarını SQLite uyumlu hale getirir.  
  - Index, foreign key ve özel kısıtlamaları ayrıştırır.  
  - `AUTO_INCREMENT`, `ENGINE`, `UNSIGNED` gibi SQLite tarafından desteklenmeyen ifadeleri temizler.  

- **Veri Aktarımı:**  
  - Toplu veri ekleme (`executemany`) ile yüksek performans.  
  - UTF-8 karakter kodlaması desteği.  
  - Binary verilerin otomatik dönüşümü.  

- **Hata Yönetimi:**  
  - Tablo oluşturma ve veri aktarım hatalarını detaylı loglar.  
  - Otomatik tablo silme/yeniden oluşturma.  

---

### 📦 **Kurulum**  
1. **Gereksinimler:**  
   ```bash
   pip install pymysql
   ```

2. **Depoyu Klonla:**  
   ```bash
   git clone https://github.com/adeministratorr/MySQL-to-Sqlite-Converter.git
   cd mysql-to-sqlite-converter
   ```

---

### ⚙️ **Yapılandırma**  
Aşağıdaki kısmı düzenleyin:  
```python
MYSQL_CONFIG = {
    'host': 'localhost',
    'user': 'your_user',
    'password': 'your_password',
    'database': 'your_database',
    'port': 3306,
    'charset': 'utf8mb4'
}

SQLITE_DB = 'output.db'  # SQLite çıktı dosyası
```

---

### 🛠 **Kullanım**  
```bash
python mysql_to_sqlite.py
```

**Çıktı:**  
```
✅ Tüm tablolar başarıyla aktarıldı!
📂 SQLite dosyası: output.db
```

---

### 🔧 **Teknik Detaylar**  
#### **Veri Tipi Eşlemesi**  
| MySQL          | SQLite       |
|----------------|--------------|
| INT, TINYINT   | INTEGER      |
| VARCHAR, TEXT  | TEXT         |
| FLOAT, DOUBLE  | REAL         |
| DATETIME       | TEXT         |

#### **Rezerve Kelimeler**  
`index`, `group` gibi SQLite rezerve kelimeleri otomatik tırnaklanır:  
```sql
CREATE TABLE "group" ("index" INTEGER, ...)
```

---

### 🐛 **Hata Ayıklama**  
1. **Yaygın Hatalar:**  
   - **OperationalError: near "index": syntax error** → Sütun isimlerini tırnaklayın.  
   - **Encoding Errors** → MySQL bağlantısında `charset='utf8mb4'` kullanın.  

2. **Hata Logları:**  
   ```log
   [ERROR] Tablo oluşturma hatası (users): no such column: email
   [DEBUG] Hatalı SQL: CREATE TABLE users (id INT, email VARCHAR(255))
   ```

---

### ⚡ **Optimizasyon İpuçları**  
- **Bellek Yönetimi:**  
  ```python
  sqlite_conn.execute("PRAGMA journal_mode = MEMORY")
  sqlite_conn.execute("PRAGMA synchronous = OFF")
  ```
- **Batch Boyutu:**  
  ```python
  rows = cursor.fetchmany(500)  # Performansa göre ayarlayın
  ```

---

### 📄 **Lisans**  
MIT License. 

---

### ❓ **SSS**  
**S:** Foreign key’ler aktarılmıyor.  
**C:** SQLite foreign key’leri destekler ancak `PRAGMA foreign_keys = ON` ekleyin.  

**S:** Büyük tablolarda bellek tükeniyor.  
**C:** `fetchmany(100)` değerini düşürün ve sık sık commit yapın.  

**S:** Türkçe karakterler bozuk görünüyor.  
**C:** MySQL bağlantısında `charset='utf8mb4'` kullanın.  

---


**✨ Örnek Çalışma Akışı:**  
```bash
1. MYSQL_CONFIG değişkenini düzenle
2. python mysql_to_sqlite.py
3. sqlite3 output.db ile doğrula
```
