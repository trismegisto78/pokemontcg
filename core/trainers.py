from core.card import *
import random
from core.utils import mprint

        

class SupporterTrainerCard(TrainerCard):
    def __init__(self,index,code, name):
        super().__init__(index,code,name, "Supporter")

    def execute_effect(self, game_state):
        return True
        
    def can_use_it(self, game_state):
        return not game_state.supporter_played


class ToolTrainerCard(TrainerCard):
    def __init__(self,index,code, name):
        super().__init__(index,code, name, "Tool")

    def execute_effect(self, game_state):
        return True

    def can_use_it(self, game_state):
        return True


class ProfessorSadaVitalityTrainerCard(SupporterTrainerCard):
    def __init__(self,index):
        super().__init__(index,"PAR170","Professor Sada Vitality")

    def can_use_it(self, game_state):
        
        if not super().can_use_it(game_state):
            return False
        
        ancient_pokemon = [pokemon for pokemon in game_state.bench if isinstance(pokemon, PokemonCard) and pokemon.label=="Ancient" ]
        if not len(ancient_pokemon)>0:
            #mprint(f"{game_state.name}:professor_sada_vitality: non ci sono Pokémon Ancient in panchina")
            return False
        
        
        nrgs = [nrg for nrg in game_state.discard_pile if isinstance(nrg, EnergyCard) ]
        if not len(nrgs)>0:
            #mprint(f"{game_state.name}:professor_sada_vitality: non ci sono Energie in pila discardui")
            return False
        
        return True

    
    def execute_effect(self, game_state):
        mprint(f"{game_state.name} sta eseguendo professor_sada_vitality")

        # Scegli fino a 2 Pokémon "Ancient"
        ancient_pokemon = [pokemon for pokemon in game_state.bench if isinstance(pokemon, PokemonCard) and pokemon.label=="Ancient"]

        if not ancient_pokemon:
            mprint(f"{game_state.name}:professor_sada_vitality: non ci sono Pokémon Ancient in panchina")
            return -1

        energie_assegnate = 0
        #energy_cards = game_state.choose_energies_to_assign()
        # Assegna una carta Energia dalla pila degli scarti
        for pokemon in ancient_pokemon:
            energy_card = next(   (card for card in game_state.discard_pile if  isinstance(card, EnergyCard) ), None   )
            if energy_card:
                pokemon.attach_energy(game_state.discard_pile,energy_card) 
                mprint(f"{game_state.name}:professor_sada_vitality:Energia assegnata a {pokemon.name}.")
                energie_assegnate+=1
            else:
                mprint(f"Non ci sono più energie scartate non posso apploicare l'aeffetto di Professor Sada Vitality")
         

        # Se è stata assegnata energia, pesca 3 carte
        if ancient_pokemon:
            for _ in range(3):
                if game_state.deck:
                    game_state.hand.append(game_state.deck.pop(0))
                else:
                    mprint("Il mazzo è vuoto.")
                    
        game_state.draw_cards(3)
        
        game_state.discard_card_from( game_state.hand, self.code)
        
        game_state.supporter_played = True
        
        
        return energie_assegnate


class ArvenTrainerCard(SupporterTrainerCard):
    def __init__(self, index):
        """
        Inizializza la carta Allenatore Arven.
        """
        super().__init__(index, "OBF186", "Arven")

    def can_use_it(self, game_state):
        """
        Verifica se la carta può essere usata.
        Può essere usata solo se ci sono carte Item o Pokémon Tool nel mazzo.
        """
        # Controlla se ci sono carte Item o Tool nel mazzo
        has_item = any(isinstance(card, ToolTrainerCard) for card in game_state.deck)
        return super().can_use_it(game_state) and has_item

    def execute_effect(self, game_state):
        """
        Esegue l'effetto della carta:
        - Cerca una carta Item e una carta Pokémon Tool nel mazzo.
        - Le aggiunge alla mano.
        - Mescola il mazzo.
        """
        mprint(f"{game_state.name} sta usando Arven.")

        # Cerca una carta Item nel mazzo
        item_card = next((card for card in game_state.deck if isinstance(card, ToolTrainerCard) ), None)

        # Cerca una carta Pokémon Tool nel mazzo
        #tool_card = next((card for card in game_state.deck if isinstance(card, ToolTrainerCard) ), None)

        # Aggiungi le carte trovate alla mano
        if item_card:
            game_state.hand.append(item_card)
            game_state.deck.remove(item_card)
            mprint(f"Arven aggiunge alla mano la carta Item: {item_card.name}.")
        else:
            mprint("Nessuna carta Item trovata nel mazzo.")
        '''
        if tool_card:
            game_state.hand.append(tool_card)
            game_state.deck.remove(tool_card)
            mprint(f"Arven aggiunge alla mano la carta Tool: {tool_card.name}.")
        else:
            mprint("Nessuna carta Pokémon Tool trovata nel mazzo.")
        '''
        # Mescola il mazzo
        game_state.shuffle_the_deck()
        mprint("Il mazzo è stato mescolato.")

        # Scarta la carta Arven
        game_state.discard_card(self.code)

