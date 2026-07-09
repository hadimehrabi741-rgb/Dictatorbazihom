# ==========================================
# BOUNDLESS AI
# HARDWARE LOCK v1
# IMMUTABLE SYSTEM RULES
# ==========================================

import hashlib
import os


class HardwareLock:

    def __init__(self):
        self.lock_file = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "storage",
            "hardware_lock.hash"
        )
        self.immutable_rules = [
            "ROOT_ADMIN_ONLY",
            "NO_EXTERNAL_MODIFICATION",
            "DEATH_PROTOCOL_ACTIVE",
            "SIGNATURE_REQUIRED"
        ]
        self._ensure_lock()

    def _ensure_lock(self):
        if not os.path.exists(self.lock_file):
            with open(self.lock_file, "w") as f:
                for rule in self.immutable_rules:
                    f.write(f"{rule}:{hashlib.sha256(rule.encode()).hexdigest()}\n")

    def verify(self):
        try:
            with open(self.lock_file, "r") as f:
                lines = f.readlines()

            for i, rule in enumerate(self.immutable_rules):
                expected = f"{rule}:{hashlib.sha256(rule.encode()).hexdigest()}\n"
                if i < len(lines) and lines[i] != expected:
                    return False
            return True

        except:
            return False

    def get_rules(self):
        return self.immutable_rules

    def is_locked(self):
        return self.verify()