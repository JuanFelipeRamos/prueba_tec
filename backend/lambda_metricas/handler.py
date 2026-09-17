import os
from dotenv import load_dotenv
import json
import MySQLdb

load_dotenv()

DB_HOST = os.environ.get('DB_HOST')
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_NAME = os.environ.get('DB_NAME')

def lambda_handler(event, context):
    try:
        conexion = MySQLdb.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
        )
        with conexion.cursor() as cursor:
            cursor.execute("SELECT estado, COUNT(*) FROM notas_notas GROUP BY estado")
            filas = cursor.fetchall()

        conteo = {"pendiente": 0, "en curso": 0, "hecho": 0}
        for estado, cantidad in filas:
            conteo[estado] = cantidad

        datos = {
            "total": sum(conteo.values()),
            "pendientes": conteo["pendiente"],
            "en_curso": conteo["en curso"],
            "hechas": conteo["hecho"],
        }

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(datos),
        }

    except Exception as error:
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({"error": str(error)}),
        }
    finally:
        if 'conexion' in locals():
            conexion.close()
