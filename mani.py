# ==========================================
# BOUNDLESS AI
# MAIN LAUNCHER
# ==========================================

import sys
import os


BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)


if BASE_DIR not in sys.path:

    sys.path.insert(
        0,
        BASE_DIR
    )



from interface.chat import BoundlessChat



def main():

    print(
        "=========================================="
    )

    print(
        "        BOUNDLESS AI START"
    )

    print(
        "=========================================="
    )


    try:

        app = BoundlessChat()

        app.start()


    except Exception as e:

        print(
            "SYSTEM ERROR:"
        )

        print(e)



if __name__ == "__main__":

    main()