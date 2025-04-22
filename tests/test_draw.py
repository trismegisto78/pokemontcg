# tests/test_draw.py

from core.player import GameState
from env.rules_engine import RulesEngine

def test_dynamic_draw():
    game_state = GameState()
    rules = RulesEngine(game_state)
    game_state.reset(5)

   
    assert rules.validate_action("draw 3") is True
    rules.apply_action("draw 3")
    assert len(game_state.deck) == 2
    assert len(game_state.hand) == 3

    # Test draw con numero maggiore delle carte nel mazzo
    assert rules.validate_action("draw 10") is False

    # Test draw senza numero
    assert rules.validate_action("draw") is False
    
    
if __name__ == "__main__":
    test_dynamic_draw()

