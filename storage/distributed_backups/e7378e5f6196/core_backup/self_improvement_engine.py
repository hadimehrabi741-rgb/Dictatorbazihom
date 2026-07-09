# ==========================================
# BOUNDLESS AI
# SELF IMPROVEMENT ENGINE v2
# RULE MANAGEMENT CORE
# ==========================================


import os
import json
from datetime import datetime



class SelfImprovementEngine:



    def __init__(self):


        self.base_path = os.path.join(

            os.path.dirname(__file__),

            "..",

            "memory"

        )


        os.makedirs(

            self.base_path,

            exist_ok=True

        )


        self.file = os.path.join(

            self.base_path,

            "knowledge_memory.json"

        )


        self.rules = self.load()





    # ======================================
    # LOAD
    # ======================================

    def load(self):


        if not os.path.exists(self.file):

            return []



        try:

            with open(

                self.file,

                "r",

                encoding="utf-8"

            ) as f:


                return json.load(f)



        except:


            return []







    # ======================================
    # SAVE
    # ======================================

    def save(self):


        with open(

            self.file,

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
            rule_text
    ):


        # جلوگیری از تکرار

        for rule in self.rules:


            if rule["rule"] == rule_text:


                return {

                    "success": False,

                    "message": "این قانون قبلا وجود دارد"

                }





        new_id = 1



        if self.rules:


            new_id = max(

                r["id"]

                for r in self.rules

            ) + 1





        rule = {


            "id": new_id,


            "rule": rule_text,


            "active": True,


            "created":

            str(datetime.now())

        }



        self.rules.append(rule)


        self.save()



        return {


            "success": True,

            "message": "قانون اضافه شد",

            "rule": rule

        }








    # ======================================
    # LIST RULES
    # ======================================

    def list_rules(self):


        return self.rules







    # ======================================
    # DELETE RULE
    # ======================================

    def delete_rule(
            self,
            rule_id
    ):


        before = len(self.rules)



        self.rules = [

            r for r in self.rules

            if r["id"] != rule_id

        ]



        self.save()



        if len(self.rules) < before:


            return {


                "success": True,

                "message":

                f"قانون {rule_id} حذف شد"

            }



        return {


            "success": False,

            "message":

            "قانون پیدا نشد"

        }







    # ======================================
    # ENABLE RULE
    # ======================================

    def enable_rule(
            self,
            rule_id
    ):


        for rule in self.rules:


            if rule["id"] == rule_id:


                rule["active"] = True


                self.save()



                return True



        return False







    # ======================================
    # DISABLE RULE
    # ======================================

    def disable_rule(
            self,
            rule_id
    ):


        for rule in self.rules:


            if rule["id"] == rule_id:


                rule["active"] = False


                self.save()



                return True



        return False







    # ======================================
    # FIND ACTIVE RULE
    # ======================================

    def find_rule(
            self,
            text
    ):


        results = []



        text = str(text)



        for rule in self.rules:


            if not rule["active"]:

                continue



            words = rule["rule"].split()



            for word in words:


                if word in text:


                    results.append(rule)

                    break



        return results







    # ======================================
    # DETECT COMMAND
    # ======================================

    def detect_learning_command(
            self,
            text
    ):


        commands = [

            "قانون جدید",

            "اضافه کن",

            "یاد بگیر",

            "به ساختار اضافه کن"

        ]



        for c in commands:


            if c in text:


                return True



        return False







    # ======================================
    # PARSE ADD COMMAND
    # ======================================

    def extract_rule(
            self,
            text
    ):


        text = str(text)



        for key in [

            "قانون جدید:",

            "قانون جدید",

            "یاد بگیر"

        ]:


            if key in text:


                return text.split(

                    key,

                    1

                )[1].strip()



        return None







# ==========================================
# TEST
# ==========================================


if __name__ == "__main__":


    engine = SelfImprovementEngine()



    print(

        engine.add_rule(

            "وقتی گفتم گزارش بده حافظه را نمایش بده"

        )

    )



    print(

        engine.list_rules()

    )