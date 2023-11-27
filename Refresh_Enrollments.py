# ------------------------------------------------------------ #
# Title: Refresh_Enrollments.py
# Desc: To reset the Enrollments.py or test_enrollments.py file
# Change Log: (Who, When, What)
#   BCM, 2023-11-26, Created Script

# ------------------------------------------------------------ #
import json

STARTERTEXT: list = [{"FirstName": "Jane", "LastName": "Jam", "CourseName": "Python 100"},
                     {"FirstName": "Petra", "LastName": "Pepper", "CourseName": "Python 100"}]

# Ask user which file to update (test or main)
QUESTION: str = f"""
Which file do you need to update?
Enrollments.json (e) or
test_enrollments.json (t)
"""

file_name: str = ""
# ------------------------------------------------------------ #

choice = input(QUESTION)

# if main, update Enrollments.json
if choice == "e":
    file_name = "Enrollments.json"

# if test, update test_enrollments.json
elif choice == "t":
    file_name = "test_enrollments.json"

file = open(file_name, "w")
json.dump(STARTERTEXT, file)
file.close()

print(f"The {file_name} has been updated.")
