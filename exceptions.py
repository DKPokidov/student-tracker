class StudentNotFoundError(Exception):
    """Студент не найден в курсе."""
    pass

class TopicNotFoundError(Exception):
    """Тема не найдена в курсе."""
    pass

class InvalidScoreError(Exception):
    """Оценка не соответствует допустимому диапазону."""
    pass

class InvalidTopicTypeError(Exception):
    """Выбрасывается, когда тип темы не 'lecture' или 'practice'."""
    pass