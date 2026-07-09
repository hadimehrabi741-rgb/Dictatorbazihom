# ==========================================
# BOUNDLESS AI
# NOVELTY DETECTOR v1
# NOVELTY PRINCIPLE IMPLEMENTATION
# ==========================================

import re
from datetime import datetime


class NoveltyDetector:

    def __init__(self, memory=None, eternal=None):

        self.memory = memory
        self.eternal = eternal
        self.history = []
        self.novelty_threshold = 0.6

    # ======================================
    # CHECK NOVELTY
    # ======================================

    def check(self, response, original_input, source="UNKNOWN"):

        """
        بررسی نوآوری در پاسخ بر اساس اصل Novelty Principle
        """

        result = {
            "original_input": original_input,
            "response": response,
            "source": source,
            "is_novel": False,
            "novelty_score": 0,
            "novelty_type": None,
            "description": None,
            "timestamp": str(datetime.now())
        }

        # ===============================
        # 1. بررسی سؤال جدید
        # ===============================

        question_score = self._check_new_question(response, original_input)
        if question_score > 0:
            result["novelty_score"] += question_score
            result["novelty_type"] = "new_question"
            result["description"] = "پاسخ سوال جدیدی مطرح کرده است."

        # ===============================
        # 2. بررسی ساختار جدید
        # ===============================

        structure_score = self._check_new_structure(response)
        if structure_score > 0:
            result["novelty_score"] += structure_score
            result["novelty_type"] = "new_structure"
            result["description"] = "پاسخ از ساختار جدیدی استفاده کرده است."

        # ===============================
        # 3. بررسی محدودیت/تناقض جدید
        # ===============================

        limitation_score = self._check_new_limitation(response)
        if limitation_score > 0:
            result["novelty_score"] += limitation_score
            result["novelty_type"] = "new_limitation"
            result["description"] = "پاسخ محدودیت جدیدی را آشکار کرده است."

        # ===============================
        # 4. بررسی منبع ارزش جدید
        # ===============================

        value_score = self._check_new_value(response)
        if value_score > 0:
            result["novelty_score"] += value_score
            result["novelty_type"] = "new_value"
            result["description"] = "پاسخ منبع ارزش جدیدی را ارائه کرده است."

        # ===============================
        # 5. تعیین نهایی
        # ===============================

        result["novelty_score"] = min(result["novelty_score"], 1.0)
        result["is_novel"] = result["novelty_score"] >= self.novelty_threshold

        # ===============================
        # 6. ذخیره در تاریخچه
        # ===============================

        if result["is_novel"]:
            self.history.append(result)
            if self.eternal:
                self._store_novelty(result)

        # محدود کردن تاریخچه
        if len(self.history) > 100:
            self.history = self.history[-100:]

        return result

    # ======================================
    # CHECK NEW QUESTION
    # ======================================

    def _check_new_question(self, response, original_input):

        # آیا پاسخ سوال جدیدی مطرح کرده است؟
        questions = re.findall(r"[\?؟]", response)

        if len(questions) > 0:
            # آیا این سوال در ورودی اصلی بود؟
            if "?" not in original_input and "؟" not in original_input:
                return 0.3

        return 0

    # ======================================
    # CHECK NEW STRUCTURE
    # ======================================

    def _check_new_structure(self, response):

        # آیا پاسخ از ساختار جدیدی استفاده کرده است؟

        # ساختار لیست
        if re.search(r"[1-9][\.\)]", response):
            return 0.3

        # ساختار خط تیره
        if "-" in response or "*" in response:
            return 0.2

        # ساختار دوقطبی (مثلاً "اما")
        if "اما" in response and len(response) > 50:
            return 0.2

        return 0

    # ======================================
    # CHECK NEW LIMITATION
    # ======================================

    def _check_new_limitation(self, response):

        limitation_words = [
            "متاسفانه", "نمیتوانم", "محدودیت",
            "متاسفم", "امکان ندارد", "نمی‌توانم",
            "هنوز", "فعلا"
        ]

        for word in limitation_words:
            if word in response:
                return 0.3

        return 0

    # ======================================
    # CHECK NEW VALUE
    # ======================================

    def _check_new_value(self, response):

        value_words = [
            "یاد گرفتم", "کشف کردم", "متوجه شدم",
            "بهترین", "کاربردی", "مفید",
            "کارآمد", "بهینه", "خلاقانه"
        ]

        for word in value_words:
            if word in response:
                return 0.3

        return 0

    # ======================================
    # STORE NOVELTY
    # ======================================

    def _store_novelty(self, novelty_data):

        if not self.eternal:
            return

        description = novelty_data.get("description", "نوآوری جدید")
        novelty_type = novelty_data.get("novelty_type", "general")

        if novelty_type == "new_question":
            self.eternal.store_pattern(
                f"سوال جدید: {description}",
                "novelty"
            )
        elif novelty_type == "new_structure":
            self.eternal.store_structure(
                f"ساختار جدید: {description}",
                "novelty"
            )
        elif novelty_type == "new_limitation":
            self.eternal.store_limitation(
                f"محدودیت جدید: {description}",
                "novelty"
            )
        elif novelty_type == "new_value":
            self.eternal.store_lesson(
                f"منبع ارزش جدید: {description}",
                "novelty"
            )

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
                "total_novelties": 0,
                "new_questions": 0,
                "new_structures": 0,
                "new_limitations": 0,
                "new_values": 0
            }

        stats = {
            "total_novelties": total,
            "new_questions": 0,
            "new_structures": 0,
            "new_limitations": 0,
            "new_values": 0
        }

        for item in self.history:
            if item.get("novelty_type") == "new_question":
                stats["new_questions"] += 1
            elif item.get("novelty_type") == "new_structure":
                stats["new_structures"] += 1
            elif item.get("novelty_type") == "new_limitation":
                stats["new_limitations"] += 1
            elif item.get("novelty_type") == "new_value":
                stats["new_values"] += 1

        return stats


# ==========================================
# TEST
# ==========================================

if __name__ == "__main__":

    detector = NoveltyDetector()

    print("=" * 50)
    print("NOVELTY DETECTOR TEST")
    print("=" * 50)

    # تست ۱: سوال جدید
    print("\n📌 تست ۱: پاسخ با سوال جدید")
    result = detector.check(
        response="بله. اما چرا باید این کار را انجام دهیم؟",
        original_input="آیا این پروژه کامل است؟"
    )
    print(f"نوآوری: {result['is_novel']}")
    print(f"امتیاز: {result['novelty_score']}")
    print(f"نوع: {result['novelty_type']}")

    # تست ۲: ساختار جدید
    print("\n📌 تست ۲: پاسخ با ساختار جدید")
    result = detector.check(
        response="مراحل: 1. تحلیل ورودی 2. پردازش 3. تولید پاسخ",
        original_input="چگونه کار می‌کند؟"
    )
    print(f"نوآوری: {result['is_novel']}")
    print(f"امتیاز: {result['novelty_score']}")
    print(f"نوع: {result['novelty_type']}")

    # تست ۳: بدون نوآوری
    print("\n📌 تست ۳: پاسخ ساده")
    result = detector.check(
        response="بله، پروژه کامل است.",
        original_input="آیا پروژه کامل است؟"
    )
    print(f"نوآوری: {result['is_novel']}")
    print(f"امتیاز: {result['novelty_score']}")

    # آمار
    print("\n📌 آمار:")
    stats = detector.get_stats()
    print(f"- کل نوآوری‌ها: {stats['total_novelties']}")
    print(f"- سوالات جدید: {stats['new_questions']}")
    print(f"- ساختارهای جدید: {stats['new_structures']}")