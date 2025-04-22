# tests/test_discard.py

from core.player import GameState
from env.rules_engine import RulesEngine
from core.card import Card

def test_discard_card():
    game_state = GameState()
    rules = RulesEngine(game_state)

    # Setup iniziale
    card1 = Card("Energia_Erba", "Energy")
    card2 = Card("Energia_Fuoco", "Energy")
    game_state.hand = [card1, card2]

    # Test scartare una carta valida
    assert rules.validate_action("discard Energia_Erba") is True
    rules.apply_action("discard Energia_Erba")
    assert len(game_state.hand) == 1
    assert len(game_state.discard_pile) == 1
    assert game_state.discard_pile[0].name == "Energia_Erba"

    # Test scartare una carta non presente
    assert rules.validate_action("discard Energia_Acqua") is False


if __name__ == "__main__":
    test_discard_card()