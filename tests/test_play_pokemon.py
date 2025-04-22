# tests/test_play_pokemon.py

from core.player import GameState
from env.rules_engine import RulesEngine
from core.card import PokemonCard,RagingBoltPokemonCard

def test_play_pokemon():
    game_state = GameState()
    rules = RulesEngine(game_state)

    # Setup iniziale
    pikachu = PokemonCard("Pikachu", 60, [("Thunderbolt", 50)], 1)
    bulbasaur = PokemonCard("Bulbasaur", 70, [("Vine Whip", 40)], 1)
    game_state.hand = [pikachu, bulbasaur]

    # Test giocare un Pokémon in panchina
    assert rules.validate_action("play_pokemon Pikachu bench") is True
    rules.apply_action("play_pokemon Pikachu bench")
    assert len(game_state.bench) == 1
    assert game_state.bench[0].name == "Pikachu"
    assert len(game_state.hand) == 1

    # Test giocare un Pokémon come attivo
    assert rules.validate_action("play_pokemon Bulbasaur active") is True
    rules.apply_action("play_pokemon Bulbasaur active")
    assert game_state.active_pokemon.name == "Bulbasaur"
    assert len(game_state.hand) == 0

    # Test giocare un Pokémon in panchina con panchina piena
    game_state.bench = [PokemonCard(f"Benchmon{i}", 50, [], 1) for i in range(5)]
    assert rules.validate_action("play_pokemon Pikachu bench") is False

    # Test giocare un Pokémon come attivo con posizione attiva occupata
    assert rules.validate_action("play_pokemon Pikachu active") is False
    
if __name__ == "__main__":
    RagingBoltPokemonCard()
