from core.card import *
from core.utils import mprint

        
        
class RagingBoltPokemonCard(PokemonBaseCard):
    def __init__(self,index):
        super().__init__(index,"TEF123","Raging Bolt Ex","Dragon",240, 3, None, None,"ex","Ancient")
        
    def attack_count(self):
        return 2
        
    def attack_instructions(self,attIndex,player,opponent_player):
        pokemon_to = opponent_player.active_pokemon
        if attIndex==0:
            if len(self.attached_energies)>=1:
                player.discard_full_hand()
                player.draw_cards(6)                        
                mprint(f"{self.name} esegue l'attacco Burst Roaro")
                return True
            else:
                mprint(f"{self.name} Attacco non valido. Mancano le energie.")
                return False
        if attIndex==1:
            if len(self.attached_energies)>=2: #per semplicità due energie qualsiasi
                energies = player.discard_energy_from_bench(2) # scarta solo 2 energie
                total_damage = 70 * len(energies)
                mprint(f"{self.name} esegue l'attacco LF Bellowing Thunder 70× {total_damage}")
                pokemon_to.receive_damage(total_damage, opponent_player)
                return True
            else:
                mprint(f"{self.name} Attacco non valido. Mancano le energie.")
                return False
        mprint(f"{self.name} Attacco non valido.")      
        return False
    
    
class Teal_Mask_Ogerpon_ex(PokemonBaseCard):
    def __init__(self,index):
        super().__init__(index,"TWM25","Teal Mask Ogerpon ex ","Grass",210, 1, None, None,"ex","Tera")
        
    def attack_count(self):
        return 1

    def can_use_ability(self, game_state):
        """
        Verifica se l'abilità Teal Dance può essere usata.
    
        Args:
            game_state: L'oggetto che rappresenta lo stato attuale del gioco.
    
        Returns:
            bool: True se l'abilità può essere usata, False altrimenti.
        """
        # Verifica che il Pokémon attivo sia Teal Mask Ogerpon ex
        if not (game_state.active_pokemon and isinstance(game_state.active_pokemon, Teal_Mask_Ogerpon_ex)   ):
            #mprint("Teal Dance non può essere usato perché il Pokémon attivo non è Teal Mask Ogerpon ex.")
            return False
    
        # Controlla se l'abilità è già stata usata in questo turno
        if getattr(game_state.active_pokemon, "teal_dance_used", False):
            #mprint("Teal Dance è già stato usato in questo turno.")
            return False
    
        # Controlla se c'è almeno una carta Energia Base Erba nella mano
        energy_card = next((card for card in game_state.hand if isinstance(card, EnergyCard) ), None)
    
        if not energy_card:
            #mprint("Non ci sono carte Energia Base Erba nella mano.")
            return False
    
        # Se tutte le condizioni sono soddisfatte
        return True
    
    def execute_ability(self,game_state):
        mprint("Eseguo Abilità Teal Dance")
        """
        Abilità: Teal Dance
        Una volta durante il turno, puoi assegnare una carta Energia Base Erba dalla tua mano
        a questo Pokémon. Se lo fai, pesca una carta.
    
        Args:
            game_state: L'oggetto che rappresenta lo stato attuale del gioco.
        """
        pokemon = game_state.active_pokemon
    
        # Verifica che il Pokémon attivo sia Teal Mask Ogerpon ex
        if not (pokemon and pokemon.code == "TWM25"):
            mprint("Teal Dance può essere usato solo da Teal Mask Ogerpon ex come Pokémon attivo.")
            return False
    
        # Controlla se l'abilità è già stata usata in questo turno
        if getattr(pokemon, "teal_dance_used", False):
            mprint("Teal Dance è già stato usato in questo turno.")
            return False
    
        # Trova una carta Energia Base Erba nella mano
        energy_card = next((card for card in game_state.hand if isinstance(card, EnergyCard) and card.energy_type == "Grass"), None)
    
        if not energy_card:
            mprint("Non ci sono carte Energia Base Erba nella tua mano.")
            return False
        
        
        # Assegna l'Energia al Pokémon
        pokemon.attach_energy(game_state.hand, energy_card)
        mprint(f"Energia {energy_card.code} assegnata a {pokemon.name} tramite Teal Dance.")
    
        # Segna l'abilità come utilizzata
        pokemon.teal_dance_used = True
    
        # Pesca una carta
        if game_state.deck:
            drawn_card = game_state.deck.pop(0)
            game_state.hand.append(drawn_card)
            mprint(f"Pesca una carta grazie a Teal Dance: {drawn_card.name}")
        else:
            mprint("Non ci sono carte nel mazzo da pescare.")
    
        return True

        
    def attack_instructions(self,attIndex,player,opponent_player):
        pokemon_to = opponent_player.active_pokemon
        if attIndex==0 or attIndex==1:
            if len(self.attached_energies)>=3: #per semplicità due energie qualsiasi
                total_damage = 30*(len(self.attached_energies)+len(pokemon_to.attached_energies))
                mprint(f"{self.name} esegue l'attacco  Myriad Leaf Shower 30+ {total_damage}")
                pokemon_to.receive_damage(total_damage, opponent_player)
                if pokemon_to.hp<=0:
                    player.hand.append(player.prizes[0])
                    player.prizes.pop(0)
                return 100
            else:
                mprint(f"{self.name} Attacco non valido. Mancano le energie.")
                return -100
        mprint(f"{self.name} Attacco non valido.")      
        return -100
    
        
