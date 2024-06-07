# models.py

import mysql.connector
from database import connectMySQL  # Importamos la conexión desde database.py

# Definimos la clase Reservation con los mismos atributos
class Reservation:
    def __init__(self, customer_name, number_of_people, reservation_datetime, status="active"):
        self.customer_name = customer_name
        self.number_of_people = number_of_people
        self.reservation_datetime = reservation_datetime
        self.status = status

# Función para agregar una nueva reserva
def create_reservation(reservation):
    cursor = connectMySQL.cursor()
    add_reservation = ("INSERT INTO reservations "
                       "(customer_name, number_of_people, reservation_datetime, status) "
                       "VALUES (%s, %s, %s, %s)")
    data_reservation = (reservation.customer_name, reservation.number_of_people, reservation.reservation_datetime, reservation.status)
    cursor.execute(add_reservation, data_reservation)
    connectMySQL.commit()
    cursor.close()

# Ejemplo de uso
new_reservation = Reservation('Juan Perez', 4, '2024-06-07 20:00:00')
create_reservation(new_reservation)
