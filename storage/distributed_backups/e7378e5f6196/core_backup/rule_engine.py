# ==========================================
# BOUNDLESS AI
# RULE ENGINE v1
# USER COMMAND RULE SYSTEM
# ==========================================


import os
import json
from datetime import datetime



class RuleEngine:


    def __init__(self):


        self.base_path = os.path.join(

            os.path.dirname(__file__),

            "..",

            "storage"

        )


        self.base_path = os.path.abspath(

            self.base_path

        )


        os.makedirs(

            self.base_path,

            exist_ok=True

        )


        self.rule_file = os.path.join(

            self.base_path,

            "rules.json"

        )


        self.rules = self.load_rules()






    # ======================================
    # LOAD
    # ======================================

    def load_rules(self):


        if not os.path.exists(

            self.rule_file

        ):


            return []



        try:


            with open(

                self.rule_file,

                "r",

                encoding="utf-8"

            ) as f:


                return json.load(f)



        except:


            return []







    # ======================================
    # SAVE
    # ======================================

    def save_rules(self):


        with open(

            self.rule_file,

            "w",

            encoding="utf-8"

        ) as f:


            json.dump(

                self.rules,

                f,

                ensure_ascii=False,

                indent=4

            )







    # ======================================
    # ADD RULE
    # ======================================

    def add_rule(
            self,
            rule
    ):


        for item in self.rules:


            if item["rule"] == rule:


                return {

                    "success": False,

                    "message":

                    "این قانون قبلاً وجود دارد."

                }



        new_rule = {


            "id":

            len(self.rules) + 1,


            "rule":

            rule,


            "active":

            True,


            "created":

            str(datetime.now())

        }



        self.rules.append(

            new_rule

        )


        self.save_rules()



        return {


            "success":

            True,


            "message":

            "قانون اضافه شد.",


            "rule":

            new_rule

        }








    # ======================================
    # REMOVE RULE
    # ======================================

    def remove_rule(
            self,
            rule_id
    ):


        for item in self.rules:


            if item["id"] == rule_id:


                self.rules.remove(

                    item

                )


                self.save_rules()



                return {


                    "success":

                    True,


                    "message":

                    "قانون حذف شد."

                }



        return {


            "success":

            False,


            "message":

            "قانون پیدا نشد."

        }







    # ======================================
    # GET RULES
    # ======================================

    def get_rules(self):


        return self.rules







    # ======================================
    # MATCH RULE
    # ======================================

    def match(
            self,
            text
    ):


        results = []



        for rule in self.rules:


            if not rule.get(

                "active",

                False

            ):


                continue



            if rule["rule"] in text:


                results.append(

                    rule

                )



        return results





    # ======================================
    # COMMAND PARSER
    # ======================================

    def detect_add_command(
            self,
            text
    ):


        words = [

            "قانون اضافه کن",

            "یک قانون اضافه کن",

            "قانون جدید"

        ]


        for w in words:


            if w in text:


                return True



        return False







    def extract_rule(
            self,
            text
    ):


        if ":" in text:


            return text.split(

                ":",

                1

            )[1].strip()



        if "کن" in text:


            parts = text.split(

                "کن",

                1

            )


            return parts[-1].strip()



        return None