class SlitherWing(PokemonBaseCard):
    def __init__(self,index):
        super().__init__(index,"PAR107","Slither Wing","Fighting ",140, 3, None, None,"ex","Ancient")
        
    def attack_count(self):
        return 2
        
    def attack_instructions(self,attIndex,game_state,opponent_player):
        pokemon_to = opponent_player.active_pokemon
        if attIndex==0:#Stomp Off
            if len(self.attached_energies)>=1:
                if opponent_player.deck:
                    card = opponent_player.deck.pop(0)
                    opponent_player.discard_pile.append(card)
                    mprint(f"{self.name} esegue l'attacco Stomp Off")
                    return 100
            else:
                mprint(f"{self.name} Attacco non valido. Mancano le energie.")
                return -100
        if attIndex==1:#Burning Turbulence 120
            if len(self.attached_energies)>=2: #per semplicità due energie qualsiasi
                energies = game_state.discard_energy_from_bench(2) # scarta solo 2 energie
                total_damage = 70 * len(energies)
                mprint(f"{self.name} esegue l'attacco Burning Turbulence 120{total_damage}")
                pokemon_to.receive_damage(120, opponent_player)
                final_rate=0
                if pokemon_to.hp<=0:
                    final_rate = 120
                final_rate = 240
                return final_rate
            else:
                mprint(f"{self.name} Attacco non valido. Mancano le energie.")
                return -100
        mprint(f"{self.name} Attacco non valido.")      
        return -100  
    
    
class DuraludonCard(PokemonBaseCard):
    """
    Duraludon Base Pokémon – 130 HP
    Attacchi:
      - Hammer In: Metal: infligge 30 danni.
      - Raging Hammer: Metal Metal Colorless: infligge 80 danni + 10 per ogni damage counter su questo Pokémon.
    """
    def __init__(self, index):
        # index: identificatore univoco nel mazzo
        super().__init__(
            index,
            "DUR001",           # codice carta (da aggiornare)
            "Duraludon",       # nome
            "Metal",           # tipo Pokémon
            130,                # punti salute
            2,                  # costo ritiro (2)
            weakness="Fire",  # debolezza
            resistance="Grass"# resistenza
        )
        # Conserva HP massimi per calcolare damage counters
        self.max_hp = 130

    def attack_count(self):
        """
        Restituisce il numero di attacchi disponibili.
        """
        return 2

    def attack_instructions(self, attIndex, player, opponent_player):
        """
        Esegue l'attacco specificato da attIndex:
          0 -> Hammer In
          1 -> Raging Hammer
        """
        pokemon_to = opponent_player.active_pokemon

        # Attacco 0: Hammer In
        if attIndex == 0:
            metal = sum(1 for e in self.attached_energies if getattr(e, 'energy_type', None) == "Metal")
            if metal >= 1:
                mprint(f"{self.name} usa Hammer In e infligge 30 danni.")
                pokemon_to.receive_damage(30, opponent_player)
                return True
            else:
                mprint(f"{self.name} non ha sufficiente Energia Metal per usare Hammer In.")
                return False

        # Attacco 1: Raging Hammer
        elif attIndex == 1:
            metal = sum(1 for e in self.attached_energies if getattr(e, 'energy_type', None) == "Metal")
            total = len(self.attached_energies)
            if metal >= 2 and total >= 3:
                # Calcola bonus danno per damage counters (ogni 10 HP mancanti = 1 counter)
                counters = (self.max_hp - self.hp) // 10
                damage = 80 + 10 * counters
                mprint(f"{self.name} usa Raging Hammer e infligge {damage} danni ({80} + 10×{counters}).")
                pokemon_to.receive_damage(damage, opponent_player)
                return True
            else:
                mprint(f"{self.name} non ha sufficiente energia per usare Raging Hammer.")
                return False

        # Attacco non valido
        mprint(f"{self.name} attacco non valido.")
        return False

