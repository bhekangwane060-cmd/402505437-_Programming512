import tkinter as tk
from tkinter import messagebox
import sqlite3


# ==========================================================
# 1. DATA COLLECTIONS
# ==========================================================

CAMPUSES = {
    "Musgrave": {
        "maximum": 2,
        "start": "08:00",
        "end": "17:00"
    },

    "Umhlanga": {
        "maximum": 3,
        "start": "08:00",
        "end": "18:00"
    },

    "Pretoria":{
        "maximum": 4,
        "start": "07:00",
        "end": "19:00"
    }
}

# A set containing the campus names
CAMPUS_SET = set(CAMPUSES.keys())


# ==========================================================
# 2. OBJECT ORIENTED PROGRAMMING
# ==========================================================

class User:

    def __init__(self, username, password, role, campus):
        # Hidden attributes
        self.__username = username
        self.__password = password

        # Normal attributes
        self.role = role
        self.campus = campus

    # Return username
    def get_username(self):
        return self.__username

    # Check password
    def check_password(self, password):
        return self.__password == password


# Lecturer inherits from User
class Lecturer(User):

    def book_resource(self):
        return "Lecturer can create bookings."


# Campus Administrator inherits from User
class CampusAdministrator(User):

    def manage_resources(self):
        return "Administrator can manage resources."


# System Operator inherits from User
class SystemOperator(User):

    def view_all_data(self):
        return "System Operator can view all campus data."


# ==========================================================
# 3. BOOKING POLICY AND POLYMORPHISM
# ==========================================================

class BookingPolicy:

    def __init__(self, campus):
        self.campus = campus

    def maximum_duration(self):
        return 2

    def opening_time(self):
        return "08:00"

    def closing_time(self):
        return "17:00"

    def get_policy(self):
        return (
            "Maximum: "
            + str(self.maximum_duration())
            + " hour(s), "
            + self.opening_time()
            + " to "
            + self.closing_time()
        )


# Musgarve policy
class MusgravePolicy(BookingPolicy):

    def maximum_duration(self):
        return 2

    def opening_time(self):
        return "08:00"

    def closing_time(self):
        return "17:00"


# Umhlanga policy
class UmhlangaPolicy(BookingPolicy):

    def maximum_duration(self):
        return 3

    def opening_time(self):
        return "08:00"

    def closing_time(self):
        return "18:00"


# Pretoria policy
class PretoriaPolicy(BookingPolicy):

    def maximum_duration(self):
        return 4

    def opening_time(self):
        return "07:00"

    def closing_time(self):
        return "19:00"


# ==========================================================
# 4. DATABASE CLASS
# ==========================================================

