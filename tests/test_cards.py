# tests/test_cards.py
from core.player import GameState
from env.rules_engine import RulesEngine
from core.card import PokemonCard,Card
from core.abilities import teal_dance, burst_roar

def test_teal_dance():
    game_state = GameState()
    teal_mask = PokemonCard(
        "Teal Mask Ogerpon ex",
        210,
        [("Myriad Leaf Shower", 30)],
        2,
        ability=teal_dance
    )
    game_state.hand = [Card("Energia Erba", "Energy")]
    game_state.deck = [Card("Test Card", "Trainer")]

    assert teal_mask.activate_ability(game_state) is True
    assert len(teal_mask.attached_energies) == 1
    assert len(game_state.hand) == 1

def test_burst_roar():
    game_state = GameState()
    raging_bolt = PokemonCard(
        "Raging Bolt ex",
        240,
        [("Burst Roar", 0)],
        1,
        ability=burst_roar
    )
    game_state.hand = [Card("Test Card", "Trainer")]
    game_state.deck = [Card(f"Card {i}", "Trainer") for i in range(6)]

    assert raging_bolt.activate_ability(game_state) is True
    assert len(game_state.hand) == 6
    
if __name__ == "__main__":
    print("Teal Dance")
    test_teal_dance()
    print("test_burst_roar")
    test_burst_roar()
