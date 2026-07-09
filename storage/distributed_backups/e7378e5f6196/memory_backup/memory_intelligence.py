# ==========================================
# BOUNDLESS AI
# MEMORY INTELLIGENCE v4
# Σ STRUCTURED MEMORY CORE
# ==========================================


import os
import json
from datetime import datetime



class MemoryIntelligence:



    def __init__(self):


        self.base_path = os.path.join(

            os.path.dirname(__file__),

            "storage"

        )


        os.makedirs(

            self.base_path,

            exist_ok=True

        )



        self.short_file = os.path.join(

            self.base_path,

            "short_memory.json"

        )


        self.long_file = os.path.join(

            self.base_path,

            "long_memory.json"

        )



        self.short_memory = self.load(

            self.short_file

        )


        self.long_memory = self.load(

            self.long_file

        )





    # ======================================
    # LOAD
    # ======================================

    def load(self, path):


        if not os.path.exists(path):

            return []



        try:

            with open(

                path,

                "r",

                encoding="utf-8"

            ) as f:

                return json.load(f)



        except:


            return []





    # ======================================
    # SAVE
    # ======================================

    def save(
            self,
            path,
            data
    ):


        with open(

            path,

            "w",

            encoding="utf-8"

        ) as f:


            json.dump(

                data,

                f,

                ensure_ascii=False,

                indent=4

            )





    # ======================================
    # REMEMBER v4
    # ======================================

    def remember(
            self,
            user,
            assistant,
            metadata=None
    ):


        item = {


            "user": user,


            "assistant": assistant,


            "time": str(datetime.now()),


            "importance":

            self.calculate_importance(user),


            "analysis":

            {},


            "type":

            "general"

        }



        # اضافه کردن تحلیل Memory Manager

        if isinstance(metadata, dict):


            item.update({

                "analysis":

                metadata.get(

                    "analysis",

                    {}

                ),


                "type":

                metadata.get(

                    "type",

                    "general"

                ),


                "importance":

                metadata.get(

                    "importance",

                    item["importance"]

                ),


                "confidence":

                metadata.get(

                    "confidence",

                    0.5

                )

            })





        # جلوگیری از تکرار متن

        for old in self.long_memory + self.short_memory:


            if (

                old.get("user")

                ==

                item.get("user")

            ):


                return {


                    "stored": False,


                    "type": "duplicate"

                }





        # ذخیره بر اساس اهمیت


        if item["importance"] >= 2:


            self.long_memory.append(item)


            self.save(

                self.long_file,

                self.long_memory

            )


            return {


                "stored": True,


                "type": "long_memory",


                "importance":

                item["importance"]

            }





        else:


            self.short_memory.append(item)


            self.save(

                self.short_file,

                self.short_memory

            )


            return {


                "stored": True,


                "type": "short_memory",


                "importance":

                item["importance"]

            }







    # ======================================
    # IMPORTANCE
    # ======================================

    def calculate_importance(
            self,
            text
    ):


        score = 0



        keywords = [


            "اسم",

            "نام",

            "من هستم",

            "هستم",

            "علاقه",

            "دوست دارم",

            "پروژه",

            "می سازم",

            "کار"


        ]



        for word in keywords:


            if word in text:


                score += 1



        return score






    # ======================================
    # SAVE LONG
    # ======================================

    def save_long_memory(
            self,
            data
    ):


        data["time"] = str(datetime.now())


        self.long_memory.append(data)


        self.save(

            self.long_file,

            self.long_memory

        )



        return True





    # ======================================
    # CONTEXT
    # ======================================

    def get_context(self):


        return {


            "long_memory":

            self.long_memory,


            "short_memory":

            self.short_memory[-10:]


        }





    # ======================================
    # CLEAR (FOR TEST)
    # ======================================

    def clear(self):


        self.short_memory = []

        self.long_memory = []


        self.save(

            self.short_file,

            []

        )


        self.save(

            self.long_file,

            []

        )



        return True





if __name__ == "__main__":


    memory = MemoryIntelligence()


    print(

        memory.remember(

            "سلام من حامد هستم",

            "خوش آمدی حامد",

            metadata={

                "type":"identity",

                "importance":5

            }

        )

    )


    print(

        memory.get_context()

    )