# ==========================================
# BOUNDLESS AI
# MEMORY MANAGER v8
# SMART CLASSIFICATION + STRICT MEMORY
# ==========================================


from datetime import datetime



class MemoryManager:


    def __init__(
            self,
            memory=None,
            reasoner=None
    ):

        self.memory = memory
        self.reasoner = reasoner




    # ======================================
    # STORE
    # ======================================

    def store(
            self,
            user_input,
            assistant_response="",
            memory_type=None
    ):


        text = str(user_input).strip()


        if not text:

            return {
                "stored": False,
                "reason": "empty"
            }



        if self.is_question(text):

            return {
                "stored": False,
                "reason": "question"
            }




        self.clean_duplicates()



        if self.exists(text):

            return {
                "stored": False,
                "reason": "duplicate"
            }





        item = {

            "memory": text,

            "type":
            memory_type
            if memory_type
            else self.detect_type(text),

            "time":
            str(datetime.now()),

            "confidence":
            0.95

        }





        if self.memory:


            self.memory.save_long_memory(
                item
            )


            return {

                "stored": True,

                "type":
                item["type"]

            }



        return {

            "stored": False,

            "reason":
            "no_memory"

        }








    # ======================================
    # EXIST
    # ======================================

    def exists(
            self,
            text
    ):


        if not self.memory:

            return False



        for item in self.memory.long_memory:


            if isinstance(item,dict):


                old = item.get(
                    "memory",
                    ""
                ).strip()



                if old == text.strip():

                    return True



        return False








    # ======================================
    # TYPE DETECTOR v8
    # ======================================

    def detect_type(
            self,
            text
    ):


        t = text.strip()



        # هویت

        identity_words = [

            "من حامدم",

            "من حامد هستم",

            "سلام من حامدم",

            "سلام من حامد هستم",

            "اسم من",

            "نام من"

        ]


        for w in identity_words:

            if w in t:

                return "identity"







        # علاقه


        preference_words = [

            "علاقه دارم",

            "دوست دارم",

            "علاقه‌مندم"

        ]


        for w in preference_words:

            if w in t:

                return "preference"







        # پروژه


        project_words = [

            "پروژه",

            "میسازم",

            "می‌سازم",

            "در حال ساخت"

        ]


        for w in project_words:

            if w in t:

                return "project"






        return "general"









    # ======================================
    # QUESTION FILTER
    # ======================================

    def is_question(
            self,
            text
    ):


        words = [

            "چرا",

            "چطور",

            "چگونه",

            "چیست",

            "؟"

        ]


        for w in words:

            if w in text:

                return True



        return False







    # ======================================
    # CLEAN DUPLICATE
    # ======================================

    def clean_duplicates(self):


        if not self.memory:

            return False



        result = []

        seen = set()



        for item in self.memory.long_memory:


            if not isinstance(item,dict):

                continue



            text = item.get(
                "memory",
                ""
            ).strip()



            if not text:

                continue



            if text not in seen:


                seen.add(text)

                result.append(item)





        self.memory.long_memory = result


        self.memory.save(

            self.memory.long_file,

            result

        )


        return True