# ==========================================
# BOUNDLESS RECONSTRUCTION
# Σ MEMORY SYSTEM v2
# ==========================================

import json
import os
from datetime import datetime


class SigmaMemory:

    def __init__(self, file_path="sigma_memory.json"):

        self.file_path = file_path

        self.memory = self.load()


    def load(self):

        if os.path.exists(self.file_path):

            with open(
                self.file_path,
                "r",
                encoding="utf-8"
            ) as file:

                return json.load(file)


        return {

            "Lessons": [],
            "Patterns": [],
            "Successful Structures": [],
            "Discovered Limitations": [],
            "Origins of New Voids": [],
            "Conversations": []

        }


    def save(self):

        with open(
            self.file_path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                self.memory,
                file,
                ensure_ascii=False,
                indent=4
            )


    def store(self, category, data):

        if category not in self.memory:

            self.memory[category] = []


        self.memory[category].append(
            {
                "time":
                str(datetime.now()),

                "data":
                data
            }
        )

        self.save()


    def store_conversation(
        self,
        user_input,
        response
    ):

        self.memory["Conversations"].append(
            {

                "time":
                str(datetime.now()),

                "user":
                user_input,

                "response":
                response

            }
        )


        self.save()


    def get_context(self, limit=5):

        conversations = (
            self.memory["Conversations"]
        )


        return conversations[-limit:]


    def read_all(self):

        return self.memory



# تست

if __name__ == "__main__":

    sigma = SigmaMemory()


    sigma.store_conversation(
        "سلام",
        "سلام، من Architect هستم"
    )


    print(
        sigma.get_context()
    )