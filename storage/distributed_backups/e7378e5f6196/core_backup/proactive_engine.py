# ==========================================
# BOUNDLESS AI
# PROACTIVE ENGINE v1
# 3 SCENARIO PREDICTION
# ==========================================

class ProactiveEngine:

    def __init__(self, memory=None):
        self.memory = memory

    def predict(self, user_input):
        """
        پیش‌بینی ۳ سناریو بر اساس ورودی کاربر
        """

        text = str(user_input).strip()

        scenarios = {
            "سلام": {
                "scenario_1": "کاربر قصد شروع مکالمه دارد → پاسخ خوشامدگویی مناسب.",
                "scenario_2": "کاربر ممکن است نیاز به راهنمایی داشته باشد → ارائه منو.",
                "scenario_3": "کاربر در حال تست سیستم است → پاسخ ساده و سریع."
            },
            "پروژه": {
                "scenario_1": "کاربر می‌خواهد بداند پروژه چیست → توضیح مختصر.",
                "scenario_2": "کاربر به دنبال مستندات است → ارجاع به فایل‌ها.",
                "scenario_3": "کاربر قصد توسعه دارد → پیشنهاد افزودن ماژول جدید."
            },
            "حافظه": {
                "scenario_1": "کاربر می‌خواهد حافظه را ببیند → نمایش Σ.",
                "scenario_2": "کاربر می‌خواهد حافظه را پاک کند → درخواست تأیید.",
                "scenario_3": "کاربر به دنبال بازیابی اطلاعات است → جستجو در Σ."
            }
        }

        for key, value in scenarios.items():
            if key in text:
                return {
                    "input": text,
                    "scenario_1": value["scenario_1"],
                    "scenario_2": value["scenario_2"],
                    "scenario_3": value["scenario_3"]
                }

        return {
            "input": text,
            "scenario_1": "کاربر در حال پرسش عمومی است → پاسخ از LOCAL KNOWLEDGE.",
            "scenario_2": "کاربر ممکن است به راهنمایی نیاز داشته باشد → پیشنهاد منو.",
            "scenario_3": "کاربر در حال آزمایش سیستم است → پاسخ پیش‌فرض."
        }

    def get_preventative_strategies(self, user_input):
        """
        ارائه راهکارهای پیشگیرانه برای هر سناریو
        """

        prediction = self.predict(user_input)

        strategies = {
            "scenario_1": "پاسخ مستقیم و مفید.",
            "scenario_2": "ارائه گزینه‌های بیشتر.",
            "scenario_3": "ثبت درخواست برای تحلیل بعدی."
        }

        result = {}
        for key in ["scenario_1", "scenario_2", "scenario_3"]:
            result[key] = {
                "prediction": prediction.get(key, ""),
                "strategy": strategies.get(key, "پاسخ پیش‌فرض.")
            }

        return result