# ==========================================
# BOUNDLESS AI
# ARCHITECT BRAIN v2.4
# FIXED DECISION LOGIC
# ==========================================

import re


class ArchitectBrain:

    def __init__(self, memory=None, manager=None, retrieval=None):

        self.memory = memory
        self.manager = manager
        self.retrieval = retrieval

    # ======================================
    # ANALYZE
    # ======================================

    def analyze(self, user_input):

        text = str(user_input).strip()

        result = {
            "input": text,
            "intent": "general",
            "confidence": 0,
            "needs_memory": False,
            "name": None
        }

        # ===============================
        # MEMORY IDENTITY
        # ===============================

        memory_questions = [
            "من کی هستم", "منو میشناسی", "یادت هست",
            "قبلا با هم صحبت کردیم", "قبلاً با هم صحبت کردیم",
            "قبلا ملاقات کردیم"
        ]

        for item in memory_questions:
            if item in text:
                result["intent"] = "memory_identity"
                result["needs_memory"] = True
                result["confidence"] = 0.95
                return result

        # ===============================
        # MEMORY SUMMARY
        # ===============================

        summary_questions = [
            "دیگه چی بهت گفتم", "دیگه چه چیزی گفتم",
            "چه چیزی از من یادت هست", "چی از من میدونی",
            "چه چیزهایی از من میدانی", "از من چی یادت مونده"
        ]

        for item in summary_questions:
            if item in text:
                result["intent"] = "memory_summary"
                result["needs_memory"] = True
                result["confidence"] = 0.95
                return result

        # ===============================
        # INTEREST
        # ===============================

        interest_questions = [
            "به چی علاقه دارم", "علایقم چیست", "چه چیزی دوست دارم"
        ]

        for item in interest_questions:
            if item in text:
                result["intent"] = "interest_question"
                result["needs_memory"] = True
                result["confidence"] = 0.95
                return result

        # ===============================
        # IDENTITY UPDATE
        # ===============================

        patterns = [
            r"من\s+(.+)\s+هستم",
            r"اسم\s+من\s+(.+)",
            r"نام\s+من\s+(.+)"
        ]

        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                result["intent"] = "identity_update"
                result["name"] = match.group(1).strip()
                result["confidence"] = 0.95
                return result

        # ===============================
        # PREFERENCE
        # ===============================

        if "علاقه دارم" in text or "دوست دارم" in text:
            result["intent"] = "preference"
            return result

        # ===============================
        # GENERAL (بدون حافظه)
        # ===============================

        return result

    # ======================================
    # DECISION (اصلاح‌شده)
    # ======================================

    def decide(self, user_input):

        analysis = self.analyze(user_input)
        result = {
            "handled": False,
            "answer": None,
            "analysis": analysis
        }

        intent = analysis["intent"]

        # ===============================
        # فقط در صورت نیاز به حافظه پاسخ بده
        # ===============================

        if intent == "memory_identity":
            result["handled"] = True
            result["answer"] = self.get_identity()
            return result

        if intent == "memory_summary":
            result["handled"] = True
            result["answer"] = self.get_memory_summary()
            return result

        if intent == "interest_question":
            result["handled"] = True
            result["answer"] = self.get_interest()
            return result

        if intent == "identity_update":
            self.save_identity(analysis["name"])
            result["handled"] = True
            result["answer"] = "خوش آمدی " + analysis["name"] + "."
            return result

        # ===============================
        # اگر نیاز به حافظه نبود، از GROQ یا Local استفاده کن
        # ===============================

        return result

    # ======================================
    # MEMORY READER
    # ======================================

    def read_memory(self):

        text = ""

        try:
            if self.retrieval:
                text += str(self.retrieval.get_context())
        except:
            pass

        try:
            if self.memory:
                text += str(self.memory.get_context())
        except:
            pass

        return text

    # ======================================
    # IDENTITY
    # ======================================

    def get_identity(self):

        data = self.read_memory()

        if "حامد" in data:
            return "تو حامد هستی."

        return "من اطلاعات کافی از هویت تو در حافظه Σ ندارم."

    # ======================================
    # INTEREST
    # ======================================

    def get_interest(self):

        data = self.read_memory()

        if "برنامه نویسی" in data or "برنامه‌نویسی" in data:
            return "تو به برنامه نویسی علاقه داری."

        return "علاقه ثبت شده‌ای در حافظه Σ پیدا نکردم."

    # ======================================
    # SUMMARY
    # ======================================

    def get_memory_summary(self):

        try:
            if self.retrieval:
                result = self.retrieval.summary()
                if result:
                    return "در حافظه Σ:\n" + result
        except Exception:
            pass

        return "اطلاعات کافی در حافظه Σ ندارم."

    # ======================================
    # SAVE IDENTITY
    # ======================================

    def save_identity(self, name):

        try:
            if self.manager:
                self.manager.store(
                    "سلام من " + name + " هستم",
                    "ثبت هویت"
                )
                return True
        except:
            pass

        return False