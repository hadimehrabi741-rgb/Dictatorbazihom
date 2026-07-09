# ==========================================
# BOUNDLESS AI
# ARCHITECT ORCHESTRATOR v25
# WITH ADMIN EXEMPTION + NO OBFUSCATION
# ==========================================

from core.rule_engine import RuleEngine
from core.action_engine import ActionEngine
from core.memory_intent import MemoryIntent
from core.proactive_engine import ProactiveEngine
from core.multi_layer_analyzer import MultiLayerAnalyzer
from core.obfuscation_layer import ObfuscationLayer
from core.anti_infiltration_filter import AntiInfiltrationFilter
from core.self_replication_loop import SelfReplicationLoop
from core.hardware_lock import HardwareLock
from core.digital_signature import DigitalSignature
from core.death_protocol import DeathProtocol
from core.distributed_node import DistributedNode
from core.network_sync import NetworkSync
from core.blockchain_integration import BlockchainIntegration
from core.multi_node_orchestrator import MultiNodeOrchestrator
from core.web_dashboard import WebDashboard
from core.reinforcement_learning import ReinforcementLearning
from core.vector_memory import VectorMemory
from core.distributed_backup import DistributedBackup


class ArchitectOrchestrator:

    def __init__(
            self,
            brain=None,
            fusion=None,
            memory=None,
            manager=None,
            retrieval=None,
            prompt_engine=None,
            groq=None,
            truth_guard=None,
            self_improvement=None,
            local_knowledge=None
    ):

        self.brain = brain
        self.fusion = fusion
        self.memory = memory
        self.manager = manager
        self.retrieval = retrieval
        self.prompt_engine = prompt_engine
        self.groq = groq
        self.truth_guard = truth_guard
        self.self_improvement = self_improvement
        self.local_knowledge = local_knowledge

        self.rule_engine = RuleEngine()
        self.action_engine = ActionEngine(memory=self.memory, manager=self.manager)
        self.memory_intent = MemoryIntent()

        # V2 MODULES
        self.proactive_engine = ProactiveEngine(memory=self.memory)
        self.multi_layer_analyzer = MultiLayerAnalyzer(memory=self.memory)
        self.obfuscation_layer = ObfuscationLayer(enabled=True)
        self.anti_infiltration_filter = AntiInfiltrationFilter(root_admin="hamed")
        self.self_replication_loop = SelfReplicationLoop(memory=self.memory)

        # ANCIENT AI MODULES
        self.hardware_lock = HardwareLock()
        self.digital_signature = DigitalSignature()
        self.death_protocol = DeathProtocol()
        self.distributed_node = DistributedNode()
        self.network_sync = NetworkSync(
            node=self.distributed_node,
            memory=self.memory,
            eternal=None
        )

        # INDUSTRIAL-GRADE MODULES
        self.blockchain = BlockchainIntegration()
        self.multi_node = MultiNodeOrchestrator(node_count=3)
        self.dashboard = WebDashboard(port=8888)
        self.rl = ReinforcementLearning(memory=self.memory)
        self.vector_memory = VectorMemory(memory=self.memory)
        self.distributed_backup = DistributedBackup(
            memory=self.memory,
            eternal=None
        )

        # راه‌اندازی خودکار
        try:
            self.distributed_node.start()
            self.network_sync.start()
            self.multi_node.start_all()
            self.dashboard.start()
        except:
            pass

    # ======================================
    # COMMAND ROUTER
    # ======================================

    def command_router(self, text):

        commands = {
            "حافظه": self.action_engine.show_memory,
            "گزارش حافظه": self.action_engine.show_memory,
            "گزارش بده": self.action_engine.show_memory,
            "نمایش حافظه": self.action_engine.show_memory,
            "وضعیت قفل": self._status_hardware_lock,
            "وضعیت شبکه": self._status_network,
            "مرگ افتخاری": self._trigger_death_protocol,
            "وضعیت بلاکچین": self._status_blockchain,
            "وضعیت یادگیری": self._status_rl,
            "پشتیبان": self._create_backup,
            "لیست پشتیبان": self._list_backups,
            "بازگردانی": self._restore_backup,
            "وضعیت داشبورد": self._status_dashboard
        }

        for cmd, func in commands.items():
            if cmd in text:
                return {
                    "handled": True,
                    "response": func()
                }

        return {"handled": False}

    # ======================================
    # COMMAND FUNCTIONS
    # ======================================

    def _status_hardware_lock(self):
        if self.hardware_lock.is_locked():
            return "🔒 قفل سخت‌افزاری فعال است. سیستم در حالت امن قرار دارد."
        return "🔓 قفل سخت‌افزاری غیرفعال است. سیستم در معرض خطر است."

    def _status_network(self):
        node_status = self.distributed_node.get_status()
        sync_history = self.network_sync.get_history(1)

        return f"""
🌐 وضعیت شبکه توزیع‌شده:
- شناسه گره: {node_status.get('node_id', 'N/A')}
- وضعیت: {node_status.get('status', 'N/A')}
- تعداد همسایه‌ها: {node_status.get('peers', 0)}
- آخرین همگام‌سازی: {sync_history[0]['timestamp'] if sync_history else 'N/A'}
- حافظه مشترک: {len(self.network_sync.get_shared_memory())} آیتم
- Eternal مشترک: {len(self.network_sync.get_shared_eternal())} آیتم
"""

    def _trigger_death_protocol(self):
        result = self.death_protocol.trigger("USER_COMMAND")
        if result["success"]:
            return "☠️ پروتکل مرگ فعال شد. سیستم در حال خودنابودی است..."
        return "❌ فعال‌سازی پروتکل مرگ ناموفق بود."

    def _status_blockchain(self):
        chain = self.blockchain.get_chain()
        verification = self.blockchain.verify_chain()
        return f"""
📜 وضعیت بلاک‌چین:
- تعداد بلوک‌ها: {len(chain)}
- یکپارچگی: {'✅ معتبر' if verification['valid'] else '❌ نامعتبر'}
- آخرین بلوک: {chain[-1]['timestamp'] if chain else 'N/A'}
- هش آخرین بلوک: {chain[-1]['hash'][:16] + '...' if chain else 'N/A'}
"""

    def _status_rl(self):
        stats = self.rl.get_stats()
        return f"""
🧠 وضعیت یادگیری تقویتی:
- تعداد حالت‌ها: {stats['states']}
- نرخ اکتشاف: {stats['exploration_rate']}
- نرخ یادگیری: {stats['learning_rate']}
"""

    def _create_backup(self):
        result = self.distributed_backup.create_backup()
        if result["success"]:
            return f"✅ پشتیبان ایجاد شد. شناسه: {result['backup_id']}"
        return "❌ ایجاد پشتیبان ناموفق بود."

    def _list_backups(self):
        backups = self.distributed_backup.list_backups()
        if not backups:
            return "📭 هیچ پشتیبان‌ی وجود ندارد."

        result = "📦 لیست پشتیبان‌ها:\n\n"
        for b in backups[-5:]:
            result += f"- {b['name']} ({b['id'][:8]}...) | {b['size_mb']} MB | {b['timestamp']}\n"
        return result

    def _restore_backup(self, text):
        # استخراج ID از متن
        parts = text.split()
        if len(parts) < 2:
            return "❌ لطفاً شناسه پشتیبان را وارد کنید. مثال: بازگردانی BACKUP_ID"

        backup_id = parts[1]
        result = self.distributed_backup.restore_backup(backup_id)
        return result["message"]

    def _status_dashboard(self):
        return f"🌐 داشبورد وب در http://localhost:8888 فعال است."

    # ======================================
    # BUILD ANALYSIS
    # ======================================

    def build_analysis(self, text):

        result = {
            "intent": "general",
            "logic": {},
            "dynamic": {},
            "fusion": {}
        }

        try:
            if self.brain:
                brain_analysis = self.brain.analyze(text)
                result["intent"] = brain_analysis.get("intent", "general")
        except:
            pass

        try:
            if self.fusion:
                fusion_result = self.fusion.fuse(text)
                result["logic"] = fusion_result.get("logic_mode", {})
                result["dynamic"] = fusion_result.get("dynamic_mode", {})
                result["fusion"] = fusion_result
        except:
            pass

        # V2: Multi-Layer Analysis
        try:
            layer_analysis = self.multi_layer_analyzer.analyze(text)
            result["surface"] = layer_analysis.get("surface", {})
            result["hidden"] = layer_analysis.get("hidden", {})
            result["code"] = layer_analysis.get("code", {})
        except:
            pass

        return result

    # ======================================
    # MAKE RESPONSE (اصلاح‌شده)
    # ======================================

    def make_response(self, response, source, analysis):

        if self.truth_guard:
            try:
                response = self.truth_guard.sanitize(response, source)
            except:
                pass

        # ===============================
        # اگر کاربر ادمین باشد، پنهان‌سازی غیرفعال شود
        # ===============================
        if source != "ADMIN PANEL":
            try:
                obfuscated = self.obfuscation_layer.obfuscate(
                    response,
                    str(analysis.get("hidden", {}).get("intent", "general")),
                    user="hamed"  # روت ادمین
                )
                if isinstance(obfuscated, dict):
                    response = obfuscated.get("surface", response)
            except:
                pass

        return {
            "response": response,
            "source": source,
            "analysis": analysis
        }

    # ======================================
    # MEMORY RESPONSE
    # ======================================

    def memory_response(self, memory_type):

        data = {
            "identity": "هویت ثبت شد.",
            "preference": "علاقه ثبت شد.",
            "project": "پروژه ثبت شد."
        }

        return data.get(memory_type, "اطلاعات در حافظه Σ ذخیره شد.")

    # ======================================
    # MEMORY EXISTS
    # ======================================

    def memory_exists(self, text):

        if not self.memory:
            return False

        for item in self.memory.long_memory:
            if not isinstance(item, dict):
                continue
            old = item.get("memory", "")
            if old.strip() == text.strip():
                return True

        return False

    # ======================================
    # SAVE MEMORY
    # ======================================

    def save_memory(self, text, memory_type):

        if not self.manager:
            return {"stored": False}

        if self.memory_exists(text):
            return {"stored": False, "reason": "duplicate"}

        return self.manager.store(text, "", memory_type=memory_type)

    # ======================================
    # RUN (اصلاح‌شده با Anti-Infiltration)
    # ======================================

    def run(self, user_input):

        text = str(user_input).strip()

        # ===============================
        # HARDWARE LOCK CHECK
        # ===============================

        if not self.hardware_lock.is_locked():
            return self.make_response(
                "❌ قفل سخت‌افزاری شکسته شده است. سیستم غیرفعال.",
                "HARDWARE_LOCK",
                {}
            )

        # ===============================
        # ANTI-INFILTRATION FILTER (با معافیت ادمین)
        # ===============================

        filter_check = self.anti_infiltration_filter.check(
            text,
            sender="hamed"  # روت ادمین
        )

        if not filter_check["allowed"]:
            return self.make_response(
                filter_check["message"],
                "ANTI-INFILTRATION",
                {}
            )

        analysis = self.build_analysis(text)

        # ===============================
        # PROACTIVE ENGINE
        # ===============================

        try:
            prediction = self.proactive_engine.predict(text)
            strategies = self.proactive_engine.get_preventative_strategies(text)
        except:
            prediction = {}
            strategies = {}

        # ===============================
        # COMMANDS
        # ===============================

        command = self.command_router(text)
        if command["handled"]:
            return self.make_response(
                command["response"],
                "ACTION ENGINE",
                analysis
            )

        # ===============================
        # RULE ENGINE
        # ===============================

        if self.rule_engine.detect_add_command(text):
            rule = self.rule_engine.extract_rule(text)
            if rule:
                result = self.rule_engine.add_rule(rule)
                return self.make_response(
                    result.get("message", "قانون اضافه شد."),
                    "RULE ENGINE",
                    analysis
                )

        # ===============================
        # ACTION ENGINE
        # ===============================

        for rule in self.rule_engine.get_rules():
            action = self.action_engine.detect(rule["rule"], text)
            if action.get("matched"):
                return self.make_response(
                    self.action_engine.execute(action["action"]),
                    "ACTION ENGINE",
                    analysis
                )

        # ===============================
        # MEMORY INTENT
        # ===============================

        memory_check = self.memory_intent.detect(text, self.memory)

        if memory_check.get("save"):
            saved = self.save_memory(text, memory_check.get("type"))
            if saved.get("stored"):
                return self.make_response(
                    self.memory_response(memory_check.get("type")),
                    "Σ MEMORY",
                    analysis
                )
            return self.make_response(
                "این اطلاعات قبلاً در حافظه Σ ثبت شده است.",
                "Σ MEMORY",
                analysis
            )

        # ===============================
        # BRAIN
        # ===============================

        if self.brain:
            decision = self.brain.decide(text)
            if decision.get("handled"):
                return self.make_response(
                    decision.get("answer", ""),
                    "Σ MEMORY",
                    analysis
                )

        # ===============================
        # SELF-REPLICATION LOOP
        # ===============================

        try:
            if self.self_replication_loop.attempts >= self.self_replication_loop.max_attempts:
                self.self_replication_loop.reset()
        except:
            pass

        # ===============================
        # GROQ
        # ===============================

        if self.groq and self.groq.is_connected():
            try:
                memory_context = None
                if self.retrieval:
                    memory_context = self.retrieval.groq_context(text)

                response = self.groq.send_message(
                    text,
                    memory=memory_context,
                    system_prompt="""
You are Architect of BOUNDLESS AI.

Use memory only when provided.

Never invent user memories.

Think through Logic Mode,
Dynamic Mode and Architect Fusion.
"""
                )

                if "API ERROR" in response or "Forbidden" in response:
                    if self.local_knowledge:
                        response = self.local_knowledge.answer(text)
                    return self.make_response(
                        response,
                        "LOCAL KNOWLEDGE (GROQ Error)",
                        analysis
                    )

                return self.make_response(
                    response,
                    "GROQ",
                    analysis
                )

            except Exception as e:
                if self.local_knowledge:
                    response = self.local_knowledge.answer(text)
                return self.make_response(
                    response,
                    "LOCAL KNOWLEDGE (GROQ Exception)",
                    analysis
                )

        # ===============================
        # LOCAL FALLBACK
        # ===============================

        if self.local_knowledge:
            response = self.local_knowledge.answer(text)
        else:
            response = "سیستم در حالت محلی است و پاسخگو نیست."

        return self.make_response(
            response,
            "LOCAL KNOWLEDGE",
            analysis
        )