import threading

class UserManager:
    def __init__(self):
        self._users = {}
        self._lock = threading.Lock()
        
    def add_user(self, user_room_id, user_name, user_id, user_motto):
        with self._lock:
            self._users[user_room_id] = {"user_name": user_name, "user_room_index": user_room_id, "user_id": user_id, "user_motto": user_motto}
    
    def remove_user(self, user_room_id):
        with self._lock:
            if user_room_id in self._users:
                del self._users[user_room_id]
                
    def get_all_users(self):
        with self._lock:
            return self._users.copy()
        
    def get_user_info(self, user_room_id):
        with self._lock:
            if user_room_id in self._users:
                return self._users[user_room_id]
            
user_manager = UserManager()