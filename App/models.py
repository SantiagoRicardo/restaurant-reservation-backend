from database import connectMySQL

# Definimos la clase Reservation con los mismos atributos
class Reservation:
    def __init__(self, customer_name, number_of_people, reservation_datetime, status="active"):
        self.customer_name = customer_name
        self.number_of_people = number_of_people
        self.reservation_datetime = reservation_datetime
        self.status = status
