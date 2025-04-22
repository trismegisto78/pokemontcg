from core.trainers import ProfessorSadaVitalityTrainerCard, IonoTrainerCard
from core.pokemons import RagingBoltPokemonCard
from core.card import EnergyCard
from core.play_turn_actions import play_supporter, assegna_attivo


def test_sada(player1,player2):
    if not player1.active_pokemon:
        assegna_attivo(player1,player2)
    
    sada = ProfessorSadaVitalityTrainerCard(100)
    player1.hand.append(sada)
    player1.bench.append(RagingBoltPokemonCard(101))
    player1.bench.append(RagingBoltPokemonCard(101))
    player1.discard_pile.append(EnergyCard(102,"SVE9","Energia_Erba"))
    player1.discard_pile.append(EnergyCard(102,"SVE9","Energia_Erba"))
    
    player1.debug_game_state()
    play_supporter(player1,sada.code,player2)
    player1.debug_game_state()
    return True


def test_iono(player1,player2):
    if not player1.active_pokemon:
        assegna_attivo(player1,player2)
    
    iono = IonoTrainerCard(100)
    player1.hand=[]
    player1.hand.append(iono)
    player1.prizes.pop(0)
    player1.bench.append(RagingBoltPokemonCard(101))
    player1.discard_pile.append(EnergyCard(102,"SVE9","Energia_Erba"))
    player1.discard_pile.append(EnergyCard(102,"SVE9","Energia_Erba"))
    
    player1.debug_game_state()
    play_supporter(player1,iono.code,player2)
    player1.debug_game_state()
    return True