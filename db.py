import psycopg2
from psycopg2 import pool

#crear un pool de conexiones
connection_pool = pool.SimpleConnectionPool(
    1, 20,
    database ="tiendasags",
    user = "postgres",
    password = "A77969805",
    host = "localhost",
    port="5432"
)

def conectar():
    return connection_pool.getconn()

def desconectar(conn):
    connection_pool.putconn(conn)