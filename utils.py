PATH = 'data/students_list.txt'
def read_students_from_file(filename: str) -> list :
    '''Read file, convert its content tolist
      and return list of students'''
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            students = f.read().split('\n')
    except FileNotFoundError as e:
        students = []
        print(e)
    return students

if __name__ == '__main__':
    students = read_students_from_file(PATH)
    print(students)