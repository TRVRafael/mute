from datetime import datetime

def get_timestamp():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def is_dic(user_motto: str) -> bool:
    return user_motto.startswith("[DIC]")