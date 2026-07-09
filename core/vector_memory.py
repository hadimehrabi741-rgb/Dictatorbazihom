# ==========================================
# BOUNDLESS AI
# VECTOR MEMORY v2
# NO NUMPY - PURE PYTHON
# ==========================================

import os
import json
import math
from datetime import datetime


class VectorMemory:

    def __init__(self, memory=None):
        self.memory = memory
        self.vector_file = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "storage",
            "vectors",
            "embeddings.json"
        )
        self._ensure_vector_file()

    def _ensure_vector_file(self):
        os.makedirs(os.path.dirname(self.vector_file), exist_ok=True)
        if not os.path.exists(self.vector_file):
            with open(self.vector_file, "w") as f:
                json.dump({"vectors": [], "metadata": []}, f, indent=4)

    def _load_vectors(self):
        with open(self.vector_file, "r") as f:
            return json.load(f)

    def _save_vectors(self, data):
        with open(self.vector_file, "w") as f:
            json.dump(data, f, indent=4)

    def _text_to_vector(self, text):
        """تبدیل متن به بردار ساده (بدون numpy)"""
        words = text.split()
        vector = [0.0] * 50
        for i, word in enumerate(words):
            if i < 50:
                vector[i] = len(word) / 10.0
        return vector

    def _cosine_similarity(self, vec1, vec2):
        """محاسبه شباهت کسینوسی (بدون numpy)"""
        if len(vec1) != len(vec2):
            return 0

        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        norm1 = math.sqrt(sum(a * a for a in vec1))
        norm2 = math.sqrt(sum(b * b for b in vec2))

        if norm1 == 0 or norm2 == 0:
            return 0

        return dot_product / (norm1 * norm2)

    def add_memory(self, text, metadata=None):
        """اضافه کردن یک حافظه به فهرست وکتوری"""
        vector = self._text_to_vector(text)
        data = self._load_vectors()

        data["vectors"].append(vector)
        data["metadata"].append({
            "text": text,
            "metadata": metadata or {},
            "timestamp": str(datetime.now()),
            "id": len(data["vectors"]) - 1
        })

        self._save_vectors(data)
        return {"success": True, "id": len(data["vectors"]) - 1}

    def search(self, query, top_k=5):
        """جستجوی معنایی در حافظه وکتوری"""
        query_vector = self._text_to_vector(query)
        data = self._load_vectors()

        if not data["vectors"]:
            return []

        similarities = []
        for i, vec in enumerate(data["vectors"]):
            sim = self._cosine_similarity(query_vector, vec)
            similarities.append((i, sim))

        similarities.sort(key=lambda x: x[1], reverse=True)
        top_results = similarities[:top_k]

        results = []
        for idx, score in top_results:
            results.append({
                "id": idx,
                "text": data["metadata"][idx]["text"],
                "metadata": data["metadata"][idx]["metadata"],
                "similarity": round(score, 4),
                "timestamp": data["metadata"][idx]["timestamp"]
            })

        return results

    def get_all(self):
        """دریافت همه حافظه‌های وکتوری"""
        data = self._load_vectors()
        return data["metadata"]

    def get_stats(self):
        """آمار حافظه وکتوری"""
        data = self._load_vectors()
        return {
            "total_vectors": len(data["vectors"]),
            "total_metadata": len(data["metadata"]),
            "last_update": data["metadata"][-1]["timestamp"] if data["metadata"] else None
        }

    def reset(self):
        """بازنشانی حافظه وکتوری"""
        self._save_vectors({"vectors": [], "metadata": []})
        return {"success": True, "message": "حافظه وکتوری بازنشانی شد."}