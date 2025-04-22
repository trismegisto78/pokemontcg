# tests/test_assign_energy.py

from core.player import GameState
from core.card import EnergyCard

if __name__ == "__main__":
    player = GameState()
    opponent = GameState()
    
    player.reset(opponent)
    player.setup_active_and_bench()
    player.debug_game_state()
    
    opponent.reset(player)
    opponent.setup_active_and_bench()

    for card in player.hand:
        if isinstance(card, EnergyCard):
            player.assign_energy(card.code, player.active_pokemon)
            break;
        
    player.reset_turn()
    
    for card in player.hand:
        if isinstance(card, EnergyCard):
            player.assign_energy(card.code, player.active_pokemon)
            break;
    
    print(f"{player.active_pokemon.attached_energies}")