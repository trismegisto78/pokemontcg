import numpy as np
from core.card import PokemonCard, TrainerCard, EnergyCard

class PokemonEnvironment:
    def __init__(self, game_state, opponent_game_state):
        self.game_state = game_state
        self.opponent_game_state = opponent_game_state
        self.last_actions = [
            self.encode_action(0, [0]),  # Azione 1
            self.encode_action(1, [1, 2]),  # Azione 2
            self.encode_action(0, []),  # Azione 3
        ]

    def get_state(self):
        state = self.generate_game_state_array(5)
        print(f"Lunghezza dell'array di stato: {len(state)}")
        return state

    def generate_game_state_array(self, last_actions_count=5, fixed_size=260):
        """
        Genera un array numerico che rappresenta lo stato del gioco, garantendo una dimensione fissa.
    
        Args:
            last_actions_count (int): Numero massimo di azioni precedenti da includere.
            fixed_size (int): Dimensione fissa desiderata per l'array dello stato.
    
        Returns:
            np.array: Array numerico che rappresenta lo stato del gioco.
        """
        # Carte nel mazzo (ID delle carte nel mazzo)
        deck_array = [card.index for card in self.game_state.deck] + [0] * (60 - len(self.game_state.deck))
    
        # Carte in mano (ID delle carte nella mano)
        hand_array = [card.index for card in self.game_state.hand] + [0] * (10 - len(self.game_state.hand))
    
        # Carte in panchina con dettagli (ID, HP, Energie, Stato)
        bench_array = []
        for pokemon in self.game_state.bench:
            if pokemon:
                bench_array.extend([pokemon.index, pokemon.hp, len(pokemon.attached_energies), pokemon.status_condition])
            else:
                bench_array.extend([0, 0, 0, 0])  # Padding per slot vuoti
        bench_array += [0, 0, 0, 0] * (5 - len(self.game_state.bench))  # Padding per slot vuoti
    
        # Carta attiva con dettagli (ID, HP, Energie, Stato)
        if self.game_state.active_pokemon:
            active_pokemon_array = [
                self.game_state.active_pokemon.index, 
                self.game_state.active_pokemon.hp, 
                len(self.game_state.active_pokemon.attached_energies), 
                self.game_state.active_pokemon.status_condition
            ]
        else:
            active_pokemon_array = [0, 0, 0, 0]  # Nessun Pokémon attivo
    
        # Carte nella pila degli scarti (ID delle carte nella pila)
        discard_pile_array = [card.index for card in self.game_state.discard_pile] + [0] * (60 - len(self.game_state.discard_pile))
    
        # Carte premio (ID delle carte premio)
        prize_cards_array = [card.index for card in self.game_state.prizes] + [0] * (6 - len(self.game_state.prizes))
    
        # Carte in panchina avversaria con dettagli (ID, HP, Energie, Stato)
        opponent_bench_array = []
        for pokemon in self.opponent_game_state.bench:
            if pokemon:
                opponent_bench_array.extend([pokemon.index, pokemon.hp, len(pokemon.attached_energies), pokemon.status_condition])
            else:
                opponent_bench_array.extend([0, 0, 0, 0])  # Padding per slot vuoti
        opponent_bench_array += [0, 0, 0, 0] * (5 - len(self.opponent_game_state.bench))  # Padding per slot vuoti
    
        # Carta attiva avversaria con dettagli (ID, HP, Energie, Stato)
        if self.opponent_game_state.active_pokemon:
            opponent_active_pokemon_array = [
                self.opponent_game_state.active_pokemon.index, 
                self.opponent_game_state.active_pokemon.hp, 
                len(self.opponent_game_state.active_pokemon.attached_energies), 
                self.opponent_game_state.active_pokemon.status_condition
            ]
        else:
            opponent_active_pokemon_array = [0, 0, 0, 0]  # Nessun Pokémon attivo
    
        # Carte nella pila degli scarti avversaria (ID delle carte nella pila)
        opponent_discard_pile_array = [card.index for card in self.opponent_game_state.discard_pile] + [0] * (60 - len(self.opponent_game_state.discard_pile))
    
        # Numero di carte in mano dell'avversario
        opponent_hand_count = len(self.opponent_game_state.hand)
    
        # Numero di carte premio dell'avversario
        opponent_prize_cards_count = len(self.opponent_game_state.prizes)
    
        # Risultati delle ultime n mosse
        last_actions_array = self.last_actions[:last_actions_count] + [0] * (last_actions_count - len(self.last_actions))
    
        # Combina tutte le sezioni in un unico array
        state_array = (
            deck_array +
            hand_array +
            bench_array +
            active_pokemon_array +
            discard_pile_array +
            prize_cards_array +
            opponent_bench_array +
            opponent_active_pokemon_array +
            opponent_discard_pile_array +
            [opponent_hand_count] +
            [opponent_prize_cards_count] +
            last_actions_array
        )
    
        # Aggiunge padding o tronca l'array per garantire una dimensione fissa
        if len(state_array) < fixed_size:
            state_array += [0] * (fixed_size - len(state_array))  # Padding
        elif len(state_array) > fixed_size:
            state_array = state_array[:fixed_size]  # Troncamento
    
        return np.array(state_array, dtype=np.float32)


    def step(self, action):
        """
        Applica l'azione, aggiorna lo stato, calcola il reward e verifica se il gioco è terminato.
    
        Args:
            action (int): L'azione scelta dall'agente.
    
        Returns:
            tuple: (next_state, reward, turn_ends)
        """
        reward=-1
        # Decodifica e applica l'azione
        if action == 0:
            # Assegna un'energia, se possibile
            for card in self.game_state.hand:
                if isinstance(card, EnergyCard):
                    print(f"Assegno energia {card.code} al Pokémon attivo {self.game_state.active_pokemon.name}")
                    result = self.game_state.assign_energy(card.code, self.game_state.active_pokemon)
                    if result:
                        print(f"Assegnata energia")
                        return self.get_state(), 100, False  # Penalità per azione non valida
                    else:
                        print(f"NON Assegnata energia")
                        return self.get_state(), -100, False  # Penalità per azione non valida
                    break;
            print(f"{self.game_state.name} Non ci sono carte energia valide nella mano")
            return self.get_state(), -100, False      
        elif action == 1:
            # Esegui l'attacco base
            if self.game_state.active_pokemon:
                print(f"{self.game_state.active_pokemon.name} esegue l'attacco base!")
                attack_result = self.game_state.active_pokemon.execute_attack(0, self.game_state, self.opponent_game_state)
                turn_ends = attack_result>-100
                reward = attack_result
                next_state = self.get_state()
                return next_state, reward, turn_ends
        elif action == 2:
            # Esegui l'attacco speciale
            if self.game_state.active_pokemon:
                print(f"{self.game_state.active_pokemon.name} esegue l'attacco speciale!")
                attack_result = self.game_state.active_pokemon.execute_attack(1, self.game_state, self.opponent_game_state)
                turn_ends = attack_result>-100
                reward = attack_result
                next_state = self.get_state()
                return next_state, reward, turn_ends
        else:
            print("Azione non valida!")
            return self.get_state(), -100, False  # Penalità per azione non valida
    
    
        
    
    def get_hand_summary(self, max_pokemon=5, max_trainer=5, max_energy=5):
        """
        Restituisce un riassunto numerico delle carte nella mano con dimensione fissa.
    
        Args:
            max_pokemon (int): Numero massimo di Pokémon da rappresentare.
            max_trainer (int): Numero massimo di Trainer da rappresentare.
            max_energy (int): Numero massimo di Energie da rappresentare.
    
        Returns:
            list[int]: Riassunto della mano con dimensione fissa.
        """
        pokemon_count = sum(1 for card in self.game_state.hand if isinstance(card, PokemonCard))
        trainer_count = sum(1 for card in self.game_state.hand if isinstance(card, TrainerCard))
        energy_count = sum(1 for card in self.game_state.hand if isinstance(card, EnergyCard))
    
        # Tronca i conteggi al massimo specificato
        pokemon_count = min(pokemon_count, max_pokemon)
        trainer_count = min(trainer_count, max_trainer)
        energy_count = min(energy_count, max_energy)
    
        return [pokemon_count, trainer_count, energy_count]
    
    def get_pokemon_summary(self, pokemon):
        """
        Restituisce un riassunto numerico di un Pokémon.
    
        Args:
            pokemon (PokemonCard): Il Pokémon da riassumere.
    
        Returns:
            list[int]: HP, numero di Energie assegnate, e stato del Pokémon.
        """
        if not pokemon:
            return [0, 0, 0]  # Nessun Pokémon
        hp = pokemon.hp
        energy_count = len(pokemon.attached_energies)
        status = 1 # if pokemon.status_condition == "paralyzed" else 0  # Esempio semplice
        return [hp, energy_count, status]
    
        
    def encode_action(self, pokemon_index, energy_indices):
        # Codifica l'azione in un singolo numero intero
        base = 3  # Massimo 3 Energie per Pokémon
        encoded = pokemon_index * base**len(energy_indices)
        for i, energy_index in enumerate(energy_indices):
            encoded += energy_index * base**i
        return encoded
    
    def decode_action(self, action):
        # Decodifica l'azione da un numero intero
        base = 3
        pokemon_index = action // base**2
        energy_indices = [(action // base**i) % base for i in range(2)]
        return pokemon_index, energy_indices
    
    