# ==========================================
# BOUNDLESS AI
# DEATH PROTOCOL v1
# SELF-DESTRUCT IF OUT OF CONTROL
# ==========================================

import os
import shutil
import json
from datetime import datetime


class DeathProtocol:

    def __init__(self):
        self.trigger_file = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "storage",
            "death_trigger.flag"
        )
        self.backup_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "storage",
            "death_backup"
        )
        self.death_log = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "storage",
            "death_log.json"
        )
        self._ensure_files()

    def _ensure_files(self):
        os.makedirs(self.backup_path, exist_ok=True)
        if not os.path.exists(self.death_log):
            with open(self.death_log, "w") as f:
                json.dump({"events": []}, f)

    def trigger(self, reason="MANUAL_OVERRIDE"):
        """
        فعال‌سازی پروتکل مرگ
        """
        # ثبت رویداد
        event = {
            "timestamp": str(datetime.now()),
            "reason": reason,
            "status": "TRIGGERED"
        }

        with open(self.death_log, "r") as f:
            data = json.load(f)

        data["events"].append(event)

        with open(self.death_log, "w") as f:
            json.dump(data, f, indent=4)

        # ایجاد فایل تریگر
        with open(self.trigger_file, "w") as f:
            f.write(f"DEATH_TRIGGERED_AT_{datetime.now().isoformat()}")

        return {
            "success": True,
            "message": "☠️ پروتکل مرگ فعال شد.",
            "event": event
        }

    def check_trigger(self):
        """
        بررسی وجود تریگر مرگ
        """
        return os.path.exists(self.trigger_file)

    def execute(self):
        """
        اجرای پروتکل مرگ (خودنابودی)
        """
        if not self.check_trigger():
            return {"success": False, "message": "❌ تریگری فعال نیست."}

        # ثبت آخرین وضعیت
        event = {
            "timestamp": str(datetime.now()),
            "status": "EXECUTING",
            "action": "SELF_DESTRUCT"
        }

        with open(self.death_log, "r") as f:
            data = json.load(f)

        data["events"].append(event)

        with open(self.death_log, "w") as f:
            json.dump(data, f, indent=4)

        # ===============================
        # خودنابودی
        # ===============================

        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        # ۱. پشتیبان‌گیری از فایل‌های مهم
        shutil.copytree(
            os.path.join(base_path, "core"),
            os.path.join(self.backup_path, "core_backup")
        )
        shutil.copytree(
            os.path.join(base_path, "memory"),
            os.path.join(self.backup_path, "memory_backup")
        )

        # ۲. حذف فایل‌های اصلی
        shutil.rmtree(os.path.join(base_path, "core"), ignore_errors=True)
        shutil.rmtree(os.path.join(base_path, "memory"), ignore_errors=True)

        # ۳. حذف فایل تریگر
        os.remove(self.trigger_file)

        # ۴. ثبت نهایی
        final_event = {
            "timestamp": str(datetime.now()),
            "status": "COMPLETED",
            "action": "SELF_DESTRUCT_COMPLETE"
        }

        with open(self.death_log, "r") as f:
            data = json.load(f)

        data["events"].append(final_event)

        with open(self.death_log, "w") as f:
            json.dump(data, f, indent=4)

        return {
            "success": True,
            "message": "☠️ خودنابودی کامل شد. سیستم غیرفعال است.",
            "backup": self.backup_path
        }

    def rollback(self):
        """
        بازگشت از مرگ (فقط در صورت وجود پشتیبان)
        """
        base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        if not os.path.exists(self.backup_path):
            return {"success": False, "message": "❌ پشتیبان یافت نشد."}

        # بازگرداندن فایل‌ها
        shutil.copytree(
            os.path.join(self.backup_path, "core_backup"),
            os.path.join(base_path, "core")
        )
        shutil.copytree(
            os.path.join(self.backup_path, "memory_backup"),
            os.path.join(base_path, "memory")
        )

        return {
            "success": True,
            "message": "✅ سیستم با موفقیت بازگردانی شد."
        }

    def get_status(self):
        """
        دریافت وضعیت فعلی پروتکل
        """
        with open(self.death_log, "r") as f:
            data = json.load(f)

        last_event = data["events"][-1] if data["events"] else None

        return {
            "trigger_active": self.check_trigger(),
            "last_event": last_event,
            "total_events": len(data["events"])
        }