class ArchaludonExCard(PokemonStage1Card):
    """
    Archaludon ex – Stage 1 ex Metal Pokémon, 300 HP
    Abilità:
      - Assemble Alloy: quando evolvi, puoi assegnare fino a 2 Basic Metal Energy dal tuo scarto ai tuoi Pokémon Metal.
    Attacco:
      - Metal Defender (Metal Metal Metal): infligge 220 danni e durante il prossimo turno questo Pokémon non ha debolezza.
    """
    def __init__(self, index):
        super().__init__(index, "DUR002", "Archaludon ex", "Metal", 300, retreat_cost=0)

    def can_use_ability(self, game_state):
        # Puoi usare l'abilità Assemble Alloy dopo aver evoluto
        return True

    def execute_ability(self, game_state):
        mprint(f"{self.name} attiva Assemble Alloy!")
        # TODO: implementare l'assegnazione di fino a 2 Basic Metal Energy dal discard a tuoi Pokémon Metal
        return True

    def attack_count(self):
        return 1

    def attack_instructions(self, attIndex, player, opponent_player):
        if attIndex != 0:
            mprint(f"{self.name} Attacco non valido.")
            return False
        # Verifica costi: 3 Energie Metal
        if len([e for e in self.attached_energies if e.energy_type == "Metal"]) >= 3:
            mprint(f"{self.name} usa Metal Defender e infligge 220 danni.")
            opp = opponent_player.active_pokemon
            opp.receive_damage(220, opponent_player)
            # TODO: gestire no debolezza per il prossimo turno
            return True
        mprint(f"{self.name} Attacco non valido. Mancano le energie.")
        return False


class BruteBonnetCard(PokemonBaseCard):
    """
    Brute Bonnet – Basic Ancient Darkness Pokémon, 120 HP
    Abilità:
      - Toxic Powder: se questo Pokémon ha un Ancient Booster Energy Capsule attaccato, puoi rendere entrambi i Pokémon attivi Tossici.
    Attacco:
      - Rampaging Hammer (Darkness Darkness Colorless): infligge 120 danni. Durante il prossimo turno, questo Pokémon non può attaccare.
    """
    def __init__(self, index):
        super().__init__(index, "BBN001", "Brute Bonnet", "Darkness", 120, retreat_cost=0)

    def can_use_ability(self, game_state):
        # Verifica se ha l'Ancient Booster Energy Capsule attaccata
        return any(e.name == "Ancient Booster Energy Capsule" for e in self.attached_energies)

    def execute_ability(self, game_state):
        mprint(f"{self.name} attiva Toxic Powder!")
        # TODO: impostare status_condition Poison per entrambi i Pokémon attivi
        return True

    def attack_count(self):
        return 1

    def attack_instructions(self, attIndex, player, opponent_player):
        if attIndex != 0:
            mprint(f"{self.name} Attacco non valido.")
            return False
        # Verifica costi: 2 Darkness + 1 qualsiasi
        darkness_count = len([e for e in self.attached_energies if e.energy_type == "Darkness"])
        if darkness_count >= 2 and len(self.attached_energies) >= 3:
            mprint(f"{self.name} usa Rampaging Hammer e infligge 120 danni.")
            opponent_player.active_pokemon.receive_damage(120, opponent_player)
            # TODO: bloccare attacchi durante il prossimo turno
            return True
        mprint(f"{self.name} Attacco non valido. Mancano le energie.")
        return False