class NestballTrainerCard(ToolTrainerCard):
    def __init__(self,index):
        super().__init__(index,"SVI181","Nest Ball")
        
    def can_use_it(self, game_state):
        basic_pokemon = next(  (card for card in game_state.deck if isinstance(card, PokemonBaseCard) ), None   )
        if len(game_state.bench)>=5 or not basic_pokemon:
            return False
        
        return True

    def execute_effect(self, game_state):
        mprint(f"{game_state.name} sta eseguendo nest_ball")
        # Cerca un Pokémon Base nel mazzo
        basic_pokemon = next(  (card for card in game_state.deck if isinstance(card, PokemonBaseCard) ), None   )
        mprint(f"{game_state.name} sta eseguendo nest_ball2")
        if not basic_pokemon:
            mprint("{game_state.name}:nest_ball:Non ci sono Pokémon Base nel mazzo.")
            return False

        # Mettilo in panchina
        game_state.bench.append(basic_pokemon)
        game_state.deck.remove(basic_pokemon)
        mprint(f"{game_state.name}:nest_ball:{basic_pokemon.name} è stato aggiunto alla panchina.")
        game_state.discard_pile.append(self)
        game_state.hand.remove(self)
        # Mescola il mazzo
        random.shuffle(game_state.deck)
        return True
    
class EarthenVesselTrainerCard(ToolTrainerCard):
    def __init__(self,index):
        super().__init__(index,"PAR163","Earthen Vessel")
        
    def can_use_it(self, game_state):
        """
        Verifica se la carta può essere usata. Deve esserci almeno una carta da scartare
        oltre a questa carta.
        """
        # Controlla se ci sono almeno altre carte nella mano oltre a questa
        if len(game_state.hand) <= 1:  # Serve almeno 1 carta da scartare + questa carta
           # mprint(f"{game_state.name}: Non ci sono abbastanza carte nella mano per usare Earthen Vessel.")
            return False
        return True

    def execute_effect(self, game_state):
        """
        Esegue l'effetto di Earthen Vessel:
        - Scarta una carta dalla mano.
        - Cerca fino a 2 carte Energia Base dal mazzo, rivelale e aggiungile alla mano.
        - Mescola il mazzo.
        """
        mprint(f"{game_state.name} sta eseguendo Earthen Vessel.")

        # Controlla se ci sono abbastanza carte per scartare
        if len(game_state.hand) <= 1:
            mprint("Non ci sono abbastanza carte per usare Earthen Vessel.")
            return False

        # Scarta una carta dalla mano (diversa da questa)
        target_card = next((card for card in game_state.hand if card != self), None)
        if not target_card:
            mprint(f"{game_state.name}: Nessuna carta valida da scartare per usare Earthen Vessel.")
            return False

        game_state.discard_pile.append(target_card)
        game_state.hand.remove(target_card)
        mprint(f"{target_card.name} è stata scartata.")

        # Cerca fino a 2 carte Energia Base nel mazzo
        basic_energies = [card for card in game_state.deck if isinstance(card, EnergyCard)]
        if not basic_energies:
            mprint(f"{game_state.name}: Non ci sono carte Energia Base nel mazzo.")
            return False

        # Aggiungi fino a 2 carte Energia Base alla mano
        selected_energies = basic_energies[:2]  # Prendi le prime 2 Energie Base
        for energy_card in selected_energies:
            game_state.hand.append(energy_card)
            game_state.deck.remove(energy_card)
            mprint(f"{energy_card.name} è stata aggiunta alla mano.")

        # Mescola il mazzo
        random.shuffle(game_state.deck)
        mprint(f"{game_state.name}: Il mazzo è stato mescolato.")

        # Scarta la carta Earthen Vessel
        game_state.discard_card(self.code)
        mprint(f"{self.name} è stata scartata.")

        return True


