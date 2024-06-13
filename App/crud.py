import uuid
from database import connectMySQL

def calculate_total_cost(age):
    base_cost = 5.0
    if age < 5:
        return 0.0
    elif 50 <= age <= 60:
        dto = (base_cost*10)/100
        resDto = base_cost-dto
        return resDto
    elif age > 60:
        dto = (base_cost*20)/100
        resDto = base_cost-dto
        return resDto
    else:
        return base_cost

def get_reservation(reservation_id: int):
    cursor = connectMySQL.cursor(dictionary=True)
    cursor.execute("SELECT * FROM reservations WHERE id = %s", (reservation_id,))
    reservation = cursor.fetchone()
    cursor.close()
    return reservation

def get_reservations(skip: int = 0, limit: int = 10):
    cursor = connectMySQL.cursor(dictionary=True)
    cursor.execute("SELECT * FROM reservations LIMIT %s OFFSET %s", (limit, skip))
    reservations = cursor.fetchall()
    cursor.close()
    return reservations

def create_reservation(reservation_data):
    cursor = connectMySQL.cursor()
    total_cost = calculate_total_cost(reservation_data['age'])
    cursor.execute(
        "INSERT INTO reservations (customer_name, number_of_people, reservation_datetime, status, age, total_cost) VALUES (%s, %s, %s, %s, %s, %s)",
        (reservation_data['customer_name'], reservation_data['number_of_people'], reservation_data['reservation_datetime'], reservation_data['status'], reservation_data['age'], total_cost)
    )
    connectMySQL.commit()
    new_id = cursor.lastrowid
    id_reservation = f"Reserva#{new_id}"
    cursor.execute(
        "UPDATE reservations SET id_reservation = %s WHERE id = %s",
        (id_reservation, new_id)
    )
    connectMySQL.commit()
    cursor.close()
    return get_reservation(new_id)

def update_reservation(reservation_id: int, reservation_data):
    cursor = connectMySQL.cursor()
    total_cost = calculate_total_cost(reservation_data['age'])
    cursor.execute(
        "UPDATE reservations SET customer_name=%s, number_of_people=%s, reservation_datetime=%s, status=%s, age=%s, total_cost=%s WHERE id=%s",
        (reservation_data['customer_name'], reservation_data['number_of_people'], reservation_data['reservation_datetime'], reservation_data['status'], reservation_data['age'], total_cost, reservation_id)
    )
    connectMySQL.commit()
    cursor.close()
    return get_reservation(reservation_id)

def delete_reservation(reservation_id: int):
    cursor = connectMySQL.cursor()
    cursor.execute("DELETE FROM reservations WHERE id = %s", (reservation_id,))
    connectMySQL.commit()
    rows_affected = cursor.rowcount
    cursor.close()
    return rows_affected > 0
