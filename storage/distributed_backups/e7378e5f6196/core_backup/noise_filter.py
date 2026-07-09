# ==========================================
# BOUNDLESS AI
# NOISE FILTER v1
# DETECT AND REMOVE NOISE
# ==========================================

import re


class NoiseFilter:

    def __init__(self):

        self.noise_patterns = {
            "empty": [
                "^$",
                "^\\s+$"
            ],
            "repetitive": [
                r"(.)\\1{5,}",
                r"(\\w+)\\s+\\1\\s+\\1"
            ],
            "irrelevant": [
                "لطفا", "لطفاً", "خواهش",
                "ببخشید", "معذرت"
            ],
            "meaningless": [
                "هوممم", "آهان", "اوهوم",
                "خب خب", "بله بله"
            ],
            "emotional": [
                "😡", "😠", "🤬", "💢",
                "😭", "😢", "😤"
            ]
        }

        self.noise_threshold = 0.3

    # ======================================
    # ANALYZE
    # ======================================

    def analyze(self, text, source="UNKNOWN"):

        """
        تحلیل نویز در ورودی یا خروجی
        """

        text = str(text)

        result = {
            "original": text,
            "clean": text,
            "noise_level": 0,
            "noise_types": [],
            "has_noise": False,
            "source": source
        }

        # ===============================
        # 1. تشخیص نویز خالی
        # ===============================

        if self._is_empty(text):
            result["noise_level"] += 0.4
            result["noise_types"].append("empty")
            result["clean"] = ""

        # ===============================
        # 2. تشخیص تکرار
        # ===============================

        if self._is_repetitive(text):
            result["noise_level"] += 0.3
            result["noise_types"].append("repetitive")
            result["clean"] = self._remove_repetition(text)

        # ===============================
        # 3. تشخیص کلمات بی‌ربط
        # ===============================

        if self._has_irrelevant(text):
            result["noise_level"] += 0.2
            result["noise_types"].append("irrelevant")
            result["clean"] = self._remove_irrelevant(text)

        # ===============================
        # 4. تشخیص بی‌معنی
        # ===============================

        if self._is_meaningless(text):
            result["noise_level"] += 0.3
            result["noise_types"].append("meaningless")
            result["clean"] = self._remove_meaningless(text)

        # ===============================
        # 5. تشخیص احساسی
        # ===============================

        if self._is_emotional(text):
            result["noise_level"] += 0.1
            result["noise_types"].append("emotional")
            result["clean"] = self._remove_emotional(text)

        # ===============================
        # 6. تعیین نهایی
        # ===============================

        result["noise_level"] = min(result["noise_level"], 1.0)
        result["has_noise"] = result["noise_level"] >= self.noise_threshold

        # پاک‌سازی نهایی
        if result["has_noise"]:
            result["clean"] = self._final_clean(result["clean"])

        return result

    # ======================================
    # FILTER
    # ======================================

    def filter(self, text, source="UNKNOWN"):

        """
        فیلتر کردن نویز و بازگرداندن متن پاک
        """

        analysis = self.analyze(text, source)
        return analysis["clean"]

    # ======================================
    # IS EMPTY
    # ======================================

    def _is_empty(self, text):

        if not text or not str(text).strip():
            return True

        if len(str(text).strip()) < 2:
            return True

        return False

    # ======================================
    # IS REPETITIVE
    # ======================================

    def _is_repetitive(self, text):

        for pattern in self.noise_patterns["repetitive"]:
            if re.search(pattern, text):
                return True
        return False

    # ======================================
    # HAS IRRELEVANT
    # ======================================

    def _has_irrelevant(self, text):

        for word in self.noise_patterns["irrelevant"]:
            if word in text:
                return True
        return False

    # ======================================
    # IS MEANINGLESS
    # ======================================

    def _is_meaningless(self, text):

        for word in self.noise_patterns["meaningless"]:
            if word in text:
                return True
        return False

    # ======================================
    # IS EMOTIONAL
    # ======================================

    def _is_emotional(self, text):

        for word in self.noise_patterns["emotional"]:
            if word in text:
                return True
        return False

    # ======================================
    # REMOVE REPETITION
    # ======================================

    def _remove_repetition(self, text):

        # حذف تکرارهای بیش از حد
        text = re.sub(r"(.)\\1{5,}", "\\1", text)
        text = re.sub(r"(\\w+)\\s+\\1\\s+\\1", "\\1", text)
        return text

    # ======================================
    # REMOVE IRRELEVANT
    # ======================================

    def _remove_irrelevant(self, text):

        for word in self.noise_patterns["irrelevant"]:
            text = text.replace(word, "")
        return text

    # ======================================
    # REMOVE MEANINGLESS
    # ======================================

    def _remove_meaningless(self, text):

        for word in self.noise_patterns["meaningless"]:
            text = text.replace(word, "")
        return text

    # ======================================
    # REMOVE EMOTIONAL
    # ======================================

    def _remove_emotional(self, text):

        for word in self.noise_patterns["emotional"]:
            text = text.replace(word, "")
        return text

    # ======================================
    # FINAL CLEAN
    # ======================================

    def _final_clean(self, text):

        # حذف فاصله‌های اضافی
        text = re.sub(r"\\s+", " ", text)

        # حذف فاصله قبل از نقطه و ویرگول
        text = re.sub(r"\\s+([\\.\\,])", "\\1", text)

        # حذف نقطه‌های اضافی
        text = re.sub(r"\\.{3,}", "...", text)

        return text.strip()

    # ======================================
    # GET STATS
    # ======================================

    def get_stats(self):

        return {
            "noise_patterns": len(self.noise_patterns),
            "threshold": self.noise_threshold
        }


# ==========================================
# TEST
# ==========================================

if __name__ == "__main__":

    filter = NoiseFilter()

    print("=" * 50)
    print("NOISE FILTER TEST")
    print("=" * 50)

    # تست ۱: نویز خالی
    print("\n📌 تست ۱: ورودی خالی")
    result = filter.analyze("")
    print(f"نویز: {result['has_noise']}")
    print(f"نوع: {result['noise_types']}")

    # تست ۲: تکرار
    print("\n📌 تست ۲: تکرار")
    result = filter.analyze("بله بله بله بله بله")
    print(f"نویز: {result['has_noise']}")
    print(f"نوع: {result['noise_types']}")
    print(f"پاک شده: {result['clean']}")

    # تست ۳: کلمات بی‌ربط
    print("\n📌 تست ۳: کلمات بی‌ربط")
    result = filter.analyze("لطفاً به من بگو ببخشید این پروژه کامل است؟")
    print(f"نویز: {result['has_noise']}")
    print(f"نوع: {result['noise_types']}")
    print(f"پاک شده: {result['clean']}")

    # تست ۴: بی‌معنی
    print("\n📌 تست ۴: بی‌معنی")
    result = filter.analyze("خب خب بله بله هوممم")
    print(f"نویز: {result['has_noise']}")
    print(f"نوع: {result['noise_types']}")
    print(f"پاک شده: {result['clean']}")

    # تست ۵: ترکیبی
    print("\n📌 تست ۵: ترکیبی")
    result = filter.analyze("لطفاً ببخشید بله بله بله هوممم 😡")
    print(f"نویز: {result['has_noise']}")
    print(f"نوع: {result['noise_types']}")
    print(f"پاک شده: {result['clean']}")