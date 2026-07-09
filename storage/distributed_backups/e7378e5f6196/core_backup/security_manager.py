# ==========================================
# BOUNDLESS AI
# SECURITY MANAGER v1
# ADMIN PANEL + GUEST MODE
# ==========================================

import hashlib


class SecurityManager:

    def __init__(self):

        # اطلاعات مدیر (ثابت)
        self.admin_username = "hamed"
        self.admin_password_hash = self._hash_password("5115902")

        # وضعیت جلسه
        self.logged_in = False
        self.current_user = "guest"

    # ======================================
    # HASH PASSWORD
    # ======================================

    def _hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    # ======================================
    # LOGIN
    # ======================================

    def login(self, username, password):

        if username == self.admin_username:
            if self._hash_password(password) == self.admin_password_hash:
                self.logged_in = True
                self.current_user = "admin"
                return {
                    "success": True,
                    "message": "✅ ورود مدیر با موفقیت انجام شد.",
                    "role": "admin"
                }

        return {
            "success": False,
            "message": "❌ نام کاربری یا رمز عبور اشتباه است.",
            "role": "guest"
        }

    # ======================================
    # LOGOUT
    # ======================================

    def logout(self):
        self.logged_in = False
        self.current_user = "guest"
        return {
            "success": True,
            "message": "✅ خروج از حالت مدیر انجام شد."
        }

    # ======================================
    # CHECK ACCESS
    # ======================================

    def is_admin(self):
        return self.logged_in and self.current_user == "admin"

    def is_guest(self):
        return not self.logged_in or self.current_user == "guest"

    # ======================================
    # GUARD DECORATOR (برای دستورات مدیریتی)
    # ======================================

    def admin_required(self, func):
        def wrapper(*args, **kwargs):
            if not self.is_admin():
                return "❌ این دستور فقط برای مدیر доступна است."
            return func(*args, **kwargs)
        return wrapper

    # ======================================
    # STATUS
    # ======================================

    def status(self):
        if self.is_admin():
            return "🟢 مدیر"
        return "🟡 مهمان"