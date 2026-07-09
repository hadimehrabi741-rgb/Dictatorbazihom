# ==========================================
# BOUNDLESS AI
# ACTION ENGINE v5
# SMART COMMAND EXECUTION
# MEMORY CONTROL SYSTEM
# ==========================================


class ActionEngine:


    def __init__(
            self,
            memory=None,
            manager=None
    ):

        self.memory = memory
        self.manager = manager





    # ======================================
    # DETECT
    # ======================================

    def detect(
            self,
            rule,
            user_input
    ):


        rule_text = str(rule).lower()

        text = str(user_input).lower()



        # ===============================
        # REPORT MEMORY
        # ===============================

        if (
            "گزارش" in rule_text
            and
            "حافظه" in rule_text
        ):


            if (
                "گزارش" in text
                or
                text == "حافظه"
            ):


                return {

                    "action":
                    "show_memory",

                    "matched":
                    True

                }





        # ===============================
        # CLEAN ALL MEMORY
        # ===============================

        if (

            "پاکسازی حافظه" in text

            or

            "پاک سازی حافظه" in text

            or

            "پاک کن حافظه" in text

        ):


            return {

                "action":
                "clean_memory",

                "matched":
                True

            }







        # ===============================
        # CLEAR SHORT MEMORY
        # ===============================

        if (

            "پاک کردن حافظه کوتاه" in text

            or

            "پاکسازی کوتاه مدت" in text

        ):


            return {

                "action":
                "clear_short",

                "matched":
                True

            }




        return {

            "action":
            None,

            "matched":
            False

        }







    # ======================================
    # EXECUTE
    # ======================================

    def execute(
            self,
            action
    ):


        if action == "show_memory":

            return self.show_memory()



        if action == "clean_memory":

            return self.clean_memory()



        if action == "clear_short":

            return self.clear_short_memory()




        return "عملیات ناشناخته"









    # ======================================
    # SHOW MEMORY
    # ======================================

    def show_memory(self):


        if self.manager:

            self.manager.clean_duplicates()



        if not self.memory:

            return "حافظه Σ فعال نیست."




        context = self.memory.get_context()



        long_memory = context.get(

            "long_memory",

            []

        )



        short_memory = context.get(

            "short_memory",

            []

        )



        result = "گزارش حافظه Σ:\n\n"



        groups = {


            "identity":
            "هویت",


            "preference":
            "علاقه‌ها",


            "project":
            "پروژه‌ها",


            "general":
            "عمومی"

        }





        for key,title in groups.items():


            result += title + ":\n"


            found = False

            seen = set()



            for item in long_memory:



                if not isinstance(item,dict):

                    continue



                text = item.get(

                    "memory",

                    ""

                ).strip()



                mtype = item.get(

                    "type",

                    "general"

                )



                if text in seen:

                    continue



                if mtype == key:


                    result += "- " + text + "\n"

                    seen.add(text)

                    found = True





            if not found:

                result += "ندارد\n"



            result += "\n"






        result += "حافظه کوتاه مدت:\n"



        if short_memory:


            for item in short_memory:

                result += "- " + str(item) + "\n"


        else:

            result += "خالی\n"




        return result







    # ======================================
    # CLEAN MEMORY
    # ======================================

    def clean_memory(self):


        if not self.memory:

            return "حافظه Σ فعال نیست."



        self.memory.long_memory = []

        self.memory.short_memory = []



        self.memory.save(

            self.memory.long_file,

            []

        )


        self.memory.save(

            self.memory.short_file,

            []

        )



        return "تمام حافظه Σ پاک شد."









    # ======================================
    # CLEAR SHORT MEMORY
    # ======================================

    def clear_short_memory(self):


        if not self.memory:

            return "حافظه فعال نیست."



        self.memory.short_memory = []



        self.memory.save(

            self.memory.short_file,

            []

        )


        return "حافظه کوتاه مدت پاک شد."