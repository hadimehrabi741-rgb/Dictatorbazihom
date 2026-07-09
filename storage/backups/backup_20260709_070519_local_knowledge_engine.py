# ==========================================
# BOUNDLESS AI
# LOCAL KNOWLEDGE ENGINE v1
# FALLBACK RESPONSE WITHOUT API
# ==========================================

import re
from datetime import datetime


class LocalKnowledgeEngine:

    def __init__(self, memory=None, eternal=None):

        self.memory = memory
        self.eternal = eternal

        # ===============================
        # دیتابیس پاسخ‌های ساده
        # ===============================

        self.fallback_responses = {
            "سلام": "سلام! چطور می‌توانم به شما کمک کنم؟",
            "خوبی": "خوبم، ممنون! شما چطورید؟",
            "چطوری": "خوبم، ممنون! شما چطورید؟",
            "متشکرم": "خواهش می‌کنم!",
            "ممنون": "خواهش می‌کنم!",
            "خداحافظ": "خداحافظ! روز خوبی داشته باشید.",
            "بای": "خداحافظ!",
            "چه خبر": "هیچی خاصی! شما بفرمایید.",
            "چی کار کنم": "می‌توانید سوال خود را بپرسید یا از من راهنمایی بخواهید.",
            "راهنمایی": "من می‌توانم در مورد پروژه، حافظه Σ، و معماری سیستم به شما کمک کنم.",
            "پروژه": "پروژه BOUNDLESS_AI شامل حافظه Σ، معمار، و ابزارهای مدیریتی است.",
            "حافظه": "حافظه Σ شامل دو بخش کوتاه‌مدت و بلندمدت است.",
            "معمار": "معمار شامل سه لایه Brain، Fusion و Orchestrator است.",
            "سیستم": "سیستم BOUNDLESS_AI بر اساس چهارچوب BOUNDLESS.RECONSTRUCTION.SEED.v5 ساخته شده است."
        }

    # ======================================
    # ANSWER
    # ======================================

    def answer(self, user_input):

        """
        پاسخ به سوال کاربر در حالت محلی
        """

        text = str(user_input).strip().lower()

        # ===============================
        # 1. بررسی حافظه Σ
        # ===============================

        memory_answer = self._check_memory(text)
        if memory_answer:
            return memory_answer

        # ===============================
        # 2. بررسی Eternal-File
        # ===============================

        eternal_answer = self._check_eternal(text)
        if eternal_answer:
            return eternal_answer

        # ===============================
        # 3. بررسی دیتابیس پاسخ‌های ساده
        # ===============================

        for key, response in self.fallback_responses.items():
            if key in text:
                return response

        # ===============================
        # 4. بررسی کلمات کلیدی
        # ===============================

        keyword_answer = self._check_keywords(text)
        if keyword_answer:
            return keyword_answer

        # ===============================
        # 5. پاسخ پیش‌فرض
        # ===============================

        return "من در حالت محلی هستم و به اینترنت دسترسی ندارم. لطفاً سوال خود را ساده‌تر بپرسید یا کلید API را وارد کنید."

    # ======================================
    # CHECK MEMORY
    # ======================================

    def _check_memory(self, text):

        if not self.memory:
            return None

        try:
            context = self.memory.get_context()

            # بررسی هویت
            if "من کی هستم" in text or "کی هستم" in text:
                for item in context.get("long_memory", []):
                    if item.get("type") == "identity":
                        return f"شما {item.get('memory', '').replace('من ', '').replace(' هستم', '')} هستید."

            # بررسی علاقه
            if "علاقه" in text:
                for item in context.get("long_memory", []):
                    if item.get("type") == "preference":
                        return f"شما به {item.get('memory', '')} علاقه دارید."

            # بررسی پروژه
            if "پروژه" in text:
                for item in context.get("long_memory", []):
                    if item.get("type") == "project":
                        return f"شما روی پروژه {item.get('memory', '')} کار می‌کنید."

        except:
            pass

        return None

    # ======================================
    # CHECK ETERNAL
    # ======================================

    def _check_eternal(self, text):

        if not self.eternal:
            return None

        try:
            results = self.eternal.search(text)
            if results:
                first = results[0]
                return f"در Eternal-File: {first['data'].get('text', '')[:200]}"
        except:
            pass

        return None

    # ======================================
    # CHECK KEYWORDS
    # ======================================

    def _check_keywords(self, text):

        keywords = {
            "هوش مصنوعی": "BOUNDLESS_AI یک سیستم هوش مصنوعی مبتنی بر چهارچوب BOUNDLESS.RECONSTRUCTION.SEED.v5 است.",
            "معماری": "معماری سیستم شامل سه لایه Brain، Fusion و Orchestrator است.",
            "سیستم عامل": "سیستم عامل BOUNDLESS_AI بر پایه Python ساخته شده است.",
            "پایتون": "کدهای BOUNDLESS_AI به زبان Python 3 نوشته شده‌اند.",
            "گیت": "می‌توانید پروژه را با Git مدیریت کنید."
        }

        for key, response in keywords.items():
            if key in text:
                return response

        return None

    # ======================================
    # ADD FALLBACK
    # ======================================

    def add_fallback(self, key, response):

        """
        اضافه کردن پاسخ جدید به دیتابیس
        """

        self.fallback_responses[key.lower()] = response
        return {"success": True, "message": f"پاسخ جدید برای '{key}' اضافه شد."}

    # ======================================
    # GET STATS
    # ======================================

    def get_stats(self):

        return {
            "fallback_responses": len(self.fallback_responses),
            "has_memory": self.memory is not None,
            "has_eternal": self.eternal is not None,
            "total_answers": len(self.fallback_responses)
        }


# ==========================================
# TEST
# ==========================================

if __name__ == "__main__":

    engine = LocalKnowledgeEngine()

    print("=" * 50)
    print("LOCAL KNOWLEDGE ENGINE TEST")
    print("=" * 50)

    # تست ۱: سلام
    print("\n📌 تست ۱: سلام")
    print(engine.answer("سلام"))

    # تست ۲: راهنمایی
    print("\n📌 تست ۲: راهنمایی")
    print(engine.answer("راهنمایی"))

    # تست ۳: پروژه
    print("\n📌 تست ۳: پروژه")
    print(engine.answer("پروژه چیست؟"))

    # تست ۴: سوال ناشناخته
    print("\n📌 تست ۴: سوال ناشناخته")
    print(engine.answer("هوا امروز چند درجه است؟"))

    # تست ۵: اضافه کردن پاسخ جدید
    print("\n📌 تست ۵: اضافه کردن پاسخ جدید")
    result = engine.add_fallback("هوا", "من اطلاعاتی درباره هوا ندارم. لطفاً از یک منبع خارجی استفاده کنید.")
    print(result["message"])
    print(engine.answer("هوا امروز چطور است؟"))