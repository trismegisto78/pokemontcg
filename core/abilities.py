# abilities.py

def teal_dance(game_state, pokemon):
    # Verifica che ci sia un'Energia Erba nella mano
    energy_card = next((card for card in game_state.hand if card.name == "Energia Erba"), None)
    if not energy_card:
        print("Non ci sono Energie Erba nella mano.")
        return False

    # Assegna l'energia a Teal Mask Ogerpon ex
    pokemon.attached_energies.append(energy_card)
    game_state.hand.remove(energy_card)
    print(f"Energia Erba assegnata a {pokemon.name}.")

    # Pesca una carta
    if game_state.deck:
        drawn_card = game_state.deck.pop(0)
        game_state.hand.append(drawn_card)
        print(f"Hai pescato: {drawn_card.name}")
    else:
        print("Il mazzo è vuoto. Nessuna carta pescata.")
    return True

def burst_roar(game_state, pokemon):
    # Scarta l'intera mano
    game_state.discard_pile.extend(game_state.hand)
    game_state.hand.clear()
    print("Hai scartato tutta la mano.")

    # Pesca 6 carte
    for _ in range(6):
        if game_state.deck:
            card = game_state.deck.pop(0)
            game_state.hand.append(card)
        else:
            print("Il mazzo è vuoto. Non puoi pescare altre carte.")
            break
    return True