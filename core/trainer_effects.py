# trainer_effects.py
import random

def bravery_charm(game_state, pokemon):
    pokemon.hp += 50
    print(f"{pokemon.name} ottiene +50 HP. HP totali: {pokemon.hp}")
    return True

def switch_cart(game_state):
    print(f"{game_state.name} sta eseguendo switch_cart")
    if not game_state.bench:
        print(f"{game_state.name}:switch_cart:Non ci sono Pokémon in panchina.")
        return False

    # Scegli un Pokémon in panchina
    switched_pokemon = game_state.bench.pop(0)  # Per semplicità, prende il primo
    game_state.bench.append(game_state.active_pokemon)
    game_state.active_pokemon = switched_pokemon

    # Cura 30 danni
    game_state.active_pokemon.hp += 30
    print(f"{game_state.name}:switch_cart:{game_state.active_pokemon.name} è ora attivo. Ha recuperato 30 HP.")
    return True


def professor_sada_vitality(game_state):
    print(f"{game_state.name} sta eseguendo professor_sada_vitality")
    # Scegli fino a 2 Pokémon "Ancient"
    ancient_pokemon = [
        pokemon for pokemon in game_state.bench if "Ancient" in pokemon.name
    ][:2]
    if not ancient_pokemon:
        print("{game_state.name}:professor_sada_vitality:Non ci sono Pokémon Ancient in panchina.")
        return False

    # Assegna una carta Energia dalla pila degli scarti
    for pokemon in ancient_pokemon:
        energy_card = next(
            (card for card in game_state.discard_pile if "Energia" in card.name), None
        )
        if energy_card:
            pokemon.attached_energies.append(energy_card)
            game_state.discard_pile.remove(energy_card)
            print(f"{game_state.name}:professor_sada_vitality:Energia assegnata a {pokemon.name}.")
    
    # Se è stata assegnata energia, pesca 3 carte
    if ancient_pokemon:
        for _ in range(3):
            if game_state.deck:
                game_state.hand.append(game_state.deck.pop(0))
            else:
                print("Il mazzo è vuoto.")
    return True

def nest_ball(game_state):
    print(f"{game_state.name} sta eseguendo nest_ball")
    # Cerca un Pokémon Base nel mazzo
    basic_pokemon = next(
        (card for card in game_state.deck if card.card_type == "Pokemon" and "Base" in card.name), None
    )
    if not basic_pokemon:
        print("{game_state.name}:nest_ball:Non ci sono Pokémon Base nel mazzo.")
        return False

    # Mettilo in panchina
    game_state.bench.append(basic_pokemon)
    game_state.deck.remove(basic_pokemon)
    print(f"{game_state.name}:nest_ball:{basic_pokemon.name} è stato aggiunto alla panchina.")

    # Mescola il mazzo
    random.shuffle(game_state.deck)
    return True


def energy_retrieval(game_state):
    print(f"{game_state.name} sta eseguendo energy_retrieval")
    # Recupera fino a 2 Energie Base dalla pila degli scarti
    for _ in range(2):
        energy_card = next(
            (card for card in game_state.discard_pile if "Energia" in card.name), None
        )
        if energy_card:
            game_state.hand.append(energy_card)
            game_state.discard_pile.remove(energy_card)
            print(f"{energy_card.name} è stata aggiunta alla mano.")
        else:
            print("Non ci sono più Energie Base nella pila degli scarti.")
            break
    return True


def ultra_ball(game_state):
    # Controlla se ci sono abbastanza carte da scartare
    if len(game_state.hand) < 3:
        print("Non hai abbastanza carte per usare Ultra Ball.")
        return False

    # Scarta 2 carte dalla mano
    discarded = 0
    while discarded < 2:
        card_to_discard = game_state.hand.pop(0)  # Per semplicità, scarta le prime 2
        game_state.discard_pile.append(card_to_discard)
        discarded += 1
        print(f"{card_to_discard.name} è stata scartata.")

    # Cerca un Pokémon nel mazzo
    target_pokemon = next((card for card in game_state.deck if card.card_type == "Pokemon"), None)
    if not target_pokemon:
        print("Non ci sono Pokémon nel mazzo.")
        return False

    # Aggiungi il Pokémon alla mano
    game_state.hand.append(target_pokemon)
    game_state.deck.remove(target_pokemon)
    print(f"{target_pokemon.name} è stato aggiunto alla mano.")

    # Mescola il mazzo
    random.shuffle(game_state.deck)
    return True


def pokegear(game_state):
    # Guarda le prime 7 carte del mazzo
    top_cards = game_state.deck[:7]
    supporter = next(
        (card for card in top_cards if card.card_type == "Supporter"), None
    )
    if supporter:
        game_state.hand.append(supporter)
        game_state.deck.remove(supporter)
        print(f"{supporter.name} è stato aggiunto alla mano.")

    # Rimetti le altre carte nel mazzo
    game_state.deck = game_state.deck[:7] + game_state.deck[7:]
    random.shuffle(game_state.deck)
    return True
