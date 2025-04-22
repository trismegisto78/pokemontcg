
from core.card import EnergyCard, PokemonBaseCard, TrainerCard,\
    PokemonStage1Card, PokemonCard, PokemonStage2Card
import random
from core.utils import mprint
import time
from core.pokemons_charizard_ex import CharmanderPokemonCard,\
    CharmeleonPokemonCard, CharizardExPokemonCard


def choose_for_active_pokemon_from_hand(player,opponent_player):
    base_pokemon = [card for card in player.hand if isinstance(card, PokemonBaseCard) ]
    if base_pokemon:
        chosen_index = random.randint(0, len(base_pokemon) - 1)
        chosen_pokemon = base_pokemon[chosen_index]
        mprint(f"Pokémon Base scelto: {chosen_pokemon.name}")
        return chosen_pokemon.code
    else:
        mprint("Nessun Pokémon Base disponibile nella mano.")
        return None
    
def choose_for_active_pokemon_from_bench(player,opponent_player):
    base_pokemon = [card for card in player.bench if isinstance(card, PokemonCard) ]
    if base_pokemon:
        chosen_index = random.randint(0, len(base_pokemon) - 1)
        chosen_pokemon = base_pokemon[chosen_index]
        mprint(f"Pokémon Base scelto: {chosen_pokemon.name}")
        return chosen_pokemon.code
    else:
        mprint("Nessun Pokémon Base disponibile in panchina.")
        return None
    

# carte attive
def assign_active_pokemon_from_hand(player,chosen_pokemon_code,opponent_player):
    mprint(f"Array hand {player.hand}")
    chosen_index = next((i for i, card in enumerate(player.hand) if isinstance(card,PokemonBaseCard) and card.code == chosen_pokemon_code), None)
    
    if chosen_index is not None:
        mprint(f"L'indice dell'elemento con code '{chosen_pokemon_code}' è: {chosen_index}")
    else:
        mprint(f"Nessun elemento trovato con code '{chosen_pokemon_code}'.")
    
    player.active_pokemon=player.hand[chosen_index]
    player.hand.pop(chosen_index)
    
# carte attive
def assign_active_pokemon_from_bench(player,chosen_pokemon_code,opponent_player):
    chosen_index = next((i for i, card in enumerate(player.bench) if isinstance(card,PokemonCard) and card.code == chosen_pokemon_code), None)
    
    if chosen_index is not None:
        mprint(f"L'indice dell'elemento con code '{chosen_pokemon_code}' è: {chosen_index}")
    else:
        mprint(f"Nessun elemento trovato con code '{chosen_pokemon_code}'.")
    
    player.active_pokemon=player.bench[chosen_index]
    player.bench.pop(chosen_index)
    
    
def can_assign_turn_energy(player):
    return (not player.energy_attached_this_turn and len([card for card in player.hand if isinstance(card, EnergyCard) ])>0),0

def do_i_have_energy_to_assign(player):
    hand_energies = [card for card in player.hand if isinstance(card, EnergyCard) ]
    if hand_energies:
        return True
    else:
        return False
   
# determina se assegnare l'energia
def who_needs_energy(player,opponent_player):
    if not player.active_pokemon:
        return  random.choice([0,2])
    if player.bench:
        if random.randint(0, 100)>60:
            return random.choice([0,1,2])
        else:
            return 1
    else:
        return  random.choice([0,1])


def choose_energy_for_assign_to_active(player,opponent_player):
    hand_energies = [card for card in player.hand if isinstance(card, EnergyCard) ]
    if hand_energies:
        chosen_index = random.randint(0, len(hand_energies) - 1)
        chosen_energy = hand_energies[chosen_index]
        #mprint(f"Energia scelta: {chosen_energy.code}")
    else:
        mprint("Nessun chosen_energy disponibile nella mano.")
        
    return chosen_energy.code

def choose_energy_for_assign_to_bench(player,opponent_player):
    hand_energies = [card for card in player.hand if isinstance(card, EnergyCard) ]
    if hand_energies:
        chosen_index = random.randint(0, len(hand_energies) - 1)
        chosen_energy = hand_energies[chosen_index]
        #mprint(f"Energia scelta: {chosen_energy.code}")
    else:
        mprint("Nessun chosen_energy disponibile nella mano.")
        
    return chosen_energy.code

