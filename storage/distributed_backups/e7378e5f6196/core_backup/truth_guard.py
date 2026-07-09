# ==========================================
# BOUNDLESS AI
# TRUTH GUARD v2
# Σ MEMORY VALIDATION ENGINE
# ==========================================


import re



class TruthGuard:



    def __init__(
            self,
            memory=None
    ):

        self.memory = memory





    # ======================================
    # MAIN CHECK
    # ======================================

    def check(
            self,
            response,
            source="UNKNOWN"
    ):


        text = str(response)



        result = {

            "safe": True,

            "original": text,

            "warnings": [],

            "final": text

        }





        # ===============================
        # MEMORY CLAIM CHECK
        # ===============================


        memory_words = [

            "قبلا",

            "قبلاً",

            "ملاقات کردیم",

            "یادم هست",

            "من تو را میشناسم",

            "می‌شناسم"

        ]



        for word in memory_words:


            if word in text:


                if source != "Σ MEMORY":


                    result["safe"] = False


                    result["warnings"].append(

                        "possible_false_memory"

                    )


                    result["final"] = (

                        "من چنین خاطره‌ای در "

                        "حافظه Σ ندارم."

                    )


                    return result







        # ===============================
        # WEATHER CHECK
        # ===============================


        weather_words = [

            "هوا سرد است",

            "هوا گرم است",

            "هوا خوب است",

            "باران می‌بارد",

            "آفتابی است"

        ]



        for word in weather_words:


            if word in text:


                if source == "GROQ":


                    result["safe"] = False


                    result["warnings"].append(

                        "requires_verification"

                    )


                    result["final"] = (

                        "من اطلاعات تایید شده‌ای "

                        "درباره وضعیت هوا ندارم."

                    )


                    return result








        # ===============================
        # CONFIDENCE CHECK
        # ===============================


        uncertain = [

            "قطعا",

            "مطمئن هستم",

            "صددرصد",

            "همیشه"

        ]



        for word in uncertain:


            if word in text:


                result["warnings"].append(

                    "strong_claim"

                )



        return result







    # ======================================
    # MEMORY VALIDATION
    # ======================================

    def validate_memory(
            self,
            claim
    ):


        if not self.memory:


            return False



        try:


            context = self.memory.get_context()



            data = str(context)



            if claim in data:


                return True



        except:


            pass



        return False







    # ======================================
    # CLEAN RESPONSE
    # ======================================

    def sanitize(
            self,
            response,
            source
    ):


        checked = self.check(

            response,

            source

        )


        return checked["final"]







    # ======================================
    # TEST
    # ======================================

if __name__ == "__main__":


    guard = TruthGuard()



    print(

        guard.check(

            "ما قبلا ملاقات کردیم",

            "GROQ"

        )

    )



    print(

        guard.check(

            "هوا سرد است",

            "GROQ"

        )

    )



    print(

        guard.check(

            "تو حامد هستی",

            "Σ MEMORY"

        )

    )