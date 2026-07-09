# ==========================================
# BOUNDLESS AI
# MEMORY RETRIEVAL v4
# SMART Σ CONTEXT FILTER
# ==========================================


class MemoryRetrieval:


    def __init__(
            self,
            memory=None
    ):

        self.memory = memory





    # ======================================
    # LOAD
    # ======================================

    def load_memory(self):


        if not self.memory:

            return []



        try:

            context = self.memory.get_context()


            data = []


            data.extend(
                context.get(
                    "long_memory",
                    []
                )
            )


            data.extend(
                context.get(
                    "short_memory",
                    []
                )
            )


            return data


        except Exception:


            return []







    # ======================================
    # TEXT EXTRACT
    # ======================================

    def extract_text(
            self,
            item
    ):


        if isinstance(item,str):

            return item.strip()



        if isinstance(item,dict):

            return str(
                item.get(
                    "memory",
                    ""
                )
            ).strip()



        return ""








    # ======================================
    # CLEAN
    # ======================================

    def clean(
            self,
            text
    ):


        words = [

            "ثبت شد",

            "ذخیره شد",

            "در حافظه Σ",

            "هویت ثبت شد",

            "علاقه ثبت شد"

        ]


        for word in words:


            text = text.replace(
                word,
                ""
            )


        return text.strip()








    # ======================================
    # SHOULD USE MEMORY
    # ======================================

    def should_use_memory(
            self,
            query
    ):


        q = str(query).lower()



        triggers = [


            "من کی هستم",

            "کی هستم",

            "اسم من",

            "نام من",

            "حافظه من",

            "علاقه من",

            "چه علاقه",

            "پروژه من",

            "پروژه‌ام",

            "در مورد من"

        ]



        for item in triggers:


            if item in q:

                return True



        return False








    # ======================================
    # CONTEXT
    # ======================================

    def get_context(
            self,
            query=None
    ):


        result = {


            "identity": [],

            "preferences": [],

            "projects": [],

            "facts": []

        }




        # بدون درخواست، حافظه نده

        if query and not self.should_use_memory(query):


            return result





        for item in self.load_memory():


            text = self.clean(

                self.extract_text(item)

            )



            if not text:

                continue



            lower = text.lower()



            # ======================
            # IDENTITY
            # ======================

            if (

                "من حامد" in text

                or

                "اسم من" in text

                or

                "نام من" in text

            ):


                result["identity"].append(
                    text
                )

                continue






            # ======================
            # PREFERENCE
            # ======================

            if (

                "علاقه" in text

                or

                "دوست دارم" in text

            ):


                result["preferences"].append(
                    text
                )

                continue






            # ======================
            # PROJECT
            # ======================

            if "پروژه" in text:


                result["projects"].append(
                    text
                )

                continue






            result["facts"].append(
                text
            )







        for key in result:


            result[key] = list(
                dict.fromkeys(
                    result[key]
                )
            )



        return result







    # ======================================
    # SEARCH
    # ======================================

    def search(
            self,
            query
    ):


        data = self.get_context(query)



        q = str(query)



        if "کی هستم" in q:

            return data["identity"]



        if "علاقه" in q:

            return data["preferences"]



        if "پروژه" in q:

            return data["projects"]



        return []







    # ======================================
    # GROQ CONTEXT
    # ======================================

    def groq_context(
            self,
            query
    ):


        data = self.get_context(query)



        output = []



        for key in [

            "identity",

            "preferences",

            "projects",

            "facts"

        ]:


            output.extend(

                data[key]

            )



        return output