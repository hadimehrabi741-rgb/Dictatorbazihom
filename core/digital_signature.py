# ==========================================
# BOUNDLESS AI
# DIGITAL SIGNATURE v1
# FORCED SIGNATURE VERIFICATION
# ==========================================

import hashlib
import os
import json
from datetime import datetime


class DigitalSignature:

    def __init__(self):
        self.signature_file = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "storage",
            "signature.json"
        )
        self.private_key = "ROOT_ADMIN_HAMED_5115902"  # کلید خصوصی روت ادمین
        self._ensure_signature_file()

    def _ensure_signature_file(self):
        if not os.path.exists(self.signature_file):
            with open(self.signature_file, "w") as f:
                json.dump({
                    "signatures": [],
                    "last_verified": str(datetime.now())
                }, f)

    def sign(self, data):
        """
        امضای یک داده با کلید خصوصی
        """
        combined = data + self.private_key
        return hashlib.sha256(combined.encode()).hexdigest()

    def verify(self, data, signature):
        """
        بررسی امضای یک داده
        """
        expected = self.sign(data)
        return expected == signature

    def sign_file(self, file_path):
        """
        امضای یک فایل
        """
        if not os.path.exists(file_path):
            return {"success": False, "message": "فایل وجود ندارد."}

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        signature = self.sign(content)

        # ذخیره امضا
        with open(self.signature_file, "r") as f:
            data = json.load(f)

        data["signatures"].append({
            "file": file_path,
            "signature": signature,
            "timestamp": str(datetime.now())
        })

        with open(self.signature_file, "w") as f:
            json.dump(data, f, indent=4)

        return {
            "success": True,
            "signature": signature,
            "message": "✅ فایل با موفقیت امضا شد."
        }

    def verify_file(self, file_path):
        """
        بررسی امضای یک فایل
        """
        if not os.path.exists(file_path):
            return {"success": False, "message": "فایل وجود ندارد."}

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        current_signature = self.sign(content)

        # بررسی امضای ذخیره‌شده
        with open(self.signature_file, "r") as f:
            data = json.load(f)

        for sig_record in data["signatures"]:
            if sig_record["file"] == file_path:
                if sig_record["signature"] == current_signature:
                    return {"success": True, "message": "✅ امضا معتبر است."}
                return {"success": False, "message": "❌ امضا نامعتبر است."}

        return {"success": False, "message": "❌ امضایی برای این فایل یافت نشد."}

    def verify_all(self):
        """
        بررسی همه فایل‌های امضا شده
        """
        with open(self.signature_file, "r") as f:
            data = json.load(f)

        results = []
        for sig_record in data["signatures"]:
            file_path = sig_record["file"]
            result = self.verify_file(file_path)
            results.append({
                "file": file_path,
                "valid": result["success"],
                "message": result["message"]
            })

        return results

    def get_last_signature(self):
        """
        دریافت آخرین امضای ثبت شده
        """
        with open(self.signature_file, "r") as f:
            data = json.load(f)

        if data["signatures"]:
            return data["signatures"][-1]

        return None