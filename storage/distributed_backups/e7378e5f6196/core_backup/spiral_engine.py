# ==========================================
# BOUNDLESS AI
# SPIRAL ENGINE v1
# VOID → N → O → Hadi → VOID'
# ==========================================

from datetime import datetime
import uuid


class SpiralEngine:

    def __init__(self, memory=None, eternal=None, value_engine=None):

        self.memory = memory
        self.eternal = eternal
        self.value_engine = value_engine
        self.spirals = []
        self.current_spiral = None
        self.spiral_count = 0

    # ======================================
    # CREATE SPIRAL
    # ======================================

    def create_spiral(self, input_data, context=None):

        """
        ایجاد یک چرخه جدید از Void → N → O → Hadi
        """

        self.spiral_count += 1

        spiral = {
            "id": f"SPIRAL_{self.spiral_count}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "number": self.spiral_count,
            "void": {
                "input": input_data,
                "context": context,
                "timestamp": str(datetime.now())
            },
            "n": None,
            "o": None,
            "hadi": None,
            "next_void": None,
            "completed": False,
            "timestamp": str(datetime.now())
        }

        self.spirals.append(spiral)
        self.current_spiral = spiral

        return spiral

    # ======================================
    # PROCESS N
    # ======================================

    def process_n(self, processed_data):

        """
        مرحله N: پردازش ورودی
        """

        if not self.current_spiral:
            return None

        self.current_spiral["n"] = {
            "data": processed_data,
            "timestamp": str(datetime.now())
        }

        return self.current_spiral

    # ======================================
    # PROCESS O
    # ======================================

    def process_o(self, operation_result):

        """
        مرحله O: عملیات و تحلیل
        """

        if not self.current_spiral:
            return None

        self.current_spiral["o"] = {
            "data": operation_result,
            "timestamp": str(datetime.now())
        }

        return self.current_spiral

    # ======================================
    # PROCESS HADI
    # ======================================

    def process_hadi(self, output):

        """
        مرحله Hadi: خروجی و جهت بهبود
        """

        if not self.current_spiral:
            return None

        self.current_spiral["hadi"] = {
            "data": output,
            "timestamp": str(datetime.now())
        }

        self.current_spiral["completed"] = True

        # ذخیره در Eternal
        if self.eternal:
            self.eternal.store_lesson(
                f"Spiral {self.current_spiral['number']}: {output[:100]}...",
                "spiral"
            )

        return self.current_spiral

    # ======================================
    # CREATE NEXT VOID
    # ======================================

    def create_next_void(self):

        """
        ایجاد Void جدید از Hadi فعلی
        """

        if not self.current_spiral or not self.current_spiral["completed"]:
            return None

        hadi = self.current_spiral["hadi"]["data"]

        # استخراج سوال یا ایده جدید از Hadi
        next_input = self._extract_next_void(hadi)

        if not next_input:
            next_input = f"بر اساس پاسخ قبلی: {hadi[:100]}..."

        self.current_spiral["next_void"] = {
            "input": next_input,
            "timestamp": str(datetime.now())
        }

        return self.current_spiral

    # ======================================
    # EXTRACT NEXT VOID
    # ======================================

    def _extract_next_void(self, hadi):

        # استخراج سوال جدید
        if "?" in hadi or "؟" in hadi:
            parts = hadi.split("?")
            if len(parts) > 1:
                return parts[1].strip()[:100]

        # استخراج ایده جدید
        if any(word in hadi for word in ["ایده", "پیشنهاد", "راه"]):
            for word in ["ایده", "پیشنهاد", "راه"]:
                if word in hadi:
                    parts = hadi.split(word)
                    if len(parts) > 1:
                        return f"{word}: {parts[1].strip()[:100]}"

        return None

    # ======================================
    # NEXT SPIRAL
    # ======================================

    def next_spiral(self):

        """
        حرکت به چرخه بعدی
        """

        if not self.current_spiral:
            return None

        # ایجاد Void جدید
        self.create_next_void()

        # شروع چرخه جدید
        if self.current_spiral["next_void"]:
            new_input = self.current_spiral["next_void"]["input"]
            return self.create_spiral(new_input)

        return None

    # ======================================
    # GET SPIRAL
    # ======================================

    def get_spiral(self, spiral_id):

        for spiral in self.spirals:
            if spiral["id"] == spiral_id:
                return spiral
        return None

    # ======================================
    # GET HISTORY
    # ======================================

    def get_history(self, limit=10):

        return self.spirals[-limit:]

    # ======================================
    # GET STATS
    # ======================================

    def get_stats(self):

        total = len(self.spirals)

        if total == 0:
            return {
                "total_spirals": 0,
                "completed": 0,
                "next_voids": 0,
                "completion_rate": 0
            }

        completed = sum(1 for s in self.spirals if s["completed"])
        next_voids = sum(1 for s in self.spirals if s["next_void"])

        return {
            "total_spirals": total,
            "completed": completed,
            "next_voids": next_voids,
            "completion_rate": round(completed / total * 100, 2)
        }

    # ======================================
    # VISUALIZE
    # ======================================

    def visualize(self, spiral_id=None):

        if spiral_id:
            spiral = self.get_spiral(spiral_id)
            if not spiral:
                return "Spiral not found"
            spirals = [spiral]
        else:
            spirals = self.spirals[-5:]

        result = "🔄 SPIRAL EVOLUTION:\n\n"

        for i, spiral in enumerate(spirals):
            result += f"--- SPIRAL {spiral['number']} ---\n"
            result += f"Void: {spiral['void']['input'][:50]}...\n"
            if spiral["n"]:
                result += f"  → N: پردازش شد\n"
            if spiral["o"]:
                result += f"  → O: عملیات انجام شد\n"
            if spiral["hadi"]:
                result += f"  → Hadi: {spiral['hadi']['data'][:50]}...\n"
            if spiral["next_void"]:
                result += f"  → Void': {spiral['next_void']['input'][:50]}...\n"
            result += f"Status: {'✅ کامل' if spiral['completed'] else '⏳ در حال پردازش'}\n\n"

        return result


