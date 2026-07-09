# ==========================================
# BOUNDLESS AI
# MEMORY REASONER v2.1
# COMPATIBILITY PATCH
# ==========================================


from datetime import datetime



class MemoryReasoner:


    def __init__(self, memory=None):

        self.memory = memory





    # ======================================
    # PREPARE
    # compatibility with MemoryManager
    # ======================================

    def prepare(
            self,
            user_text,
            assistant_text=""
    ):


        return self.build_memory(

            user_text,

            assistant_text

        )







    # ======================================
    # ANALYZE
    # ======================================

    def analyze(
            self,
            text
    ):


        text = self.normalize(text)



        result = {

            "text": text,

            "type": "general",

            "importance":0,

            "confidence":0.5,

            "timestamp":str(datetime.now())

        }



        if "من " in text and " هستم" in text:


            result["type"]="identity"

            result["importance"]=5

            result["confidence"]=0.95



        elif (

            "علاقه" in text

            or

            "دوست دارم" in text

        ):


            result["type"]="preference"

            result["importance"]=4

            result["confidence"]=0.9




        elif (

            "پروژه" in text

        ):


            result["type"]="project"

            result["importance"]=4

            result["confidence"]=0.85



        return result






    # ======================================
    # NORMALIZE
    # ======================================

    def normalize(self,text):


        fixes={

            "یرنامه":"برنامه",

            "برنامه‌ نویسی":"برنامه نویسی"

        }



        for a,b in fixes.items():

            text=text.replace(a,b)



        return text







    # ======================================
    # BUILD MEMORY
    # ======================================

    def build_memory(
            self,
            user_text,
            assistant_text=""
    ):


        analysis=self.analyze(user_text)



        return {


            "memory":

                analysis["text"],


            "type":

                analysis["type"],


            "importance":

                analysis["importance"],


            "confidence":

                analysis["confidence"],


            "assistant":

                assistant_text,


            "store":

                analysis["importance"] >= 2

        }







    # ======================================
    # STORE CHECK
    # ======================================

    def should_store(
            self,
            data
    ):


        return data.get(

            "importance",

            0

        ) >= 2