def assign_energy_from_hand_to_active(player,energy_code):
    chosen_index = next((i for i, card in enumerate(player.hand) if isinstance(card,EnergyCard) and card.code == energy_code), None)
    player.active_pokemon.attached_energies.append(player.hand[chosen_index])
    player.hand.pop(chosen_index)
    
def assign_energy_from_hand_to_bench(player,energy_code,index):
    chosen_index = next((i for i, card in enumerate(player.hand) if isinstance(card,EnergyCard) and card.code == energy_code), None)
    if player.bench:
        player.bench[index].attached_energies.append(player.hand[chosen_index])
        player.hand.pop(chosen_index)
 
def which_pok_needs_nrg_on_bench(player):
    if player.bench:
        chosen_index = random.randint(0, len(player.bench) - 1)
        return chosen_index

def put_on_bench(player,pokemon_code):
    chosen_index = next((i for i, card in enumerate(player.hand) if isinstance(card,PokemonBaseCard) and card.code == pokemon_code), None)
    player.bench.append( player.hand[chosen_index])
    mprint(f"Metto in panchina {player.hand[chosen_index].name}")
    player.hand.pop(chosen_index)
    
def choose_pokmn_for_bench(player):
    base_pokemon = [card for card in player.hand if isinstance(card, PokemonBaseCard) ]
    chosen_pokmon = random.choice( base_pokemon )
    return chosen_pokmon.code
   

def can_set_pokms_on_bench(player):
    base_pokemon = [card for card in player.hand if isinstance(card, PokemonBaseCard) ]
    if base_pokemon and len(player.bench)<5:
        #mprint(f"true can_set_pokms_on_bench={len(player.bench)} ")
        return True,1
    else:
        #mprint(f"false can_set_pokms_on_bench={len(player.bench)}")
        return False,1
    
def chose_an_action(arrayofactions,player1,player2):
    chosen_index = random.randint(0, len(arrayofactions) - 1)
    return chosen_index


def assegna_attivo(player1,player2):
    if not player1.active_pokemon:
        chosen_pok_code = choose_for_active_pokemon_from_hand(player1,player2)
        #mprint(f"chosen_pok_code={chosen_pok_code}")
        assign_active_pokemon_from_hand(player1,chosen_pok_code,player2)
    #else:
        #mprint("Pokemon attivo gia impostato")
        
def assegna_attivo_from_bench(player1,player2):
    if not player1.active_pokemon:
        chosen_pok_code = choose_for_active_pokemon_from_bench(player1,player2)
        mprint(f"chosen_pok_code={chosen_pok_code}")
        if not chosen_pok_code:
                return False
        assign_active_pokemon_from_bench(player1,chosen_pok_code,player2)
    else:
        mprint("Pokemon attivo gia impostato")
    
    return True
            
def choose_if_skip_turn(player1):
    if not player1.active_pokemon:
        return False
    else:
        return random.randint(0, 100)<50
    
def can_skip_turn(player1):
    return player1.active_pokemon,2


    
def execute_an_ability(player1,player2):
    mprint(f"execute_an_ability>>> A")
    pk_with_ability = []
    if player1.active_pokemon.can_use_ability(player1):
        pk_with_ability.append(player1.active_pokemon)
        if isinstance(player1.active_pokemon,CharizardExPokemonCard):
            mprint(f"execute_an_ability>>> y")
            player1.active_pokemon.execute_ability(player1)
            player1.abilities_done.append(player1.active_pokemon)           
    bench_pokemons = [card for card in player1.hand if isinstance(card, PokemonBaseCard)  and card.can_use_ability( player1) ]
    if bench_pokemons:
        pk_with_ability=pk_with_ability+bench_pokemons
        pokemon = next((pok for pok in pk_with_ability if pok not in player1.abilities_done), None)
        if pokemon:
            pokemon.execute_ability(player1)
            player1.abilities_done.append(pokemon)
    
    
