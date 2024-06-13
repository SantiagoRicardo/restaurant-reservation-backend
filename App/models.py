from database import connectMySQL

class Reservation:
    def __init__(self, customer_name, number_of_people, reservation_datetime, age, status="active", total_cost=5.0):
        self.customer_name = customer_name
        self.number_of_people = number_of_people
        self.reservation_datetime = reservation_datetime
        self.age = age
        self.status = status
        self.total_cost = total_cost  # El costo se inicializa con el valor base

    # Método para calcular el costo basado en la edad
    def calculate_cost(self):
        if self.age < 5:
            self.total_cost = 0.0
        elif 50 <= self.age <= 60:
            self.total_cost *= 0.9
        elif self.age > 60:
            self.total_cost *= 0.8

    # Método para generar un identificador único de reserva
    def generate_reservation_id(self):
        import uuid
        return f"Reserva#{uuid.uuid4().hex[:8]}"  # Genera un ID corto y único

# Ejemplo de uso:
# reserva = Reservation('Juan Perez', 4, '2024-06-15 19:00:00', 55)
# reserva.calculate_cost()
# print(reserva.total_cost)  # Debería mostrar 4.5 después de aplicar el descuento
