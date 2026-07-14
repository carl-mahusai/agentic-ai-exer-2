from agents.memory import SQLiteSession

DB_PATH = "sessions.db"

_sessions = {}


def get_session(session_id):

    if session_id not in _sessions:
        _sessions[session_id] = SQLiteSession(
            session_id=session_id,
            db_path=DB_PATH,
        )

    return _sessions[session_id]