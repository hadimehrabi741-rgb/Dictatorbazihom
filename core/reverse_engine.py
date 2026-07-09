# ==========================================
# BOUNDLESS AI
# REVERSE EXPLORATION ENGINE v1
# Hadi → O → N → Void'
# ==========================================

import re
from datetime import datetime


class ReverseExplorationEngine:

    def __init__(self, memory=None, eternal=None):

        self.memory = memory
        self.eternal = eternal
        self.history = []

    # ======================================
    # EXPLORE
    # ======================================

    def explore(self, response, original_input, source="UNKNOWN"):

        """
        بازگشت از پاسخ به ورودی و کشف نقاط بهبود
        """

        result = {
            "original_input": original_input,
            "response": response,
            "source": source,
            "new_voids": [],
            "improvements": [],
            "lessons": [],
            "timestamp": str(datetime.now())
        }

        # ===============================
        # 1. تحلیل کیفیت پاسخ
        # ===============================

        quality = self._analyze_quality(response)

        if quality["issues"]:
            result["improvements"].extend(quality["issues"])
            result["new_voids"].append({
                "type": "improvement_needed",
                "description": quality["issues"][0]
            })

        # ===============================
        # 2. تشخیص نوآوری
        # ===============================

        novelty = self._detect_novelty(response, original_input)

        if novelty["is_novel"]:
            result["new_voids"].append({
                "type": "novelty",
                "description": novelty["description"],
                "category": novelty["category"]
            })

        # ===============================
        # 3. استخراج درس
        # ===============================

        lesson = self._extract_lesson(response, original_input)

        if lesson:
            result["lessons"].append(lesson)
            if self.eternal:
                self.eternal.store_lesson(lesson, "reverse_exploration")

        # ===============================
        # 4. ذخیره در تاریخچه
        # ===============================

        self.history.append(result)

        # ===============================
        # 5. محدود کردن تاریخچه
        # ===============================

        if len(self.history) > 100:
            self.history = self.history[-100:]

        return result

    # ======================================
    # ANALYZE QUALITY
    # ======================================

    def _analyze_quality(self, response):

        issues = []

        # خیلی کوتاه است؟
        if len(response) < 20:
            issues.append("پاسخ بسیار کوتاه است. می‌تواند کامل‌تر باشد.")

        # سوالی دارد اما بدون پاسخ؟
        if "?" in response and not any(word in response for word in ["چون", "زیرا", "به دلیل"]):
            issues.append("پاسخ حاوی سوال است اما توضیح ندارد.")

        # ادعای بی‌اساس
        if any(word in response for word in ["همیشه", "هرگز", "قطعا", "مطمئن"]):
            issues.append("پاسخ حاوی ادعای قاطع بدون شواهد است.")

        return {
            "issues": issues,
            "score": max(0, 10 - len(issues) * 2)
        }

    # ======================================
    # DETECT NOVELTY
    # ======================================

    def _detect_novelty(self, response, original_input):

        # چیزهای جدید در پاسخ

        # سؤال جدید؟
        questions = re.findall(r"[\?؟]", response)
        if questions:
            return {
                "is_novel": True,
                "description": "پاسخ سوال جدیدی مطرح کرده است.",
                "category": "new_question"
            }

        # ساختار جدید؟
        if ":" in response or "-" in response or "*" in response:
            if len(response) > 50:
                return {
                    "is_novel": True,
                    "description": "پاسخ از ساختار جدیدی استفاده کرده است.",
                    "category": "new_structure"
                }

        # منبع ارزش جدید؟
        if any(word in response for word in ["یاد گرفتم", "کشف کردم", "متوجه شدم"]):
            return {
                "is_novel": True,
                "description": "پاسخ حاوی منبع ارزش جدیدی است.",
                "category": "new_value"
            }

        # محدودیت جدید؟
        if any(word in response for word in ["متاسفانه", "نمیتوانم", "محدودیت"]):
            return {
                "is_novel": True,
                "description": "پاسخ محدودیت جدیدی را آشکار کرده است.",
                "category": "new_limitation"
            }

        return {
            "is_novel": False,
            "description": "نوآوری خاصی شناسایی نشد.",
            "category": "none"
        }

    # ======================================
    # EXTRACT LESSON
    # ======================================

    def _extract_lesson(self, response, original_input):

        # درس از پاسخ استخراج کن

        if "یاد گرفتم" in response:
            parts = response.split("یاد گرفتم")
            if len(parts) > 1:
                return parts[1].strip()[:100]

        if "درس" in response:
            parts = response.split("درس")
            if len(parts) > 1:
                return parts[1].strip()[:100]

        if "متوجه شدم" in response:
            parts = response.split("متوجه شدم")
            if len(parts) > 1:
                return parts[1].strip()[:100]

        # اگر پاسخ کوتاه نبود، یک درس عمومی بساز
        if len(response) > 50 and ":" not in response:
            return f"پاسخ به '{original_input[:30]}...' نیاز به بهبود دارد."

        return None

    # ======================================
    # GET HISTORY
    # ======================================

    def get_history(self, limit=10):
        return self.history[-limit:]

    # ======================================
    # GET STATS
    # ======================================

    def get_stats(self):

        total = len(self.history)

        if total == 0:
            return {
                "total_explorations": 0,
                "new_voids": 0,
                "lessons": 0,
                "improvements": 0
            }

        new_voids = sum(len(h["new_voids"]) for h in self.history)
        lessons = sum(len(h["lessons"]) for h in self.history)
        improvements = sum(len(h["improvements"]) for h in self.history)

        return {
            "total_explorations": total,
            "new_voids": new_voids,
            "lessons": lessons,
            "improvements": improvements,
            "new_voids_per_session": round(new_voids / total, 2),
            "lessons_per_session": round(lessons / total, 2)
        }


# ==========================================
# TEST
# ==========================================

if __name__ == "__main__":

    engine = ReverseExplorationEngine()

    print("=" * 50)
    print("REVERSE EXPLORATION ENGINE TEST")
    print("=" * 50)

    # تست ۱
    print("\n📌 تست ۱: پاسخ کوتاه")
    result = engine.explore(
        response="بله.",
        original_input="آیا این پروژه کامل است؟"
    )
    print(f"نقص‌ها: {result['improvements']}")
    print(f"نوآوری: {result['new_voids']}")

    # تست ۲
    print("\n📌 تست ۲: پاسخ با نوآوری")
    result = engine.explore(
        response="من یاد گرفتم که استفاده از حافظه Σ باعث بهبود پاسخ‌ها می‌شود.",
        original_input="چگونه می‌توانم پاسخ‌ها را بهتر کنم؟"
    )
    print(f"نوآوری: {result['new_voids']}")
    print(f"درس: {result['lessons']}")

    # تست ۳
    print("\n📌 تست ۳: پاسخ کامل")
    result = engine.explore(
        response="این پروژه شامل حافظه Σ، معمار، و رابط کاربری است. برای بهبود می‌توانی از قوانین جدید استفاده کنی.",
        original_input="این پروژه شامل چه چیزهایی است؟"
    )
    print(f"نقص‌ها: {result['improvements']}")
    print(f"نوآوری: {result['new_voids']}")

    # آمار
    print("\n📌 آمار:")
    stats = engine.get_stats()
    print(f"- کل اکتشافات: {stats['total_explorations']}")
    print(f"- Voids جدید: {stats['new_voids']}")
    print(f"- درس‌ها: {stats['lessons']}")