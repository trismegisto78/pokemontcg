# tests/test_play_trainer.py

from core.player import GameState
from env.rules_engine import RulesEngine
from core.card import TrainerCard

def test_play_trainer():
    game_state = GameState()
    rules = RulesEngine(game_state)

    # Setup iniziale
    def draw_effect(game_state):
        print("Effetto: pesca 2 carte.")
        
        # Setup iniziale
    def draw7_effect(game_state):
        print("Effetto: pesca 7 carte.")
    
    item_card = TrainerCard("Nest_Ball", "Item", draw_effect)
    supporter_card = TrainerCard("Professor_s_Research", "Supporter", draw7_effect)
    stadium_card = TrainerCard("Pokémon_Stadium", "Stadium", lambda gs: print("Effetto Stadio."))

    game_state.hand = [item_card, supporter_card, stadium_card]

    # Test giocare una carta Strumento
    assert rules.validate_action("play_trainer Nest_Ball") is True
    rules.apply_action("play_trainer Nest_Ball")
    assert len(game_state.hand) == 2
    assert len(game_state.discard_pile) == 1

    # Test giocare una carta Aiuto
    assert rules.validate_action("play_trainer Professor_s_Research") is True
    rules.apply_action("play_trainer Professor_s_Research")
    assert game_state.supporter_played is True

    # Test giocare una seconda carta Aiuto
    assert rules.validate_action("play_trainer Professor_s_Research") is False

    # Test giocare una carta Stadio
    assert rules.validate_action("play_trainer Pokémon_Stadium") is True
    rules.apply_action("play_trainer Pokémon_Stadium")
    assert game_state.stadium_card.name == "Pokémon_Stadium"
    
    
if __name__ == "__main__":
    test_play_trainer()
