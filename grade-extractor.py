import csv
import re
from gooey import Gooey, GooeyParser
from pprint import pprint
import sys

def extract_grades(filePath, max_points_constraint, columnRegex):
    student_grades = {}
    with open(filePath) as csvfile:
        reader = csv.DictReader(csvfile)
        data  = {}
        relevant_headers = []
        for h in reader.fieldnames:
            m = re.search(columnRegex, h)
            if m is not None:
                relevant_headers.append(h)

        print(f"Extracting data from: {relevant_headers}")
        for row in reader:
            student = row["student"]
            if student not in data :
                data [student] = {}
            student_data = data [student]
            for rh in relevant_headers:
                if rh not in student_data:
                    student_data[rh] = []
                if row[rh] is not None and row[rh] != "":
                    student_data[rh].append(int(row[rh]))

        for student, assignments in data.items():
            assignmentNames = list(assignments.keys())
            print(student)
            for an in assignmentNames:
                actual_grade, original_grade = 0,0
                grades = assignments[an]
                # the last element is the grade
                # get actual_grade
                if len(grades) != 0:
                    original_grade = grades[-1]
                    actual_grade = original_grade
                    if(original_grade < max(grades)):
                        actual_grade = max_points_constraint
                # add assignment to grades if not present
                if an not in student_grades:
                    student_grades[an] = {}
                student_grades[an][student] = actual_grade
        
        pprint(student_grades)
        # len(student_grades) returns number of assignments
        # len(student_grades[assignment]])
        data_rows = [] # need in data in format [studentName, *anGrade], anGrade = gi
        students = []
        # empty list of assignments, needs to be of size students, nested will be size of assignments
        assignments = [str(key) for key in student_grades.keys()]
        grades = [[] for _ in range(len(student_grades[assignments[0]]))]
        for assignment in student_grades.keys():
            for si, student_name in enumerate(student_grades[assignment]):
                sg = student_grades[assignment][student_name]
                grades[si].append(sg)
                students.append(student_name)
        with open("extracted.csv",  mode="w") as csvfile:
            writer = csv.writer(csvfile, dialect="excel", lineterminator="\n")
            columns = ["student", *assignments]
            writer.writerow(["student", *assignments])
            for student, G in zip(students, grades):
                row = (student, *G)
                writer.writerow(row)
@Gooey
def main():
    parser = GooeyParser()
    parser.add_argument("--file", widget="FileChooser")
    parser.add_argument("--reg_ex", type=str, default="^(?!.*Date).*Check for Understanding")
    parser.add_argument("--max_points_second", type=int, widget="IntegerField")
    args = parser.parse_args()
    print(args)
    extract_grades(args.file, args.max_points_second, args.reg_ex)


main()