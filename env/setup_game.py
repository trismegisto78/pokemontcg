# setup_game.py

from core.card import  EnergyCard
from core.pokemons import *
from core.trainers import *
from core.utils import mprint
from core.pokemons_charizard_ex import *


def create_deck_charizard(log=False):
    deck = []
    index = 2000
    
    for _ in range(4):
        deck.append( CharmanderPokemonCard(index) )
        index+=1
       
    for _ in range(4):
        deck.append(CharmeleonPokemonCard(index))
        index+=1
        
    for _ in range(4):
        deck.append(CharizardExPokemonCard(index))
        index+=1

    for _ in range(4):
        deck.append( PidgeottoCard(index) )
        index+=1

    for _ in range(4):
        deck.append( PidgeyCard(index) )
        index+=1

    for _ in range(12):
        deck.append(EnergyCard(index,"SVE10","Fire_Energy","Fire"))
        index+=1
        
    for _ in range(4):
        deck.append(UltraBallTrainerCard(index) )
        index+=1
        
    # Aggiungi Energie di base
   
    for _ in range(4):
        deck.append(EnergyRetrievalTrainerCard(index))
        index+=1
     
    for _ in range(4):
        deck.append(NestballTrainerCard(index) )
        index+=1
    
    for _ in range(4):
        deck.append( IonoTrainerCard(index) )
        index+=1
        
    for _ in range(4):
        deck.append( BossOrdersTrainerCard(index) )
        index+=1  
    
    for _ in range(4):
        deck.append( BuddyBuddyPoffinTrainerCard(index) )
        index+=1     
        
    for _ in range(4):
        deck.append( RareCandyTrainerCard(index) )
        index+=1     
            
    
    if log:
        print(f"Charizard Deck {len(deck)}")
    return deck






def create_deck_arch(log=False):
    deck = []
    index = 2000   

    for _ in range(4):
        deck.append( DuraludonCard(index) )
        index+=1

    for _ in range(4):
        deck.append( ArchaludonExCard(index) )
        index+=1

    for _ in range(2):
        deck.append( HopsDubwoolCard(index) )
        index+=1

    for _ in range(2):
        deck.append( HopsWoolooCard(index) )
        index+=1

    for _ in range(1):
        deck.append( RelicanthCard(index) )
        index+=1
    for _ in range(1):
        deck.append( HopsZacianExCard(index) )
        index+=1

    for _ in range(1):
        deck.append( FezandipitiExCard(index) )
        index+=1
    for _ in range(1):
        deck.append( SquawkabillyExCard(index) )
        index+=1

    for _ in range(4):
        deck.append( ProfessorsResearchCard(index) )
        index+=1
    for _ in range(4):
        deck.append( BossOrdersTrainerCard(index) )
        index+=1
    for _ in range(3):
        deck.append( BlackBeltsTrainingCard(index) )
        index+=1
    for _ in range(3):
        deck.append( IonoTrainerCard(index) )
        index+=1
    for _ in range(3):
        deck.append( ProfessorTuroSScenarioCard(index) )
        index+=1
    for _ in range(4):
        deck.append( NestballTrainerCard(index) )
        index+=1
    for _ in range(4):
        deck.append( UltraBallTrainerCard(index) )
        index+=1
    for _ in range(4):
        deck.append( NightStretcherCard(index) )
        index+=1
    for _ in range(3):
        deck.append( EarthenVesselTrainerCard(index) )
        index+=1
    for _ in range(3):
        deck.append( Pokegear30Card(index) )
        index+=1
    for _ in range(3):
        deck.append( PalPadCard (index) )
        index+=1
    for _ in range(3):
        deck.append( ScoopUpCycloneCard (index) )
        index+=1
    for _ in range(3):
        deck.append( JammingTowerCard(index) )
        index+=1
    if log:
        print(f"Archaludon Deck {len(deck)}")
    return deck




def create_deck_ragingbolt(log=False):
    deck = []
    index = 2000
    
    for _ in range(2):
        deck.append( IonoTrainerCard(index) )
        index+=1
    
    for _ in range(4):
        deck.append( RagingBoltPokemonCard(index) )
        index+=1
        
    for _ in range(2):
        deck.append( SlitherWing(index)  )
        index+=1
    
    for _ in range(4):
        deck.append( Teal_Mask_Ogerpon_ex(index)  )
        index+=1
        # Aggiungi Trainer Cards
    for _ in range(4):
        deck.append(ProfessorSadaVitalityTrainerCard(index) )
        index+=1
    
    for _ in range(4):
        deck.append(NestballTrainerCard(index) )
        index+=1
    
   
    for _ in range(4):
        deck.append(UltraBallTrainerCard(index) )
        index+=1



    #Aggiungi Energie di base
    for _ in range(4):
        deck.append(EarthenVesselTrainerCard(index))
        index+=1
        
    # Aggiungi Energie di base
    for _ in range(2):
        deck.append(EnergyRetrievalTrainerCard(index))
        index+=1
        
        

    # Aggiungi Energie di base
    for _ in range(5):
        deck.append(EnergyCard(index,"SVE9","Energia_Erba","Grass"))
        index+=1
    
    for _ in range(5):
        deck.append(EnergyCard(index,"SVE12","Lightning_Energy","Grass"))
        index+=1
        
    mprint(len(deck))
    if log:
        print(f"Opponent Deck {len(deck)}")
    return deck


def create_deck2():
    deck = []
    index = 2000
    
    for _ in range(3):
        deck.append( IonoTrainerCard(index) )
        index+=1
    
    for _ in range(4):
        deck.append( RagingBoltPokemonCard(index) )
        index+=1
        
    for _ in range(4):
        deck.append( SlitherWing(index)  )
        index+=1
    
    for _ in range(4):
        deck.append( Teal_Mask_Ogerpon_ex(index)  )
        index+=1
        # Aggiungi Trainer Cards
    for _ in range(4):
        deck.append(ProfessorSadaVitalityTrainerCard(index) )
        index+=1
    
    for _ in range(4):
        deck.append(NestballTrainerCard(index) )
        index+=1
    
   
    for _ in range(4):
        deck.append(UltraBallTrainerCard(index) )
        index+=1

    for _ in range(4):
        deck.append(EarthenVesselTrainerCard(index))
        index+=1

    # Aggiungi Energie di base
    for _ in range(13):
        deck.append(EnergyCard(index,"SVE9","Energia_Erba","Grass"))
        index+=1
    
    for _ in range(16):
        deck.append(EnergyCard(index,"SVE12","Lightning_Energy","Grass"))
        index+=1
        

    mprint(len(deck))
    return deck



