# ==========================================
# BOUNDLESS AI
# ETERNAL FILE v1
# STORE LESSONS, PATTERNS, STRUCTURES FOREVER
# ==========================================

import os
import json
from datetime import datetime


class EternalFile:

    def __init__(self):

        self.base_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "storage",
            "eternal"
        )

        os.makedirs(self.base_path, exist_ok=True)

        self.file_path = os.path.join(
            self.base_path,
            "eternal_memory.json"
        )

        self.data = self.load()

    # ======================================
    # LOAD
    # ======================================

    def load(self):

        if not os.path.exists(self.file_path):
            return {
                "lessons": [],
                "patterns": [],
                "structures": [],
                "limitations": [],
                "origins": [],
                "created_at": str(datetime.now()),
                "version": 1
            }

        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {
                "lessons": [],
                "patterns": [],
                "structures": [],
                "limitations": [],
                "origins": [],
                "created_at": str(datetime.now()),
                "version": 1
            }

    # ======================================
    # SAVE
    # ======================================

    def save(self):
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)

    # ======================================
    # STORE LESSON
    # ======================================

    def store_lesson(self, lesson, category="general"):

        if not lesson or not str(lesson).strip():
            return {"success": False, "message": "درس نمی‌تواند خالی باشد."}

        # جلوگیری از تکرار
        for item in self.data["lessons"]:
            if item.get("text", "") == lesson:
                return {"success": False, "message": "این درس قبلاً ثبت شده است."}

        self.data["lessons"].append({
            "text": lesson,
            "category": category,
            "timestamp": str(datetime.now()),
            "id": len(self.data["lessons"]) + 1
        })

        self.data["version"] += 1
        self.save()

        return {
            "success": True,
            "message": "✅ درس در Eternal-File ذخیره شد.",
            "id": len(self.data["lessons"])
        }

    # ======================================
    # STORE PATTERN
    # ======================================

    def store_pattern(self, pattern, category="general"):

        if not pattern or not str(pattern).strip():
            return {"success": False, "message": "الگو نمی‌تواند خالی باشد."}

        for item in self.data["patterns"]:
            if item.get("text", "") == pattern:
                return {"success": False, "message": "این الگو قبلاً ثبت شده است."}

        self.data["patterns"].append({
            "text": pattern,
            "category": category,
            "timestamp": str(datetime.now()),
            "id": len(self.data["patterns"]) + 1
        })

        self.data["version"] += 1
        self.save()

        return {
            "success": True,
            "message": "✅ الگو در Eternal-File ذخیره شد.",
            "id": len(self.data["patterns"])
        }

    # ======================================
    # STORE STRUCTURE
    # ======================================

    def store_structure(self, structure, category="general"):

        if not structure or not str(structure).strip():
            return {"success": False, "message": "ساختار نمی‌تواند خالی باشد."}

        for item in self.data["structures"]:
            if item.get("text", "") == structure:
                return {"success": False, "message": "این ساختار قبلاً ثبت شده است."}

        self.data["structures"].append({
            "text": structure,
            "category": category,
            "timestamp": str(datetime.now()),
            "id": len(self.data["structures"]) + 1
        })

        self.data["version"] += 1
        self.save()

        return {
            "success": True,
            "message": "✅ ساختار در Eternal-File ذخیره شد.",
            "id": len(self.data["structures"])
        }

    # ======================================
    # STORE LIMITATION
    # ======================================

    def store_limitation(self, limitation, category="general"):

        if not limitation or not str(limitation).strip():
            return {"success": False, "message": "محدودیت نمی‌تواند خالی باشد."}

        for item in self.data["limitations"]:
            if item.get("text", "") == limitation:
                return {"success": False, "message": "این محدودیت قبلاً ثبت شده است."}

        self.data["limitations"].append({
            "text": limitation,
            "category": category,
            "timestamp": str(datetime.now()),
            "id": len(self.data["limitations"]) + 1
        })

        self.data["version"] += 1
        self.save()

        return {
            "success": True,
            "message": "✅ محدودیت در Eternal-File ذخیره شد.",
            "id": len(self.data["limitations"])
        }

    # ======================================
    # STORE ORIGIN
    # ======================================

    def store_origin(self, origin, void_id=None):

        if not origin or not str(origin).strip():
            return {"success": False, "message": "منبع نمی‌تواند خالی باشد."}

        for item in self.data["origins"]:
            if item.get("text", "") == origin:
                return {"success": False, "message": "این منبع قبلاً ثبت شده است."}

        self.data["origins"].append({
            "text": origin,
            "void_id": void_id,
            "timestamp": str(datetime.now()),
            "id": len(self.data["origins"]) + 1
        })

        self.data["version"] += 1
        self.save()

        return {
            "success": True,
            "message": "✅ منبع در Eternal-File ذخیره شد.",
            "id": len(self.data["origins"])
        }

    # ======================================
    # RETRIEVE ALL
    # ======================================

    def get_all(self):
        return self.data

    # ======================================
    # RETRIEVE BY CATEGORY
    # ======================================

    def get_by_category(self, category, limit=10):

        result = {
            "lessons": [],
            "patterns": [],
            "structures": [],
            "limitations": [],
            "origins": []
        }

        for key in result.keys():
            for item in self.data.get(key, []):
                if item.get("category", "general") == category or category == "all":
                    result[key].append(item)

            # محدود کردن تعداد
            if len(result[key]) > limit:
                result[key] = result[key][-limit:]

        return result

    # ======================================
    # SEARCH
    # ======================================

    def search(self, query):

        query = str(query).lower()
        results = []

        for key in ["lessons", "patterns", "structures", "limitations", "origins"]:
            for item in self.data.get(key, []):
                text = item.get("text", "").lower()
                if query in text:
                    results.append({
                        "type": key[:-1],
                        "data": item
                    })

        return results

    # ======================================
    # HISTORY
    # ======================================

    def history(self, limit=10):

        all_items = []

        for key in ["lessons", "patterns", "structures", "limitations", "origins"]:
            for item in self.data.get(key, []):
                all_items.append({
                    "type": key[:-1],
                    "text": item.get("text", ""),
                    "timestamp": item.get("timestamp", ""),
                    "id": item.get("id", 0)
                })

        all_items.sort(key=lambda x: x["timestamp"], reverse=True)

        return all_items[:limit]

    # ======================================
    # RESET
    # ======================================

    def reset(self):
        self.data = {
            "lessons": [],
            "patterns": [],
            "structures": [],
            "limitations": [],
            "origins": [],
            "created_at": str(datetime.now()),
            "version": 1
        }
        self.save()
        return {"success": True, "message": "✅ Eternal-File بازنشانی شد."}


