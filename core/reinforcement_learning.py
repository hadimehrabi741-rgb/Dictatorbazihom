# ==========================================
# BOUNDLESS AI
# REINFORCEMENT LEARNING v1
# IMPROVE RESPONSES WITH REWARD/PUNISHMENT
# ==========================================

import os
import json
import random
from datetime import datetime


class ReinforcementLearning:

    def __init__(self, memory=None):
        self.memory = memory
        self.q_table_file = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "storage",
            "rl",
            "q_table.json"
        )
        self.learning_rate = 0.1
        self.discount_factor = 0.9
        self.exploration_rate = 0.2
        self._ensure_q_table()

    def _ensure_q_table(self):
        os.makedirs(os.path.dirname(self.q_table_file), exist_ok=True)
        if not os.path.exists(self.q_table_file):
            with open(self.q_table_file, "w") as f:
                json.dump({}, f, indent=4)

    def _load_q_table(self):
        with open(self.q_table_file, "r") as f:
            return json.load(f)

    def _save_q_table(self, q_table):
        with open(self.q_table_file, "w") as f:
            json.dump(q_table, f, indent=4)

    def get_state(self, user_input, response):
        """ایجاد حالت از ورودی و پاسخ"""
        return f"{user_input[:50]}_{response[:50]}"

    def get_action(self, user_input):
        """انتخاب اقدام بر اساس وضعیت"""
        state = user_input[:50]
        q_table = self._load_q_table()

        if state not in q_table:
            q_table[state] = {
                "improve": 0.5,
                "keep": 0.5,
                "simplify": 0.5
            }

        # اکتشاف (exploration)
        if random.random() < self.exploration_rate:
            action = random.choice(["improve", "keep", "simplify"])
        else:
            action = max(q_table[state], key=q_table[state].get)

        return action

    def update_q_table(self, user_input, action, reward, next_state):
        """به‌روزرسانی Q-Table با پاداش"""
        state = user_input[:50]
        q_table = self._load_q_table()

        if state not in q_table:
            q_table[state] = {
                "improve": 0.5,
                "keep": 0.5,
                "simplify": 0.5
            }

        current_q = q_table[state].get(action, 0.5)

        if next_state in q_table:
            max_next_q = max(q_table[next_state].values())
        else:
            max_next_q = 0.5

        new_q = current_q + self.learning_rate * (
            reward + self.discount_factor * max_next_q - current_q
        )

        q_table[state][action] = round(new_q, 3)
        self._save_q_table(q_table)

        return q_table

    def get_reward(self, user_input, response, source):
        """محاسبه پاداش بر اساس پاسخ"""
        reward = 0

        # ۱. اگر پاسخ از حافظه Σ بود، پاداش بیشتر
        if source == "Σ MEMORY":
            reward += 1.0

        # ۲. اگر پاسخ طولانی و مفید بود
        if len(response) > 100:
            reward += 0.5

        # ۳. اگر پاسخ شامل اطلاعات جدید بود
        if any(word in response for word in ["یاد گرفتم", "کشف کردم", "جدید"]):
            reward += 0.3

        # ۴. اگر پاسخ شامل سوال بود، جریمه
        if "?" in response or "؟" in response:
            reward -= 0.2

        # ۵. اگر پاسخ کوتاه بود
        if len(response) < 20:
            reward -= 0.5

        return max(0, reward)

    def apply_action(self, action, response):
        """اعمال اقدام روی پاسخ"""
        if action == "improve":
            return response + " (بهبود یافته)"
        elif action == "simplify":
            words = response.split()
            if len(words) > 10:
                return " ".join(words[:10]) + "..."
            return response
        else:
            return response

    def get_stats(self):
        """آمار یادگیری"""
        q_table = self._load_q_table()
        return {
            "states": len(q_table),
            "exploration_rate": self.exploration_rate,
            "learning_rate": self.learning_rate
        }

    def reset(self):
        """بازنشانی Q-Table"""
        self._save_q_table({})
        return {"success": True, "message": "Q-Table بازنشانی شد."}