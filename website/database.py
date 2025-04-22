import mariadb

conn = mariadb.connect(
    user = 'root',
    password = 'admin1234',
    host = '127.0.0.1',
    port = 3307,
    database = 'Shopix'
)

cur = conn.cursor()

print(cur)
print(conn)

conn.close()