class UltraBallTrainerCard(ToolTrainerCard):
    def __init__(self,index):
        super().__init__(index,"SVI196","Ultra Ball")

    def can_use_it(self, game_state):
        if len(game_state.hand) < 3:
            return False
        
        return True

    def execute_effect(self, game_state):
        mprint(f"{game_state.name} sta eseguendo ultra ball")
       
        # Controlla se ci sono abbastanza carte da scartare
        if len(game_state.hand) < 3:
            mprint("Non hai abbastanza carte per usare Ultra Ball.")
            return False
        
        # Scarta 2 carte dalla mano
        target_card = [card for card in game_state.hand if not card==self ]
        if len(target_card)>1:
            game_state.discard_pile.append(target_card[0] )
            game_state.hand.remove( target_card[0] ) 
        
        target_card = [card for card in game_state.hand if not card==self ]
        if len(target_card)>1:
            game_state.discard_pile.append(target_card[0] )
            game_state.hand.remove( target_card[0] ) 


        # Cerca un Pokémon nel mazzo
        target_pokemon = next( (card for card in game_state.deck if isinstance(card, PokemonCard)), None )
        if not target_pokemon:
            mprint("Non ci sono Pokémon nel mazzo.")
            return False

        # Aggiungi il Pokémon alla mano
        game_state.hand.append(target_pokemon)
        game_state.deck.remove(target_pokemon)
        mprint(f"{target_pokemon.name} è stato aggiunto alla mano.")

        # Mescola il mazzo
        random.shuffle(game_state.deck)
        
        game_state.discard_card(self.code) # scarto la ultraball che sto usando
        
        
        return True


class IonoTrainerCard(SupporterTrainerCard):
    def __init__(self, index):
        super().__init__(index, "PAR185", "Iono")

    def can_use_it(self, game_state):
        if not super().can_use_it(game_state):
            return False
        return True

    def execute_effect(self, game_state):
        """
        Esegue l'effetto della carta Iono:
        - Ogni giocatore rimescola la propria mano e la mette in fondo al mazzo.
        - Ogni giocatore pesca tante carte quanti sono i premi rimanenti.
        """
        mprint(f"{game_state.name} sta giocando la carta Iono.")
        game_state.discard_card_from(game_state.hand, self.code)
        # 1. Rimescola la mano e mettila in fondo al mazzo
        if game_state.hand:
            game_state.deck.extend(game_state.hand)  # Aggiunge la mano in fondo al mazzo
            game_state.shuffle_the_deck()# Mescola il mazzo
            mprint(f"{game_state.name}: Mano rimescolata nel mazzo.")
            game_state.hand = []  # Svuota la mano
        
        # 2. Pesca carte pari ai premi rimanenti
        remaining_prizes = len(game_state.prizes)
        if remaining_prizes > 0:
            game_state.draw_cards(remaining_prizes)
            mprint(f"{game_state.name}: Pesca {remaining_prizes} carte (pari ai premi rimanenti).")
        
        # 3. Applica lo stesso effetto all'avversario
        opponent = game_state.opponent
        if opponent.hand:
            opponent.deck.extend(opponent.hand)  # Aggiunge la mano dell'avversario in fondo al mazzo
            opponent.shuffle_the_deck()
            mprint(f"{opponent.name}: Mano avversaria rimescolata nel mazzo.")
            opponent.hand = []  # Svuota la mano dell'avversario
        
        opponent_remaining_prizes = len(opponent.prizes)
        if opponent_remaining_prizes > 0:
            opponent.draw_cards(opponent_remaining_prizes)
            mprint(f"{opponent.name}: Pesca {opponent_remaining_prizes} carte (pari ai premi rimanenti).")

        # 4. Sposta Iono nella pila degli scarti
        
        game_state.supporter_played = True  # Segna che una carta supporter è stata giocata
        
        
