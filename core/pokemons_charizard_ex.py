from core.card import PokemonBaseCard, PokemonStage1Card, PokemonStage2Card,\
    PokemonCard, EnergyCard
from core.utils import mprint

        
            
    
class CharmanderPokemonCard(PokemonBaseCard):
    def __init__(self, index):
        """
        Inizializza il Pokémon Charmander.
        """
        super().__init__(index, "MEW004", "Charmander", "Fire", 70, 1, "Water", None, "Basic", None,["PAF008","MEW5"],["OBF125","PAF234","PAF054"])


    def attack_count(self):
        """
        Restituisce il numero di attacchi disponibili.
        """
        return 2

    def attack_instructions(self, attIndex, player, opponent_player):
        """
        Esegue uno degli attacchi di Charmander.

        Args:
            attIndex (int): L'indice dell'attacco da eseguire (0 o 1).
            player: Il giocatore che controlla Charmander.
            opponent_player: L'avversario.
        
        Returns:
            bool: True se l'attacco è stato eseguito con successo, False altrimenti.
        """
        pokemon_to = opponent_player.active_pokemon

        # Primo attacco: Blazing Destruction
        if attIndex == 0:
            if len(self.attached_energies) >= 1:  # Richiede almeno 1 Energia Fuoco
                if player.stadium_card:
                    mprint(f"{self.name} usa Blazing Destruction e scarta lo Stadio in gioco: {player.stadium_card.name}.")
                    player.discard_pile.append(player.stadium_card)
                    player.stadium_card = None
                    return True
                else:
                    mprint(f"{self.name} usa Blazing Destruction, ma non c'è nessuno Stadio in gioco.")
                    return False
            else:
                mprint(f"{self.name} Attacco non valido. Mancano le energie.")
                return False

        # Secondo attacco: Steady Firebreathing
        elif attIndex == 1:
            if len(self.attached_energies) > 1:  # Richiede almeno 2 Energia Fuoco
                mprint(f"{self.name} usa Steady Firebreathing e infligge 30 danni.")
                pokemon_to.receive_damage(30, opponent_player)
                return True
            else:
                mprint(f"{self.name} Attacco non valido. Mancano le energie.")
                return False

        # Attacco non valido
        mprint(f"{self.name} Attacco non valido.")
        return False
    
    
class CharmeleonPokemonCard(PokemonStage1Card):
    def __init__(self, index):
        """
        Inizializza il Pokémon Charmeleon.
        """
        super().__init__(index, "PAF008", "Charmeleon", "Fire", 90, 2, "Water", None, None, None,["PAF054"])

    def can_use_ability(self, player=None):
        """
        Verifica se l'abilità Flare Veil può essere attivata.
        In questo caso, è sempre attiva finché Charmeleon è il Pokémon attivo.
        """
        return True

    def execute_ability(self, game_state):
        """
        Esegue l'abilità Flare Veil: previene tutti gli effetti degli attacchi degli avversari su Charmeleon.
        """
        mprint(f"{self.name} attiva Flare Veil: Previene tutti gli effetti degli attacchi dell'avversario su questo Pokémon (eccetto il danno).")
        # Imposta una flag o un attributo per indicare che l'effetto è attivo
        self.flare_veil_active = True
        return True

    def attack_count(self):
        """
        Restituisce il numero di attacchi disponibili.
        """
        return 1

    def attack_instructions(self, attIndex, player, opponent_player):
        mprint(f"{self.name} usa Combustion e infligge 50 danni")
        """
        Esegue l'attacco Combustion.

        Args:
            attIndex (int): L'indice dell'attacco (in questo caso solo 0).
            player: Il giocatore che controlla Charmeleon.
            opponent_player: L'avversario.
        
        Returns:
            bool: True se l'attacco è stato eseguito con successo, False altrimenti.
        """
        if attIndex == 0:
            # Controlla che ci siano abbastanza energie assegnate
            if len(self.attached_energies) >= 2:
                # Infligge 50 danni al Pokémon attivo avversario
                opponent_pokemon = opponent_player.active_pokemon
                if opponent_pokemon:
                    mprint(f"{self.name} usa Combustion e infligge 50 danni a {opponent_pokemon.name}.")
                    opponent_pokemon.receive_damage(50, opponent_player)
                    return True
                else:
                    mprint("Non c'è un Pokémon attivo avversario.")
                    return False
            else:
                mprint(f"{self.name} non ha abbastanza Energie per usare Combustion.")
                return False

        # Attacco non valido
        mprint(f"{self.name} Attacco non valido.")
        return False



