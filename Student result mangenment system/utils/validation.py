def validate_name(name):
    if not name.isalpha():
        raise ValueError("Name must contain only letters")
    return True

def validate_mark(mark):
    if not (0 <= mark <= 100):
        raise ValueError("Mark must be between 0 and 100")
    return True
