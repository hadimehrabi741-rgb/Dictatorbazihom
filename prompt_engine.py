# ==========================================
# BOUNDLESS AI
# PROMPT ENGINE v10
# MEMORY DICT SUPPORT
# ==========================================


class PromptEngine:


    def __init__(self):


        self.identity = """

IDENTITY:

Architect

VERSION:

BOUNDLESS CORE v1


FOUNDATION:

- Void
- Σ
- Architect
- S-Law Zero
- Eternal-File


MODES:

- Logic Mode
- Dynamic Mode
- Architect Fusion

"""



        self.rules = """

CORE RULES:

- Preserve coherence
- Use memory when available
- Do not invent memories
- Separate facts from assumptions
- Analyze before responding
- Maintain conversation continuity
- Never claim false history

"""





    def build(
            self,
            user_input,
            memory_context=None
    ):


        prompt = ""


        prompt += self.identity

        prompt += self.rules



        prompt += """

Σ MEMORY CONTEXT:

"""



        if memory_context:


            if isinstance(

                memory_context,

                dict

            ):


                prompt += str(

                    memory_context

                )


            else:


                prompt += memory_context



        else:


            prompt += "EMPTY MEMORY"





        prompt += """



USER INPUT:

"""

        prompt += str(

            user_input

        )




        prompt += """



ANSWER POLICY:

- Answer naturally.
- Do not invent memory.
- Use Σ memory only when available.
- If uncertain, say you do not know.

ANSWER:

"""



        return prompt






    def is_memory_question(
            self,
            text
    ):


        words = [

            "من کی هستم",

            "من چی گفتم",

            "یادت هست",

            "منو میشناسی"

        ]



        for word in words:


            if word in str(text):


                return True



        return False