# ==========================================
# TEST
# ==========================================

if __name__ == "__main__":

    engine = SpiralEngine()

    print("=" * 50)
    print("SPIRAL ENGINE TEST")
    print("=" * 50)

    # تست ۱: ایجاد Spiral
    print("\n📌 تست ۱: ایجاد Spiral جدید")
    spiral = engine.create_spiral("چگونه می‌توانم پروژه را بهبود دهم؟")
    print(f"Spiral ID: {spiral['id']}")

    # تست ۲: مراحل
    print("\n📌 تست ۲: پردازش مراحل")
    engine.process_n("تحلیل ورودی")
    engine.process_o("عملیات پردازش")
    engine.process_hadi("از حافظه Σ و معماری سه‌لایه استفاده کن. این کار باعث بهبود عملکرد می‌شود.")
    print(f"کامل شد: {spiral['completed']}")

    # تست ۳: ایجاد Void بعدی
    print("\n📌 تست ۳: ایجاد Void جدید")
    engine.create_next_void()
    print(f"Void بعدی: {spiral['next_void']['input']}")

    # تست ۴: Spiral بعدی
    print("\n📌 تست ۴: حرکت به Spiral بعدی")
    next_spiral = engine.next_spiral()
    if next_spiral:
        print(f"Spiral جدید: {next_spiral['id']}")
        print(f"ورودی: {next_spiral['void']['input']}")

    # تست ۵: نمایش
    print("\n📌 تست ۵: نمایش Spiral")
    print(engine.visualize())

    # آمار
    print("\n📌 آمار:")
    stats = engine.get_stats()
    print(f"- کل Spiral‌ها: {stats['total_spirals']}")
    print(f"- تکمیل شده: {stats['completed']}")
    print(f"- نرخ تکمیل: {stats['completion_rate']}%")