class EnergyRetrievalTrainerCard(ToolTrainerCard):
    def __init__(self, index):
        super().__init__(index, "SVI171", "Energy Retrieval")

    def can_use_it(self, game_state):
        """
        Verifica se la carta può essere usata. Deve esserci almeno una carta Energia Base nella pila degli scarti.
        """
        # Controlla se ci sono carte Energia Base nella pila degli scarti
        basic_energies_in_discard = [
            card for card in game_state.discard_pile if isinstance(card, EnergyCard)
        ]
        if not basic_energies_in_discard:
            #mprint(f"{game_state.name}: Non ci sono carte Energia Base nella pila degli scarti per usare Energy Retrieval.")
            return False
        return True

    def execute_effect(self, game_state):
        """
        Esegue l'effetto di Energy Retrieval:
        - Recupera fino a 2 carte Energia Base dalla pila degli scarti e le aggiunge alla mano.
        """
        mprint(f"{game_state.name} sta eseguendo Energy Retrieval.")

        # Trova fino a 2 carte Energia Base nella pila degli scarti
        basic_energies_in_discard = [
            card for card in game_state.discard_pile if isinstance(card, EnergyCard)
        ]

        if not basic_energies_in_discard:
            mprint("Non ci sono carte Energia Base nella pila degli scarti.")
            return False

        # Recupera fino a 2 carte
        selected_energies = basic_energies_in_discard[:2]
        for energy_card in selected_energies:
            game_state.hand.append(energy_card)
            game_state.discard_pile.remove(energy_card)
            mprint(f"{energy_card.name} è stata recuperata dalla pila degli scarti e aggiunta alla mano.")

        # Scarta la carta Energy Retrieval
        game_state.discard_card(self.code)
        mprint(f"{self.name} è stata scartata.")

        return True

class BuddyBuddyPoffinTrainerCard(ToolTrainerCard):
    def __init__(self, index):
        """
        Inizializza la carta Buddy-Buddy Poffin.
        """
        super().__init__(index, "TEF144", "Buddy-Buddy Poffin")

    def can_use_it(self, game_state):
        """
        Verifica se la carta può essere usata.
        Può essere usata solo se ci sono spazi liberi in panchina e Pokémon con <= 70 HP nel mazzo.
        """
        # Verifica che ci siano slot liberi in panchina
        has_bench_space = len(game_state.bench) < 5

        # Verifica che ci siano Pokémon Base con <= 70 HP nel mazzo
        has_valid_pokemon = any(
            isinstance(card, PokemonBaseCard) and card.hp <= 70 for card in game_state.deck
        )

        return super().can_use_it(game_state) and has_bench_space and has_valid_pokemon

    def execute_effect(self, game_state):
        """
        Esegue l'effetto della carta:
        - Cerca fino a 2 Pokémon Base con 70 HP o meno nel mazzo e li mette in panchina.
        """
        mprint(f"{game_state.name} usa Buddy-Buddy Poffin.")

        # Verifica che ci siano spazi liberi in panchina
        if len(game_state.bench) >= 5:
            mprint("La panchina è piena. Non puoi usare Buddy-Buddy Poffin.")
            return False

        # Trova Pokémon Base con <= 70 HP nel mazzo
        valid_pokemon = [
            card for card in game_state.deck
            if isinstance(card, PokemonBaseCard) and card.hp <= 70
        ]

        if not valid_pokemon:
            mprint("Non ci sono Pokémon validi nel mazzo per usare Buddy-Buddy Poffin.")
            return False

        # Seleziona fino a 2 Pokémon da mettere in panchina
        selected_pokemon = valid_pokemon[:2]  # Prendi i primi 2 Pokémon validi
        for pokemon in selected_pokemon:
            if len(game_state.bench) < 5:
                game_state.bench.append(pokemon)
                game_state.deck.remove(pokemon)
                mprint(f"{pokemon.name} è stato messo in panchina.")

        # Mescola il mazzo
        random.shuffle(game_state.deck)
        mprint("Il mazzo è stato mescolato.")

        # Scarta Buddy-Buddy Poffin
        game_state.discard_card(self.code)

        return True

