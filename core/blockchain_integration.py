# ==========================================
# BOUNDLESS AI
# BLOCKCHAIN INTEGRATION v1
# IMMUTABLE STORAGE FOR SIGNATURES
# ==========================================

import os
import json
import hashlib
from datetime import datetime


class BlockchainIntegration:

    def __init__(self):
        self.chain_file = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "storage",
            "blockchain",
            "chain.json"
        )
        self._ensure_chain()

    def _ensure_chain(self):
        os.makedirs(os.path.dirname(self.chain_file), exist_ok=True)
        if not os.path.exists(self.chain_file):
            genesis_block = {
                "index": 0,
                "timestamp": str(datetime.now()),
                "data": "GENESIS_BLOCK",
                "previous_hash": "0",
                "hash": self._calculate_hash(0, "GENESIS_BLOCK", "0")
            }
            with open(self.chain_file, "w") as f:
                json.dump([genesis_block], f, indent=4)

    def _calculate_hash(self, index, data, previous_hash):
        block_string = f"{index}{data}{previous_hash}"
        return hashlib.sha256(block_string.encode()).hexdigest()

    def add_block(self, data):
        """اضافه کردن یک بلوک جدید به زنجیره"""
        with open(self.chain_file, "r") as f:
            chain = json.load(f)

        last_block = chain[-1]
        new_index = last_block["index"] + 1
        new_hash = self._calculate_hash(new_index, data, last_block["hash"])

        new_block = {
            "index": new_index,
            "timestamp": str(datetime.now()),
            "data": data,
            "previous_hash": last_block["hash"],
            "hash": new_hash
        }

        chain.append(new_block)

        with open(self.chain_file, "w") as f:
            json.dump(chain, f, indent=4)

        return new_block

    def verify_chain(self):
        """بررسی یکپارچگی زنجیره"""
        with open(self.chain_file, "r") as f:
            chain = json.load(f)

        for i in range(1, len(chain)):
            current = chain[i]
            previous = chain[i-1]

            if current["previous_hash"] != previous["hash"]:
                return {
                    "valid": False,
                    "error": f"شکست در بلوک {i}: هش قبلی مطابقت ندارد."
                }

            calculated_hash = self._calculate_hash(
                current["index"],
                current["data"],
                current["previous_hash"]
            )

            if current["hash"] != calculated_hash:
                return {
                    "valid": False,
                    "error": f"شکست در بلوک {i}: هش محاسبه‌شده مطابقت ندارد."
                }

        return {"valid": True, "length": len(chain)}

    def get_chain(self):
        """دریافت کل زنجیره"""
        with open(self.chain_file, "r") as f:
            return json.load(f)

    def get_last_block(self):
        """دریافت آخرین بلوک"""
        chain = self.get_chain()
        return chain[-1] if chain else None

    def get_history(self, limit=10):
        """دریافت تاریخچه بلوک‌ها"""
        chain = self.get_chain()
        return chain[-limit:]

    def search(self, query):
        """جستجو در داده‌های بلوک‌ها"""
        chain = self.get_chain()
        results = []
        for block in chain:
            if query in str(block["data"]):
                results.append(block)
        return results