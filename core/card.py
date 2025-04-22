# core/card.py
from core.utils import mprint



        
        
# card_type -> Pokemon, trainer, Energy, -->  Item,Supporter, Stadium, Tool, Basic Energy, Special Energy
class Card:
        
    def __init__(self,index,code, name, card_type, mechanic=None,label=None):
        self.name = name
        self.card_type = card_type  # "Pokemon", "Energy", "Trainer"
        self.code = code
        self.mechanic = mechanic # ex V GX Radiant Start Shining
        self.label = label # Ancient Future
        self.index = index

# pokemon_type = Grass, Fire, Dragon 
class PokemonCard(Card):
    def __init__(self,index,code, name,pokemon_type, stage="Basic", hp=0, retreat_cost=0, weakness=None, 
                resistance=None, mechanic=None,label=None,stage1_code=None,stage2_code=None):
        super().__init__(index,code,name, "Pokemon", mechanic, label)
        self.pokemon_type=pokemon_type
        self.hp = hp
        self.retreat_cost = retreat_cost  # Energy required for attacks
        self.attached_energies = []  # Liste delle energie assegnate
        self.attached_item = None  # Oggetto assegnato
        self.weakness = weakness  # Tipo al quale è debole (es. "Electric")
        self.resistance = resistance  # Tipo al quale è resistente (es. "Grass")
        self.stage=stage
        self.status_condition=1
        self.stage1_code=stage1_code
        self.stage2_code=stage2_code
    
    def attach_energy(self, fromPlace,energy_card):
        self.attached_energies.append(energy_card)
        fromPlace.remove(energy_card)
        
    
    def receive_damage(self, damage, player ):
        
        # Applica debolezze
        if self.weakness == self.pokemon_type:
            damage *= 2
            print(f"Danno raddoppiato per debolezza! Danno totale: {damage}")
        # Applica resistenze
        if self.resistance == self.pokemon_type:
            damage -= 30
            damage = max(0, damage)  # Il danno non può essere negativo
            mprint(f"Danno ridotto per resistenza. Danno totale: {damage}")

        # Riduci gli HP
        self.hp -= damage
        mprint(f"{self.name} ha ricevuto {damage} danni. HP rimanenti: {self.hp}")

        # Controlla se è KO
        if self.hp <= 0:
            while self.attached_energies:
                energy = self.attached_energies.pop(0)
                player.discard_pile.append(energy)
            if player.active_pokemon == self:
                player.discard_pile.append(player.active_pokemon)
                player.active_pokemon = None
            elif self in player.bench:
                player.bench.remove(self)
                player.discard_pile.append(self)
            mprint(f"{self.name} è stato messo KO!")
            
            return True
        return False
    
    def execute_ability(self, game_state):
        return False
    
    def attack_instructions(self,attIndex,player,opponent_player):
        return False
    
    def execute_attack(self,attIndex,player,opponent_player):
        self.attack_instructions(attIndex, player,opponent_player)

    
    def attack_count(self):
        return 1
    
    def can_use_ability(self,player=None):
        return False
        
class PokemonBaseCard(PokemonCard):
    def __init__(self,index,code, name,pokemon_type, hp, retreat_cost, weakness=None, resistance=None, mechanic=None,label=None,stage1_code=None,stage2_code=None ):
        super().__init__(index,code, name,pokemon_type,"Basic", hp, retreat_cost, weakness, resistance, mechanic,label,stage1_code,stage2_code)


class PokemonStage1Card(PokemonCard):
    def __init__(self,index,code, name,pokemon_type, hp, retreat_cost, weakness=None, resistance=None, mechanic=None,label=None,stage2_code=None ):
        super().__init__(index,code, name,pokemon_type,"Stage1", hp, retreat_cost, weakness, resistance, mechanic,label,None,stage2_code)
        
    def can_evolve_pokemon(self, game_state):
        """
        Verifica se il Pokémon Stage1 può evolvere un Pokémon Base in panchina o attivo.

        Args:
            game_state (GameState): Lo stato attuale del gioco.

        Returns:
            bool: True se esiste un Pokémon Base che può essere evoluto, False altrimenti.
        """
        
        if game_state.turn_count==1:
            mprint(f"{self.name} non può evolvere al primo turno")
        # Controlla il Pokémon attivo
        if game_state.active_pokemon and isinstance(game_state.active_pokemon, PokemonBaseCard):
            mprint(f"game_state.active_pokemon={game_state.active_pokemon.name}")
            if self.code in game_state.active_pokemon.stage1_code:
                return True

        # Controlla i Pokémon in panchina
        for pokemon in game_state.bench:
            if isinstance(pokemon, PokemonBaseCard):
                if self.code in pokemon.stage1_code:
                    return True

        # Nessun Pokémon evolvibile trovato
        return False
        
        
class PokemonStage2Card(PokemonCard):
    def __init__(self,index,code, name,pokemon_type, hp, retreat_cost, weakness=None, resistance=None, mechanic=None,label=None ):
        super().__init__(index,code, name,pokemon_type,"Stage2", hp, retreat_cost, weakness, resistance, mechanic,label,None,None)
    

    def can_evolve_pokemon(self, game_state):
        # Nessun Pokémon evolvibile trovato
        return False
        

class EnergyCard(Card):
    def __init__(self,index,code, name,energy_type="Energy"):
        super().__init__(index,code,name, "Energy")
        self.energy_type=energy_type

class TrainerCard(Card):
    def __init__(self,index,code, name, trainer_type):
        super().__init__(index,code,name, "Trainer")
        self.trainer_type = trainer_type  # "Item", "Supporter", "Stadium"

    def execute_effect(self, game_state,opponent=None):
        return True
    
    def can_use_it(self, game_state, opponent=None):
        return True