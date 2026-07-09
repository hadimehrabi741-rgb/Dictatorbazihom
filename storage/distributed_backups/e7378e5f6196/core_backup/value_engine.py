# ==========================================
# BOUNDLESS AI
# VALUE ENGINE v1
# EVALUATE, PRIORITIZE, OPTIMIZE
# ==========================================

from datetime import datetime


class ValueEngine:

    def __init__(self, memory=None, eternal=None):

        self.memory = memory
        self.eternal = eternal
        self.history = []

    # ======================================
    # EVALUATE
    # ======================================

    def evaluate(self, candidate, context=None):

        """
        ارزیابی یک مسیر یا پاسخ بر اساس معیارهای ارزش
        """

        result = {
            "candidate": candidate,
            "context": context,
            "score": 0,
            "breakdown": {},
            "timestamp": str(datetime.now())
        }

        # ===============================
        # 1. ارزش دانش
        # ===============================

        knowledge_score = self._score_knowledge(candidate)
        result["breakdown"]["knowledge"] = knowledge_score

        # ===============================
        # 2. ارزش انسجام
        # ===============================

        coherence_score = self._score_coherence(candidate)
        result["breakdown"]["coherence"] = coherence_score

        # ===============================
        # 3. ارزش عملی
        # ===============================

        practical_score = self._score_practical(candidate)
        result["breakdown"]["practical"] = practical_score

        # ===============================
        # 4. ارزش نوآوری
        # ===============================

        novelty_score = self._score_novelty(candidate)
        result["breakdown"]["novelty"] = novelty_score

        # ===============================
        # 5. ارزش کشف
        # ===============================

        discovery_score = self._score_discovery(candidate)
        result["breakdown"]["discovery"] = discovery_score

        # ===============================
        # 6. امتیاز نهایی
        # ===============================

        total_score = (
            knowledge_score * 0.3 +
            coherence_score * 0.25 +
            practical_score * 0.2 +
            novelty_score * 0.15 +
            discovery_score * 0.1
        )

        result["score"] = round(total_score, 3)

        # ===============================
        # 7. ذخیره در تاریخچه
        # ===============================

        self.history.append(result)
        if len(self.history) > 100:
            self.history = self.history[-100:]

        return result

    # ======================================
    # COMPARE
    # ======================================

    def compare(self, candidates, context=None):

        """
        مقایسه چند مسیر و انتخاب بهترین
        """

        results = []
        for candidate in candidates:
            result = self.evaluate(candidate, context)
            results.append(result)

        # مرتب‌سازی بر اساس امتیاز
        results.sort(key=lambda x: x["score"], reverse=True)

        return {
            "best": results[0] if results else None,
            "ranking": results,
            "context": context
        }

    # ======================================
    # SCORE KNOWLEDGE
    # ======================================

    def _score_knowledge(self, text):

        score = 0

        # اطلاعات جدید
        if any(word in text for word in ["یاد گرفتم", "کشف کردم", "متوجه شدم"]):
            score += 0.4

        # اطلاعات تخصصی
        if any(word in text for word in ["معماری", "سیستم", "الگوریتم", "هوش مصنوعی"]):
            score += 0.3

        # جزئیات
        if len(text) > 100:
            score += 0.3

        return min(score, 1.0)

    # ======================================
    # SCORE COHERENCE
    # ======================================

    def _score_coherence(self, text):

        score = 0

        # ساختار منطقی
        if any(word in text for word in ["اول", "دوم", "سوم", "نهایتاً", "بنابراین"]):
            score += 0.3

        # نتیجه‌گیری
        if any(word in text for word in ["پس", "در نتیجه", "بنابراین"]):
            score += 0.3

        # طول مناسب
        if 30 <= len(text) <= 500:
            score += 0.2

        # بدون تناقض ظاهری
        if not any(word in text for word in ["اما", "ولی"] for _ in range(3)):
            score += 0.2

        return min(score, 1.0)

    # ======================================
    # SCORE PRACTICAL
    # ======================================

    def _score_practical(self, text):

        score = 0

        # راهکار عملی
        if any(word in text for word in ["می‌توانی", "روش", "راه", "استفاده کن"]):
            score += 0.4

        # قابل اجرا
        if any(word in text for word in ["کد", "فایل", "دستور", "مسیر"]):
            score += 0.3

        # مختصر و مفید
        if 20 <= len(text) <= 200:
            score += 0.3

        return min(score, 1.0)

    # ======================================
    # SCORE NOVELTY
    # ======================================

    def _score_novelty(self, text):

        score = 0

        # ایده جدید
        if any(word in text for word in ["جدید", "خلاقانه", "نوآورانه"]):
            score += 0.4

        # سوال جدید
        if "?" in text or "؟" in text:
            score += 0.3

        # رویکرد جدید
        if any(word in text for word in ["رویکرد", "روش جدید", "شیوه"]):
            score += 0.3

        return min(score, 1.0)

    # ======================================
    # SCORE DISCOVERY
    # ======================================

    def _score_discovery(self, text):

        score = 0

        # کشف
        if any(word in text for word in ["کشف", "یافته", "دریافتم"]):
            score += 0.5

        # بینش
        if any(word in text for word in ["بینش", "درک", "فهم"]):
            score += 0.3

        # ارتباط جدید
        if any(word in text for word in ["ارتباط", "رابطه", "پیوند"]):
            score += 0.2

        return min(score, 1.0)

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
                "total_evaluations": 0,
                "average_score": 0,
                "best_score": 0,
                "worst_score": 0
            }

        scores = [h["score"] for h in self.history]

        return {
            "total_evaluations": total,
            "average_score": round(sum(scores) / total, 3),
            "best_score": max(scores),
            "worst_score": min(scores)
        }


# ==========================================
# TEST
# ==========================================

if __name__ == "__main__":

    engine = ValueEngine()

    print("=" * 50)
    print("VALUE ENGINE TEST")
    print("=" * 50)

    # تست ۱: پاسخ با ارزش بالا
    print("\n📌 تست ۱: پاسخ با ارزش بالا")
    result = engine.evaluate(
        "من یاد گرفتم که استفاده از حافظه Σ و معماری سه‌لایه باعث بهبود کیفیت پاسخ‌ها می‌شود. برای این کار می‌توانی از متدهای جدید استفاده کنی."
    )
    print(f"امتیاز: {result['score']}")
    print(f"جزئیات: {result['breakdown']}")

    # تست ۲: پاسخ ساده
    print("\n📌 تست ۲: پاسخ ساده")
    result = engine.evaluate(
        "بله، پروژه کامل است."
    )
    print(f"امتیاز: {result['score']}")

    # تست ۳: مقایسه
    print("\n📌 تست ۳: مقایسه ۳ پاسخ")
    comparison = engine.compare([
        "بله.",
        "بله، پروژه کامل است و شامل حافظه Σ و معمار است.",
        "من یاد گرفتم که معماری سه‌لایه باعث بهبود عملکرد می‌شود. می‌توانی از متدهای جدید برای بهینه‌سازی استفاده کنی."
    ])
    print(f"بهترین امتیاز: {comparison['best']['score']}")
    print(f"بهترین پاسخ: {comparison['best']['candidate'][:50]}...")

    # آمار
    print("\n📌 آمار:")
    stats = engine.get_stats()
    print(f"- کل ارزیابی‌ها: {stats['total_evaluations']}")
    print(f"- میانگین امتیاز: {stats['average_score']}")
    print(f"- بهترین امتیاز: {stats['best_score']}")