# -------------------------------------------------------------------------- #
# Title: Assignment07
# Desc: This assignment demonstrates using classes and objects
# Change Log: (Who, When, What)
#   BCM, 2023-11-22, Created Script added Person and Student classes
#   BCM, 2023-11-25, Added properties
#   BCM, 2023-11-26, Modifications for use of class objects
# -------------------------------------------------------------------------- #
# Setup Code
import json
from json import JSONDecodeError

# Constants
FILE_NAME: str = "Enrollments.json"
MENU: str = f"""
---- Course Registration Program ----
Select from the following menu:
1. Register a Student for a Course
2. Show current data
3. Save data to the {FILE_NAME} file
4. Exit the program
--------------------------------------
"""

# Variables
students: list = []  # Table of student data (list of dictionary rows)
menu_choice: str = ""  # Holds the user menu selection value (user input)

# -------------------------------------------------------------------------- #
# Classes
# Data Classes


class Person:
    """
    Class for people data.

    Properties:
        - student_first_name (str): The student's first name.
        - student_last_name (str): The student's last name.

    Change log:
        - BCM, 2023-11-25, Created class
        - BCM, 2023-11-26, Moved __str__ to after properties
    """
    def __init__(self, student_first_name: str = '', student_last_name: str = ''):
        self.student_first_name = student_first_name
        self.student_last_name = student_last_name

    # Getter & setter for first name
    @property  # getter
    def student_first_name(self):
        return self.__student_first_name.strip()

    @student_first_name.setter
    def student_first_name(self, value: str):
        if value.isalpha() or value == "":  # allow characters or the default empty string
            self.__student_first_name = value
        else:
            raise ValueError("The first name should only contain letters.")

    # Getter & setter for last name
    @property  # getter
    def student_last_name(self):
        return self.__student_last_name.strip()

    @student_last_name.setter
    def student_last_name(self, value: str):
        if value.isalpha() or value == "":  # allow characters or the default empty string
            self.__student_last_name = value
        else:
            raise ValueError("The last name should only contain letters.")

    def __str__(self):
        return f"{self.student_first_name},{self.student_last_name}"


class Student (Person):
    """
    Class for student data. Inherits from Person class.

    Properties:
        - course_name (str): The course the student is registered.
        - student_first_name (str): Inherited from Person class. Student's first name.
        - student_last_name (str): Inherited from Person class. Student's last name.

    Change log:
        - BCM, 2023-11-25, Created class
        - BCM, 2023-11-26, Moved __str__ to after properties
    """
    def __init__(self, student_first_name: str = '', student_last_name: str = '', course_name: str = ''):
        super().__init__(student_first_name=student_first_name, student_last_name=student_last_name)
        self.course_name = course_name

    # Getter & setter for course name
    @property  # getter for course_name
    def course_name(self):
        return self.__course_name.strip()

    @course_name.setter  # setter for course_name
    def course_name(self, value: str):
        # Check values. Default empty OK, otherwise should be alphanumeric
        # Course names usually contain a space (ex. 'Python 100'), so address by
        # removing spaces to check for just alphanumeric
        if value.replace(' ', '').isalnum() or value == "":
            self.__course_name = value
        else:
            raise ValueError("The course name should only contain letters and numbers. Ex. 'History 101'")

    def __str__(self):
        return f"{self.student_first_name},{self.student_last_name},{self.course_name}"

# ---------------------------------------------------------------------------#
# Processing Classes --------------------------------------- #


class FileProcessor:
    """
    Functions to read and write data between a file and a list.

    ChangeLog: (Who, When, What)
        - BCM, 2023-11-22, Created Class
        - BCM, 2023-11-25, Modified to use objects
        - BCM, 2023-11-26, Further modifications for use of objects
    """

    @staticmethod
    def read_data_from_file(file_name: str, student_data: list):
        """
        Reads data from json into table.

        :param file_name: name of json file with enrollments
        :param student_data: empty table of student details
        :return: student data to populate students table

        Change log:
        BCM, 2023-11-25, Modified for use of objects
        BCM, 2023-11-26, Further modifications for use of objects
        """
        file: json = None
        try:
            file = open(file_name, 'r')

            list_of_dict_data = json.load(file)
            # Convert the Json dictionary objects to student objects
            for each_student in list_of_dict_data:
                student_obj: Student = Student(student_first_name=each_student["FirstName"],
                                               student_last_name=each_student["LastName"],
                                               course_name=each_student["CourseName"])
                student_data.append(student_obj)
            file.close()
        except FileNotFoundError as e:
            IO.output_error_messages('File not found.', e)
            print('Creating file as it does not exist.')
            file = open(file_name, 'w')
            json.dump(student_data, file)

        except JSONDecodeError as e:
            IO.output_error_messages('JSON data in file is not valid.', e)
            print('Resetting it.')
            file = open(file_name, 'w')
            json.dump(student_data, file)

        except Exception as e:
            IO.output_error_messages('An error has occurred:', e)

        finally:
            if file and not file.closed:
                file.close()
        return student_data

    @classmethod
    def write_data_to_file(cls, file_name: str, student_data: list):
        """
         Writes data to json file from list.

        :param file_name: name of file
        :param student_data: table of students data
        :return: none

        Change log:
        BCM, 2023-11-25, modified for use of objects
        """
        file = None
        try:
            list_of_dict_data: list = []

            # Add Student objects to Json compatible list of dictionaries.
            for each_student in student_data:
                student_json: dict \
                    = {"FirstName": each_student.student_first_name,
                       "LastName": each_student.student_last_name,
                       "CourseName": each_student.course_name}
                list_of_dict_data.append(student_json)

            file = open(file_name, "w")
            json.dump(list_of_dict_data, file)
            file.close()

            # Present the current data
            print()
            print("_ " * 25)
            print("The file contains: \n")
            for each_student in list_of_dict_data:
                print(
                    f'{each_student["CourseName"]}, '
                    f'{each_student["LastName"]}, '
                    f'{each_student["FirstName"]}'
                )
            print("_" * 50, '\n')

        except TypeError as e:

            IO.output_error_messages(
                "Please check that the data is a valid JSON format", e)
        except Exception as e:
            IO.output_error_messages(
                "There was a non-specific error!", e)
        finally:
            if file and not file.closed:
                file.close()