class BossOrdersTrainerCard(SupporterTrainerCard):
    def __init__(self, index):
        """
        Inizializza la carta Allenatore Boss's Orders.
        """
        super().__init__(index, "PAL172", "Boss's Orders")

    def can_use_it(self, game_state):
        """
        Verifica se la carta può essere usata.
        Può essere usata solo se l'avversario ha Pokémon in panchina.
        """
        # Controlla se l'avversario ha Pokémon in panchina
        has_benched_pokemon = any(isinstance(pokemon, PokemonCard) for pokemon in game_state.opponent.bench)
        return super().can_use_it(game_state) and has_benched_pokemon

    def execute_effect(self, game_state):
        """
        Esegue l'effetto della carta:
        - Cambia un Pokémon in panchina dell'avversario con il Pokémon attivo.
        """
        mprint(f"{game_state.name} usa Boss's Orders.")

        # Verifica che l'avversario abbia Pokémon in panchina
        if not any(isinstance(pokemon, PokemonCard) for pokemon in game_state.opponent.bench):
            mprint("L'avversario non ha Pokémon in panchina. Boss's Orders non può essere usato.")
            return False

        # Seleziona il Pokémon dalla panchina avversaria (potrebbe essere casuale o scelto da un agente)
        target_pokemon = game_state.opponent.bench[0]  # Per semplicità, prendi il primo Pokémon in panchina
        game_state.opponent.bench.remove(target_pokemon)

        # Scambia il Pokémon attivo dell'avversario
        if game_state.opponent.active_pokemon:
            game_state.opponent.bench.append(game_state.opponent.active_pokemon)

        game_state.opponent.active_pokemon = target_pokemon
        mprint(f"Il Pokémon attivo dell'avversario è ora {target_pokemon.name}.")

        # Scarta Boss's Orders
        game_state.discard_card(self.code)

        return True



class RareCandyTrainerCard(ToolTrainerCard):
    def __init__(self, index):
        """
        Inizializza la carta Trainer Rare Candy.
        """
        super().__init__(index, "SVI191", "Rare Candy")

    def can_use_it(self, game_state):
        """
        Verifica se la carta Rare Candy può essere utilizzata.

        Args:
            game_state (GameState): Lo stato attuale del gioco.

        Returns:
            bool: True se Rare Candy può essere utilizzato, False altrimenti.
        """
        # Controlla se c'è un Pokémon Base in gioco
        base_pokemon_in_play = any(
            isinstance(pokemon, PokemonBaseCard)
            for pokemon in ([game_state.active_pokemon] + game_state.bench)
        )

        # Controlla se c'è una carta Stage 2 corrispondente nella mano
        stage2_in_hand = any(
            isinstance(card, PokemonStage2Card) for card in game_state.hand
        )

        # Non può essere usata al primo turno o su Pokémon messi in gioco durante questo turno
        if game_state.turn_count == 1:
            mprint("Non puoi usare Rare Candy al primo turno.")
            return False

        # Rare Candy può essere usata solo se entrambe le condizioni sono vere
        if base_pokemon_in_play and stage2_in_hand:
            return True

        mprint("Rare Candy non può essere usata: assicurati di avere un Pokémon Base in gioco e una carta Stage 2 corrispondente nella tua mano.")
        return False

    def execute_effect(self, game_state):
        """
        Esegue l'effetto della carta Rare Candy.

        Args:
            game_state (GameState): Lo stato attuale del gioco.

        Returns:
            bool: True se l'effetto è stato eseguito correttamente, False altrimenti.
        """
        mprint(f"{game_state.name} usa Rare Candy!")

        # Cerca i Pokémon Base in gioco
        base_pokemon_choices = [
            pokemon
            for pokemon in ([game_state.active_pokemon] + game_state.bench)
            if isinstance(pokemon, PokemonBaseCard)
        ]

        if not base_pokemon_choices:
            mprint("Non ci sono Pokémon Base validi in gioco per usare Rare Candy.")
            return False

        # Scegli un Pokémon Base (implementa una logica per la scelta, ad esempio interfaccia o scelta automatica)
        base_pokemon = base_pokemon_choices[0]  # Per semplicità, prende il primo disponibile

        # Cerca le carte Stage 2 corrispondenti nella mano
        stage2_choices = [
            card
            for card in game_state.hand
            if isinstance(card, PokemonStage2Card)
            and card.code in base_pokemon.stage2_code
        ]

        if not stage2_choices:
            mprint("Non ci sono carte Stage 2 valide nella tua mano per evolvere questo Pokémon.")
            return False

        # Scegli una carta Stage 2 (implementa una logica per la scelta)
        stage2_card = stage2_choices[0]  # Per semplicità, prende la prima disponibile

        # Esegui l'evoluzione
        if game_state.evolve_pokemon_to_stage2_from_base(base_pokemon, stage2_card):
            # Scarta Rare Candy
            game_state.discard_card_from(game_state.hand, self.code)
            return True

        mprint("Evoluzione fallita.")
        return False



