from agents.memory import SQLiteSession

DB_PATH = "sessions.db"

_sessions = {}


def get_session(username: str, session_id: str):

    key = (username, session_id)

    if key not in _sessions:
        _sessions[key] = SQLiteSession(
            session_id=session_id,
            db_path=DB_PATH,
        )

    return _sessions[key]