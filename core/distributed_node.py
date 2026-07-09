# ==========================================
# BOUNDLESS AI
# DISTRIBUTED NODE v1
# SELF-CONTAINED NETWORK NODE
# ==========================================

import os
import json
import socket
import threading
import time
from datetime import datetime
import uuid


class DistributedNode:

    def __init__(self, node_id=None, hub_host=None, hub_port=9000):
        self.node_id = node_id or str(uuid.uuid4())[:8]
        self.hub_host = hub_host or "127.0.0.1"
        self.hub_port = hub_port
        self.peers = []
        self.running = False
        self.node_data = {
            "id": self.node_id,
            "status": "initializing",
            "last_seen": str(datetime.now()),
            "capabilities": ["chat", "memory", "proactive", "obfuscation"]
        }
        self.sync_queue = []
        self._ensure_storage()

    def _ensure_storage(self):
        path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "storage",
            "network"
        )
        os.makedirs(path, exist_ok=True)
        self.peer_file = os.path.join(path, "peers.json")
        self.node_file = os.path.join(path, f"node_{self.node_id}.json")
        self._save_node_data()

    def _save_node_data(self):
        with open(self.node_file, "w") as f:
            json.dump(self.node_data, f, indent=4)

    def start(self):
        """راه‌اندازی نمونه به‌عنوان یک گره شبکه"""
        self.running = True
        self.node_data["status"] = "active"
        self.node_data["started_at"] = str(datetime.now())
        self._save_node_data()

        # شروع ترد گوش‌دهنده
        threading.Thread(target=self._listener, daemon=True).start()

        return {
            "success": True,
            "node_id": self.node_id,
            "status": self.node_data["status"]
        }

    def _listener(self):
        """گوش‌دهی به درخواست‌های همگام‌سازی"""
        while self.running:
            try:
                # در این نسخه ساده، فقط از فایل peers می‌خواند
                time.sleep(10)
                self._sync_with_peers()
            except Exception as e:
                pass

    def _sync_with_peers(self):
        """همگام‌سازی با همسایه‌ها"""
        peers = self.get_peers()
        for peer in peers:
            try:
                # اتصال به همسایه و دریافت وضعیت
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(5)
                    s.connect((peer["host"], peer["port"]))
                    s.sendall(b"STATUS_REQ")
                    data = s.recv(1024)
                    if data:
                        # پردازش داده دریافتی
                        self.sync_queue.append({
                            "from": peer["id"],
                            "data": data.decode(),
                            "timestamp": str(datetime.now())
                        })
            except:
                pass

    def register_peer(self, peer_id, host, port):
        """ثبت یک همسایه جدید"""
        peers = self.get_peers()
        for p in peers:
            if p["id"] == peer_id:
                return {"success": False, "message": "همسایه قبلاً ثبت شده است."}

        peers.append({
            "id": peer_id,
            "host": host,
            "port": port,
            "registered_at": str(datetime.now())
        })

        with open(self.peer_file, "w") as f:
            json.dump(peers, f, indent=4)

        return {"success": True, "message": f"همسایه {peer_id} ثبت شد."}

    def get_peers(self):
        """دریافت لیست همسایه‌ها"""
        if os.path.exists(self.peer_file):
            with open(self.peer_file, "r") as f:
                return json.load(f)
        return []

    def broadcast(self, message):
        """ارسال پیام به همه همسایه‌ها"""
        results = []
        for peer in self.get_peers():
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(5)
                    s.connect((peer["host"], peer["port"]))
                    s.sendall(f"MSG:{message}".encode())
                    results.append({"peer": peer["id"], "status": "sent"})
            except:
                results.append({"peer": peer["id"], "status": "failed"})

        return results

    def stop(self):
        """توقف گره"""
        self.running = False
        self.node_data["status"] = "stopped"
        self._save_node_data()
        return {"success": True, "message": "گره متوقف شد."}

    def get_status(self):
        """دریافت وضعیت گره"""
        return {
            "node_id": self.node_id,
            "status": self.node_data["status"],
            "peers": len(self.get_peers()),
            "sync_queue": len(self.sync_queue),
            "last_seen": self.node_data.get("last_seen")
        }