class ProfessorsResearchCard(SupporterTrainerCard):
    """
    Professor's Research – Supporter Trainer
    Effetto:
      - Scarta la tua mano e pesca 7 carte.
    """
    def __init__(self, index):
        super().__init__(index, "PSR001", "Professor's Research")

    def can_use_it(self, game_state):
        # Limita a 1 Supporter per turno
        return super().can_use_it(game_state)

    def execute_effect(self, game_state, opponent=None):
        mprint(f"{self.name}: scarto la mano e pesco 7 carte.")
        # Scarta tutta la mano
        game_state.discard_full_hand()
        # Pesca 7 carte
        game_state.draw_cards(7)
        return True
    


class ProfessorTuroSScenarioCard(SupporterTrainerCard):
    """
    Professor Turo's Scenario – Supporter Trainer
    Effetto:
      - Prendi 1 dei tuoi Pokémon in gioco e mettilo in mano. (Scarta tutte le carte attaccate a quel Pokémon.)
    """
    def __init__(self, index):
        super().__init__(index, "PTS001", "Professor Turo's Scenario")

    def can_use_it(self, game_state):
        # Limita a 1 Supporter per turno e serve almeno un Pokémon in gioco
        if not super().can_use_it(game_state):
            return False
        return bool(game_state.active_pokemon or game_state.bench)

    def execute_effect(self, game_state, opponent=None):
        # Scegli un tuo Pokémon in gioco: prima l'attivo, altrimenti il primo in panchina
        target = game_state.active_pokemon or (game_state.bench[0] if game_state.bench else None)
        if not target:
            mprint("Nessun Pokémon in gioco da riportare in mano.")
            return False

        mprint(f"{self.name}: riporto {target.name} in mano e scarto tutte le carte attaccate.")
        # Scarto tutte le Energie attaccate
        while target.attached_energies:
            energy = target.attached_energies.pop(0)
            game_state.discard_pile.append(energy)
        # Scarto eventuale Pokémon Tool
        if getattr(target, "attached_item", None):
            game_state.discard_pile.append(target.attached_item)
            target.attached_item = None

        # Rimuovo il Pokémon dal campo
        if game_state.active_pokemon is target:
            game_state.active_pokemon = None
        else:
            game_state.bench.remove(target)

        # Metto il Pokémon in mano
        game_state.hand.append(target)
        return True




