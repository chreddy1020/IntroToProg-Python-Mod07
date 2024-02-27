# ------------------------------------------------------------------------------------------ #
# Title: Assignment07
# Desc: This assignment demonstrates using data classes
# with structured error handling
# Change Log: (Who, When, What)
# AReddy, 02/24/2024, Started editing starter script for assignment 07
# ------------------------------------------------------------------------------------------ #
import json

# Define the Data Constants
MENU: str = '''
---- Course Registration Program ----
  Select from the following menu:  
    1. Register a Student for a Course.
    2. Show current data.  
    3. Save data to a file.
    4. Exit the program.
----------------------------------------- 
'''
FILE_NAME: str = "Enrollments.json"

# Define the Data Variables
students: list = []  # a table of student data
menu_choice: str  # Hold the choice made by the user.


class Person:
    """
    A class representing Person.

    Properties:
    - student_first_name (str): The person's first name.
    - student_last_name (str): The person's last name.

    """

    def __init__(self, student_first_name: str = "", student_last_name: str = ""):
        self.student_first_name = student_first_name
        self.student_last_name = student_last_name

    @property
    def student_first_name(self):
        return self.__student_first_name.title()

    @student_first_name.setter
    def student_first_name(self, value: str):
        if value.isalpha() or value == "":
            self.__student_first_name = value
        else:
            raise ValueError("The first name should not contain numbers.")

    @property
    def student_last_name(self):
        return self.__student_last_name.title()

    @student_last_name.setter
    def student_last_name(self, value: str):
        if value.isalpha() or value == "":
            self.__student_last_name = value
        else:
            raise ValueError("The last name should not contain numbers.")

    def __str__(self):
        return f"{self.student_first_name},{self.student_last_name}"

class Student(Person):
    """
    A class representing student data. Inherits from Person class. Adds input for course.

    Properties:
    - student_first_name (str): The student's first name.
    - student_last_name (str): The student's last name.
    - course_name (str): The student's course.
    
    """

    def __init__(self, student_first_name: str = "", student_last_name: str = "", course_name: str = ""):

        super().__init__(student_first_name=student_first_name,student_last_name=student_last_name)
        self.course_name = course_name

    @property
    def course_name(self):
        return self.__course_name.strip()

    @course_name.setter
    def course_name(self, value: str):
        if value.replace(' ', '').isalnum() or value == "":
            self.__course_name = value
        else:
            raise ValueError("The course name should only contain letters and numbers.")

    def __str__(self):
        return f"{self.student_first_name},{self.student_last_name},{self.course_name}"


# Processing --------------------------------------- #
class FileProcessor:
    """
    A collection of processing layer functions that work with Json files.

    """
    
    @staticmethod
    def read_data_from_file(file_name: str, student_data: list):
        """
        Reads data from json into table.

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
            print("-" * 50)
            print("The file contains: ")
            for each_student in list_of_dict_data:
                print(
                    f'{each_student["FirstName"]}, '
                    f'{each_student["LastName"]}, '
                    f'{each_student["CourseName"]}'
                )
            print("-" * 50,)

        except TypeError as e:

            IO.output_error_messages(
                "Please check that the data is a valid JSON format", e)
        except Exception as e:
            IO.output_error_messages(
                "There was a non-specific error!", e)
        finally:
            if file and not file.closed:
                file.close()

# Presentation --------------------------------------- #
class IO:
    """
    A collection of presentation layer functions that manage user input and output

    """

    @staticmethod
    def output_error_messages(message: str, error: Exception = None):
        """
        This function displays the a custom error messages to the user

        """
        print(message, end="\n\n")
        if error is not None:
            print("-- Technical Error Message -- ")
            print(error, error.__doc__, type(error), sep='\n')

    @staticmethod
    def output_menu(menu: str):
        """
        This function displays the menu of choices to the user

        """
        print()  # Adding extra space to make it look nicer.
        print(menu)
        print()  # Adding extra space to make it look nicer.

    @staticmethod
    def input_menu_choice():
        """
        This function gets a menu choice from the user
        
        """
        choice = "0"
        try:
            choice = input("Enter your menu choice number: ")
            if choice not in ("1","2","3","4"):  # Note these are strings
                raise Exception("Please, choose only 1, 2, 3, or 4")
        except Exception as e:
            IO.output_error_messages(e.__str__())  # Not passing e to avoid the technical message

        return choice

    @staticmethod
    def output_student_and_course_names(student_data: list):
        """
        Function to display the student info in the table.
        
        """

        print("-" * 50)
        print('Class Registration:\n')
        for each_student in student_data:
            message = "{} {} is registered for {}"
            print(message.format(each_student.student_first_name,
                                 each_student.student_last_name,
                                 each_student.course_name))
        print("-" * 50)

    @staticmethod
    def input_student_data(student_data: list):
        """
        This function gets the student's first name and last name, with a course name from the user
     
        """

        try:
            student_object = Student()
            student_object.student_first_name = input("Enter the student's first name: ")
            student_object.student_last_name = input("Enter the student's last name: ")
            student_object.course_name = input("Enter the course name: ")
            student_data.append(student_object)
            print()
            print(f"You have registered {student_object.student_first_name} {student_object.student_last_name} for {student_object.course_name}.")
        except ValueError as e:
            IO.output_error_messages(message="One of the values was the correct type of data!", error=e)
        except Exception as e:
            IO.output_error_messages(message="Error: There was a problem with your entered data.", error=e)
        return student_data
            
# Program

# When the program starts, read the file data into a list of lists (table)
# Extract the data from the file
students = FileProcessor.read_data_from_file(file_name=FILE_NAME, student_data=students)

# Present and Process the data
while (True):

    # Present the menu of choices
    IO.output_menu(menu=MENU)

    menu_choice = IO.input_menu_choice()

    # Input user data
    if menu_choice == "1":  # This will not work if it is an integer!
        students = IO.input_student_data(student_data=students)
        continue

    # Present the current data
    elif menu_choice == "2":
        IO.output_student_and_course_names(students)
        continue

    # Save the data to a file
    elif menu_choice == "3":
        FileProcessor.write_data_to_file(file_name=FILE_NAME, student_data=students)
        continue

    # Stop the loop
    elif menu_choice == "4":
        break  # out of the loop
    else:
        print("Please only choose option 1, 2, or 3")

print("Program Ended")
