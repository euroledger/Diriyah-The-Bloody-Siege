# Import the compilation engine from your card-generator file
from card_generator import generate_single_card


def build_game_deck():
    print("--- STARTING DECK COMPILATION ---")

    # -------------------------------------------------------------
    # CARD 3: TURKISH PHASE
    # -------------------------------------------------------------
    generate_single_card(
        card_id = 3,
        title = "ARTILLERY",
        event_text = "Add Artillery unit to all three fronts.",
        advance_marker = "W, NE, S",
        action_points = 3,
        card_type = "Turkish"
    )

        # -------------------------------------------------------------
        # CARD 30: SAUDI PHASE
        # -------------------------------------------------------------
        # generate_single_card(
        #     card_id=30,
        #     title="STORM IN SIEGE CAMP",
        #     event_text="All Ottoman artillery reduced to 2 until REINFORCEMENTS card drawn",
        #     advance_marker="NONE",
        #     action_points=4,
        #     card_type="Saudi"
        # )

        # -------------------------------------------------------------
        # CARD 4: ENTER YOUR NEXT DATA BLOCK HERE WHEN READY
        # -------------------------------------------------------------


    print("--- DECK COMPILATION COMPLETE ---")

if __name__ == "__main__":
    build_game_deck()