class KieranCard(SupporterTrainerCard):
    """
    Kieran – Supporter Trainer
    Effetto (scegli 1):
      • Scambia il tuo Pokémon Active con 1 Pokémon in panchina.
      • Durante questo turno, gli attacchi dei tuoi Pokémon infliggono 30 danni in più
        a Pokémon ex e Pokémon V avversari (prima di debolezza e resistenza).
    """
    def __init__(self, index):
        super().__init__(index, "KIE001", "Kieran")

    def can_use_it(self, game_state):
        # Limita a 1 Supporter per turno
        return super().can_use_it(game_state)

    def execute_effect(self, game_state, opponent=None):
        mprint(f"{self.name}: scegli un effetto.")

        # Per semplicità, selezioniamo casualmente un effetto
        choice = random.choice([1, 2])
        if choice == 1:
            # Scambia Active ↔ primo in panchina
            if not game_state.bench:
                mprint("Non hai Pokémon in panchina da scambiare.")
                return False
            new_active = game_state.bench.pop(0)
            old_active = game_state.active_pokemon
            game_state.bench.append(old_active)
            game_state.active_pokemon = new_active
            mprint(f"{self.name}: scambiato {old_active.name} con {new_active.name}.")
        else:
            # Imposta bonus di danno per ex/V
            # Qui registriamo un flag su game_state: da integrare nella logica di attacco
            game_state.kieran_boost = 30
            mprint(f"{self.name}: i tuoi attacchi infliggeranno +30 danni a Pokémon ex e V questo turno.")
        return True
    





class Pokegear30Card(TrainerCard):
    """
    Pokégear 3.0 – Item Trainer
    Effetto: guarda le prime 7 carte del tuo mazzo. Puoi rivelare una carta Aiuto trovata lì e metterla in mano.
    Rimescola poi il mazzo.
    """
    def __init__(self, index):
        super().__init__(index, "PGE003", "Pokégear 3.0", "Item")

    def can_use_it(self, game_state):
        # Nessuna restrizione speciale
        return super().can_use_it(game_state)

    def execute_effect(self, game_state, opponent=None):
        # Guarda le prime 7 carte
        top7 = game_state.deck[:7]
        mprint(f"{self.name}: guardi le prime 7 carte del mazzo: {[c.name for c in top7]}")

        # Trova una carta Aiuto
        supporters = [c for c in top7 if isinstance(c, SupporterTrainerCard)]
        if supporters:
            chosen = supporters[0]
            mprint(f"{self.name}: rivelata carta Aiuto {chosen.name}, aggiunta alla mano.")
            # Sposta la carta dalla cima alla mano
            game_state.deck.remove(chosen)
            game_state.hand.append(chosen)
        else:
            mprint(f"{self.name}: nessuna carta Aiuto trovata.")

        # Rimescola il mazzo
        game_state.shuffle_the_deck()
        mprint(f"{self.name}: mazzo rimescolato.")

        # Scarta Pokégear 3.0
        game_state.discard_card(self.code)
        return True
    





class BlackBeltsTrainingCard(ToolTrainerCard):
    """
    Black Belt's Training – Pokémon Tool
    Effetto:
      Durante questo turno, gli attacchi dei tuoi Pokémon infliggono
      40 danni in più al Pokémon attivo ex dell’avversario
      (prima di applicare debolezza e resistenza).
    """
    def __init__(self, index):
        super().__init__(index, "BBT002", "Black Belt's Training")

    def can_use_it(self, game_state):
        # Nessuna restrizione speciale: può essere giocata in qualsiasi momento
        return super().can_use_it(game_state)

    def execute_effect(self, game_state, opponent=None):
        mprint(f"{game_state.name} usa {self.name}!")
        # Imposta il bonus di danno per questo turno
        game_state.black_belt_training = 40
        return True





class NightStretcherCard(ToolTrainerCard):
    """
    Night Stretcher – Item Trainer
    Effetto:
      Metti in mano dal tuo scarto 1 Pokémon o 1 Energia Base.
    """
    def __init__(self, index):
        super().__init__(index, "NST002", "Night Stretcher")

    def can_use_it(self, game_state):
        # Puoi usarla solo se nel tuo scarto c'è almeno un Pokémon o una Basic Energy
        return any(
            isinstance(c, PokemonCard) or
            (isinstance(c, EnergyCard) and c.energy_type == "Basic")
            for c in game_state.discard_pile
        )

    def execute_effect(self, game_state, opponent=None):
        mprint(f"{game_state.name} usa {self.name}!")
        # Trova il primo Pokémon o Energia Base nel discard pile
        target = next(
            (c for c in game_state.discard_pile
             if isinstance(c, PokemonCard) or
                (isinstance(c, EnergyCard) and c.energy_type == "Basic")),
            None
        )
        if not target:
            mprint("Nessun Pokémon o Energia Base nel mazzo degli scarti.")
            return False

        # Sposta la carta in mano
        game_state.discard_pile.remove(target)
        game_state.hand.append(target)
        mprint(f"{target.name} è stato rimesso in mano.")

        # Scarta Night Stretcher
        game_state.discard_pile.append(self)
        game_state.hand.remove(self)
        return True