class CharizardExPokemonCard(PokemonStage2Card):
    def __init__(self, index):
        """
        Inizializza il Pokémon Charizard ex.
        """
        super().__init__(
            index, 
            "PAF054", 
            "Charizard ex", 
            "Fire", 
            330, 
            3, 
            "Grass", 
            None, 
            mechanic="EX", 
            label="Tera"
        )

    def can_use_ability(self, game_state):
        """
        Verifica se l'abilità Infernal Reign può essere utilizzata.
        """
        
        if self in game_state.abilities_done:
            mprint("Infernal Reignè gia stata usata")
            return False
        # Può essere usata solo quando Charizard viene giocato dalla mano per evolvere un Pokémon
        if game_state.active_pokemon == self:
            mprint("Infernal Reign può essere usata.")
            return True
        mprint("Infernal Reign non può essere usata in questo momento.")
        return False

    def execute_ability(self, game_state):
        """
        Esegue l'abilità Infernal Reign:
        Quando Charizard ex è giocato, cerca fino a 3 Energie Base nel mazzo e assegnale ai Pokémon come preferisci.
        """
        mprint(f"{self.name} attiva Infernal Reign!")
        if not self.can_use_ability(game_state):
            mprint("Non è possibile utilizzare Infernal Reign.")
            return False

        # Cerca fino a 3 Energie Base nel mazzo
        basic_energies = [card for card in game_state.deck if isinstance(card, EnergyCard)]
        selected_energies = basic_energies[:3]  # Prendi fino a 3 Energie Base disponibili

        if not selected_energies:
            mprint("Non ci sono Energie Base disponibili nel mazzo.")
            return False

        # Assegna le Energie Base trovate
        for energy_card in selected_energies:
            if game_state.active_pokemon and len(game_state.active_pokemon.attached_energies)<2:
                game_state.active_pokemon.attach_energy(game_state.deck, energy_card)
            else:
                # Puoi aggiungere una logica di selezione per i Pokémon (es. interfaccia o scelta automatica)
                pokemon = next((p for p in game_state.bench if isinstance(p, PokemonCard)), None)
                if pokemon:
                    pokemon.attach_energy(game_state.deck, energy_card)
                    mprint(f"{self.name} assegna {energy_card.name} a {pokemon.name}.")
                else:
                    mprint("Nessun Pokémon valido in panchina per assegnare l'Energia.")
                    break

        # Mescola il mazzo
        game_state.shuffle_the_deck()
        mprint("Il mazzo è stato mescolato.")

        return True

    def attack_count(self):
        """
        Restituisce il numero di attacchi disponibili.
        """
        return 1

    def attack_instructions(self, attIndex, player, opponent_player):
        """
        Esegue l'attacco Burning Darkness.

        Args:
            attIndex (int): L'indice dell'attacco (in questo caso solo 0).
            player: Il giocatore che controlla Charizard ex.
            opponent_player: L'avversario.
        
        Returns:
            bool: True se l'attacco è stato eseguito con successo, False altrimenti.
        """
        if attIndex == 0:
            # Controlla che ci siano abbastanza Energie assegnate
            if len(self.attached_energies) >= 2:
                opponent_pokemon = opponent_player.active_pokemon
                if opponent_pokemon:
                    # Calcola il danno base
                    base_damage = 180
                    # Aggiungi 30 danni per ogni carta premio presa dall'avversario
                    bonus_damage = 30 * (6 - len(opponent_player.prizes))
                    total_damage = base_damage + bonus_damage
                    mprint(f"{self.name} usa Burning Darkness infliggendo {total_damage} danni a {opponent_pokemon.name}.")
                    opponent_pokemon.receive_damage(total_damage, opponent_player)
                    return True
                else:
                    mprint("Non c'è un Pokémon attivo avversario.")
                    return False
            else:
                mprint(f"{self.name} non ha abbastanza Energie per usare Burning Darkness.")
                return False

        # Attacco non valido
        mprint(f"{self.name} Attacco non valido.")
        return False
    
    
    
    def rareCandy(self,game_state):
        rare_candies = next( (card for card in game_state.hand if card.code in ["SVI191"] ), None )
        if rare_candies:
            return True
        
    
    def can_evolve_pokemon(self, game_state):
        """
        Verifica se il Pokémon può evolvere un Pokémon Base o Stage1 in panchina o attivo.
    
        Args:
            game_state (GameState): Lo stato attuale del gioco.
    
        Returns:
            bool: True se esiste un Pokémon che può essere evoluto, False altrimenti.
        """
        
        # Controlla se Rare Candy è disponibile
        has_rare_candy = any(card.code == "SVI191" for card in game_state.hand)
    
        # Verifica il Pokémon attivo
        active_pok = game_state.active_pokemon
        if active_pok:
            mprint(f"can_evolve_pokemon >> {active_pok.name}")
            # Può evolvere con Rare Candy
            if has_rare_candy and isinstance(active_pok, CharmanderPokemonCard):
                mprint(f"can_evolve_pokemon >> A")
                return True
            # Può evolvere normalmente
            if isinstance(active_pok, CharmeleonPokemonCard):
                mprint(f"can_evolve_pokemon >> B")
                return True
    
        # Verifica i Pokémon in panchina
        for pokemon in game_state.bench:
            if isinstance(pokemon, CharmanderPokemonCard) and has_rare_candy:
                return True
            if isinstance(pokemon, CharmeleonPokemonCard):
                return True
    
        # Nessun Pokémon evolvibile trovato
        return False

