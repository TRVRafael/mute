class Room:
    def __init__(self, current_room_id: int = None):
        self._current_room_id = current_room_id
        
    def set_current_room_id(self, room_id):
        self._current_room_id = room_id
    
    def get_current_room_id(self):
        return self._current_room_id
    
room_manager = Room()