class SquawkabillyExCard(PokemonBaseCard):
    """
    Squawkabilly ex – Basic ex Colorless Pokémon, 160 HP
    Abilità:
      - Squawk and Seize: una volta durante il primo turno, puoi scartare la tua mano e pescare 6 carte.
    Attacco:
      - Motivate (Colorless): infligge 20 danni e assegna fino a 2 Basic Energy dal tuo scarto a un Pokémon in panchina.
    """
    def __init__(self, index):
        super().__init__(index, "SQW001", "Squawkabilly ex", "Colorless", 160, retreat_cost=0)
        self.ability_used = False

    def can_use_ability(self, game_state):
        return (game_state.turn_count == 1 and not self.ability_used)

    def execute_ability(self, game_state):
        mprint(f"{self.name} attiva Squawk and Seize!")
        # Scarta la mano e pesca 6 carte
        discard = list(game_state.hand)
        for card in discard:
            game_state.discard_pile.append(card)
        game_state.hand.clear()
        for _ in range(6):
            game_state.draw_card()
        self.ability_used = True
        return True

    def attack_count(self):
        return 1

    def attack_instructions(self, attIndex, player, opponent_player):
        if attIndex != 0:
            mprint(f"{self.name} Attacco non valido.")
            return False
        if len(self.attached_energies) >= 1:
            mprint(f"{self.name} usa Motivate e infligge 20 danni.")
            opponent_player.active_pokemon.receive_damage(20, opponent_player)
            # Assegna fino a 2 Basic Energy dal discard a un Pokémon in panchina
            basic_energies = [c for c in player.discard_pile if isinstance(c, EnergyCard) and c.energy_type == "Basic"]
            attachments = basic_energies[:2]
            if attachments and player.bench:
                for energy in attachments:
                    player.discard_pile.remove(energy)
                    player.bench[0].attached_energies.append(energy)
                    mprint(f"{self.name} assegna {energy.name} a {player.bench[0].name}.")
            return True
        mprint(f"{self.name} Attacco non valido. Mancano le energie.")
        return False

class FezandipitiExCard(PokemonBaseCard):
    """
    Fezandipiti ex – Basic ex Colorless Pokémon, 210 HP
    Abilità:
      - Flip the Script: una volta durante il tuo turno, se uno dei tuoi Pokémon è stato messo KO
        nel turno precedente dell'avversario, puoi pescare 3 carte.
    Attacco:
      - Cruel Arrow (Colorless Colorless Colorless): infligge 100 danni a 1 dei Pokémon dell'avversario,
        ignorando debolezza e resistenza.
    """
    def __init__(self, index):
        super().__init__(index, "FEZ001", "Fezandipiti ex", "Colorless", 210, retreat_cost=0)
        self.ability_used = False

    def can_use_ability(self, game_state):
        # Condizione: un tuo Pokémon è stato KO nel turno precedente
        return (not self.ability_used and getattr(game_state, "last_turn_ko_count", 0) > 0)

    def execute_ability(self, game_state):
        mprint(f"{self.name} attiva Flip the Script!")
        for _ in range(3):
            game_state.draw_card()
        self.ability_used = True
        return True

    def attack_count(self):
        return 1

    def attack_instructions(self, attIndex, player, opponent_player):
        if attIndex != 0:
            mprint(f"{self.name} Attacco non valido.")
            return False

        # Seleziona un bersaglio: di default l'Active Pokémon
        target = opponent_player.active_pokemon
        mprint(f"{self.name} usa Cruel Arrow e infligge 100 danni a {target.name}, ignorando debolezza e resistenza.")
        
        # Temporaneamente bypassiamo debolezza/resistenza
        original_weakness = target.weakness
        original_resistance = target.resistance
        target.weakness = target.resistance = None
        
        target.receive_damage(100, opponent_player)
        
        # Ripristiniamo
        target.weakness = original_weakness
        target.resistance = original_resistance

        return True


class MewExCard(PokemonBaseCard):
    """
    Mew ex – Basic ex Colorless Pokémon, 180 HP
    Abilità:
      - Restart: una volta durante il tuo turno, puoi pescare carte finché non hai 3 carte in mano.
    Attacco:
      - Genome Hacking (Colorless Colorless Colorless): scegli 1 degli attacchi del Pokémon attivo dell'avversario e usalo come questo attacco.
    """
    def __init__(self, index):
        super().__init__(index, "MEW001", "Mew ex", "Colorless", 180, retreat_cost=0)
        self.ability_used = False

    def can_use_ability(self, game_state):
        # Puoi usare Restart una sola volta per turno
        return not self.ability_used

    def execute_ability(self, game_state):
        mprint(f"{self.name} attiva Restart!")
        # Pesca fino a 3 carte in mano
        needed = max(0, 3 - len(game_state.hand))
        if needed > 0:
            game_state.draw_cards(needed)
        self.ability_used = True
        return True

    def attack_count(self):
        return 1

    def attack_instructions(self, attIndex, player, opponent_player):
        if attIndex != 0:
            mprint(f"{self.name} Attacco non valido.")
            return False

        opp_pokemon = opponent_player.active_pokemon
        if not opp_pokemon:
            mprint(f"{self.name} non c'è un Pokémon attivo avversario.")
            return False

        import random
        choice = random.randint(0, opp_pokemon.attack_count() - 1)
        mprint(f"{self.name} usa Genome Hacking copiando l'attacco {choice} di {opp_pokemon.name}!")

        # Esegue l'attacco copiato
        # Nota: chiama direttamente il metodo di opp_pokemon, potrebbe richiedere energia su quel Pokémon
        return opp_pokemon.attack_instructions(choice, opponent_player, player)


