# ==========================================
# BOUNDLESS AI
# KIVY MOBILE APP — MAIN ENTRY POINT
# ==========================================

import os
import sys
import threading
from kivy.config import Config

# Configure Kivy for RTL text (Persian/Arabic)
Config.set('graphics', 'multisampling', 'True')

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.utils import get_color_from_hex
from kivy.graphics import Color, RoundedRectangle
from kivy.core.text import LabelBase
from kivy.support import install_gobject_iteration


# ==========================================
# REGISTER PERSIAN FONT
# ==========================================

font_path = os.path.join(BASE_DIR, 'assets', 'fonts', 'IranSans.ttf')
if os.path.exists(font_path):
    LabelBase.register(name='IranSans', fn_regular=font_path)
    print(f"✅ Font registered: {font_path}")
else:
    print(f"⚠️ Warning: Font not found at {font_path}")


# ==========================================
# COLORS
# ==========================================

BG_COLOR       = get_color_from_hex("#0D0D0D")
PANEL_COLOR    = get_color_from_hex("#1A1A2E")
USER_BUBBLE    = get_color_from_hex("#16213E")
BOT_BUBBLE     = get_color_from_hex("#0F3460")
ACCENT         = get_color_from_hex("#E94560")
TEXT_COLOR     = get_color_from_hex("#EAEAEA")
HINT_COLOR     = get_color_from_hex("#888888")


def make_bubble(text, align="left", bg=None):
    """Create a single chat bubble label."""
    color = bg or (BOT_BUBBLE if align == "left" else USER_BUBBLE)
    lbl = Label(
        text=text,
        markup=True,
        size_hint_y=None,
        size_hint_x=0.85,
        halign="right" if align == "right" else "left",
        valign="top",
        padding=(14, 10),
        color=TEXT_COLOR,
        font_size="14sp",
        font_name="IranSans",
    )
    lbl.bind(texture_size=lambda inst, val: setattr(inst, "height", val[1] + 20))
    lbl.bind(width=lambda inst, val: setattr(inst, "text_size", (val, None)))

    wrapper = BoxLayout(
        size_hint_y=None,
        height=0,
        padding=(8, 4),
    )
    lbl.bind(height=lambda inst, val: setattr(wrapper, "height", val + 8))

    if align == "right":
        wrapper.add_widget(BoxLayout(size_hint_x=0.15))
    wrapper.add_widget(lbl)
    if align == "left":
        wrapper.add_widget(BoxLayout(size_hint_x=0.15))

    return wrapper


# ==========================================
# LOGIN SCREEN
# ==========================================

class LoginScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.clearcolor = BG_COLOR

        root = BoxLayout(orientation="vertical", padding=40, spacing=20)

        root.add_widget(BoxLayout(size_hint_y=0.2))

        title = Label(
            text="[b]BOUNDLESS AI[/b]",
            markup=True,
            font_size="28sp",
            color=ACCENT,
            size_hint_y=None,
            height=50,
            font_name="IranSans",
        )
        root.add_widget(title)

        sub = Label(
            text="ورود به سیستم",
            font_size="16sp",
            color=HINT_COLOR,
            size_hint_y=None,
            height=30,
            font_name="IranSans",
            halign="right",
        )
        root.add_widget(sub)

        root.add_widget(BoxLayout(size_hint_y=None, height=20))

        self.username = TextInput(
            hint_text="نام کاربری  (Enter for guest)",
            multiline=False,
            size_hint_y=None,
            height=48,
            font_size="15sp",
            background_color=PANEL_COLOR,
            foreground_color=TEXT_COLOR,
            cursor_color=ACCENT,
            hint_text_color=HINT_COLOR,
            font_name="IranSans",
        )
        root.add_widget(self.username)

        self.password = TextInput(
            hint_text="رمز عبور",
            multiline=False,
            password=True,
            size_hint_y=None,
            height=48,
            font_size="15sp",
            background_color=PANEL_COLOR,
            foreground_color=TEXT_COLOR,
            cursor_color=ACCENT,
            hint_text_color=HINT_COLOR,
            font_name="IranSans",
        )
        root.add_widget(self.password)

        self.status = Label(
            text="",
            color=ACCENT,
            size_hint_y=None,
            height=30,
            font_size="13sp",
            font_name="IranSans",
        )
        root.add_widget(self.status)

        btn = Button(
            text="ورود",
            size_hint_y=None,
            height=50,
            font_size="16sp",
            background_color=ACCENT,
            color=(1, 1, 1, 1),
            font_name="IranSans",
        )
        btn.bind(on_press=self.do_login)
        root.add_widget(btn)

        root.add_widget(BoxLayout(size_hint_y=0.3))
        self.add_widget(root)

    def do_login(self, *args):
        from core.security_manager import SecurityManager
        sec = SecurityManager()
        uname = self.username.text.strip()
        pwd   = self.password.text.strip()
        result = sec.login(uname, pwd)

        chat_screen = self.manager.get_screen("chat")
        chat_screen.set_role(result["role"], result["message"])
        self.manager.current = "chat"


# ==========================================
# CHAT SCREEN
# ==========================================

