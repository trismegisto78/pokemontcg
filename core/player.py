# core/game_state.py
from core.utils import mprint
from core.card import PokemonCard, EnergyCard, Card, PokemonBaseCard
import random



#from core.RLPokemonAgent import RLPokemonAgent
#from env.pokemon_env import PokemonEnvironment

class GameState:
    def __init__(self):
        self.name ="Unknown"
        self.deck = []  # Mazzo del giocatore
        self.hand = []  # Carte in mano
        self.bench = []  # Pokémon in panchina
        self.discard_pile = []  # Pila degli scarti
        self.game_over = False  # Stato della partita
        self.energy_attached_this_turn = False  # Stato per limitare a 1 energia per turno
        self.active_pokemon = None  # Pokémon attivo
        self.opponent_active_pokemon = None  # Pokémon attivo dell'avversario
        self.stadium_card = None  # Carta Stadio attualmente in gioco
        self.supporter_played = False  # Limita a 1 carta Aiuto per turno
        self.prizes = []  # Carte premio del giocatore
        self.opponent_prizes = []  # Carte premio dell'avversario
        self.abilities_done=[]
        #self.agent = RLPokemonAgent(state_size=260, action_size=3)
        self.vittorie = 0
        self.turn_count=0

            
        
    def reset(self,opponent,create_deck):
        self.deck = []  # Mazzo del giocatore
        self.hand = []  # Carte in mano
        self.bench = []  # Pokémon in panchina
        self.discard_pile = []  # Pila degli scarti
        self.game_over = False  # Stato della partita
        self.energy_attached_this_turn = False  # Stato per limitare a 1 energia per turno
        self.active_pokemon = None  # Pokémon attivo
        self.opponent_active_pokemon = None  # Pokémon attivo dell'avversario
        self.stadium_card = None  # Carta Stadio attualmente in gioco
        self.supporter_played = False  # Limita a 1 carta Aiuto per turno
        self.prizes = []  # Carte premio del giocatore
        self.opponent_prizes = []  # Carte premio dell'avversario
        self.opponent=opponent
        self.abilities_done=[]
        # Crea e mescola il mazzo
        self.deck = create_deck()#create_deck()
        mprint(f"Creato mazzo: {len(self.deck)} carte")
        random.shuffle(self.deck)

        # Inizializza le componenti di gioco
        self.hand = []  # Mano del giocatore
        self.discard_pile = []  # Pila degli scarti
        self.prizes = []  # Carte premio
        self.bench = []  # Pokémon in panchina
        self.active_pokemon = None  # Pokémon attivo
        self.opponent_active_pokemon = None  # Pokémon attivo dell'avversario

        # Pesca la mano iniziale (tipicamente 7 carte)
        self.hand = [self.deck.pop(0) for _ in range(7)]

        # Imposta le carte premio (tipicamente 6 carte)
        self.prizes = [self.deck.pop(0) for _ in range(6)]
        
        #self.env = PokemonEnvironment(self, opponent)
        mprint(f"Mano iniziale: {[card.name for card in self.hand]}")
        mprint(f"Carte premio impostate: {[card.name for card in self.prizes]}")
        
        
    def setup_active_and_bench(self,create_deck):
        while True:
            # Cerca Pokémon Base nella mano
            base_pokemon = [card for card in self.hand if isinstance(card, PokemonBaseCard) ]
    
            if base_pokemon:
                # Imposta il Pokémon attivo (prendi il primo Pokémon Base)
                self.active_pokemon = base_pokemon.pop(0)
                self.hand.remove(self.active_pokemon)
                
                mprint(f"Pokémon attivo: {self.active_pokemon.name}")
    
                # Imposta i Pokémon in panchina (fino a un massimo di 5)
                self.bench = base_pokemon[:5]
                for pokemon in self.bench:
                    self.hand.remove(pokemon)
    
                mprint(f"Pokémon in panchina: {[pokemon.name for pokemon in self.bench]}")
                break
    
            else:
                # Mulligan: rimescola la mano e pesca una nuova
                mprint("Non ci sono Pokémon Base nella mano. Mulligan!")
                #self.discard_pile.extend(self.hand)  # Metti la mano corrente nella pila degli scarti
                #self.hand = []  # Svuota la mano
    
                #if len(self.deck) < 7:
                #    mprint("Errore: Non ci sono abbastanza carte nel mazzo per un Mulligan.")
                #    return False  # Termina il gioco se non ci sono abbastanza carte
    
                # Pesca una nuova mano di 7 carte
                #self.hand = [self.deck.pop(0) for _ in range(7)]
                #random.shuffle(self.deck)  # Mescola il mazzo
                self.reset(self.opponent,create_deck)
                mprint(f"Nuova mano: {[card.name for card in self.hand]}")
                
    def debug_game_state(self):
        totale_num_carte = 0
        mprint(f"\n===================== STATO {self.name}============================")
        mprint(f"POKEMON ATTIVO\n\t{self.active_pokemon.name if self.active_pokemon else 'Nessuno'} HP={self.active_pokemon.hp} energies {self.active_pokemon.attached_energies}")
        mprint(f"PANCHINA")
        for i, pokemon in enumerate(self.bench):
            totale_num_carte = totale_num_carte + len(pokemon.attached_energies)
            mprint(
                f"\t{i + 1}) ==> {pokemon.name}, Energie assegnate: {[energy.code for energy in pokemon.attached_energies]}"
                if pokemon else f"Slot {i + 1} della panchina vuoto."
            )
        mprint(f"MANO\n\t{[card.name for card in self.hand]}")
        mprint(f"PREMIO\n\t {[card.name for card in self.prizes]}")
        mprint(f"SCARTI\n\t{[card.name for card in self.discard_pile]}")
        mprint(f"\nN°CARTE MAZZO: {len(self.deck)}")
        totale_num_carte = totale_num_carte+len(self.bench )+len(self.hand)+len(self.deck)+len(self.prizes)+(1 if self.active_pokemon else 0)+len(self.discard_pile)+len(self.active_pokemon.attached_energies)
        
        full_array = self.bench+self.hand+self.deck+self.prizes+self.discard_pile
        
        
        mprint(f"\nN°CARTE TOTALI: {len(full_array)}")
        mprint("===============================================================")
       

    def draw_card(self):
        if not self.deck:
            mprint("Non ci sono carte nel mazzo! Hai perso il turno.")
            return None
        card = self.deck.pop(0)  # Rimuove la prima carta dal mazzo
        self.hand.append(card)  # Aggiunge la carta alla mano
        return card
    
    def draw_cards(self, n):
        for _ in range(n):
            if not self.deck:
                mprint("Non ci sono più carte nel mazzo!")
                self.game_over=True
                break
            self.draw_card()

    def reset_turn(self):
        self.energy_attached_this_turn = False
        self.supporter_played = False
        self.abilities_done=[]





    def assign_energy(self, energy_card_code, target_pokemon):
        if self.energy_attached_this_turn:
            mprint("Hai già assegnato un'energia in questo turno.")
            return False

        # Controlla se la carta Energia è nella mano
        energy_card = next((card for card in self.hand if card.code == energy_card_code), None)
        if not energy_card:
            mprint(f"Non hai la carta Energia {energy_card_code} nella tua mano.")
            return False

        # Controlla se il Pokémon di destinazione è valido
        if target_pokemon not in [self.active_pokemon] + self.bench:
            mprint("Il Pokémon selezionato non è valido.")
            return False

        # Assegna l'energia
        target_pokemon.attach_energy(self.hand,energy_card)
        self.energy_attached_this_turn = True
        mprint(f"Energia {energy_card_code} assegnata a {target_pokemon.name}.")
        return True

    def play_pokemon(self, pokemon_name, target="bench"):
        # Cerca il Pokémon nella mano
        pokemon_card = next((card for card in self.hand if card.name == pokemon_name), None)
        if not pokemon_card:
            mprint(f"Non hai il Pokémon {pokemon_name} nella tua mano.")
            return False

        if target == "bench":
            # Verifica che ci sia spazio in panchina
            if len(self.bench) >= 5:
                mprint("La panchina è piena. Non puoi aggiungere altri Pokémon.")
                return False

            self.bench.append(pokemon_card)
            self.hand.remove(pokemon_card)
            mprint(f"{pokemon_name} è stato aggiunto alla panchina.")
            return True

        elif target == "active":
            # Verifica che la posizione attiva sia vuota
            if self.active_pokemon:
                mprint("C'è già un Pokémon attivo. Non puoi aggiungerne un altro.")
                return False

            self.active_pokemon = pokemon_card
            self.hand.remove(pokemon_card)
            mprint(f"{pokemon_name} è ora il Pokémon attivo.")
            return True

        mprint("Destinazione non valida. Usa 'bench' o 'active'.")
        return False
    
    def attack(self, attack_name):
        attacker = self.active_pokemon
        defender = self.opponent_active_pokemon
    
        if not attacker:
            mprint("Non hai un Pokémon attivo per attaccare.")
            return False
    
        if not defender:
            mprint("L'avversario non ha un Pokémon attivo da attaccare.")
            return False
    
        # Trova l'attacco scelto
        attack = next((atk for atk in attacker.attacks if atk[0] == attack_name), None)
        if not attack:
            mprint(f"L'attacco {attack_name} non è valido per {attacker.name}.")
            return False
    
        # Verifica che ci siano abbastanza energie per l'attacco
        required_energy = attack[2]
        if len(attacker.attached_energies) < required_energy:
            mprint(f"{attacker.name} non ha abbastanza Energie per usare {attack_name}.")
            return False
    
        # Calcola il danno
        base_damage = attack[1]
        mprint(f"{attacker.name} usa {attack_name} e infligge {base_damage} danni base!")
    
        # Applica il danno al difensore
        is_ko = defender.receive_damage(base_damage, attacker.card_type)
    
        # Gestione del KO
        if is_ko:
            mprint(f"{defender.name} è stato messo KO!")
            self.opponent_active_pokemon = None
            self.draw_prize_card()
        
        return True

    def getBenchPokemon(self):
        bench_pokemon = [pokemon for pokemon in self.bench if isinstance(pokemon, PokemonCard) ]
        return bench_pokemon
    
    def discard_card(self, card_code):
        # Cerca la carta nella mano
        card = next((c for c in self.hand if c.code == card_code), None)
        if not card:
            mprint(f"Non hai la carta {card_code} nella tua mano.")
            return False

        # Sposta la carta dalla mano alla pila degli scarti
        self.hand.remove(card)
        self.discard_pile.append(card)
        mprint(f"La carta {card.name} è stata scartata.")
        return True
    
    def discard_card_from(self, _from, card_code):
        # Cerca la carta nella mano
        card = next((c for c in _from if c.code == card_code), None)
        if not card:
            mprint(f"Non hai la carta {card_code}.")
            return False

        # Sposta la carta dalla mano alla pila degli scarti
        self.discard_pile.append(card)
        _from.remove(card)
        
        mprint(f"La carta {card.name} è stata scartata.")
        return True
    
    def discard_full_hand(self):
        # Cerca la carta nella mano
        for card in self.hand:
            self.discard_card(card.code)
        return True
    
    def play_trainer(self, card_name):
        # Cerca la carta nella mano
        trainer_card = next((c for c in self.hand if c.name == card_name and c.card_type == "Trainer"), None)
        if not trainer_card:
            mprint(f"Non hai la carta Allenatore {card_name} nella tua mano.")
            return False

        # Regole per le diverse tipologie di carte Allenatore
        if trainer_card.trainer_type == "Supporter":
            if self.supporter_played:
                mprint("Hai già giocato un Aiuto in questo turno.")
                return False
            self.supporter_played = True

        elif trainer_card.trainer_type == "Stadium":
            mprint(f"La carta Stadio {card_name} è ora in gioco, sostituendo {self.stadium_card.name if self.stadium_card else 'nessuno'}.")
            self.stadium_card = trainer_card
            self.hand.remove(trainer_card)
            return True

        # Gioca la carta Allenatore ed esegui il suo effetto
        trainer_card.activate_effect(self)
        self.hand.remove(trainer_card)
        self.discard_pile.append(trainer_card)
        mprint(f"La carta Allenatore {card_name} è stata giocata e il suo effetto è stato applicato.")
        return True
    
    def draw_prize_card(self):
        if not self.prizes:
            mprint("Non ci sono più carte premio.")
            return None

        prize_card = self.prizes.pop(0)
        mprint(f"Hai pescato una carta premio: {prize_card.name}")
        return prize_card
    
    def discard_energy_from_bench(self, n):
        discarded_energies = []  # Array delle Energie scartate
        energies_to_discard = n  # Numero di Energie da scartare
    
        for pokemon in self.bench:
            if not isinstance(pokemon, PokemonCard):
                continue  # Salta se non è un Pokémon valido
    
            # Controlla quante Energie ha il Pokémon
            if len(pokemon.attached_energies) > 0:
                # Determina quante Energie scartare da questo Pokémon
                discard_count = min(len(pokemon.attached_energies), energies_to_discard)
    
                # Scarta le Energie
                for _ in range(discard_count):
                    enrg = pokemon.attached_energies.pop(0)
                    discarded_energies.append(enrg)  # Rimuove l'Energia dalla lista
                    self.discard_pile.append(enrg)
    
                energies_to_discard -= discard_count  # Aggiorna il numero di Energie ancora da scartare
    
            # Se non ci sono più Energie da scartare, termina
            if energies_to_discard == 0:
                break
    
        # Restituisce l'array delle Energie scartate
        mprint(f"Energie scartate: {[energy.name for energy in discarded_energies]}")
        return discarded_energies
    
    def select_pokemon_for_energy_discard(self):
        """
        Restituisce una lista di indici dei Pokémon in panchina che hanno Energie assegnate.
    
        Returns:
            list[int]: Lista di indici dei Pokémon in panchina con Energie assegnate.
        """
        selected_pokemon = [
            i for i, pokemon in enumerate(self.bench)
            if isinstance(pokemon, PokemonCard) and len(pokemon.attached_energies) > 0
        ]
        mprint(f"Pokémon selezionati per lo scarto di Energie: {selected_pokemon}")
        return selected_pokemon
    
    def select_energies_to_discard(self, pokemon_index, max_energies=None):
        """
        Restituisce una lista di indici delle Energie da scartare per un Pokémon specifico.
    
        Args:
            pokemon_index (int): Indice del Pokémon nella panchina.
            max_energies (int, optional): Numero massimo di Energie da scartare. Default: tutte.
    
        Returns:
            list[int]: Lista di indici delle Energie da scartare.
        """
        if pokemon_index >= len(self.bench):
            mprint(f"Indice {pokemon_index} fuori dal range della panchina.")
            return []
    
        pokemon = self.bench[pokemon_index]
        if not isinstance(pokemon, PokemonCard) or len(pokemon.attached_energies) == 0:
            mprint(f"Il Pokémon in posizione {pokemon_index} non ha Energie assegnate.")
            return []
    
        # Seleziona tutte le Energie o un massimo specificato
        energy_indices = list(range(len(pokemon.attached_energies)))
        if max_energies is not None:
            energy_indices = energy_indices[:max_energies]
    
        mprint(f"Energie selezionate per lo scarto: {energy_indices}")
        return energy_indices
    
    def apply_energy_discard(self, pokemon_index, energy_indices):
        """
        Scarta le Energie specificate da un Pokémon in panchina.
    
        Args:
            pokemon_index (int): Indice del Pokémon nella panchina.
            energy_indices (list[int]): Indici delle Energie da scartare.
    
        Returns:
            list[EnergyCard]: Lista delle Energie effettivamente scartate.
        """
        if pokemon_index >= len(self.bench):
            mprint(f"Indice {pokemon_index} fuori dal range della panchina.")
            return []
    
        pokemon = self.bench[pokemon_index]
        if not isinstance(pokemon, PokemonCard):
            mprint(f"Il Pokémon in posizione {pokemon_index} non è valido.")
            return []
    
        discarded_energies = []
        for energy_index in sorted(energy_indices, reverse=True):  # Ordine inverso per evitare problemi di indice
            if energy_index < len(pokemon.attached_energies):
                discarded_energies.append(pokemon.attached_energies.pop(energy_index))
            else:
                mprint(f"Indice {energy_index} fuori dall'intervallo delle Energie assegnate.")
    
        mprint(f"Energie scartate dal Pokémon in posizione {pokemon_index}: {[e.name for e in discarded_energies]}")
        return discarded_energies
    
    
    
    def evolve_pokemon_to_stage1(self, base_pokemon, stage1_card):
        """
        Evolve un Pokémon Base a una carta Stage1.

        Args:
            base_pokemon (PokemonBaseCard): Il Pokémon Base da evolvere.
            stage1_card (PokemonStage1Card): La carta Stage1 da utilizzare per l'evoluzione.

        Returns:
            bool: True se l'evoluzione ha avuto successo, False altrimenti.
        """
        # Controlla se la carta Stage1 è nella mano
        if stage1_card not in self.hand:
            mprint(f"La carta {stage1_card.name} non è nella tua mano.")
            return False

        # Controlla se il Pokémon Base è in panchina o attivo
        if base_pokemon not in self.bench and base_pokemon != self.active_pokemon:
            mprint(f"{base_pokemon.name} non si trova né in panchina né è il Pokémon attivo.")
            return False
        
        # Controlla che il Pokémon Base corrisponda alla carta Stage1
        if stage1_card.code not in base_pokemon.stage1_code :
            mprint(f"{stage1_card.name} non può evolvere {base_pokemon.name}.")
            return False

        # Mantieni le Energie e le condizioni di stato
        stage1_card.attached_energies = base_pokemon.attached_energies
        base_pokemon.attached_energies=[]
        stage1_card.status_condition = base_pokemon.status_condition

        # Sostituisci la carta Base con la carta Stage1
        if base_pokemon == self.active_pokemon:
            self.active_pokemon = stage1_card
        else:
            bench_index = self.bench.index(base_pokemon)
            self.bench[bench_index] = stage1_card

        # Rimuovi la carta Stage1 dalla mano
        self.hand.remove(stage1_card)

        # Sposta la carta Base sotto la carta Stage1 (opzionale)
        stage1_card.previous_stage = base_pokemon

        mprint(f"{base_pokemon.name} è evoluto in {stage1_card.name}!")
        return True
    
    def shuffle_the_deck(self):
        random.shuffle(self.deck)
        
    def evolve_pokemon_to_stage2(self, stage1_pokemon, stage2_card):
        if not stage1_pokemon:
            mprint(f"evolve_pokemon_to_stage2>>stage1_pokemon è {stage1_pokemon}")
            return False
        """
        Evolve un Pokémon Stage 1 a una carta Stage 2.
    
        Args:
            stage1_pokemon (PokemonStage1Card): Il Pokémon Stage 1 da evolvere.
            stage2_card (PokemonStage2Card): La carta Stage 2 da utilizzare per l'evoluzione.
    
        Returns:
            bool: True se l'evoluzione ha avuto successo, False altrimenti.
        """
        # Controlla se la carta Stage2 è nella mano
        if stage2_card not in self.hand:
            mprint(f"La carta non è nella tua mano.")
            return False
    
        # Controlla se il Pokémon Stage 1 è in panchina o attivoùif stage1_pokemon
        if stage1_pokemon not in self.bench and stage1_pokemon != self.active_pokemon:
            mprint(f"{stage1_pokemon.name} non si trova né in panchina né è il Pokémon attivo.")
            return False
    
        # Controlla che il Pokémon Stage 1 corrisponda alla carta Stage 2
        if stage2_card.code not in stage1_pokemon.stage2_code:
            mprint(f"{stage2_card.name} non può evolvere {stage1_pokemon.name}.")
            return False
    
        # Mantieni le Energie e le condizioni di stato
        stage2_card.attached_energies = stage1_pokemon.attached_energies
        stage1_pokemon.attached_energies = []
        stage2_card.status_condition = stage1_pokemon.status_condition
    
        # Sostituisci la carta Stage 1 con la carta Stage 2
        if stage1_pokemon == self.active_pokemon:
            self.active_pokemon = stage2_card
        else:
            bench_index = self.bench.index(stage1_pokemon)
            self.bench[bench_index] = stage2_card
    
        # Rimuovi la carta Stage 2 dalla mano
        self.hand.remove(stage2_card)
    
        # Sposta la carta Stage 1 sotto la carta Stage 2 (opzionale)
        stage2_card.previous_stage = stage1_pokemon
    
        mprint(f"{stage1_pokemon.name} è evoluto in {stage2_card.name}!")
        return True

    def evolve_pokemon_to_stage2_from_base(self, base_pokemon, stage2_card):
        """
        Evolve un Pokémon Base direttamente a una carta Stage 2, ad esempio utilizzando Rare Candy.
    
        Args:
            base_pokemon (PokemonBaseCard): Il Pokémon Base da evolvere.
            stage2_card (PokemonStage2Card): La carta Stage 2 da utilizzare per l'evoluzione.
    
        Returns:
            bool: True se l'evoluzione ha avuto successo, False altrimenti.
        """
        # Controlla se la carta Stage2 è nella mano
        if stage2_card not in self.hand:
            mprint(f"La carta {stage2_card.name} non è nella tua mano.")
            return False
    
        # Controlla se il Pokémon Base è in panchina o attivo
        if base_pokemon not in self.bench and base_pokemon != self.active_pokemon:
            mprint(f"{base_pokemon.name} non si trova né in panchina né è il Pokémon attivo.")
            return False
    
        # Controlla che il Pokémon Base corrisponda alla carta Stage 2
        if stage2_card.code not in base_pokemon.stage2_code:
            mprint(f"{stage2_card.name} non può evolvere {base_pokemon.name}.")
            return False
    
        # Controlla se è disponibile Rare Candy nella mano (o altra condizione speciale)
        rare_candy = next((card for card in self.hand if card.code == "SVI191"), None)  # Codice di Rare Candy
        if not rare_candy:
            mprint("Non hai Rare Candy nella tua mano per eseguire questa evoluzione.")
            return False
    
        # Mantieni le Energie e le condizioni di stato
        stage2_card.attached_energies = base_pokemon.attached_energies
        base_pokemon.attached_energies = []
        stage2_card.status_condition = base_pokemon.status_condition
    
        # Sostituisci la carta Base con la carta Stage 2
        if base_pokemon == self.active_pokemon:
            self.active_pokemon = stage2_card
        else:
            bench_index = self.bench.index(base_pokemon)
            self.bench[bench_index] = stage2_card
    
        # Rimuovi la carta Stage 2 dalla mano
        self.hand.remove(stage2_card)
    
        # Scarta Rare Candy
        self.discard_card_from(self.hand, rare_candy.code)
    
        # Sposta la carta Base sotto la carta Stage 2 (opzionale)
        stage2_card.previous_stage = base_pokemon
    
        mprint(f"{base_pokemon.name} è evoluto direttamente in {stage2_card.name} grazie a Rare Candy!")
        return True
  