class BloodmoonUrsalunaExCard(PokemonBaseCard):
    """
    Bloodmoon Ursaluna ex – Basic ex Colorless Pokémon, 260 HP
    Abilità:
      - Seasoned Skill: Blood Moon usato da questo Pokémon costa Colorless in meno
        per ogni carta premio che il tuo avversario ha già preso.
    Attacco:
      - Blood Moon (Colorless ×5): infligge 240 danni. Durante il tuo prossimo turno,
        questo Pokémon non può attaccare.
    """
    def __init__(self, index):
        super().__init__(index, "BUR001", "Bloodmoon Ursaluna ex", "Colorless", 260, retreat_cost=0)
        # Flag per impedire l’attacco nel turno successivo
        self.cannot_attack_next = False

    def attack_count(self):
        # Se è ancora sotto effetto Blood Moon, non può attaccare
        return 0 if self.cannot_attack_next else 1

    def _effective_cost(self, player):
        # Calcola quante carte premio l'avversario ha già preso
        # (partendo da 6 iniziali)
        taken = 6 - len(player.opponent_prizes)
        base = 5
        return max(0, base - taken)

    def attack_instructions(self, attIndex, player, opponent_player):
        if attIndex != 0:
            mprint(f"{self.name}: attacco non valido.")
            return False
        if self.cannot_attack_next:
            mprint(f"{self.name}: non può attaccare questo turno.")
            return False

        req = self._effective_cost(player)
        if len(self.attached_energies) < req:
            mprint(f"{self.name}: attacco non valido, servono {req} energie (attaccate: {len(self.attached_energies)}).")
            return False

        mprint(f"{self.name} usa Blood Moon e infligge 240 danni a {opponent_player.active_pokemon.name}!")
        opponent_player.active_pokemon.receive_damage(240, opponent_player)
        # Imposta il vincolo: non potrà attaccare nel prossimo turno
        self.cannot_attack_next = True
        return True


class LatiasExCard(PokemonBaseCard):
    """
    Latias ex – Basic ex Psychic Pokémon, 210 HP
    Abilità:
      - Skyliner: i tuoi Pokémon Base in gioco non hanno costo di ritirata.
    Attacco:
      - Eon Blade (Psychic, Psychic, Colorless): infligge 200 danni. Durante il tuo prossimo turno,
        questo Pokémon non può attaccare.
    """
    def __init__(self, index):
        super().__init__(index, "LAT001", "Latias ex", "Psychic", 210, retreat_cost=0)
        self.ability_active = False
        self.cannot_attack_next = False

    def can_use_ability(self, game_state):
        # Skyliner è un’abilità permanente, ma la applichiamo una sola volta
        return not self.ability_active

    def execute_ability(self, game_state):
        mprint(f"{self.name} attiva Skyliner!")
        # Imposta costo di ritirata a 0 per tutti i tuoi Pokémon Base
        if game_state.active_pokemon and game_state.active_pokemon.stage == "Basic":
            game_state.active_pokemon.retreat_cost = 0
        for pokemon in game_state.bench:
            if getattr(pokemon, "stage", None) == "Basic":
                pokemon.retreat_cost = 0
        self.ability_active = True
        return True

    def attack_count(self):
        # Se sotto l’effetto di Eon Blade, non può attaccare il turno successivo
        return 0 if self.cannot_attack_next else 1

    def attack_instructions(self, attIndex, player, opponent_player):
        if attIndex != 0:
            mprint(f"{self.name}: attacco non valido.")
            return False
        if self.cannot_attack_next:
            mprint(f"{self.name}: non può attaccare questo turno.")
            return False
        # Costo: 3 energie
        if len(self.attached_energies) < 3:
            mprint(f"{self.name}: attacco non valido, servono 3 energie (attaccate: {len(self.attached_energies)}).")
            return False

        mprint(f"{self.name} usa Eon Blade e infligge 200 danni a {opponent_player.active_pokemon.name}!")
        opponent_player.active_pokemon.receive_damage(200, opponent_player)
        # Blocca l’attacco nel prossimo turno
        self.cannot_attack_next = True
        return True







