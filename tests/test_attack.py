# tests/test_attack_system.py

from core.player import GameState
from env.rules_engine import RulesEngine
from core.card import PokemonCard
from core.pokemons import RagingBoltPokemonCard

def test_attack():
    game_state = GameState()
    rules = RulesEngine(game_state)

    # Setup iniziale
    attacker = PokemonCard("Teal_Mask_Ogerpon_ex", 210, [("Myriad_Leaf_Shower", 30, 2)], 2, weakness="Fire", resistance="Water")
    defender = PokemonCard("Raging_Bolt_ex", 240, [("Burst_Roar", 0)], 1, weakness="Grass", resistance="Electric")

    game_state.active_pokemon = attacker
    game_state.opponent_active_pokemon = defender

    # Assegna Energie
    attacker.attached_energies = ["Energia_Erba", "Energia_Erba"]

    # Test attacco valido
    assert rules.validate_action("attack Myriad_Leaf_Shower") is True
    rules.apply_action("attack Myriad_Leaf_Shower")
    print(f"defender.hp {defender.hp}")
    assert defender.hp == 210  # Danno base di 30

    # Test KO
    defender.hp = 30
    rules.apply_action("attack Myriad_Leaf_Shower")
    assert game_state.opponent_active_pokemon is None
    
if __name__ == "__main__":
    player = GameState()
    player.reset()
    
    player2 = GameState()
    player2.reset()
    
    ragbolt = RagingBoltPokemonCard()
    attacker = RagingBoltPokemonCard()
    attacker.execute_attack(player, player2)
    