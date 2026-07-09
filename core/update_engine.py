# ==========================================
# BOUNDLESS AI
# UPDATE ENGINE v1
# CODE UPDATE + ROLLBACK
# ==========================================

import os
import json
import subprocess
import sys
from datetime import datetime


class UpdateEngine:

    def __init__(self):

        self.base_path = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )

        self.backup_path = os.path.join(
            self.base_path,
            "storage",
            "backups"
        )

        os.makedirs(self.backup_path, exist_ok=True)

        self.update_file = os.path.join(
            self.backup_path,
            "update_log.json"
        )

        self.log = self.load_log()

    # ======================================
    # LOAD LOG
    # ======================================

    def load_log(self):

        if not os.path.exists(self.update_file):
            return {
                "updates": [],
                "current_version": 1,
                "last_update": None
            }

        try:
            with open(self.update_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {
                "updates": [],
                "current_version": 1,
                "last_update": None
            }

    # ======================================
    # SAVE LOG
    # ======================================

    def save_log(self):
        with open(self.update_file, "w", encoding="utf-8") as f:
            json.dump(self.log, f, ensure_ascii=False, indent=4)

    # ======================================
    # APPLY UPDATE
    # ======================================

    def apply_update(self, file_path, new_code, admin_user="hamed"):

        file_path = str(file_path).strip()
        new_code = str(new_code)

        if not file_path or not new_code:
            return {
                "success": False,
                "message": "❌ مسیر فایل یا کد خالی است."
            }

        # ===============================
        # 1. گرفتن نسخه پشتیبان
        # ===============================

        full_path = os.path.join(self.base_path, file_path)

        if not os.path.exists(full_path):
            return {
                "success": False,
                "message": f"❌ فایل {file_path} وجود ندارد."
            }

        backup_name = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{os.path.basename(file_path)}"
        backup_full = os.path.join(self.backup_path, backup_name)

        with open(full_path, "r", encoding="utf-8") as f:
            old_code = f.read()

        with open(backup_full, "w", encoding="utf-8") as f:
            f.write(old_code)

        # ===============================
        # 2. ذخیره کد جدید
        # ===============================

        with open(full_path, "w", encoding="utf-8") as f:
            f.write(new_code)

        # ===============================
        # 3. تست کد جدید (اجرای سریع)
        # ===============================

        test_result = self.test_code(full_path)

        if not test_result["success"]:
            # برگرداندن کد قبلی
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(old_code)

            return {
                "success": False,
                "message": f"❌ کد جدید خطا دارد: {test_result['error']}",
                "rolled_back": True
            }

        # ===============================
        # 4. ثبت در لاگ
        # ===============================

        self.log["current_version"] += 1
        self.log["last_update"] = str(datetime.now())

        self.log["updates"].append({
            "version": self.log["current_version"],
            "file": file_path,
            "admin": admin_user,
            "backup": backup_name,
            "time": str(datetime.now()),
            "status": "success"
        })

        self.save_log()

        return {
            "success": True,
            "message": f"✅ کد جدید با موفقیت اعمال شد. نسخه: {self.log['current_version']}",
            "version": self.log["current_version"],
            "backup": backup_name
        }

    # ======================================
    # TEST CODE
    # ======================================

    def test_code(self, file_path):

        try:
            result = subprocess.run(
                [sys.executable, "-c", f"import {os.path.basename(file_path).replace('.py', '')}"],
                capture_output=True,
                text=True,
                timeout=5,
                cwd=os.path.dirname(file_path)
            )

            if result.returncode == 0:
                return {"success": True}

            return {"success": False, "error": result.stderr or result.stdout}

        except subprocess.TimeoutExpired:
            return {"success": False, "error": "Timeout"}

        except Exception as e:
            return {"success": False, "error": str(e)}

    # ======================================
    # ROLLBACK
    # ======================================

    def rollback(self, version=None):

        if not self.log["updates"]:
            return {
                "success": False,
                "message": "❌ هیچ به‌روزرسانی قبلی برای بازگشت وجود ندارد."
            }

        if version is None:
            # بازگشت به آخرین نسخه قبل
            version = self.log["current_version"] - 1

        # پیدا کردن بکاپ مربوط به نسخه
        backup_file = None
        for update in reversed(self.log["updates"]):
            if update["version"] == version:
                backup_file = update["backup"]
                break

        if not backup_file:
            return {
                "success": False,
                "message": f"❌ نسخه {version} پیدا نشد."
            }

        backup_full = os.path.join(self.backup_path, backup_file)

        if not os.path.exists(backup_full):
            return {
                "success": False,
                "message": f"❌ فایل بکاپ {backup_file} وجود ندارد."
            }

        # پیدا کردن مسیر فایل اصلی
        file_path = None
        for update in self.log["updates"]:
            if update["backup"] == backup_file:
                file_path = update["file"]
                break

        if not file_path:
            return {
                "success": False,
                "message": "❌ مسیر فایل پیدا نشد."
            }

        full_path = os.path.join(self.base_path, file_path)

        # بازگرداندن بکاپ
        with open(backup_full, "r", encoding="utf-8") as f:
            old_code = f.read()

        with open(full_path, "w", encoding="utf-8") as f:
            f.write(old_code)

        # به‌روزرسانی لاگ
        self.log["current_version"] = version

        self.log["updates"].append({
            "version": self.log["current_version"],
            "file": file_path,
            "admin": "system",
            "backup": backup_file,
            "time": str(datetime.now()),
            "status": "rollback"
        })

        self.save_log()

        return {
            "success": True,
            "message": f"✅ بازگشت به نسخه {version} با موفقیت انجام شد."
        }

    # ======================================
    # HISTORY
    # ======================================

    def history(self, limit=10):

        updates = self.log["updates"][-limit:]

        if not updates:
            return "📋 هیچ به‌روزرسانی ثبت نشده است."

        result = "📋 تاریخچه به‌روزرسانی:\n\n"

        for update in reversed(updates):
            result += f"نسخه {update['version']} | {update['file']} | {update['time']} | {update['status']}\n"

        return result


# ==========================================
# TEST
# ==========================================

if __name__ == "__main__":

    engine = UpdateEngine()

    print("=" * 50)
    print("UPDATE ENGINE TEST")
    print("=" * 50)

    print("\n📌 تاریخچه:")
    print(engine.history())

    print("\n📌 اعمال به‌روزرسانی (فایل تست):")
    result = engine.apply_update(
        "core/test.py",
        "print('Hello from new code')"
    )
    print(result["message"])

    print("\n📌 تاریخچه جدید:")
    print(engine.history())