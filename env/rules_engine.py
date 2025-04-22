# env/rules_engine.py

class RulesEngine:
    def __init__(self, game_state):
        self.game_state = game_state

    def validate_action(self, action):
        # Controlla se l'azione è del tipo "draw N"
        if action.startswith("draw"):
            try:
                # Estrae il numero di carte da pescare
                _, count = action.split()
                count = int(count)
            except ValueError:
                print("Formato del comando non valido. Usa 'draw N', dove N è un numero.")
                return False
    
            # Controlla se il mazzo è vuoto
            if len(self.game_state.deck) == 0:
                print("Il mazzo è vuoto! Hai perso la partita.")
                self.game_state.game_over = True
                return False
            
            # Controlla se ci sono abbastanza carte nel mazzo
            if len(self.game_state.deck) < count:
                print(f"Non ci sono abbastanza carte nel mazzo per pescare {count} carte.")
                return False
    
            return True
        
        # Controlla se l'azione è del tipo "assign_energy Energia NomePokémon"
        if action.startswith("assign_energy"):
            parts = action.split()
            print(f"{parts}")
            if len(parts) != 3:
                print("Formato dell'azione non valido. Usa: 'assign_energy NomeEnergia NomePokémon'")
                return False
            
            energy_card_name, pokemon_name = parts[1], parts[2]
            
            # Controlla se la carta Energia è nella mano
            if not any(card.name == energy_card_name for card in self.game_state.hand):
                print(f"Non hai la carta Energia {energy_card_name} nella tua mano.")
                return False
            
            # Controlla se il Pokémon di destinazione è valido
            all_pokemons = [self.game_state.active_pokemon] + self.game_state.bench
            if not any(pokemon.name == pokemon_name for pokemon in all_pokemons):
                print(f"Il Pokémon {pokemon_name} non è valido.")
                return False
            
            # Controlla se è già stata assegnata un'energia in questo turno
            if self.game_state.energy_attached_this_turn:
                print("Hai già assegnato un'energia in questo turno.")
                return False

            return True


        # Controlla se l'azione è del tipo "play_pokemon NomePokemon [bench|active]"
        if action.startswith("play_pokemon"):
            parts = action.split()
            if len(parts) < 2 or len(parts) > 3:
                print("Formato dell'azione non valido. Usa: 'play_pokemon NomePokemon [bench|active]'.")
                return False

            pokemon_name = parts[1]
            target = parts[2] if len(parts) == 3 else "bench"

            # Verifica che il Pokémon sia nella mano
            if not any(card.name == pokemon_name for card in self.game_state.hand):
                print(f"Non hai il Pokémon {pokemon_name} nella tua mano.")
                return False

            # Verifica lo spazio in panchina
            if target == "bench" and len(self.game_state.bench) >= 5:
                print("La panchina è piena. Non puoi aggiungere altri Pokémon.")
                return False

            # Verifica la posizione attiva
            if target == "active" and self.game_state.active_pokemon:
                print("C'è già un Pokémon attivo.")
                return False

            return True
        
        # Controlla se l'azione è del tipo "attack NomeAttacco"
        # Controlla se l'azione è "attack NomeAttacco"
        if action.startswith("attack"):
            parts = action.split()
            if len(parts) != 2:
                print("Formato dell'azione non valido. Usa: 'attack NomeAttacco'.")
                return False

            attack_name = parts[1]

            # Controlla che ci sia un Pokémon attivo
            if not self.game_state.active_pokemon:
                print("Non hai un Pokémon attivo per attaccare.")
                return False

            # Controlla che l'attacco sia valido
            if not any(atk[0] == attack_name for atk in self.game_state.active_pokemon.attacks):
                print(f"{self.game_state.active_pokemon.name} non può usare l'attacco {attack_name}.")
                return False

            return True


        # Controlla se l'azione è del tipo "discard NomeCarta"
        if action.startswith("discard"):
            parts = action.split()
            if len(parts) != 2:
                print("Formato dell'azione non valido. Usa: 'discard NomeCarta'.")
                return False

            card_name = parts[1]

            # Verifica che la carta sia nella mano
            if not any(c.name == card_name for c in self.game_state.hand):
                print(f"La carta {card_name} non è nella tua mano.")
                return False

            return True
        
        # Controlla se l'azione è del tipo "play_trainer NomeCarta"
        if action.startswith("play_trainer"):
            parts = action.split()
            if len(parts) != 2:
                print("Formato dell'azione non valido. Usa: 'play_trainer NomeCarta'.")
                return False

            card_name = parts[1]

            # Verifica che la carta sia nella mano e sia una carta Allenatore
            if not any(c.name == card_name and c.card_type == "Trainer" for c in self.game_state.hand):
                print(f"La carta {card_name} non è una carta Allenatore valida nella tua mano.")
                return False

            # Regole per le carte Aiuto
            trainer_card = next(c for c in self.game_state.hand if c.name == card_name)
            if trainer_card.trainer_type == "Supporter" and self.game_state.supporter_played:
                print("Hai già giocato un Aiuto in questo turno.")
                return False

            return True
                
        
        # Azione non riconosciuta
        print(f"Azione non riconosciuta: #{action}#")
        return False


    def apply_action(self, action):
        if action.startswith("draw"):
            try:
                _, count = action.split()
                count = int(count)
            except ValueError:
                print("Formato del comando non valido.")
                return
    
            for _ in range(count):
                card = self.game_state.draw_card()
                if card:
                    print(f"Hai pescato: {card.name}")
                else:
                    break

        if action.startswith("assign_energy"):
            parts = action.split()
            energy_card_name, pokemon_name = parts[1], parts[2]
            
            # Trova il Pokémon corrispondente
            all_pokemons = [self.game_state.active_pokemon] + self.game_state.bench
            target_pokemon = next(pokemon for pokemon in all_pokemons if pokemon.name == pokemon_name)
            
            # Assegna l'energia
            self.game_state.assign_energy(energy_card_name, target_pokemon)
            
        if action.startswith("play_pokemon"):
            parts = action.split()
            pokemon_name = parts[1]
            target = parts[2] if len(parts) == 3 else "bench"

            self.game_state.play_pokemon(pokemon_name, target)
            
        if action.startswith("attack"):
            parts = action.split()
            attack_name = parts[1]
            self.game_state.attack(attack_name)
            
        if action.startswith("discard"):
            parts = action.split()
            card_name = parts[1]
            self.game_state.discard_card(card_name)
            
        if action.startswith("play_trainer"):
            parts = action.split()
            card_name = parts[1]
            self.game_state.play_trainer(card_name)