class Database:

    def __init__(self):

        # Connect to SQLite database
        self.connection = sqlite3.connect("smart_campus.db")

        # Create cursor
        self.cursor = self.connection.cursor()

        # Create database tables
        self.create_tables()

        # Add starting data
        self.add_default_data()


    # ------------------------------------------------------
    # CREATE TABLES
    # ------------------------------------------------------

    def create_tables(self):

        # Users table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE,
                password TEXT,
                role TEXT,
                campus TEXT
            )
        """)

        # Resources table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS resources (
                id INTEGER PRIMARY KEY,
                resource_id TEXT UNIQUE,
                name TEXT,
                campus TEXT
            )
        """)

        # Bookings table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS bookings (
                id INTEGER PRIMARY KEY,
                username TEXT,
                resource_id TEXT,
                campus TEXT,
                booking_date TEXT,
                start_time TEXT,
                duration INTEGER,
                status TEXT
            )
        """)

        self.connection.commit()


    # ------------------------------------------------------
    # DEFAULT DATA
    # ------------------------------------------------------

    def add_default_data(self):

        # Default users
        users = [
            ("lecturer", "1234", "Lecturer", "Musgrave"),
            ("admin", "1234", "Campus Administrator", "Musgrave"),
            ("operator", "1234", "System Operator", "All")
        ]

        for user in users:

            try:
                self.cursor.execute(
                    """
                    INSERT INTO users
                    (username, password, role, campus)
                    VALUES (?, ?, ?, ?)
                    """,
                    user
                )

            except sqlite3.IntegrityError:
                pass


        # Default resources
        resources = [

            ("DUR-LAB-01",
             "Computer Laboratory 1",
             "Durban"),

            ("DUR-PROJ-01",
             "Multimedia Projector",
             "Durban"),

            ("DUR-SEM-01",
             "Seminar Room 1",
             "Durban"),


            ("PMB-LAB-01",
             "Computer Laboratory 1",
             "Pietermaritzburg"),

            ("PMB-PROJ-01",
             "Multimedia Projector",
             "Pietermaritzburg"),

            ("PMB-SEM-01",
             "Seminar Room 1",
             "Pietermaritzburg"),


            ("JHB-LAB-01",
             "Computer Laboratory 1",
             "Johannesburg"),

            ("JHB-PROJ-01",
             "Multimedia Projector",
             "Johannesburg"),

            ("JHB-SEM-01",
             "Seminar Room 1",
             "Johannesburg")
        ]


        for resource in resources:

            try:

                self.cursor.execute(
                    """
                    INSERT INTO resources
                    (resource_id, name, campus)
                    VALUES (?, ?, ?)
                    """,
                    resource
                )

            except sqlite3.IntegrityError:
                pass

        self.connection.commit()


    # ------------------------------------------------------
    # LOGIN
    # ------------------------------------------------------

    def login(self, username, password):

        self.cursor.execute(
            """
            SELECT username, password, role, campus
            FROM users
            WHERE username = ? AND password = ?
            """,
            (username, password)
        )

        return self.cursor.fetchone()


    # ------------------------------------------------------
    # REGISTER USER
    # ------------------------------------------------------

    def register_user(self, username, password, role, campus):

        try:

            self.cursor.execute(
                """
                INSERT INTO users
                (username, password, role, campus)
                VALUES (?, ?, ?, ?)
                """,
                (username, password, role, campus)
            )

            self.connection.commit()

            return True

        except sqlite3.IntegrityError:

            return False


    # ------------------------------------------------------
    # GET RESOURCES
    # ------------------------------------------------------

    def get_resources(self, campus):

        self.cursor.execute(
            """
            SELECT resource_id, name, campus
            FROM resources
            WHERE campus = ?
            """,
            (campus,)
        )

        return self.cursor.fetchall()


    # ------------------------------------------------------
    # ADD RESOURCE
    # ------------------------------------------------------

    def add_resource(self, resource_id, name, campus):

        try:

            self.cursor.execute(
                """
                INSERT INTO resources
                (resource_id, name, campus)
                VALUES (?, ?, ?)
                """,
                (resource_id, name, campus)
            )

            self.connection.commit()

            return True

        except sqlite3.IntegrityError:

            return False


    # ------------------------------------------------------
    # UPDATE RESOURCE
    # ------------------------------------------------------

    def update_resource(self, resource_id, name):

        self.cursor.execute(
            """
            UPDATE resources
            SET name = ?
            WHERE resource_id = ?
            """,
            (name, resource_id)
        )

        self.connection.commit()


    # ------------------------------------------------------
    # DELETE RESOURCE
    # ------------------------------------------------------

    def delete_resource(self, resource_id):

        self.cursor.execute(
            """
            DELETE FROM resources
            WHERE resource_id = ?
            """,
            (resource_id,)
        )

        self.connection.commit()


    # ------------------------------------------------------
    # CHECK FOR DOUBLE BOOKING
    # ------------------------------------------------------

    def booking_exists(
        self,
        resource_id,
        campus,
        booking_date,
        start_time,
        duration
    ):

        # Convert new booking time to minutes
        new_start = self.time_to_minutes(start_time)

        new_end = new_start + duration * 60


        self.cursor.execute(
            """
            SELECT start_time, duration
            FROM bookings
            WHERE resource_id = ?
            AND campus = ?
            AND booking_date = ?
            AND status = 'Active'
            """,
            (
                resource_id,
                campus,
                booking_date
            )
        )


        bookings = self.cursor.fetchall()


        # Check each existing booking
        for booking in bookings:

            old_start = self.time_to_minutes(
                booking[0]
            )

            old_end = old_start + booking[1] * 60


            # Check if times overlap
            if new_start < old_end and new_end > old_start:

                return True


        return False


    # ------------------------------------------------------
    # ADD BOOKING
    # ------------------------------------------------------

    def add_booking(
        self,
        username,
        resource_id,
        campus,
        booking_date,
        start_time,
        duration
    ):

        self.cursor.execute(
            """
            INSERT INTO bookings
            (
                username,
                resource_id,
                campus,
                booking_date,
                start_time,
                duration,
                status
            )
            VALUES (?, ?, ?, ?, ?, ?, 'Active')
            """,
            (
                username,
                resource_id,
                campus,
                booking_date,
                start_time,
                duration
            )
        )

        self.connection.commit()


    # ------------------------------------------------------
    # USER BOOKING HISTORY
    # ------------------------------------------------------

    def get_user_bookings(self, username):

        self.cursor.execute(
            """
            SELECT
                id,
                resource_id,
                campus,
                booking_date,
                start_time,
                duration,
                status
            FROM bookings
            WHERE username = ?
            ORDER BY booking_date, start_time
            """,
            (username,)
        )

        return self.cursor.fetchall()


    # ------------------------------------------------------
    # CAMPUS BOOKINGS
    # ------------------------------------------------------

    def get_campus_bookings(self, campus):

        self.cursor.execute(
            """
            SELECT
                id,
                username,
                resource_id,
                booking_date,
                start_time,
                duration,
                status
            FROM bookings
            WHERE campus = ?
            ORDER BY booking_date, start_time
            """,
            (campus,)
        )

        return self.cursor.fetchall()


    # ------------------------------------------------------
    # ALL BOOKINGS
    # ------------------------------------------------------

    def get_all_bookings(self):

        self.cursor.execute(
            """
            SELECT
                id,
                username,
                resource_id,
                campus,
                booking_date,
                start_time,
                duration,
                status
            FROM bookings
            ORDER BY campus, booking_date, start_time
            """
        )

        return self.cursor.fetchall()


    # ------------------------------------------------------
    # CANCEL BOOKING
    # ------------------------------------------------------

    def cancel_booking(self, booking_id, username):

        self.cursor.execute(
            """
            UPDATE bookings
            SET status = 'Cancelled'
            WHERE id = ?
            AND username = ?
            AND status = 'Active'
            """,
            (
                booking_id,
                username
            )
        )

        self.connection.commit()

        return self.cursor.rowcount


    # ------------------------------------------------------
    # CAMPUS REPORT DATA
    # ------------------------------------------------------

    def get_report_data(self, campus):

        self.cursor.execute(
            """
            SELECT resource_id, duration
            FROM bookings
            WHERE campus = ?
            AND status = 'Active'
            """,
            (campus,)
        )

        return self.cursor.fetchall()


    # ------------------------------------------------------
    # ALL REPORT DATA
    # ------------------------------------------------------

    def get_all_report_data(self):

        self.cursor.execute(
            """
            SELECT campus, resource_id, duration
            FROM bookings
            WHERE status = 'Active'
            """
        )

        return self.cursor.fetchall()


    # ------------------------------------------------------
    # CONVERT TIME TO MINUTES
    # ------------------------------------------------------

    def time_to_minutes(self, value):

        parts = value.split(":")

        hour = int(parts[0])
        minute = int(parts[1])

        return hour * 60 + minute


    # ------------------------------------------------------
    # CLOSE DATABASE
    # ------------------------------------------------------

    def close(self):

        self.connection.close()


# ==========================================================
# 5. MAIN APPLICATION
# ==========================================================

class SmartCampusApp:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "Smart Campus Resource Booking System"
        )

        self.root.geometry("850x650")

        # Create database object
        self.database = Database()

        # No user logged in at the beginning
        self.current_user = None

        # Starting campus
        self.current_campus = "Durban"

        # Show login screen
        self.login_screen()


    # ======================================================
    # CLEAR WINDOW
    # ======================================================

    def clear_window(self):

        for widget in self.root.winfo_children():

            widget.destroy()


    # ======================================================
    # LOGIN SCREEN
    # ======================================================

    def login_screen(self):

        self.clear_window()


        frame = tk.Frame(self.root)

        frame.pack(pady=80)


        tk.Label(
            frame,
            text="Smart Campus Resource Booking System",
            font=("Arial", 18)
        ).grid(
            row=0,
            column=0,
            columnspan=2,
            pady=20
        )


        tk.Label(
            frame,
            text="Username"
        ).grid(
            row=1,
            column=0,
            padx=10,
            pady=10
        )


        self.username_entry = tk.Entry(frame)

        self.username_entry.grid(
            row=1,
            column=1,
            padx=10,
            pady=10
        )


        tk.Label(
            frame,
            text="Password"
        ).grid(
            row=2,
            column=0,
            padx=10,
            pady=10
        )


        self.password_entry = tk.Entry(
            frame,
            show="*"
        )

        self.password_entry.grid(
            row=2,
            column=1,
            padx=10,
            pady=10
        )


        tk.Button(
            frame,
            text="Login",
            command=self.login
        ).grid(
            row=3,
            column=0,
            columnspan=2,
            pady=10
        )


        tk.Button(
            frame,
            text="Register Lecturer",
            command=self.registration_screen
        ).grid(
            row=4,
            column=0,
            columnspan=2,
            pady=10
        )


        tk.Label(
            frame,
            text="Demo accounts:"
        ).grid(
            row=5,
            column=0,
            columnspan=2
        )


        tk.Label(
            frame,
            text="lecturer / 1234"
        ).grid(
            row=6,
            column=0,
            columnspan=2
        )


        tk.Label(
            frame,
            text="admin / 1234"
        ).grid(
            row=7,
            column=0,
            columnspan=2
        )


        tk.Label(
            frame,
            text="operator / 1234"
        ).grid(
            row=8,
            column=0,
            columnspan=2
        )


    # ======================================================
    # LOGIN FUNCTION
    # ======================================================

    def login(self):

        username = self.username_entry.get()

        password = self.password_entry.get()


        if username == "" or password == "":

            messagebox.showwarning(
                "Input",
                "Please enter username and password."
            )

            return


        result = self.database.login(
            username,
            password
        )


        if result is None:

            messagebox.showerror(
                "Login",
                "Incorrect username or password."
            )

            return


        # Create correct object according to role
        if result[2] == "Lecturer":

            self.current_user = Lecturer(
                result[0],
                result[1],
                result[2],
                result[3]
            )


        elif result[2] == "Campus Administrator":

            self.current_user = CampusAdministrator(
                result[0],
                result[1],
                result[2],
                result[3]
            )


        else:

            self.current_user = SystemOperator(
                result[0],
                result[1],
                result[2],
                result[3]
            )


        if self.current_user.campus != "All":

            self.current_campus = self.current_user.campus


        self.dashboard()


    # ======================================================
    # LECTURER REGISTRATION
    # ======================================================

    def registration_screen(self):

        self.clear_window()


        frame = tk.Frame(self.root)

        frame.pack(pady=50)


        tk.Label(
            frame,
            text="Lecturer Registration",
            font=("Arial", 18)  
        ).grid(
            row=0,
            column=0,
            columnspan=2,
            pady=20
        )


        tk.Label(
            frame,
            text="Username"
        ).grid(
            row=1,
            column=0,
            pady=8
        )


        username_entry = tk.Entry(frame)

        username_entry.grid(
            row=1,
            column=1,
            pady=8
        )


        tk.Label(
            frame,
            text="Password"
        ).grid(
            row=2,
            column=0,
            pady=8
        )


        password_entry = tk.Entry(
            frame,
            show="*"
        )

        password_entry.grid(
            row=2,
            column=1,
            pady=8
        )


        tk.Label(
            frame,
            text="Campus"
        ).grid(
            row=3,
            column=0,
            pady=8
        )


        campus_list = tk.Listbox(
            frame,
            height=3
        )

        campus_list.grid(
            row=3,
            column=1,
            pady=8
        )


        for campus in CAMPUSES:

            campus_list.insert(
                tk.END,
                campus
            )


        # Register button function
        def register():

            selected = campus_list.curselection()


            if (
                username_entry.get() == ""
                or password_entry.get() == ""
            ):

                messagebox.showwarning(
                    "Input",
                    "Please complete all fields."
                )

                return


            if len(selected) == 0:

                messagebox.showwarning(
                    "Campus",
                    "Please select a campus."
                )

                return


            campus = campus_list.get(
                selected[0]
            )


            success = self.database.register_user(
                username_entry.get(),
                password_entry.get(),
                "Lecturer",
                campus
            )


            if success:

                messagebox.showinfo(
                    "Registration",
                    "Lecturer registered successfully."
                )

                self.login_screen()


            else:

                messagebox.showerror(
                    "Registration",
                    "Username already exists."
                )


        tk.Button(
            frame,
            text="Register",
            command=register
        ).grid(
            row=4,
            column=0,
            columnspan=2,
            pady=10
        )


        tk.Button(
            frame,
            text="Back to Login",
            command=self.login_screen
        ).grid(
            row=5,
            column=0,
            columnspan=2,
            pady=10
        )


    # ======================================================
    # DASHBOARD
    # ======================================================

    def dashboard(self):

        self.clear_window()


        top = tk.Frame(self.root)

        top.pack(pady=10)


        tk.Label(
            top,
            text="Smart Campus Resource Booking System",
            font=("Arial", 18)
        ).pack()


        tk.Label(
            top,
            text=
            "Logged in as: "
            + self.current_user.get_username()
            + " | Role: "
            + self.current_user.role
        ).pack()


        # Campus selection
        campus_frame = tk.Frame(self.root)

        campus_frame.pack(pady=10)


        tk.Label(
            campus_frame,
            text="Active Campus:"
        ).grid(
            row=0,
            column=0
        )


        self.campus_list = tk.Listbox(
            campus_frame,
            height=3
        )

        self.campus_list.grid(
            row=0,
            column=1,
            padx=10
        )


        for campus in CAMPUSES:

            self.campus_list.insert(
                tk.END,
                campus
            )


        self.select_current_campus()


        tk.Button(
            campus_frame,
            text="Select Campus",
            command=self.select_campus
        ).grid(
            row=0,
            column=2,
            padx=10
        )


        # Booking policy
        self.policy_label = tk.Label(
            self.root,
            text=""
        )

        self.policy_label.pack(
            pady=5
        )

        self.show_policy()


        # Buttons
        button_frame = tk.Frame(self.root)

        button_frame.pack(
            pady=10
        )


        # Lecturer buttons
        if self.current_user.role == "Lecturer":

            tk.Button(
                button_frame,
                text="View Resources",
                command=self.resources_screen
            ).grid(
                row=0,
                column=0,
                padx=5,
                pady=5
            )


            tk.Button(
                button_frame,
                text="Book Resource",
                command=self.booking_screen
            ).grid(
                row=0,
                column=1,
                padx=5,
                pady=5
            )


            tk.Button(
                button_frame,
                text="My Bookings",
                command=self.my_bookings_screen
            ).grid(
                row=0,
                column=2,
                padx=5,
                pady=5
            )


        # Administrator buttons
        elif self.current_user.role == "Campus Administrator":

            tk.Button(
                button_frame,
                text="Manage Resources",
                command=self.resource_management_screen
            ).grid(
                row=0,
                column=0,
                padx=5,
                pady=5
            )


            tk.Button(
                button_frame,
                text="Campus Bookings",
                command=self.campus_bookings_screen
            ).grid(
                row=0,
                column=1,
                padx=5,
                pady=5
            )


            tk.Button(
                button_frame,
                text="Campus Report",
                command=self.campus_report_screen
            ).grid(
                row=0,
                column=2,
                padx=5,
                pady=5
            )


        # System Operator buttons
        else:

            tk.Button(
                button_frame,
                text="All Bookings",
                command=self.all_bookings_screen
            ).grid(
                row=0,
                column=0,
                padx=5,
                pady=5
            )


            tk.Button(
                button_frame,
                text="Campus Report",
                command=self.campus_report_screen
            ).grid(
                row=0,
                column=1,
                padx=5,
                pady=5
            )


            tk.Button(
                button_frame,
                text="Cross-Campus Report",
                command=self.cross_campus_report_screen
            ).grid(
                row=0,
                column=2,
                padx=5,
                pady=5
            )


        tk.Button(
            self.root,
            text="Logout",
            command=self.logout
        ).pack(
            pady=15
        )


    # ======================================================
    # SELECT CURRENT CAMPUS
    # ======================================================

    def select_campus(self):
        selected = self.campus_list.curselection()
        if not selected:
            messagebox.showwarning("Cumpus","Please select a camous")
            return

        #Update current campus
        self.current_campus = self.campus_list.get(selected[0])

        #Refresh the policy label
        self.show_policy()

        #Optionally reload dashboard so buttons/resources update
        self.dashboard()


    # ======================================================
    # SELECT CAMPUS
    # ======================================================

  def select_campus(self):
    selected = self.campus_list.curselection()
    if not selected:
        messagebox.showwarning("Campus", "Please select a campus.")
        return

    # Update current campus
    self.current_campus = self.campus_list.get(selected[0])

    # Refresh the policy label
    self.show_policy()

    # Optionally reload dashboard so buttons/resources update
    self.dashboard()



        # Administrator can only use assigned campus
        if self.current_user.role == "Campus Administrator":

            if self.current_user.campus != selected_campus:

                messagebox.showwarning(
                    "Campus",
                    "You can only manage your assigned campus."
                )

                self.current_campus = self.current_user.campus

                self.select_current_campus()

                return


        # Use set for campus validation
        if selected_campus in CAMPUS_SET:

            self.current_campus = selected_campus


        self.show_policy()


        messagebox.showinfo(
            "Campus",
            "Active campus is now "
            + self.current_campus
        )


    # ======================================================
    # SHOW BOOKING POLICY
    # ======================================================

    def show_policy(self):

        policy = self.get_policy(
            self.current_campus
        )


        self.policy_label.config(
            text=
            "Booking policy: "
            + policy.get_policy()
        )


    # ======================================================
    # GET POLICY
    # ======================================================

    def get_policy(self, campus):

        if campus == "Musgrave":

            return MusgravePolicy(campus)


        elif campus == "Umhlanga":

            return UmhlangaPolicy(campus)


        else:

            return PretoriaPolicy(campus)


    # ======================================================
    # LOGOUT
    # ======================================================

    def logout(self):

        self.current_user = None

        self.login_screen()


    # ======================================================
    # VIEW RESOURCES
    # ======================================================

    def resources_screen(self):

        self.clear_window()


        tk.Label(
            self.root,
            text=
            "Available Resources - "
            + self.current_campus,
            font=("Arial", 16)
        ).pack(
            pady=15
        )


        resources = self.database.get_resources(
            self.current_campus
        )


        listbox = tk.Listbox(
            self.root,
            width=60,
            height=12
        )

        listbox.pack(
            pady=10
        )


        for resource in resources:

            listbox.insert(
                tk.END,
                resource[0]
                + " - "
                + resource[1]
            )


        tk.Button(
            self.root,
            text="Back",
            command=self.dashboard
        ).pack(
            pady=10
        )


    # ======================================================
    # CREATE BOOKING SCREEN
    # ======================================================

    def booking_screen(self):

        self.clear_window()


        tk.Label(
            self.root,
            text="Create Resource Booking",
            font=("Arial", 16)
        ).pack(
            pady=10
        )


        frame = tk.Frame(self.root)

        frame.pack(
            pady=10
        )


        # Resource
        tk.Label(
            frame,
            text="Resource"
        ).grid(
            row=0,
            column=0,
            pady=8
        )


        resources = self.database.get_resources(
            self.current_campus
        )


        resource_list = tk.Listbox(
            frame,
            height=5,
            width=35
        )

        resource_list.grid(
            row=0,
            column=1,
            pady=8
        )


        for resource in resources:

            resource_list.insert(
                tk.END,
                resource[0]
                + " - "
                + resource[1]
            )


        # Date
        tk.Label(
            frame,
            text="Date (YYYY-MM-DD)"
        ).grid(
            row=1,
            column=0,
            pady=8
        )


        date_entry = tk.Entry(frame)

        date_entry.grid(
            row=1,
            column=1,
            pady=8
        )


        # Time
        tk.Label(
            frame,
            text="Start time (HH:MM)"
        ).grid(
            row=2,
            column=0,
            pady=8
        )


        time_entry = tk.Entry(frame)

        time_entry.grid(
            row=2,
            column=1,
            pady=8
        )


        # Duration
        tk.Label(
            frame,
            text="Duration (hours)"
        ).grid(
            row=3,
            column=0,
            pady=8
        )


        duration_entry = tk.Entry(frame)

        duration_entry.grid(
            row=3,
            column=1,
            pady=8
        )


        # Create booking function
        def create_booking():

            selected = resource_list.curselection()


            if len(selected) == 0:

                messagebox.showwarning(
                    "Booking",
                    "Please select a resource."
                )

                return


            booking_date = date_entry.get()

            start_time = time_entry.get()

            duration_text = duration_entry.get()


            if (
                booking_date == ""
                or start_time == ""
                or duration_text == ""
            ):

                messagebox.showwarning(
                    "Booking",
                    "Please complete all fields."
                )

                return


            # Convert duration to integer
            try:

                duration = int(
                    duration_text
                )

            except ValueError:

                messagebox.showerror(
                    "Booking",
                    "Duration must be a whole number."
                )

                return


            if duration <= 0:

                messagebox.showerror(
                    "Booking",
                    "Duration must be greater than zero."
                )

                return


            resource_text = resource_list.get(
                selected[0]
            )


            resource_id = resource_text.split(
                " - "
            )[0]


            # Check time
            if not self.valid_time(start_time):

                messagebox.showerror(
                    "Booking",
                    "Start time must use HH:MM."
                )

                return


            # Get campus policy
            policy = self.get_policy(
                self.current_campus
            )


            start_minutes = (
                self.database.time_to_minutes(
                    start_time
                )
            )


            opening = (
                self.database.time_to_minutes(
                    policy.opening_time()
                )
            )


            closing = (
                self.database.time_to_minutes(
                    policy.closing_time()
                )
            )


            ending = (
                start_minutes
                + duration * 60
            )


            # Maximum duration
            if duration > policy.maximum_duration():

                messagebox.showerror(
                    "Booking",
                    "This campus allows a maximum of "
                    + str(
                        policy.maximum_duration()
                    )
                    + " hour(s)."
                )

                return


            # Campus opening and closing times
            if (
                start_minutes < opening
                or ending > closing
            ):

                messagebox.showerror(
                    "Booking",
                    "The booking is outside the allowed campus hours."
                )

                return


            # Check double booking
            if self.database.booking_exists(
                resource_id,
                self.current_campus,
                booking_date,
                start_time,
                duration
            ):

                messagebox.showerror(
                    "Booking",
                    "The resource is already booked for an overlapping time."
                )

                return


            # Save booking
            self.database.add_booking(
                self.current_user.get_username(),
                resource_id,
                self.current_campus,
                booking_date,
                start_time,
                duration
            )


            messagebox.showinfo(
                "Booking",
                "Booking created successfully."
            )


            self.dashboard()


        tk.Button(
            frame,
            text="Create Booking",
            command=create_booking
        ).grid(
            row=4,
            column=0,
            columnspan=2,
            pady=10
        )


        tk.Button(
            frame,
            text="Back",
            command=self.dashboard
        ).grid(
            row=5,
            column=0,
            columnspan=2,
            pady=10
        )


    # ======================================================
    # VALIDATE TIME
    # ======================================================

    def valid_time(self, value):

        parts = value.split(":")


        if len(parts) != 2:

            return False


        try:

            hour = int(parts[0])

            minute = int(parts[1])

        except ValueError:

            return False


        if hour < 0 or hour > 23:

            return False


        if minute < 0 or minute > 59:

            return False


        return True


    # ======================================================
    # MY BOOKINGS
    # ======================================================

    def my_bookings_screen(self):

        self.clear_window()


        tk.Label(
            self.root,
            text="My Booking History",
            font=("Arial", 16)
        ).pack(
            pady=15
        )


        bookings = self.database.get_user_bookings(
            self.current_user.get_username()
        )


        listbox = tk.Listbox(
            self.root,
            width=100,
            height=15
        )

        listbox.pack(
            pady=10
        )


        for booking in bookings:

            text = (
                "ID: "
                + str(booking[0])
                + " | Resource: "
                + booking[1]
                + " | Campus: "
                + booking[2]
                + " | Date: "
                + booking[3]
                + " | Time: "
                + booking[4]
                + " | Duration: "
                + str(booking[5])
                + " hour(s)"
                + " | Status: "
                + booking[6]
            )


            listbox.insert(
                tk.END,
                text
            )


        # Cancel booking
        def cancel():

            selected = listbox.curselection()


            if len(selected) == 0:

                messagebox.showwarning(
                    "Cancel",
                    "Please select a booking."
                )

                return


            booking = bookings[
                selected[0]
            ]


            if booking[6] != "Active":

                messagebox.showwarning(
                    "Cancel",
                    "This booking has already been cancelled."
                )

                return


            result = self.database.cancel_booking(
                booking[0],
                self.current_user.get_username()
            )


            if result > 0:

                messagebox.showinfo(
                    "Cancel",
                    "Booking cancelled."
                )

                self.my_bookings_screen()


        tk.Button(
            self.root,
            text="Cancel Selected Booking",
            command=cancel
        ).pack(
            pady=5
        )


        tk.Button(
            self.root,
            text="Back",
            command=self.dashboard
        ).pack(
            pady=5
        )


    # ======================================================
    # ADMIN RESOURCE MANAGEMENT
    # ======================================================

    def resource_management_screen(self):

        self.clear_window()


        tk.Label(
            self.root,
            text=
            "Manage Resources - "
            + self.current_campus,
            font=("Arial", 16)
        ).pack(
            pady=10
        )


        frame = tk.Frame(self.root)

        frame.pack(
            pady=10
        )


        tk.Label(
            frame,
            text="Resource ID"
        ).grid(
            row=0,
            column=0
        )


        id_entry = tk.Entry(frame)

        id_entry.grid(
            row=0,
            column=1
        )


        tk.Label(
            frame,
            text="Resource Name"
        ).grid(
            row=1,
            column=0
        )


        name_entry = tk.Entry(frame)

        name_entry.grid(
            row=1,
            column=1
        )


        resource_list = tk.Listbox(
            self.root,
            width=60,
            height=10
        )

        resource_list.pack(
            pady=10
        )


        # Load resources
        def load_resources():

            resource_list.delete(
                0,
                tk.END
            )


            resources = self.database.get_resources(
                self.current_campus
            )


            for resource in resources:

                resource_list.insert(
                    tk.END,
                    resource[0]
                    + " - "
                    + resource[1]
                )


        # Add resource
        def add():

            resource_id = id_entry.get()

            name = name_entry.get()


            if resource_id == "" or name == "":

                messagebox.showwarning(
                    "Resource",
                    "Please enter resource ID and name."
                )

                return


            success = self.database.add_resource(
                resource_id,
                name,
                self.current_campus
            )


            if success:

                messagebox.showinfo(
                    "Resource",
                    "Resource added."
                )

                load_resources()


            else:

                messagebox.showerror(
                    "Resource",
                    "Resource ID already exists."
                )


        # Update resource
        def update():

            selected = resource_list.curselection()


            if len(selected) == 0:

                messagebox.showwarning(
                    "Resource",
                    "Select a resource to update."
                )

                return


            resource_text = resource_list.get(
                selected[0]
            )


            resource_id = resource_text.split(
                " - "
            )[0]


            name = name_entry.get()


            if name == "":

                messagebox.showwarning(
                    "Resource",
                    "Enter the new resource name."
                )

                return


            self.database.update_resource(
                resource_id,
                name
            )


            messagebox.showinfo(
                "Resource",
                "Resource updated."
            )


            load_resources()


        # Delete resource
        def delete():

            selected = resource_list.curselection()


            if len(selected) == 0:

                messagebox.showwarning(
                    "Resource",
                    "Select a resource to remove."
                )

                return


            resource_text = resource_list.get(
                selected[0]
            )


            resource_id = resource_text.split(
                " - "
            )[0]


            self.database.delete_resource(
                resource_id
            )


            messagebox.showinfo(
                "Resource",
                "Resource removed."
            )


            load_resources()


        button_frame = tk.Frame(
            self.root
        )

        button_frame.pack(
            pady=5
        )


        tk.Button(
            button_frame,
            text="Add",
            command=add
        ).grid(
            row=0,
            column=0,
            padx=5
        )


        tk.Button(
            button_frame,
            text="Update",
            command=update
        ).grid(
            row=0,
            column=1,
            padx=5
        )


        tk.Button(
            button_frame,
            text="Remove",
            command=delete
        ).grid(
            row=0,
            column=2,
            padx=5
        )


        tk.Button(
            button_frame,
            text="Back",
            command=self.dashboard
        ).grid(
            row=0,
            column=3,
            padx=5
        )


        load_resources()


    # ======================================================
    # CAMPUS BOOKINGS
    # ======================================================

    def campus_bookings_screen(self):

        self.clear_window()


        tk.Label(
            self.root,
            text=
            "Campus Bookings - "
            + self.current_campus,
            font=("Arial", 16)
        ).pack(
            pady=15
        )


        bookings = self.database.get_campus_bookings(
            self.current_campus
        )


        listbox = tk.Listbox(
            self.root,
            width=100,
            height=15
        )

        listbox.pack(
            pady=10
        )


        for booking in bookings:

            text = (
                "ID: "
                + str(booking[0])
                + " | User: "
                + booking[1]
                + " | Resource: "
                + booking[2]
                + " | Date: "
                + booking[3]
                + " | Time: "
                + booking[4]
                + " | Duration: "
                + str(booking[5])
                + " | Status: "
                + booking[6]
            )


            listbox.insert(
                tk.END,
                text
            )


        tk.Button(
            self.root,
            text="Back",
            command=self.dashboard
        ).pack(
            pady=10
        )


    # ======================================================
    # ALL BOOKINGS
    # ======================================================

    def all_bookings_screen(self):

        self.clear_window()


        tk.Label(
            self.root,
            text="All Campus Bookings",
            font=("Arial", 16)
        ).pack(
            pady=15
        )


        bookings = self.database.get_all_bookings()


        listbox = tk.Listbox(
            self.root,
            width=110,
            height=18
        )

        listbox.pack(
            pady=10
        )


        for booking in bookings:

            text = (
                "ID: "
                + str(booking[0])
                + " | User: "
                + booking[1]
                + " | Resource: "
                + booking[2]
                + " | Campus: "
                + booking[3]
                + " | Date: "
                + booking[4]
                + " | Time: "
                + booking[5]
                + " | Duration: "
                + str(booking[6])
                + " | Status: "
                + booking[7]
            )


            listbox.insert(
                tk.END,
                text
            )


        tk.Button(
            self.root,
            text="Back",
            command=self.dashboard
        ).pack(
            pady=10
        )


    # ======================================================
    # CAMPUS REPORT
    # ======================================================

    def campus_report_screen(self):

        self.clear_window()


        tk.Label(
            self.root,
            text=
            "Campus Report - "
            + self.current_campus,
            font=("Arial", 16)
        ).pack(
            pady=15
        )


        data = self.database.get_report_data(
            self.current_campus
        )


        total_bookings = len(data)

        total_duration = 0


        # Dictionary for counting resources
        resource_count = {}


        for row in data:

            total_duration += row[1]


            if row[0] in resource_count:

                resource_count[row[0]] += 1

            else:

                resource_count[row[0]] = 1


        # Calculate average
        if total_bookings > 0:

            average = (
                total_duration
                / total_bookings
            )

        else:

            average = 0


        # Find most used resource
        most_used = "No bookings"


        if len(resource_count) > 0:

            most_used_count = 0


            for resource in resource_count:

                if (
                    resource_count[resource]
                    > most_used_count
                ):

                    most_used = resource

                    most_used_count = (
                        resource_count[resource]
                    )


        text = ( 
            "Campus: "
            + self.current_campus
            + "\nTotal bookings: "
            + str(total_bookings)
            + "\nMost frequently used resource: "
            + most_used
            + "\nAverage booking duration: "
            + str(round(average, 2))
            + " hour(s)"
        )


        tk.Label(
            self.root,
            text=text,
            justify=tk.LEFT,
            font=("Arial", 13)
        ).pack(
            pady=20
        )


        tk.Button(
            self.root,
            text="Back",
            command=self.dashboard
        ).pack(
            pady=10
        )


    # ======================================================
    # CROSS-CAMPUS REPORT
    # ======================================================

    def cross_campus_report_screen(self):

        self.clear_window()


        tk.Label(
            self.root,
            text="Cross-Campus Comparison",
            font=("Arial", 16)
        ).pack(
            pady=15
        )


        data = self.database.get_all_report_data()


        # Dictionary for campus report
        campus_data = {}


        # Add each campus to dictionary
        for campus in CAMPUSES:

            campus_data[campus] = {
                "bookings": 0,
                "duration": 0
            }


        # Add booking information
        for row in data:

            campus = row[0]

            campus_data[campus]["bookings"] += 1

            campus_data[campus]["duration"] += row[2]


        listbox = tk.Listbox(
            self.root,
            width=80,
            height=10
        )

        listbox.pack(
            pady=10
        )


        for campus in CAMPUSES:

            bookings = (
                campus_data[campus]["bookings"]
            )

            duration = (
                campus_data[campus]["duration"]
            )


            if bookings > 0:

                average = (
                    duration / bookings
                )

            else:

                average = 0


            text = (
                campus
                + " | Bookings: "
                + str(bookings)
                + " | Total hours: "
                + str(duration)
                + " | Average hours: "
                + str(round(average, 2))
            )


            listbox.insert(
                tk.END,
                text
            )


        tk.Button(
            self.root,
            text="Back",
            command=self.dashboard
        ).pack(
            pady=10
        )


    # ======================================================
    # CLOSE APPLICATION
    # ======================================================

    def close(self):

        self.database.close()

        self.root.destroy()


# ==========================================================
# 6. START PROGRAM
# ==========================================================

root = tk.Tk()

app = SmartCampusApp(root)

root.protocol(
    "WM_DELETE_WINDOW",
    app.close
)

root.mainloop()