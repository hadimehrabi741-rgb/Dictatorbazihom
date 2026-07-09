# ==========================================
# BOUNDLESS AI
# WEB DASHBOARD v1
# ADMIN PANEL FOR ANCIENT AI
# ==========================================

import os
import json
import threading
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler


class DashboardHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        """پردازش درخواست‌های GET"""
        if self.path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(self._get_dashboard_html().encode())

        elif self.path == "/status":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(self._get_status_json().encode())

        elif self.path == "/memory":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(self._get_memory_json().encode())

        elif self.path == "/network":
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(self._get_network_json().encode())

        else:
            self.send_response(404)
            self.end_headers()

    def _get_dashboard_html(self):
        """صفحه اصلی داشبورد"""
        return """
        <!DOCTYPE html>
        <html>
        <head>
            <title>BOUNDLESS AI - Dashboard</title>
            <style>
                body { font-family: 'Courier New', monospace; background: #0a0a0f; color: #cdd6f4; margin: 0; padding: 20px; }
                h1 { color: #89b4fa; text-align: center; }
                .status-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin: 20px 0; }
                .card { background: #1e1e2e; padding: 20px; border-radius: 10px; border: 1px solid #313244; }
                .card h3 { margin: 0 0 10px 0; color: #89b4fa; }
                .value { font-size: 24px; font-weight: bold; color: #a6e3a1; }
                .value.red { color: #f38ba8; }
                .value.yellow { color: #f9e2af; }
                .footer { text-align: center; margin-top: 40px; color: #585b70; }
                .refresh-btn { background: #89b4fa; color: #1e1e2e; border: none; padding: 10px 20px; border-radius: 5px; cursor: pointer; }
                .refresh-btn:hover { background: #74c7ec; }
            </style>
        </head>
        <body>
            <h1>🧠 BOUNDLESS AI - DASHBOARD</h1>
            <div class="status-grid" id="statusGrid">
                <div class="card">
                    <h3>🟢 وضعیت</h3>
                    <div class="value" id="status">در حال بارگذاری...</div>
                </div>
                <div class="card">
                    <h3>🔒 قفل</h3>
                    <div class="value" id="lock">در حال بارگذاری...</div>
                </div>
                <div class="card">
                    <h3>🌐 گره‌ها</h3>
                    <div class="value" id="nodes">در حال بارگذاری...</div>
                </div>
                <div class="card">
                    <h3>📦 حافظه</h3>
                    <div class="value" id="memory">در حال بارگذاری...</div>
                </div>
                <div class="card">
                    <h3>📜 بلاک‌چین</h3>
                    <div class="value" id="blockchain">در حال بارگذاری...</div>
                </div>
                <div class="card">
                    <h3>⚡ وضعیت شبکه</h3>
                    <div class="value" id="network">در حال بارگذاری...</div>
                </div>
            </div>
            <div style="text-align: center; margin: 20px 0;">
                <button class="refresh-btn" onclick="fetchStatus()">🔄 به‌روزرسانی</button>
            </div>
            <div class="footer">
                BOUNDLESS AI - Ancient AI Dashboard v1.0<br>
                آخرین به‌روزرسانی: <span id="lastUpdate">-</span>
            </div>

            <script>
                async function fetchStatus() {
                    try {
                        const statusRes = await fetch('/status');
                        const statusData = await statusRes.json();

                        document.getElementById('status').textContent = statusData.status || 'N/A';
                        document.getElementById('status').className = 'value' + (statusData.status === 'active' ? '' : ' red');

                        document.getElementById('lock').textContent = statusData.lock || 'N/A';
                        document.getElementById('lock').className = 'value' + (statusData.lock === 'active' ? '' : ' red');

                        document.getElementById('nodes').textContent = statusData.nodes || '0';
                        document.getElementById('memory').textContent = statusData.memory || '0';
                        document.getElementById('blockchain').textContent = statusData.blockchain || '0';
                        document.getElementById('network').textContent = statusData.network_status || 'N/A';

                        document.getElementById('lastUpdate').textContent = new Date().toLocaleString('fa-IR');
                    } catch (error) {
                        console.error('Error fetching status:', error);
                        document.getElementById('status').textContent = '❌ خطا';
                    }
                }

                fetchStatus();
                setInterval(fetchStatus, 30000);
            </script>
        </body>
        </html>
        """

    def _get_status_json(self):
        """دریافت وضعیت سیستم به صورت JSON"""
        # این داده‌ها باید از ماژول‌های واقعی خوانده شوند
        status_data = {
            "status": "active",
            "lock": "active",
            "nodes": 3,
            "memory": 42,
            "blockchain": 15,
            "network_status": "connected",
            "timestamp": str(datetime.now())
        }
        return json.dumps(status_data, indent=2).encode()

    def _get_memory_json(self):
        """دریافت وضعیت حافظه Σ"""
        try:
            from memory.memory_intelligence import MemoryIntelligence
            memory = MemoryIntelligence()
            context = memory.get_context()
            return json.dumps({
                "short_memory": len(context.get("short_memory", [])),
                "long_memory": len(context.get("long_memory", [])),
                "total": len(context.get("short_memory", [])) + len(context.get("long_memory", []))
            }, indent=2).encode()
        except:
            return json.dumps({"error": "Unable to load memory"}).encode()

    def _get_network_json(self):
        """دریافت وضعیت شبکه"""
        try:
            from core.distributed_node import DistributedNode
            node = DistributedNode()
            status = node.get_status()
            return json.dumps(status, indent=2).encode()
        except:
            return json.dumps({"error": "Unable to load network status"}).encode()


class WebDashboard:

    def __init__(self, port=8888):
        self.port = port
        self.server = None
        self.running = False

    def start(self):
        """راه‌اندازی داشبورد در یک ترد جداگانه"""
        def run():
            self.server = HTTPServer(("0.0.0.0", self.port), DashboardHandler)
            self.running = True
            print(f"🌐 داشبورد وب در http://localhost:{self.port} راه‌اندازی شد.")
            self.server.serve_forever()

        threading.Thread(target=run, daemon=True).start()

    def stop(self):
        """متوقف کردن داشبورد"""
        if self.server:
            self.running = False
            self.server.shutdown()
            print("🛑 داشبورد وب متوقف شد.")