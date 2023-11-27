
# ------------------------------------------------------------------ #
# Title: UnitTest_A07
# Desc: To perform testing for Assignment07.py

# Change Log: (Who, When, What)
#   BCM, 2023-11-25, Created script. Drafted by AI.
#   BCM, 2023-11-25, Refreshed test draft by AI for updated A07 program
#                    Currently have not been able to get it to work.
# ------------------------------------------------------------------ #


import unittest
from unittest.mock import patch
import io
import sys
from Assignment07 import Person, Student, FileProcessor, IO

class UnitTest_A07(unittest.TestCase):

    def test_person_class(self):
        person = Person("John", "Doe")
        self.assertEqual(person.student_first_name, "John")
        self.assertEqual(person.student_last_name, "Doe")
        self.assertEqual(str(person), "John,Doe")

    def test_student_class(self):
        student = Student("Jane", "Smith", "Math 101")
        self.assertEqual(student.student_first_name, "Jane")
        self.assertEqual(student.student_last_name, "Smith")
        self.assertEqual(student.course_name, "Math 101")
        self.assertEqual(str(student), "Jane,Smith,Math 101")

    def test_file_processor_read_data_from_file(self):
        student_data = []
        with patch('builtins.open', return_value=io.StringIO('[]')):
            FileProcessor.read_data_from_file("test_enrollments.json", student_data)
        self.assertEqual(student_data, [])

    def test_file_processor_write_data_to_file(self):
        student_data = [Student("Alice", "Johnson", "History 101")]
        with patch('builtins.open', create=True) as mock_open:
            with patch('json.dump') as mock_dump:
                # Create a specific MagicMock instance for the file context manager
                mock_file_instance = mock_open.return_value.__enter__.return_value

                FileProcessor.write_data_to_file("test_enrollments.json", student_data)

                # Check if open was called with the correct parameters
                mock_open.assert_called_once_with("test_enrollments.json", "w")

                # Check if json.dump was called with the correct parameters
                mock_dump.assert_called_once_with(
                    [
                        {
                            "FirstName": "Alice",
                            "LastName": "Johnson",
                            "CourseName": "History 101"
                        }
                    ],
                    mock_file_instance.write
                )

                # Ensure that the mock returned by __enter__ is used consistently
                mock_open_instance = mock_open().__enter__()
                mock_dump_instance = mock_dump.call_args[0][0]

                self.assertIs(mock_open_instance, mock_file_instance, "The __enter__ mock objects should be the same.")
                self.assertIs(mock_open_instance, mock_dump_instance, "The __enter__ mock objects should be the same.")

    @patch('builtins.input', side_effect=["1", "Alice", "Johnson", "History 101", "2", "3", "4"])
    @patch('sys.stdout', new_callable=io.StringIO)
    def test_io_input_output_flow(self, mock_stdout, mock_input):
        students = []
        IO.input_menu_choice()
        IO.input_student_data(students)
        IO.output_student_courses(students)
        IO.output_error_messages("Test error message", ValueError("Test error"))
        self.assertIn("History 101", mock_stdout.getvalue())
        self.assertIn("Alice,Johnson", mock_stdout.getvalue())
        self.assertIn("Test error message", mock_stdout.getvalue())

if __name__ == '__main__':
    unittest.main()

# -----------------#
#
#
# import unittest
# from io import StringIO
# from unittest.mock import patch
#
# # Import the classes and functions to be tested
# from Assignment07 import Student, FileProcessor, IO
#
#
# class UnitTest_A07(unittest.TestCase):
#
#     # # Test Person class
#     # def test_person_class(self):
#     #     person = Person("John", "Doe")
#     #     self.assertEqual(person.student_first_name, "John")
#     #     self.assertEqual(person.student_last_name, "Doe")
#     #
#     # # Test Student class
#     # def test_student_class(self):
#     #     student = Student("Jane", "Smith", "Math")
#     #     self.assertEqual(student.student_first_name, "Jane")
#     #     self.assertEqual(student.student_last_name, "Smith")
#     #     self.assertEqual(student.course_name, "Math")
#
#     # Test FileProcessor class
#     def test_read_data_from_file(self):
#         student_data = []
#         file_name = "test_enrollments.json"
#         file_data = '[{"FirstName": "John", "LastName": "Doe", "CourseName": "Math"}]'
#         with patch("builtins.open", return_value=StringIO(file_data)):
#             FileProcessor.read_data_from_file(file_name, student_data)
#         self.assertEqual(len(student_data), 1)
#         self.assertEqual(student_data[0].student_first_name, "John")
#         self.assertEqual(student_data[0].student_last_name, "Doe")
#         self.assertEqual(student_data[0].course_name, "Math")
#
#     @staticmethod
#     def test_write_data_to_file():
#         student_data = [Student("Jane", "Smith", "Science")]
#         file_name = "test_enrollments.json"
#         with patch("builtins.open", create=True) as mock_file:
#             FileProcessor.write_data_to_file(file_name, student_data)
#             mock_file.assert_called_with(file_name, "w")
#             mock_file().write.assert_called_with(
#                 '[{"FirstName": "Jane", "LastName": "Smith", "CourseName": "Science"}]'
#             )
#
#     # Test IO class
#     @patch('builtins.input', side_effect=['John', 'Doe', 'Math'])
#     def test_input_student_data(self, mock_input):
#         student_data = []
#         expected_data = [Student("John", "Doe", "Math")]
#         IO.input_student_data(student_data)
#         self.assertEqual(student_data, expected_data)
#
#     @patch('sys.stdout', new_callable=StringIO)
#     def test_output_student_courses(self, mock_stdout):
#         student_data = [Student("John", "Doe", "Math"), Student("Jane", "Smith", "Science")]
#         expected_output = \
#             ("Class Registration:\\n\\n"
#              "- John Doe is registered for Math\\n"
#              "- Jane Smith is registered for Science\\n")
#         IO.output_student_courses(student_data)
#         self.assertEqual(mock_stdout.getvalue(), expected_output)
#
#
# if __name__ == '__main__':
#     unittest.main()
