from g_python.hpacket import HPacket

from habbo.config.config import habbo_logger, ext

def ban_player(user_id : int, room_id, user_name):
    #{out:BanUserWithDuration}{i:80599039}{i:149281613}{s:"RWUAM_BAN_USER_PERM"}
    try:
        ext.send_to_server(HPacket("BanUserWithDuration", user_id, room_id, "RWUAM_BAN_USER_PERM"))
        habbo_logger.warning(f"User {user_name} banned froom room.")
    except Exception as err:
        habbo_logger.error(f"Error banning user from room. -> {err}")
    
def mute_player(user_id: int, room_id, user_name, message):
    #out:MuteUser}{i:80599039}{i:149281613}{i:10}
    try:
        ext.send_to_server(HPacket("MuteUser", user_id, room_id, 60))
        habbo_logger.warning(f"User {user_name} muted - {message}")
    except Exception as err:
        habbo_logger.error(f"Error mutting user from room. -> {err}")