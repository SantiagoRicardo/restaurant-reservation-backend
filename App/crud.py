from database import connectMySQL

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
    cursor.execute(
        "INSERT INTO reservations (customer_name, number_of_people, reservation_datetime, status) VALUES (%s, %s, %s, %s)",
        (reservation_data['customer_name'], reservation_data['number_of_people'], reservation_data['reservation_datetime'], reservation_data['status'])
    )
    connectMySQL.commit()
    new_id = cursor.lastrowid
    cursor.close()
    return get_reservation(new_id)

def update_reservation(reservation_id: int, reservation_data):
    cursor = connectMySQL.cursor()
    cursor.execute(
        "UPDATE reservations SET customer_name=%s, number_of_people=%s, reservation_datetime=%s, status=%s WHERE id=%s",
        (reservation_data['customer_name'], reservation_data['number_of_people'], reservation_data['reservation_datetime'], reservation_data['status'], reservation_id)
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