# Presentation Classes --------------------------------------- #


class IO:
    """
    Functions to handle inputs and outputs.

    ChangeLog: (Who, When, What)
        - BCM, 2023-11-22, Created Class
        - BCM, 2023-11-25, Modified to use objects
        - BCM, 2023-11-26, Further modifications for use of objects
    """

    # ---- Input ------ #
    @staticmethod
    def input_menu_choice():
        """
        Collects user selection from menu options.

        Properties
            :return: user's choice

        Change Log:
            - BCM, 2023-11-22, Created Class

        """
        choice = "0"
        try:
            choice = input(f"\nWhat would you like to do? \n").strip()
            if choice not in ("1", "2", "3", "4"):  # Intentionally strings
                raise Exception("Please, choose only 1, 2, 3, or 4")
        except Exception as e:
            IO.output_error_messages(e.__str__())
        return choice

    @staticmethod
    def input_student_data(student_data: list):
        """
        Function to capture student details from user, add to table of students.
        :param student_data: existing table of student info
        :return: updated table of student info
        """
        # Input the data
        # Error handling when the user enters incorrect data
        try:
            student_object = Student()
            # Collect input from user
            student_object.student_first_name = input("Enter the student's first name: ").strip()
            student_object.student_last_name = input("Enter the student's last name: ").strip()
            student_object.course_name = input("Enter the course name: ").strip().capitalize()
            # Add to list
            student_data.append(student_object)

            print()
            print("_ " * 25, '\n')
            print(f'{student_object.student_first_name} {student_object.student_last_name} '
                  f'has been added to {student_object.course_name}.')
            print("_" * 50, '\n')

        except ValueError as e:
            print()
            IO.output_error_messages("Incorrect data type.", e)
        except Exception as e:
            print()
            IO.output_error_messages("There was a non-specific error", e)
        return student_data

    # ---- Output ------ #
    @staticmethod
    def output_menu(menu: str):
        """
        Present the menu of choices to the user.
        :return: none
        """
        print(menu)

    @staticmethod
    def output_student_courses(student_data: list):
        """
        Function to display the student info in the table.
        :param student_data: table of students
        :return: none
        """

        print("_ " * 25, '\n')
        print('Class Registration:\n')
        for each_student in student_data:
            message = "- {} {} is registered for {}"
            print(message.format(each_student.student_first_name,
                                 each_student.student_last_name,
                                 each_student.course_name))
        print("_" * 50, '\n')

    # ---- Output - Errors ------ #
    @staticmethod
    def output_error_messages(message: str, error: Exception = None):
        """
        Function to display a custom error messages to the user.
        :param message: User-friendly text to display to user.
        :param error: Technical error text from system.
        :return: None
        """
        print("_ " * 25, '\n')
        print(message)
        if error is not None:
            print("-- Technical Error Message -- ")
            print(error, error.__doc__, type(error), sep='\n')
        print("_" * 50, '\n')


# -------------------------------------------------------------------------- #
# Main body

# At start of program, load file data into a list of dictionary rows (table)
students = FileProcessor.read_data_from_file(file_name=FILE_NAME, student_data=students)

# Loop to move user through program based on user choice from menu
while True:
    IO.output_menu(MENU)
    menu_choice = IO.input_menu_choice()

    if menu_choice == '1':
        # Collect student details from user
        students = IO.input_student_data(student_data=students)
        continue

    elif menu_choice == '2':
        # Show user the current data
        IO.output_student_courses(student_data=students)
        continue

    elif menu_choice == '3':
        # Save current data to file
        FileProcessor.write_data_to_file(student_data=students, file_name=FILE_NAME)
        continue

    elif menu_choice == '4':
        print()
        print('Okay, byyeee...')
        # Exit
        break

    else:
        print("OK OK we get it... you're a rule breaker. Try again!")
        break

print("\n-- the end --")