class HopsDubwoolCard(PokemonStage1Card):
    """
    Hop's Dubwool – Stage 1 Colorless Pokémon, 120 HP
    Abilità:
      - Defiant Horn: quando giochi questo Pokémon dall mano per evolvere un tuo Pokémon,
        puoi scegliere 1 dei Pokémon in panchina dell’avversario e metterlo attivo.
    Attacco:
      - Headbutt (Colorless ×3): infligge 80 danni.
    """
    def __init__(self, index):
        super().__init__(index, "HOP001", "Hop's Dubwool", "Colorless", 120, retreat_cost=0)
        self.ability_used = False

    def can_use_ability(self, game_state):
        # Puoi usare Defiant Horn solo una volta, appena evoluto
        return not self.ability_used

    def execute_ability(self, game_state):
        mprint(f"{self.name} attiva Defiant Horn!")
        # Controlla che l'avversario abbia Pokémon in panchina
        if not game_state.opponent.bench:
            mprint("Nessun Pokémon in panchina dell’avversario da scambiare.")
            return False
        # Scegli il primo Pokémon in panchina
        target = game_state.opponent.bench[0]
        # Rimetti l’attivo corrente in panchina (se esiste)
        if game_state.opponent.active_pokemon:
            game_state.opponent.bench.append(game_state.opponent.active_pokemon)
        # Metti il bersaglio in Active
        game_state.opponent.active_pokemon = target
        game_state.opponent.bench.remove(target)
        mprint(f"{target.name} diventa il Pokémon attivo dell’avversario.")
        self.ability_used = True
        return True

    def attack_count(self):
        return 1

    def attack_instructions(self, attIndex, player, opponent_player):
        if attIndex != 0:
            mprint(f"{self.name}: attacco non valido.")
            return False
        # Headbutt richiede 3 energie qualsiasi
        if len(self.attached_energies) < 3:
            mprint(f"{self.name}: attacco non valido, servono 3 energie (hai {len(self.attached_energies)}).")
            return False
        mprint(f"{self.name} usa Headbutt e infligge 80 danni a {opponent_player.active_pokemon.name}!")
        opponent_player.active_pokemon.receive_damage(80, opponent_player)
        return True







class HopsWoolooCard(PokemonBaseCard):
    """
    Hop's Wooloo – Basic Colorless Pokémon, 70 HP
    Attacco:
      - Smash Kick (Colorless ×3): infligge 50 danni.
    """
    def __init__(self, index):
        super().__init__(index, "HOP002", "Hop's Wooloo", "Colorless", 70, retreat_cost=0)

    def attack_count(self):
        return 1

    def attack_instructions(self, attIndex, player, opponent_player):
        if attIndex != 0:
            mprint(f"{self.name}: attacco non valido.")
            return False

        # Smash Kick richiede 3 energie qualsiasi
        if len(self.attached_energies) < 3:
            mprint(f"{self.name}: attacco non valido, servono 3 energie (hai {len(self.attached_energies)}).")
            return False

        target = opponent_player.active_pokemon
        if not target:
            mprint(f"{self.name}: nessun Pokémon attivo avversario.")
            return False

        mprint(f"{self.name} usa Smash Kick e infligge 50 danni a {target.name}!")
        target.receive_damage(50, opponent_player)
        return True




