# ==========================================
# BOUNDLESS AI
# MEMORY INTENT DETECTOR v4
# FIXED DUPLICATE DETECTION
# ==========================================

class MemoryIntent:

    def detect(self, text, memory=None):

        text = str(text).strip()
        normalized = text.replace("‌", "")

        # ==================================
        # IDENTITY
        # ==================================

        identity_patterns = [
            "من حامد هستم", "من حامدم", "سلام من حامد هستم",
            "سلام من حامدم", "اسم من", "نام من", "من هستم"
        ]

        for pattern in identity_patterns:
            if pattern in normalized:
                if self._exists_in_memory(text, memory):
                    return {"save": True, "type": "identity", "existing": True}
                return {"save": True, "type": "identity", "existing": False}

        # ==================================
        # PREFERENCE
        # ==================================

        preference_patterns = [
            "علاقه دارم", "علاقه‌مندم", "دوست دارم", "علاقه من"
        ]

        for pattern in preference_patterns:
            if pattern in normalized:
                if self._exists_in_memory(text, memory):
                    return {"save": True, "type": "preference", "existing": True}
                return {"save": True, "type": "preference", "existing": False}

        # ==================================
        # PROJECT (فقط در صورت ذکر پروژه شخصی)
        # ==================================

        project_patterns = [
            "پروژه من", "پروژه‌ام", "پروژه شخصی", "پروژه جدید"
        ]

        for pattern in project_patterns:
            if pattern in normalized:
                if self._exists_in_memory(text, memory):
                    return {"save": True, "type": "project", "existing": True}
                return {"save": True, "type": "project", "existing": False}

        # ==================================
        # DEFAULT: NO SAVE
        # ==================================

        return {"save": False, "type": None}

    # ==================================
    # CHECK EXIST (اصلاح‌شده)
    # ==================================

    def _exists_in_memory(self, text, memory):

        if not memory:
            return False

        context = memory.get_context()

        for item in context.get("long_memory", []):
            if not isinstance(item, dict):
                continue

            old = item.get("memory", "")
            old_user = item.get("user", "")

            # فقط متن‌های قبلی را چک کن، نه سوالات جدید
            if old.strip() == text.strip():
                return True
            if old_user.strip() == text.strip():
                return True

        return False