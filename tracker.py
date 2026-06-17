import json
import os

class Course():
    def __init__(
        self,
        name: str,
        students: list[str] | None = None,
        topics: list[dict] | None = None,
        grades: dict[str, dict[str, int]] | None = None,
        attendance: dict[str, dict[str, bool]] | None = None
    ):
        """
        Initializes a new instance of the class.

        Args:
            name (str): The name of the class or course.
            students (list[str] | None, optional): A list of student names. Defaults to None, which initializes an empty list.
            topics (list[dict] | None, optional): A list of topic dictionaries. Defaults to None, which initializes an empty list.
            grades (dict[str, dict[str, int]] | None, optional): A nested dictionary mapping student names to their grades (topic to score). Defaults to None, which initializes an empty dict.
            attendance (dict[str, dict[str, bool]] | None, optional): A nested dictionary mapping student names to their attendance (topic to presence). Defaults to None, which initializes an empty dict.
        """
        self.name = name
        self.students = students if students is not None else []
        self.topics = topics if topics is not None else []
        self.grades = grades if grades is not None else {}
        self.attendance = attendance if attendance is not None else {}
    
    def add_student(self, student: str):
        """Adds a student to the class if they are not already present.
        
        If the student is already in the class list, a message is printed 
        indicating that the student is already enrolled.
        
        Args:
            student (str): The name of the student to be added.
        """
        if student not in self.students:
            self.students.append(student)
        else:
            print(f"{student} is already in {self.name}")

    def remove_student(self, student: str):
        """Removes a student from the class roster.

        If the student is found in the roster, they are removed.
        If the student is not found, a message is printed to the console.

        Args:
            student (str): The name of the student to be removed.
        """
        if student in self.students:
            self.students.remove(student)
        else:
            print(f'{student} is not in {self.name}')

    def get_all_students(self):
        """Retrieve all students, sort them alphabetically, and print them as a numbered list.
        
        This method fetches the internal list of students, sorts them in 
        ascending alphabetical order, and prints each student's name to the 
        console prefixed by their 1-based index.
        """
        sorted_students = sorted(self.students)
        for index, name in enumerate(sorted_students):
            print(f'{index + 1}. {name}')

    def add_topic(self, name: str, type: str, max_score: int):
        """
        Adds a new topic to the list of topics with the specified name, type, and maximum score.
        
        The topic type is case-insensitive and must be either 'lecture' or 'practice'. 
        If an invalid type is provided, the topic's type is set to None and an error message is printed.
        
        Args:
            name (str): The name of the topic.
            type (str): The type of the topic ('lecture' or 'practice').
            max_score (int): The maximum score achievable for the topic.
        """
        type = type.lower()
        if type not in ('lecture', 'practice'):
            raise ValueError(f"Invalid type: '{type}'. Must be 'lecture' or 'practice'.")
            
        topic_dict = {
            'topic_name': name,
            'topic_type': type,
            'topic_max_score': max_score
        }
        self.topics.append(topic_dict)
        print(f"Topic '{name}' added.")

    def get_all_topics(self) -> list[dict]:
        """
        Retrieve all topics.

        Returns:
            list[dict]: A list of dictionaries, where each dictionary represents a topic.
        """
        return self.topics
    
    def set_grade(self, student_name: str, topic_name: str, score: int) -> None:
        """
        Sets the grade for a specific student on a specific topic.

        Args:
            student_name (str): The name of the student.
            topic_name (str): The name of the topic.
            score (int): The score achieved by the student.

        Returns:
            None

        Raises:
            ValueError: If the student is not found in the course.
            ValueError: If the topic is not found in the course.
            ValueError: If the score is negative or exceeds the topic's maximum score.
        """
        if student_name not in self.students:
            raise ValueError(f"Student '{student_name}' not found")
        
        max_score = None
        for topic in self.topics:
            if topic['topic_name'] == topic_name:
                max_score = topic['topic_max_score']
                break
        if max_score is None:
            raise ValueError(f"Topic '{topic_name}' not found")
                
        if score > max_score or score < 0:
            raise ValueError(f'Score {score} is inappropriate!') 
        
        if student_name not in self.grades:
            self.grades[student_name] = {}
        self.grades[student_name][topic_name] = score
        print(f"Attributes {student_name}, {topic_name} and {score} have successfully added to course!")
    
    def get_grade(self, student_name: str, topic_name: str) -> int | None:
        """Retrieves the grade for a specific student and topic.

        Args:
            student_name (str): The name of the student.
            topic_name (str): The name of the topic.

        Returns:
            int | None: The grade of the student for the specified topic as an integer, 
            or None if the student does not exist or has no grade for the topic.
        """
        if student_name not in self.grades:
            return None
        return self.grades[student_name].get(topic_name)
    
    def get_all_grades(self, student_name: str) -> dict[str, int]:
        """
        Retrieve all grades for a specified student.

        Args:
            student_name (str): The name of the student whose grades are to be retrieved.

        Returns:
            dict[str, int]: A dictionary containing the subjects as keys and the corresponding 
                            grades as values for the given student. Returns an empty dictionary 
                            if the student is not found in the records.
        """
        if student_name not in self.grades:
                return {}
        return self.grades[student_name]
    
    def mark_attendance(self, student_name: str, topic_name: str, present: bool):
        """
        Marks the attendance for a specific student on a specific topic.

        Args:
            student_name (str): The name of the student to mark attendance for.
            topic_name (str): The name of the topic for which attendance is being recorded.
            present (bool): The attendance status, True if the student is present, False otherwise.

        Raises:
            ValueError: If the provided student_name does not exist in the students list.
            ValueError: If the provided topic_name does not exist in the topics list.

        Returns:
            None
        """
        if student_name not in self.students:
                raise ValueError(f"Student '{student_name}' not found")
        
        found = False
        for topic in self.topics:
                if topic['topic_name'] == topic_name:
                    found = True
                    break
        if not found:
                raise ValueError(f"Topic '{topic_name}' not found")
        
        if student_name not in self.attendance:
                self.attendance[student_name] = {}
        self.attendance[student_name][topic_name] = present
        print(f"Attendance have successfully added!")
    
    def get_attendance(self, student_name: str) -> dict[str, bool]:
        """
        Retrieve the attendance record for a specific student.

        Args:
            student_name (str): The name of the student whose attendance is to be retrieved.

        Returns:
            dict[str, bool]: A dictionary representing the student's attendance record, 
                             where keys are dates/identifiers and values are booleans 
                             indicating presence. Returns an empty dictionary if the 
                             student is not found in the attendance records.
        """
        if student_name not in self.attendance:
                return {}
        return self.attendance.get(student_name)
    
    def get_attendance_by_topic(self, topic_name: str) -> dict[str, bool]:
        """
        Retrieves the attendance status of all students for a specific topic.

        Args:
            topic_name (str): The name of the topic to check attendance for.

        Returns:
            dict[str, bool]: A dictionary where keys are student identifiers and values 
                             are booleans indicating their attendance (True if attended, 
                             False otherwise). Returns an empty dictionary if the topic 
                             is not found.
        """
        attend_dict = {}
        
        found = False
        for topic in self.topics:
            if topic['topic_name'] == topic_name:
                found = True
                break
        
        if not found:
            return attend_dict
        
        for student in self.students:
            student_attend_dict = self.get_attendance(student)
            is_attend = student_attend_dict.get(topic_name, False)
            attend_dict[student] = is_attend
        
        return attend_dict

    def get_student_average(self, student_name: str) -> float:
        """
        Calculate the average score of a specific student across all practice topics.

        Args:
            student_name (str): The name of the student whose average score is to be calculated.

        Returns:
            float: The average score of the student rounded to 1 decimal place. 
                   Returns 0.0 if the student has no valid grades in practice topics.

        Raises:
            ValueError: If the provided student_name is not found in the students list.
        """
        if student_name not in self.students:
            raise ValueError(f"Student '{student_name}' not found")
        
        total = 0
        count = 0
        for topic in self.topics:
            if topic['topic_type'] == 'practice' and topic['topic_max_score'] > 0:
                topic_name = topic['topic_name']
                grade = self.get_grade(student_name, topic_name)
                if grade is not None:
                    total += grade
                    count += 1
    
        if count == 0:
            return 0.0
        
        return round(total / count, 1)
    
    def get_group_average(self) -> float:
        """
        Calculate the average grade of the student group.

        This method computes the average of all student averages in the group,
        excluding any students with an average of 0 or less. The final result
        is rounded to one decimal place.

        Returns:
            float: The rounded average grade of the group. 
        """
        grade_list = [self.get_student_average(student) for student in self.students if self.get_student_average(student) > 0]
        return round(sum(grade_list) / len(grade_list), 1)
    
    def get_debtors(self, topic_name: str, pass_score: int) -> list[str]:
        """
        Retrieves a list of students who are considered 'debtors' for a given topic.
        
        A student is considered a debtor if their grade for the specified topic is 
        either None (meaning no grade found) or strictly less than the pass_score.
        
        Args:
            topic_name (str): The name of the topic to check grades for.
            pass_score (int): The minimum score required to pass. Students scoring 
                              below this threshold will be included in the result.
        
        Returns:
            list[str]: A list of student identifiers who did not meet the pass_score 
                       criteria for the specified topic.
        
        Raises:
            ValueError: If the provided topic_name does not exist in self.topics.
        """
        found = False
        for topic in self.topics:
            if topic['topic_name'] == topic_name:
                found = True
                break
        if not found:
            raise ValueError(f"Topic {topic_name} not found")

        grade_list = []
        for student in self.students:
            grade = self.get_grade(student, topic_name)
            if grade is None or grade < pass_score:
                grade_list.append(student)

        return grade_list
    
    def get_attendance_rate(self, student_name: str) -> float:
        """
        Calculate the attendance rate of a specific student in the course.

        Args:
            student_name (str): The name of the student whose attendance rate is to be calculated.

        Returns:
            float: The attendance rate as a percentage, rounded to one decimal place.
                   Returns 0.0 if there are no topics in the course.

        Raises:
            ValueError: If the provided student_name does not exist in the course's student list.
        """
        if student_name not in self.students:
            raise ValueError(f"There is no student '{student_name}' in the course!")
        
        topic_total = len(self.topics)
        if topic_total == 0:
            return 0.0
        
        student_attendance = self.attendance.get(student_name, {})
        stud_total = sum(student_attendance.values())
        
        return round(stud_total / topic_total * 100, 1)
        
    def save_to_file(self, filename: str):
        """
        Saves the current object's data to a JSON file.

        The data includes the object's name, students, topics, grades, and 
        attendance. If the file already exists, it will be overwritten. If the 
        file does not exist, a new file will be created. Handles permission 
        and I/O errors gracefully by printing an error message.

        Args:
            filename (str): The path to the file where the data will be saved.

        Raises:
            PermissionError: If the program lacks write permissions for the 
                target file (handled internally).
            IOError: If an input/output error occurs during file writing 
                (handled internally).
        """
        data = {}
        data['name'] = self.name
        data['students'] = self.students
        data['topics'] = self.topics
        data['grades'] = self.grades
        data['attendance'] = self.attendance
        try:
            if os.path.exists(filename):
                with open(filename, 'w', encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)
            else: 
                with open(filename, 'x', encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)
        except PermissionError:
            print(f"Error: permission denied to write to {filename}.")
        except IOError as e:
            print(f"Input/Output error: {e}")


    def load_from_file(self, filename):
        """
        Load student data from a JSON file and update the instance attributes.
        
        This method attempts to read and parse a JSON file. If successful, it 
        populates the instance attributes (name, students, topics, grades, attendance) 
        with the data retrieved from the file. It handles potential file not found, 
        permission, and JSON decoding errors gracefully by printing an error message.
        
        Args:
            filename (str): The path to the JSON file to be loaded.
        
        Returns:
            None
        
        Raises:
            FileNotFoundError: If the specified file does not exist.
            PermissionError: If the program lacks permission to read the file.
            json.JSONDecodeError: If the file contains invalid JSON format.
            Exception: For any other unexpected errors during file reading or parsing.
        """
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                student_dict = json.load(f) 
                self.name = student_dict.get('name', None)
                self.students = student_dict.get('students', [])
                self.topics = student_dict.get('topics', [])
                self.grades = student_dict.get('grades', [])
                self.attendance = student_dict.get('attendance', [])
            print("Data successfully loaded from the file.")
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
        except PermissionError:
            print(f"Error: Permission denied to read the file '{filename}'.")
        except json.JSONDecodeError as e:
            print(f"Error: The file '{filename}' contains invalid JSON. Details: {e}")
        except Exception as e:
            print(f"Unexpected error: {type(e).__name__}: {e}")

if __name__ == "__main__":
    from utils import read_students_from_file
    
    PATH = 'data/students_list.txt'
    students = read_students_from_file(PATH)
    tracker = Course(name='Python for beginners', students=students)
    
    tracker.add_topic(name='Matplotlib', type='Lecture', max_score=20)
    tracker.set_grade("Зайкова В. Д.", "Matplotlib", 5)
    tracker.mark_attendance("Зайкова В. Д.", "Matplotlib", True)
    
    print("Оценки:", tracker.grades)
    print("Посещаемость:", tracker.attendance)
    
    tracker.save_to_file('data/topics_list.json')
  
    new_tracker = Course(name="Loaded Course")
    new_tracker.load_from_file('data/topics_list.json')
    print("\n--- Загруженные данные ---")
    print("Студенты:", new_tracker.students)
    print("Темы:", new_tracker.topics)
    print("Оценки:", new_tracker.grades)
    print("Посещаемость:", new_tracker.attendance)

        