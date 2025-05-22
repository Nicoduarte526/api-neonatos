import mysql.connector

def get_conexion():
    conexion = mysql.connector.connect(
        host = 'localhost',
        port = 3306,
        user = 'root',
        password = 'Nico0307*',
        database = 'neonatosdb'
    )
    return conexion, conexion.cursor()