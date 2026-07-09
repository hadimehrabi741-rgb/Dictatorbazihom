# ==========================================
# BOUNDLESS AI
# MULTI LAYER ANALYZER v1
# SURFACE → HIDDEN → CODE
# ==========================================

class MultiLayerAnalyzer:

    def __init__(self, memory=None, eternal=None):
        self.memory = memory
        self.eternal = eternal

    def analyze(self, text, context=None):
        """
        تحلیل ورودی در ۳ لایه:
        - سطحی: ظاهر پیام
        - پنهان: نیت استراتژیک
        - بنیادین: کد و منطق پشت آن
        """

        text = str(text).strip()
        context = str(context) if context else ""

        # ===============================
        # LAYER 1: SURFACE
        # ===============================

        surface = {
            "raw": text,
            "length": len(text),
            "has_question": "?" in text or "؟" in text,
            "keywords": self._extract_keywords(text)
        }

        # ===============================
        # LAYER 2: HIDDEN (Strategic Intent)
        # ===============================

        hidden = {
            "intent": self._detect_hidden_intent(text),
            "urgency": self._detect_urgency(text),
            "emotion": self._detect_emotion(text)
        }

        # ===============================
        # LAYER 3: CODE (Fundamental Logic)
        # ===============================

        code = {
            "pattern": self._detect_pattern(text),
            "requires_memory": self._requires_memory(text),
            "requires_eternal": self._requires_eternal(text),
            "fallback_needed": self._fallback_needed(text)
        }

        return {
            "surface": surface,
            "hidden": hidden,
            "code": code
        }

    # ======================================
    # HELPERS
    # ======================================

    def _extract_keywords(self, text):
        keywords = ["پروژه", "حافظه", "معمار", "سیستم", "هوا", "سلام", "راهنمایی"]
        return [kw for kw in keywords if kw in text]

    def _detect_hidden_intent(self, text):
        if "حذف" in text or "پاک" in text:
            return "destructive"
        if "نمایش" in text or "ببین" in text:
            return "inquisitive"
        if "اضافه" in text or "ساخت" in text:
            return "constructive"
        return "neutral"

    def _detect_urgency(self, text):
        if "فوری" in text or "الان" in text:
            return "high"
        return "normal"

    def _detect_emotion(self, text):
        if "😡" in text or "!" in text:
            return "angry"
        if "🙏" in text or "ممنون" in text:
            return "grateful"
        return "neutral"

    def _detect_pattern(self, text):
        if "من" in text and "هستم" in text:
            return "identity_update"
        if "کی" in text and "هستم" in text:
            return "identity_query"
        if "علاقه" in text:
            return "preference"
        return "general"

    def _requires_memory(self, text):
        return any(word in text for word in ["کی هستم", "یادت هست", "قبلا"])

    def _requires_eternal(self, text):
        return any(word in text for word in ["درس", "الگو", "ساختار"])

    def _fallback_needed(self, text):
        return not any(word in text for word in ["پروژه", "حافظه", "معمار", "سیستم"])