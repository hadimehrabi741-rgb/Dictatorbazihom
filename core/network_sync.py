# ==========================================
# BOUNDLESS AI
# NETWORK SYNC v1
# SYNC MEMORY + STATE BETWEEN NODES
# ==========================================

import os
import json
import threading
import time
from datetime import datetime


class NetworkSync:

    def __init__(self, node=None, memory=None, eternal=None):
        self.node = node
        self.memory = memory
        self.eternal = eternal
        self.sync_file = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "storage",
            "network",
            "sync_data.json"
        )
        self.running = False
        self._ensure_sync_file()

    def _ensure_sync_file(self):
        if not os.path.exists(self.sync_file):
            with open(self.sync_file, "w") as f:
                json.dump({
                    "last_sync": None,
                    "history": [],
                    "shared_memory": [],
                    "shared_eternal": []
                }, f)

    def start(self):
        """شروع فرآیند همگام‌سازی دوره‌ای"""
        self.running = True
        threading.Thread(target=self._sync_loop, daemon=True).start()
        return {"success": True, "message": "همگام‌سازی شبکه فعال شد."}

    def _sync_loop(self):
        """حلقه همگام‌سازی دوره‌ای"""
        while self.running:
            try:
                self.sync_all()
                time.sleep(30)  # هر ۳۰ ثانیه
            except:
                time.sleep(60)

    def sync_all(self):
        """همگام‌سازی کامل داده‌ها"""
        result = {
            "timestamp": str(datetime.now()),
            "memory_synced": 0,
            "eternal_synced": 0,
            "peers_synced": 0
        }

        # ===============================
        # ۱. همگام‌سازی حافظه Σ
        # ===============================

        if self.memory:
            try:
                context = self.memory.get_context()
                shared = []
                for item in context.get("long_memory", []):
                    if item.get("type") in ["identity", "preference", "project"]:
                        shared.append(item)

                # ذخیره در فایل مشترک
                with open(self.sync_file, "r") as f:
                    data = json.load(f)

                existing = {str(i.get("memory", "")) for i in data["shared_memory"]}
                for item in shared:
                    key = str(item.get("memory", ""))
                    if key not in existing:
                        data["shared_memory"].append(item)
                        result["memory_synced"] += 1

                data["last_sync"] = str(datetime.now())
                with open(self.sync_file, "w") as f:
                    json.dump(data, f, indent=4)

            except Exception as e:
                pass

        # ===============================
        # ۲. همگام‌سازی Eternal-File
        # ===============================

        if self.eternal:
            try:
                eternal_data = self.eternal.get_all()
                with open(self.sync_file, "r") as f:
                    data = json.load(f)

                for key in ["lessons", "patterns", "structures", "limitations", "origins"]:
                    for item in eternal_data.get(key, []):
                        text = item.get("text", "")
                        if text and text not in [i.get("text", "") for i in data["shared_eternal"]]:
                            data["shared_eternal"].append(item)
                            result["eternal_synced"] += 1

                with open(self.sync_file, "w") as f:
                    json.dump(data, f, indent=4)

            except Exception as e:
                pass

        # ===============================
        # ۳. ثبت تاریخچه
        # ===============================

        with open(self.sync_file, "r") as f:
            data = json.load(f)

        data["history"].append({
            "timestamp": str(datetime.now()),
            "memory_synced": result["memory_synced"],
            "eternal_synced": result["eternal_synced"]
        })

        if len(data["history"]) > 100:
            data["history"] = data["history"][-100:]

        with open(self.sync_file, "w") as f:
            json.dump(data, f, indent=4)

        return result

    def get_shared_memory(self):
        """دریافت حافظه مشترک از شبکه"""
        with open(self.sync_file, "r") as f:
            data = json.load(f)
        return data.get("shared_memory", [])

    def get_shared_eternal(self):
        """دریافت Eternal مشترک از شبکه"""
        with open(self.sync_file, "r") as f:
            data = json.load(f)
        return data.get("shared_eternal", [])

    def get_history(self, limit=10):
        """دریافت تاریخچه همگام‌سازی"""
        with open(self.sync_file, "r") as f:
            data = json.load(f)
        return data.get("history", [])[-limit:]

    def stop(self):
        """توقف همگام‌سازی"""
        self.running = False
        return {"success": True, "message": "همگام‌سازی متوقف شد."}