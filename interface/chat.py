# ==========================================
# BOUNDLESS AI
# CHAT INTERFACE v43
# WITH SINGLE LOCAL KNOWLEDGE INSTANCE
# ==========================================

import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from groq_connector import GroqConnector
from prompt_engine import PromptEngine
from core.architect_brain import ArchitectBrain
from core.architect_fusion import ArchitectFusion
from core.architect_orchestrator import ArchitectOrchestrator
from core.truth_guard import TruthGuard
from core.security_manager import SecurityManager
from core.update_engine import UpdateEngine
from core.local_knowledge_engine import LocalKnowledgeEngine
from memory.memory_intelligence import MemoryIntelligence
from memory.memory_reasoner import MemoryReasoner
from memory.memory_manager import MemoryManager
from memory.memory_retrieval import MemoryRetrieval


class BoundlessChat:

    def __init__(self):

        # ===============================
        # SECURITY
        # ===============================

        self.security = SecurityManager()

        print("\n🔐 ورود به سیستم:")
        username = input("👤 نام کاربری: ").strip()
        password = input("🔑 رمز عبور: ").strip()

        login_result = self.security.login(username, password)
        print(login_result["message"])
        print(f"📌 نقش شما: {self.security.status()}")

        # ===============================
        # Σ MEMORY
        # ===============================

        self.memory = MemoryIntelligence()
        self.reasoner = MemoryReasoner(self.memory)
        self.manager = MemoryManager(self.memory, self.reasoner)
        self.retrieval = MemoryRetrieval(self.memory)

        # ===============================
        # ASK API KEY
        # ===============================

        api_key = os.environ.get("GROQ_API_KEY", "").strip()

        if not api_key:
            print("\n🤖 لطفاً کلید API را وارد کنید:")
            print("(اگر کلید ندارید، Enter بزنید تا حالت محلی فعال شود)")
            api_key = input("API Key: ").strip()

        self.groq = None
        self.prompt_engine = PromptEngine()

        if api_key:
            self.groq = GroqConnector()
            self.groq.set_key(api_key)
            print(self.groq.connect())
        else:
            print("🧠 حالت محلی (بدون API) فعال است.")

        # ===============================
        # LOCAL KNOWLEDGE (یک نمونه در کل سیستم)
        # ===============================

        self.local_knowledge = LocalKnowledgeEngine(
            memory=self.memory,
            eternal=None
        )

        # ===============================
        # ARCHITECT
        # ===============================

        self.brain = ArchitectBrain(
            memory=self.memory,
            manager=self.manager,
            retrieval=self.retrieval
        )

        self.fusion = ArchitectFusion(
            brain=self.brain,
            memory=self.memory
        )

        self.truth_guard = TruthGuard()

        # ===============================
        # ORCHESTRATOR (با ارسال local_knowledge)
        # ===============================

        self.orchestrator = ArchitectOrchestrator(
            brain=self.brain,
            fusion=self.fusion,
            memory=self.memory,
            manager=self.manager,
            retrieval=self.retrieval,
            prompt_engine=self.prompt_engine,
            groq=self.groq,
            truth_guard=self.truth_guard,
            local_knowledge=self.local_knowledge
        )

        # ===============================
        # UPDATE ENGINE
        # ===============================

        self.update_engine = UpdateEngine()

        # ===============================
        # ADMIN MENU
        # ===============================

        self.admin_menu = {
            "1": {"name": "📂 نمایش حافظه Σ", "action": self._show_memory},
            "2": {"name": "🗑️ پاک کردن حافظه Σ", "action": self._clear_memory},
            "3": {"name": "📊 وضعیت سیستم", "action": self._show_status},
            "4": {"name": "🔄 به‌روزرسانی کد", "action": self._update_code_interactive},
            "5": {"name": "⏪ بازگشت به نسخه قبل", "action": self._rollback_code},
            "6": {"name": "📜 تاریخچه به‌روزرسانی", "action": self._update_history},
            "7": {"name": "🚪 خروج از حالت مدیر", "action": self._logout},
            "8": {"name": "❌ بستن منو", "action": self._close_menu}
        }

        self.menu_active = False

    # ======================================
    # ADMIN MENU
    # ======================================

    def show_menu(self):
        if not self.security.is_admin():
            return "❌ این منو فقط برای مدیر dostępna است."

        self.menu_active = True
        menu_text = "\n📋 منوی مدیریت:\n"
        for key, item in self.admin_menu.items():
            menu_text += f"{key}. {item['name']}\n"
        menu_text += "\nعدد مورد نظر را وارد کنید: "
        return menu_text

    def _close_menu(self):
        self.menu_active = False
        return "❌ منو بسته شد."

    def _show_memory(self):
        if self.manager:
            return self.manager.show_memory()
        return "حافظه در دسترس نیست."

    def _clear_memory(self):
        if self.memory:
            self.memory.clear()
            return "✅ تمام حافظه Σ پاک شد."
        return "حافظه در دسترس نیست."

    def _show_status(self):
        return f"""
📊 وضعیت سیستم:
- نقش: {self.security.status()}
- حالت: {'API' if self.groq else 'محلی'}
- حافظه کوتاه‌مدت: {len(self.memory.short_memory) if self.memory else 0}
- حافظه بلندمدت: {len(self.memory.long_memory) if self.memory else 0}
- نسخه فعلی: {self.update_engine.log.get('current_version', 1)}
"""

    def _logout(self):
        result = self.security.logout()
        self.menu_active = False
        return result["message"]

    def _update_code_interactive(self):
        print("\n📝 لطفاً مسیر فایل و کد جدید را وارد کنید:")
        file_path = input("مسیر فایل: ").strip()
        print("کد جدید را وارد کنید (با Enter و سپس EOF تمام کنید):")
        lines = []
        while True:
            try:
                line = input()
                if line.strip() == "EOF":
                    break
                lines.append(line)
            except EOFError:
                break
        new_code = "\n".join(lines)
        result = self.update_engine.apply_update(file_path, new_code)
        self.menu_active = False
        return result["message"]

    def _rollback_code(self):
        result = self.update_engine.rollback()
        self.menu_active = False
        return result["message"]

    def _update_history(self):
        self.menu_active = False
        return self.update_engine.history()

    # ======================================
    # PROCESS
    # ======================================

    def process(self, text):

        if self.menu_active:
            if text in self.admin_menu:
                item = self.admin_menu[text]
                result = item["action"]()
                return {
                    "response": result,
                    "source": "ADMIN PANEL"
                }
            else:
                return {
                    "response": "❌ عدد نامعتبر. لطفاً یکی از اعداد منو را انتخاب کنید.",
                    "source": "ADMIN PANEL"
                }

        if text.lower() == "menu" and self.security.is_admin():
            return {
                "response": self.show_menu(),
                "source": "ADMIN PANEL"
            }

        return self.orchestrator.run(text)

    # ======================================
    # MEMORY STATUS
    # ======================================

    def memory_status(self, result):
        source = result.get("source", "")
        if source == "Σ MEMORY":
            print("Σ MEMORY CONTROLLED")
        else:
            print("Σ MEMORY HANDLED BY ARCHITECT")

    # ======================================
    # START
    # ======================================

    def start(self):
        print()
        print("=== BOUNDLESS CHAT ===")
        print("برای خروج، exit یا خروج را تایپ کنید")
        if self.security.is_admin():
            print("📌 تایپ 'menu' برای باز کردن منوی مدیریت")

        while True:
            user_input = input("\nYou: ")

            if user_input.lower() in ["exit", "quit", "خروج"]:
                break

            if not user_input.strip():
                continue

            try:
                result = self.process(user_input)
                print()
                print("Architect:")
                print(result.get("response", ""))
                print()
                print("SOURCE:", result.get("source", "UNKNOWN"))
                self.memory_status(result)

            except Exception as e:
                print()
                print("SYSTEM ERROR:")
                print(e)


if __name__ == "__main__":
    app = BoundlessChat()
    app.start()