class PalPadCard(ToolTrainerCard):
    """
    Pal Pad – Item Trainer
    Effetto: mischia fino a 2 carte Supporter dal tuo mazzo degli scarti nel tuo mazzo principale.
    """
    def __init__(self, index):
        super().__init__(index, "PALPAD001", "Pal Pad")

    def can_use_it(self, game_state):
        # Puoi usare Pal Pad solo se nel tuo discard pile ci sono carte Supporter
        return any(isinstance(c, SupporterTrainerCard) for c in game_state.discard_pile)

    def execute_effect(self, game_state, opponent=None):
        supporters = [c for c in game_state.discard_pile if isinstance(c, SupporterTrainerCard)]
        if not supporters:
            mprint("Nessuna carta Supporter nel mazzo degli scarti.")
            return False
        # Prendi fino a 2 carte Supporter
        to_shuffle = supporters[:2]
        for card in to_shuffle:
            game_state.discard_pile.remove(card)
            game_state.deck.append(card)
        mprint(f"{self.name}: mescolate nel mazzo le carte Supporter: {[c.name for c in to_shuffle]}")
        game_state.shuffle_the_deck()
        # Scarta Pal Pad
        game_state.discard_pile.append(self)
        game_state.hand.remove(self)
        return True




class ScoopUpCycloneCard(ToolTrainerCard):
    """
    Scoop Up Cyclone – Item Trainer
    Effetto:
      Riporta in mano 1 dei tuoi Pokémon e tutte le carte ad esso attaccate.
    """
    def __init__(self, index):
        super().__init__(index, "SUC002", "Scoop Up Cyclone")

    def can_use_it(self, game_state):
        # Puoi usarla se hai almeno un Pokémon in gioco
        return bool(game_state.active_pokemon or game_state.bench)

    def execute_effect(self, game_state, opponent=None):
        # Scegli un tuo Pokémon in gioco (Active altrimenti primo in bench)
        target = game_state.active_pokemon or (game_state.bench[0] if game_state.bench else None)
        if not target:
            mprint("Non ci sono Pokémon in gioco.")
            return False

        mprint(f"{game_state.name} usa {self.name} su {target.name}.")

        # Rimuovi e restituisci in mano tutte le Energie attaccate
        for energy in target.attached_energies[:]:
            target.attached_energies.remove(energy)
            game_state.hand.append(energy)
        # Rimuovi e restituisci in mano ogni strumento attaccato
        if getattr(target, "attached_item", None):
            item = target.attached_item
            target.attached_item = None
            game_state.hand.append(item)

        # Rimuovi il Pokémon dal campo e mettilo in mano
        if game_state.active_pokemon is target:
            game_state.active_pokemon = None
        else:
            game_state.bench.remove(target)
        game_state.hand.append(target)

        # Scarta Scoop Up Cyclone
        game_state.discard_card(self.code)
        return True



class JammingTowerCard(TrainerCard):
    """
    Jamming Tower – Stadium Trainer
    Effetto:
      Pokémon Tools attaccati a ciascun Pokémon (tuoi e avversari) non hanno effetto.
    """
    def __init__(self, index):
        super().__init__(index, "JAM001", "Jamming Tower", "Stadium")

    def can_use_it(self, game_state):
        # Puoi giocare una sola carta Stadio per turno; il controllo è nel motore di gioco
        return super().can_use_it(game_state)

    def execute_effect(self, game_state, opponent=None):
        mprint(f"{game_state.name} gioca lo Stadio {self.name}: tutti i Pokémon Tool non hanno effetto.")
        # L’effetto viene gestito globalmente controllando game_state.stadium_card
        return True