def there_are_abilities(player1):
    pk_with_ability = []
    if player1.active_pokemon.can_use_ability(player1):
        if isinstance(player1.active_pokemon,CharizardExPokemonCard):
            return True,3
        pk_with_ability.append(player1.active_pokemon)
    bench_pokemons = [card for card in player1.hand if isinstance(card, PokemonBaseCard)  and card.can_use_ability( player1) ]
    if bench_pokemons:
        pk_with_ability=pk_with_ability+bench_pokemons
        pokemon = [pok for pok in pk_with_ability if pok not in player1.abilities_done]
        return pokemon and len(pokemon)>0,3
    else:
        return False,3
    
def there_are_supporter(player1):#and card.trainer_type=='Supporter'
    supporters = [card for card in player1.hand if isinstance(card, TrainerCard)  and card.can_use_it( player1) ]
    if supporters and not player1.supporter_played:
        return True,2
    else:
        return False,2

def play_supporter(player1,sup_code,player2):   
    chosen_index = next((i for i, card in enumerate(player1.hand) if isinstance(card,TrainerCard) and card.code == sup_code), None)
    mprint(f"Play Supporter {player1.hand[chosen_index].name}")
    player1.hand[chosen_index].execute_effect( player1)
    
def chose_supporter(player1,):#and card.trainer_type=='Supporter'
    supporters = [card for card in player1.hand if isinstance(card, TrainerCard)  and card.can_use_it( player1) ]
    chosen_index = random.randint(0, len(supporters) - 1)
    return supporters[chosen_index].code

def set_turn_energy(player1,player2):
    mprint(f"Assegna energia di turno")
    # assegnazione energia di turno
    if can_assign_turn_energy(player1)[0]:
        if do_i_have_energy_to_assign(player1):  
            who_needs = who_needs_energy(player1,player2)
            if who_needs==1:#poekmon attivo
                mprint(f"Pokemon attivo necessita di energia")
                energy_code = choose_energy_for_assign_to_active(player1,player2)
                assign_energy_from_hand_to_active(player1,energy_code)
                player1.energy_attached_this_turn=True
            elif who_needs==2:#panchina
                bench_pok_needs = which_pok_needs_nrg_on_bench(player1)
                energy_code = choose_energy_for_assign_to_bench(player1,player2)
                mprint(f"Pokemon in panchina necessita di energia {bench_pok_needs} {energy_code}")
                assign_energy_from_hand_to_bench(player1,energy_code,bench_pok_needs)
                player1.energy_attached_this_turn=True
            else:#nessuno            
                mprint("nessuno necessità di energia")
    else:
        mprint("Energia di turno assegnata")     

def printEnhanced(message):
    mprint("*****************************************************************")
    mprint("*****************************************************************")
    mprint("*****************************************************************")
    mprint(f"**************************{message}********************************")
    mprint("*****************************************************************")
    mprint("*****************************************************************")
    mprint("*****************************************************************")
    
def stages1(player1):
    stages1s = [stage for stage in player1.hand if isinstance(stage, PokemonStage1Card)  and stage.can_evolve_pokemon( player1) ]
    if stages1s:
        return True,4
    else:
        return False,4
    
def stages2(player1):
    stages2s = [stage for stage in player1.hand if isinstance(stage, PokemonStage2Card)  and stage.can_evolve_pokemon( player1) ]
    if stages2s:
        return True,5
    else:
        return False,5
    
def choose_stage2_for_evolve(player1,player2):
    stages2s = [stage for stage in player1.hand if isinstance(stage, PokemonStage2Card)  and stage.can_evolve_pokemon( player1) ]
    if stages2s:
        mprint(f"choose_stage2_for_evolve>>> {stages2s}")
        chosen_pok = random.choice(stages2s)
        return chosen_pok
    else:
        return None

 
def do_you_want_evolve(player1,player2):
    perskip = random.randint(0, 100) 
    return perskip>30

def choose_stage1_for_evolve(player1,player2):
    stages1s = [stage for stage in player1.hand if isinstance(stage, PokemonStage1Card)  and stage.can_evolve_pokemon( player1) ]
    chosen_pok = random.choice(stages1s)
    return chosen_pok



def which_base_evolves(player1,player2,stage1):
    base_pok = [base_pok for base_pok in player1.bench if isinstance(base_pok, PokemonBaseCard)  and stage1.code in base_pok.stage1_code ]
    if isinstance(player1.active_pokemon, CharmanderPokemonCard):
        return player1.active_pokemon
    if base_pok:
        choosen_index  = random.randint(0, len(base_pok)-1 )
        return base_pok[choosen_index]
    else:
        return None

        
            