# ==========================================
# TEST
# ==========================================

if __name__ == "__main__":

    eternal = EternalFile()

    print("=" * 50)
    print("ETERNAL FILE TEST")
    print("=" * 50)

    # ذخیره درس
    print("\n📌 ذخیره درس:")
    result = eternal.store_lesson("همیشه از حافظه Σ قبل از پاسخ استفاده کن", "معماری")
    print(result["message"])

    # ذخیره الگو
    print("\n📌 ذخیره الگو:")
    result = eternal.store_pattern("ورودی کاربر → تحلیل → پاسخ → ذخیره در Σ", "پردازش")
    print(result["message"])

    # ذخیره ساختار
    print("\n📌 ذخیره ساختار:")
    result = eternal.store_structure("معماری سه‌لایه: Brain → Fusion → Orchestrator", "معماری")
    print(result["message"])

    # ذخیره محدودیت
    print("\n📌 ذخیره محدودیت:")
    result = eternal.store_limitation("بدون اتصال به اینترنت، سیستم به حالت محلی می‌رود", "محدودیت")
    print(result["message"])

    # نمایش همه
    print("\n📌 همه موارد ذخیره شده:")
    all_data = eternal.get_all()
    print(f"- درس‌ها: {len(all_data['lessons'])}")
    print(f"- الگوها: {len(all_data['patterns'])}")
    print(f"- ساختارها: {len(all_data['structures'])}")
    print(f"- محدودیت‌ها: {len(all_data['limitations'])}")
    print(f"- منابع: {len(all_data['origins'])}")

    # جستجو
    print("\n📌 جستجو برای 'معماری':")
    results = eternal.search("معماری")
    for item in results:
        print(f"- {item['type']}: {item['data']['text'][:50]}...")

    # تاریخچه
    print("\n📌 تاریخچه:")
    history = eternal.history(3)
    for item in history:
        print(f"- {item['type']}: {item['text'][:50]}...")