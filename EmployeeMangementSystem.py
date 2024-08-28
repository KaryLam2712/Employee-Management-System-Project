import sqlite3

def create_table():
    conn = sqlite3.connect('employee_management.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS employee (
        employee_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        role_varchar TEXT NOT NULL,
        department_ID INTEGER,
        employee_email TEXT,
        enrolment_date DATE,
        salary INTEGER
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS departments (
        department_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        department_name TEXT NOT NULL,
        total_number INTEGER NOT NULL,
        training_sessions INTEGER
    )
    ''')

    conn.commit()
    conn.close()

create_table()


def add_user(name, age, role_varchar, department_ID, employee_email, enrolment_date, salary):
    conn = sqlite3.connect('employee_management.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO employee (name, age, role_varchar, department_ID, employee_email, enrolment_date, salary)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (name, age, role_varchar, department_ID, employee_email, enrolment_date, salary))
    conn.commit()
    conn.close()
    print(f"User {name} added successfully.")


# Example usage
# add_user("John Lam", 35, "Manager", 1, "john.doe@example.com", "2023-08-23", 50000)
# add_user("Dan Chan", 33, "Junior", 4, "dan.doe@example.com", "2022-08-23", 10000)
# add_user("Coco Ji", 25, "Senior", 2, "coco.doe@example.com", "2021-08-30", 30000)
# add_user("Lily Chu", 28, "Assitant Manager", 3, "lily.doe@example.com", "2022-04-28", 40000)
# add_user("Jason Tsang", 39, "Lead", 2, "jason.doe@example.com", "2024-04-12", 70000)
# add_user("Mario Yip", 41, "Manager", 1, "mario.doe@example.com", "2021-02-03", 60000)
# add_user("Paul Chan", 30, "Senior", 3, "paul.doe@example.com", "2022-01-09", 30000)
# add_user("Peter Au", 40, "Senior Manager", 1, "peter.doe@example.com", "2022-09-23", 80000)

def add_department(department_name, total_number, training_sessions):
    conn = sqlite3.connect('employee_management.db')
    cursor = conn.cursor()
    cursor.execute('''
    INSERT INTO departments (department_name, total_number, training_sessions)
    VALUES (?, ?, ?)
    ''', (department_name, total_number, training_sessions))
    conn.commit()
    conn.close()
    print(f"Department {department_name} added successfully.")

# add_department("Engineering", 10, 10)
# add_department("Operation", 50, 10)
# add_department("HR", 5, 10)
# add_department("Sales", 10, 10)


def view_users():
    conn = sqlite3.connect('employee_management.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM employee')  # Changed 'users' to 'employee'
    
    users = cursor.fetchall()
    
    if len(users) == 0:
        print("No users found.")
    else:
        for user in users:
            print(user)
    
    conn.close()


def view_departments():
    conn = sqlite3.connect('employee_management.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM departments')
    rows = cursor.fetchall()
    conn.close()

    if rows:
        for row in rows:
            print(f"Department ID: {row[0]}, Department Name: {row[1]}, Total Number: {row[2]}, Training Sessions: {row[3]}")
    else:
        print("No departments found.")

def delete_user(employee_id):
    conn = sqlite3.connect('employee_management.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM employee WHERE employee_ID = ?', (employee_id,))
    conn.commit()
    conn.close()
    print(f"User with ID {employee_id} deleted successfully.")

def update_user(employee_id, name, age, role_varchar, department_ID, employee_email, enrolment_date, salary):
    conn = sqlite3.connect('employee_management.db')
    cursor = conn.cursor()
    cursor.execute('''
    UPDATE employee
    SET name = ?, age = ?, role_varchar = ?, department_ID = ?, employee_email = ?, enrolment_date = ?, salary = ?
    WHERE employee_ID = ?
    ''', (name, age, role_varchar, department_ID, employee_email, enrolment_date, salary, employee_id))
    conn.commit()
    conn.close()
    print(f"User with ID {employee_id} updated successfully.")



def search_department_by_employee_name(name):
    conn = sqlite3.connect('employee_management.db')
    cursor = conn.cursor()

    query = '''
    SELECT e.name, d.department_name
    FROM employee e
    JOIN departments d ON e.department_ID = d.department_ID
    WHERE e.name LIKE ?
    '''
    cursor.execute(query, ('%' + name + '%',))
    results = cursor.fetchall()

    conn.close()
    return results



def update_employee_role_by_id(employee_id, new_role):
    try:
        conn = sqlite3.connect('employee_management.db')
        cursor = conn.cursor()

        cursor.execute('''
        UPDATE employee
        SET role_varchar = ?
        WHERE employee_ID = ?
        ''', (new_role, employee_id))
        
        conn.commit()
        conn.close()
        
        print(f"Employee with ID {employee_id} updated successfully.")

    except sqlite3.Error as error:
        print("Error updating employee role:", error)



def main():
    create_table()

    while True:
        print("\n1. Add User")
        print("2. View Users")
        print("3. Add Department")
        print("4. View Department")
        print("5. Delete User")
        print("6. Search Employee")
        print("7. Update Role")
        print("8. Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            name = input("Enter name: ")
            age = int(input("Enter age: "))
            role = input("Enter role: ")
            department_id = int(input("Enter department ID: "))
            email = input("Enter email: ")
            enrolment_date = input("Enter enrolment date (YYYY-MM-DD): ")
            salary = int(input("Enter salary: "))
            add_user(name, age, role, department_id, email, enrolment_date, salary)

        elif choice == '2':
            view_users()

        elif choice == '3':
            department_name = input("Enter department name: ")
            total_number = int(input("Enter total number: "))
            training_sessions = int(input("Enter training sessions: "))
            add_department(department_name, total_number, training_sessions)
        
        elif choice == '4':
            view_departments()
        
        elif choice == '5':
            user_id = input("Enter the ID of the user to delete: ")
            delete_user(user_id)

        elif choice == '6':
            search_name = input("Enter employee name to search for: ")
            search_results = search_department_by_employee_name(search_name)
            if search_results:
                for result in search_results:
                    print(f"Employee: {result[0]}, Department: {result[1]}")
            else:
                print("No matching employee found.")


        elif choice == '7':
            employee_id = input("Enter the ID of the employee to update role: ")
            new_role = input("Enter the new role: ")
            update_employee_role_by_id(employee_id, new_role)

        elif choice == '8':
            print("Exiting...")
            break

        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()