def which_evolves(player1,player2,stage1):
    if isinstance(player1.active_pokemon, CharmeleonPokemonCard):
        mprint(f"which_evolves>>> {player1.active_pokemon.name}")
        return player1.active_pokemon
    
    rare_candies = next( (card for card in player1.hand if card.code in ["SVI191"] ), None )
    
    if rare_candies:
        if isinstance(player1.active_pokemon, CharmanderPokemonCard):
            return player1.active_pokemon
        
        base_pok = [base_pok for base_pok in player1.bench if isinstance(base_pok, CharmanderPokemonCard)  ]
        if base_pok:
            choosen_index  = random.randint(0, len(base_pok)-1 )
            return base_pok[choosen_index]

    
    stage2 = [base_pok for base_pok in player1.bench if isinstance(base_pok, CharmeleonPokemonCard)  ]
    if stage2:
        choosen_index  = random.randint(0, len(stage2)-1 )
        return stage2[choosen_index]
    else:
        return None
    

def evolve_s1_action(player1,player2 ):
    if do_you_want_evolve(player1,player2):
        stage1 = choose_stage1_for_evolve(player1,player2)
        basepok = which_base_evolves(player1,player2,stage1)
        return player1.evolve_pokemon_to_stage1(basepok,stage1)
    
def evolve_s2_action(player1,player2 ):
    mprint(f"evolve_s2_action")
    stage2 = choose_stage2_for_evolve(player1,player2)
    if not stage2:
        return False
    basepok = which_evolves(player1,player2,stage2)
    if isinstance(basepok,CharmanderPokemonCard):
        return player1.evolve_pokemon_to_stage2_from_base(basepok,stage2)
    else:
        mprint(f"evolve_pokemon_to_stage2 >>> {basepok}")
        return  player1.evolve_pokemon_to_stage2(basepok,stage2)
        
    

def esegui_turno(player1,opponent):
    player1.turn_count=opponent.turn_count+1
    timestamp = int(time.time())
    random.seed(timestamp)
    skipped = True
    printEnhanced(f"NUOVO TURNO {player1.name}")
    pescata = player1.draw_card()
    if pescata:
        mprint(f"Ha pescato {pescata.name}")
    
    while skipped:
        # assegnazione pokemon attivo
        if not player1.active_pokemon:
            if not assegna_attivo_from_bench(player1,opponent):
                printEnhanced(f"Player {player1.name} ha perso, non ha pokemon in panchina")
                break

        player1.debug_game_state()

        avail_actions = [can_assign_turn_energy,can_set_pokms_on_bench,there_are_supporter,there_are_abilities,stages1,stages2]
        enabled_actions = [available_action for available_action in avail_actions if available_action(player1)[0] ]

        if len(enabled_actions)>=1:
            action_chosen_index = chose_an_action(enabled_actions,player1,opponent)
            index = enabled_actions[action_chosen_index](player1)[1]
            
            perskip = random.randint(0, 100) 
            if perskip>98:
                index = 5
            if index==0:
                set_turn_energy(player1,opponent)
            if index==1:
                put_on_bench(player1,choose_pokmn_for_bench(player1) )
            if index==2:
                play_supporter(player1,chose_supporter(player1),opponent )
            if index==3:
                execute_an_ability(player1,opponent)
            if index==4:
                evolve_s1_action(player1,opponent )
            if index==5:
                evolve_s2_action(player1,opponent )
            if index==6:
                if choose_if_skip_turn(player1):
                    mprint(f"Skipped turn")
                    skipped=False
        else:
            mprint(f"Turno finito {len(enabled_actions)}")
            break
            
        #mprint(f"Avaible actions {len(enabled_actions)}")
        
    mprint(f"Turno finito {player1.active_pokemon}")
    count_attacks = player1.active_pokemon.attack_count()    
    player1.active_pokemon.execute_attack(random.randint(0, count_attacks-1) ,player1,opponent)
    
    

    player1.debug_game_state()
    player1.reset_turn()
    


