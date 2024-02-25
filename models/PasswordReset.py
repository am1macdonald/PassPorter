from pydantic import EmailStr

from controllers.DatabaseController import DatabaseController


class PasswordReset:
    def __init__(self):
        self.db = DatabaseController()

    def add(self, email: EmailStr) -> bool:
        self.db.connect()
        res = len(self.db.arbitrary(f'''
            INSERT INTO public.password_reset (user_id)
            SELECT users.user_id
            FROM users
            WHERE users.email = %s
            RETURNING *;''', (email,))) > 0
        if res:
            self.db.commit()
        else:
            self.db.rollback()
        self.db.disconnect()
        return res