class RelicanthCard(PokemonBaseCard):
    """
    Relicanth – Basic Fighting Pokémon, 100 HP
    Abilità:
      - Memory Dive: i tuoi Pokémon evoluti possono usare qualsiasi attacco delle loro precedenti evoluzioni.
        (Serve comunque l’energia richiesta da quell’attacco.)
    Attacco:
      - Razor Fin (Fighting, Colorless): infligge 30 danni.
    """
    def __init__(self, index):
        super().__init__(index, "REL001", "Relicanth", "Fighting", 100, retreat_cost=0)
        self.ability_active = False

    def can_use_ability(self, game_state):
        # Memory Dive è un’abilità permanente che attivi una volta
        return not self.ability_active

    def execute_ability(self, game_state):
        mprint(f"{self.name} attiva Memory Dive!")
        # Imposta flag sul game_state; in seguito il motore potrà consentire
        # ai Pokémon evoluti di usare attacchi delle loro evoluzioni precedenti
        game_state.memory_dive = True
        self.ability_active = True
        return True

    def attack_count(self):
        return 1

    def attack_instructions(self, attIndex, player, opponent_player):
        if attIndex != 0:
            mprint(f"{self.name}: attacco non valido.")
            return False

        # Controllo dei costi: Fighting + Colorless
        needed = {"Fighting": 1, "Colorless": 1}
        counts = {}
        for e in self.attached_energies:
            counts[e.energy_type] = counts.get(e.energy_type, 0) + 1
        for typ, req in needed.items():
            if counts.get(typ, 0) < req:
                mprint(f"{self.name}: attacco non valido, servono {req} energie {typ}.")
                return False

        target = opponent_player.active_pokemon
        if not target:
            mprint(f"{self.name}: nessun Pokémon attivo avversario.")
            return False

        mprint(f"{self.name} usa Razor Fin e infligge 30 danni a {target.name}!")
        target.receive_damage(30, opponent_player)
        return True






class HopsZacianExCard(PokemonBaseCard):
    """
    Hop's Zacian ex – Basic ex Metal Pokémon, 230 HP

    Attacchi:
      - Insta‑Strike (Colorless): 30 danni all’Active Pokémon e 30 danni a un Pokémon in panchina
        dell’avversario, ignorando debolezza e resistenza per il bersaglio in panchina.
      - Brave Slash (Metal ×3, Colorless): 240 danni. Durante il tuo prossimo turno, questo
        Pokémon non può usare Brave Slash.
    """
    def __init__(self, index):
        super().__init__(index, "ZAC002", "Hop's Zacian ex", "Metal", 230, retreat_cost=0)
        # Flag per bloccare Brave Slash nel turno successivo
        self.brave_slash_disabled = False

    def attack_count(self):
        return 2

    def attack_instructions(self, attIndex, player, opponent_player):
        # Insta‑Strike
        if attIndex == 0:
            # Costo: 1 qualsiasi energia
            if len(self.attached_energies) < 1:
                mprint(f"{self.name}: servono 1 energia (hai {len(self.attached_energies)}).")
                return False
            mprint(f"{self.name} usa Insta‑Strike!")
            # 30 danni all'Active
            opponent_player.active_pokemon.receive_damage(30, opponent_player)
            # 30 danni a un Pokémon in panchina (primo), ignorando debolezza/resistenza
            if opponent_player.bench:
                target = opponent_player.bench[0]
                orig_w, orig_r = target.weakness, target.resistance
                target.weakness = target.resistance = None
                mprint(f"{self.name} infligge 30 danni anche a {target.name} in panchina (ignora debolezza/resistenza).")
                target.receive_damage(30, opponent_player)
                target.weakness, target.resistance = orig_w, orig_r
            return True

        # Brave Slash
        if attIndex == 1:
            if self.brave_slash_disabled:
                mprint(f"{self.name}: Brave Slash non può essere usato questo turno.")
                return False
            # Costo: 3 Metal + 1 qualunque
            counts = {}
            for e in self.attached_energies:
                counts[e.energy_type] = counts.get(e.energy_type, 0) + 1
            total = len(self.attached_energies)
            if counts.get("Metal", 0) < 3 or total < 4:
                mprint(f"{self.name}: servono 3 Metal e 1 altra energia (hai {counts.get('Metal',0)} Metal e {total} totali).")
                return False
            mprint(f"{self.name} usa Brave Slash e infligge 240 danni a {opponent_player.active_pokemon.name}!")
            opponent_player.active_pokemon.receive_damage(240, opponent_player)
            # Impedisce Brave Slash al prossimo turno
            self.brave_slash_disabled = True
            return True

        mprint(f"{self.name}: attacco non valido.")
        return False


