from exceptions import StudentNotFoundError

def requires_student(func):
    def wrapper(self, student_name, *args, **kwargs):
        if student_name not in self.students:
            raise StudentNotFoundError(f"Student '{student_name}' not found")
        return func(self, student_name, *args, **kwargs)
    return wrapper

def log_action(func):
    def wrapper(*args, **kwargs):
        print(f"[LOG] Calling {func.__name__} with args={args[1:]} kwargs={kwargs}")
        result = func(*args, **kwargs)
        print(f"[LOG] {func.__name__} completed")
        return result
    return wrapper