class ChatScreen(Screen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orchestrator = None
        self.role = "guest"
        Window.clearcolor = BG_COLOR

        root = BoxLayout(orientation="vertical")

        # ---- header ----
        header = BoxLayout(
            size_hint_y=None, height=52,
            padding=(16, 8), spacing=8,
        )
        with header.canvas.before:
            Color(*PANEL_COLOR)
            self._header_rect = RoundedRectangle(size=header.size, pos=header.pos)
        header.bind(size=lambda i, v: setattr(self._header_rect, "size", v))
        header.bind(pos=lambda i, v: setattr(self._header_rect, "pos", v))

        self.header_lbl = Label(
            text="[b]BOUNDLESS AI[/b]",
            markup=True,
            color=TEXT_COLOR,
            font_size="17sp",
            font_name="IranSans",
            halign="right",
        )
        header.add_widget(self.header_lbl)
        root.add_widget(header)

        # ---- messages ----
        self.scroll = ScrollView(size_hint_y=1)
        self.msg_layout = BoxLayout(
            orientation="vertical",
            size_hint_y=None,
            spacing=4,
            padding=(8, 8),
        )
        self.msg_layout.bind(
            minimum_height=self.msg_layout.setter("height")
        )
        self.scroll.add_widget(self.msg_layout)
        root.add_widget(self.scroll)

        # ---- input bar ----
        bar = BoxLayout(
            size_hint_y=None, height=60,
            padding=(8, 8), spacing=8,
        )
        with bar.canvas.before:
            Color(*PANEL_COLOR)
            self._bar_rect = RoundedRectangle(size=bar.size, pos=bar.pos)
        bar.bind(size=lambda i, v: setattr(self._bar_rect, "size", v))
        bar.bind(pos=lambda i, v: setattr(self._bar_rect, "pos", v))

        self.text_input = TextInput(
            hint_text="پیام خود را بنویسید...",
            multiline=False,
            size_hint_x=1,
            font_size="14sp",
            background_color=BG_COLOR,
            foreground_color=TEXT_COLOR,
            cursor_color=ACCENT,
            hint_text_color=HINT_COLOR,
            font_name="IranSans",
        )
        self.text_input.bind(on_text_validate=self.send_message)
        bar.add_widget(self.text_input)

        send_btn = Button(
            text="▶",
            size_hint_x=None,
            width=52,
            font_size="18sp",
            background_color=ACCENT,
            color=(1, 1, 1, 1),
        )
        send_btn.bind(on_press=self.send_message)
        bar.add_widget(send_btn)
        root.add_widget(bar)

        self.add_widget(root)

    def set_role(self, role, message):
        self.role = role
        self.header_lbl.text = f"[b]BOUNDLESS AI[/b]  —  {'🟢 مدیر' if role == 'admin' else '🟡 مهمان'}"
        self._add_bubble(message, "left")
        self._init_orchestrator(role)

    def _init_orchestrator(self, role):
        def _load():
            try:
                from groq_connector import GroqConnector
                from prompt_engine import PromptEngine
                from core.architect_brain import ArchitectBrain
                from core.architect_fusion import ArchitectFusion
                from core.architect_orchestrator import ArchitectOrchestrator
                from core.truth_guard import TruthGuard
                from core.local_knowledge_engine import LocalKnowledgeEngine
                from memory.memory_intelligence import MemoryIntelligence
                from memory.memory_reasoner import MemoryReasoner
                from memory.memory_manager import MemoryManager
                from memory.memory_retrieval import MemoryRetrieval

                memory = MemoryIntelligence()
                reasoner = MemoryReasoner(memory)
                manager = MemoryManager(memory, reasoner)
                retrieval = MemoryRetrieval(memory)

                api_key = os.environ.get("GROQ_API_KEY", "").strip()
                groq = None
                if api_key:
                    groq = GroqConnector()
                    groq.set_key(api_key)
                    groq.connect()

                brain = ArchitectBrain(memory=memory, manager=manager, retrieval=retrieval)
                fusion = ArchitectFusion(brain=brain, memory=memory)
                truth_guard = TruthGuard()
                local_knowledge = LocalKnowledgeEngine(memory=memory, eternal=None)
                prompt_engine = PromptEngine()

                self.orchestrator = ArchitectOrchestrator(
                    brain=brain, fusion=fusion, memory=memory,
                    manager=manager, retrieval=retrieval,
                    prompt_engine=prompt_engine, groq=groq,
                    truth_guard=truth_guard, local_knowledge=local_knowledge,
                )
                Clock.schedule_once(lambda dt: self._add_bubble("✅ سیستم آماده است. پیام بنویسید.", "left"))
            except Exception as e:
                Clock.schedule_once(lambda dt: self._add_bubble(f"⚠️ خطا در بارگذاری: {e}", "left"))

        threading.Thread(target=_load, daemon=True).start()

    def send_message(self, *args):
        text = self.text_input.text.strip()
        if not text:
            return
        self.text_input.text = ""
        self._add_bubble(f"[b]شما:[/b] {text}", "right")

        if self.orchestrator is None:
            self._add_bubble("⏳ سیستم در حال بارگذاری است...", "left")
            return

        def _run():
            try:
                result = self.orchestrator.run(text)
                reply = result.get("response", "")
            except Exception as e:
                reply = f"⚠️ خطا: {e}"
            Clock.schedule_once(lambda dt: self._add_bubble(reply, "left"))

        threading.Thread(target=_run, daemon=True).start()

    def _add_bubble(self, text, align="left"):
        bubble = make_bubble(text, align)
        self.msg_layout.add_widget(bubble)
        Clock.schedule_once(lambda dt: setattr(self.scroll, "scroll_y", 0), 0.1)


# ==========================================
# APP
# ==========================================

class BoundlessApp(App):

    def build(self):
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(ChatScreen(name="chat"))
        return sm


if __name__ == "__main__":
    BoundlessApp().run()