class PidgeyCard(PokemonBaseCard):
    """
    Pidgey – Basic Colorless Pokémon, 60 HP
    Evoluzione: Pidgeotto
    Attacco:
      - Gust (Colorless): 20 danni.
    Debolezza: Lightning ×2
    Resistenza: Fighting -30
    Costo di ritirata: 1
    """
    def __init__(self, index):
        super().__init__(
            index,
            "SV3-162",
            "Pidgey",
            "Colorless",
            60,
            retreat_cost=1,
            weakness="Lightning",
            resistance="Fighting",
             stage1_code=["SV3PT5-17"],
              stage2_code=["SV3PT5-18"]
        )

    def attack_count(self):
        return 1

    def attack_instructions(self, attIndex, player, opponent_player):
        if attIndex != 0:
            mprint(f"{self.name}: attacco non valido.")
            return False

        # Gust richiede 1 energia Colorless
        if len(self.attached_energies) < 1:
            mprint(f"{self.name}: servono 1 energia (hai {len(self.attached_energies)}).")
            return False

        target = opponent_player.active_pokemon
        if not target:
            mprint(f"{self.name}: nessun Pokémon attivo avversario.")
            return False

        mprint(f"{self.name} usa Gust e infligge 20 danni a {target.name}!")
        target.receive_damage(20, opponent_player)
        return True



class PidgeottoCard(PokemonStage1Card):
    """
    Pidgeotto – Stage 1 Colorless Pokémon, 80 HP
    Evoluzione da: Pidgey
    Evoluzioni successive: Pidgeot
    Attacco:
      - Flap (Colorless): infligge 20 danni.
    Debolezza: Lightning ×2
    Resistenza: Fighting -30
    Costo di ritirata: 1
    """
    def __init__(self, index):
        super().__init__(
            index,
            "SV3PT5-17",
            "Pidgeotto",
            "Colorless",
            80,
            retreat_cost=1,
            weakness="Lightning",
            resistance="Fighting",
            stage2_code=["SV3PT5-18"]
        )

    def attack_count(self):
        return 1

    def attack_instructions(self, attIndex, player, opponent_player):
        if attIndex != 0:
            mprint(f"{self.name}: attacco non valido.")
            return False

        # Flap richiede 1 energia qualsiasi
        if len(self.attached_energies) < 1:
            mprint(f"{self.name}: servono 1 energia (hai {len(self.attached_energies)}).")
            return False

        target = opponent_player.active_pokemon
        if not target:
            mprint(f"{self.name}: nessun Pokémon attivo avversario.")
            return False

        mprint(f"{self.name} usa Flap e infligge 20 danni a {target.name}!")
        target.receive_damage(20, opponent_player)
        return True



import random
from core.card import PokemonStage2Card
from core.utils import mprint

class PidgeotCard(PokemonStage2Card):
    """
    Pidgeot – Stage 2 Colorless Pokémon, 130 HP
    Evoluzione da: Pidgeotto
    Attacchi:
      - Flap (Colorless): infligge 40 danni.
      - Fly (Colorless ×3): infligge 150 danni. Flip a coin: se esce testa, durante il prossimo turno
        dell’avversario previeni tutto il danno e gli effetti degli attacchi su questo Pokémon;
        se esce croce, l’attacco fallisce.
    Debolezza: Lightning ×2
    Resistenza: Fighting -30
    Costo di ritirata: 1
    """
    def __init__(self, index):
        super().__init__(
            index,
            "SV3PT5-18",
            "Pidgeot",
            "Colorless",
            130,
            retreat_cost=1,
            weakness="Lightning",
            resistance="Fighting"
        )
        # Flag per l’effetto di Fly
        self.fly_shield_active = False

    def attack_count(self):
        return 2

    def attack_instructions(self, attIndex, player, opponent_player):
        # Flap
        if attIndex == 0:
            # costo: 1 energia qualunque
            if len(self.attached_energies) < 1:
                mprint(f"{self.name}: servono 1 energia (hai {len(self.attached_energies)}).")
                return False
            mprint(f"{self.name} usa Flap e infligge 40 danni a {opponent_player.active_pokemon.name}!")
            opponent_player.active_pokemon.receive_damage(40, opponent_player)
            return True

        # Fly
        if attIndex == 1:
            # costo: 3 energie qualunque
            if len(self.attached_energies) < 3:
                mprint(f"{self.name}: servono 3 energie (hai {len(self.attached_energies)}).")
                return False
            mprint(f"{self.name} tenta Fly: lancio una moneta...")
            if not random.choice([True, False]):
                mprint(f"{self.name}: croce! Fly non ha effetto.")
                return False
            # testa: esegui danno e attiva scudo
            mprint(f"{self.name} esce testa! Fly infligge 150 danni e attiva uno scudo per il prossimo turno avversario.")
            opponent_player.active_pokemon.receive_damage(150, opponent_player)
            self.fly_shield_active = True
            return True

        mprint(f"{self.name}: attacco non valido ({attIndex}).")
        return False
