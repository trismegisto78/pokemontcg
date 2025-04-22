# main.py
from core.player import GameState
from core.play_turn_actions import esegui_turno
from env.setup_game import create_deck_charizard, create_deck_charizard_t,\
    create_deck_ragingbolt
from core.utils import mprint
import time
import threading



def check_vittory(played,opponent):
    if not opponent.deck:
        printEnhanced(f"{opponent.name} ha perso")
        played.vittorie+=1
        return True

    if not opponent.bench and not opponent.active_pokemon:
        printEnhanced(f"{opponent.name} ha perso")
        played.vittorie+=1
        return True

    if len(played.prizes)==0:
        printEnhanced(f"{played.name} ha vinto")
        played.vittorie+=1
        return True


    return False 


def printEnhanced(message):
    mprint("*****************************************************************")
    mprint("*****************************************************************")
    mprint("*****************************************************************")
    mprint(f"**************************{message}********************************")
    mprint("*****************************************************************")
    mprint("*****************************************************************")
    mprint("*****************************************************************")

def gioca(player1,player2,g):


    
    creadeck = create_deck_ragingbolt
    deckt = create_deck_charizard_t


    if g==0:#random.randint(0,1000)>=50:
        
        player1.reset(player2,deckt)
        player2.reset(player1,creadeck)
        
        player2.setup_active_and_bench(creadeck)
        player1.setup_active_and_bench(deckt)
        
    
    
        while True:
            esegui_turno(player1,player2)
            if check_vittory(player1,player2):
                return

            esegui_turno(player2,player1)
            if check_vittory(player2,player1):
                return
    else:
        player2.reset(player1,creadeck)
        player1.reset(player2,deckt)
        
        player1.setup_active_and_bench(deckt)
        player2.setup_active_and_bench(creadeck)
        
        
        while True:
            esegui_turno(player2,player1)
            if check_vittory(player2,player1):
                return  

            esegui_turno(player1,player2)
            if check_vittory(player1,player2):
                return            



# Funzione per giocare e calcolare il rate per una singola esecuzione
def esegui_gioco( player1,player2,risultati):

    for _ in  range(0,300):
        gioca(player1,player2,0)
        gioca(player1,player2,1)

    #print(f"vittorie1 {player1.vittorie}")
    #print(f"vittorie2 {player2.vittorie}")
    #rate = player1.vittorie/(player1.vittorie+player2.vittorie)*100
    #print(f"rate {rate:.2f}")
    # Calcolo del rate per questa esecuzione
    rate = player1.vittorie / (player1.vittorie + player2.vittorie) * 100
    risultati.append(rate)
    
    if risultati:
        media_rate = sum(risultati) / len(risultati)
        #print(f"Risultati individuali: {risultati}")
        print(f"********************************Media del rate: {media_rate:.2f} stages = {len(risultati)} tot={(player1.vittorie+player2.vittorie)*len(risultati) }")
    else:
        print("Nessun risultato disponibile")


if __name__ == "__main__":
    # Numero di iterazioni da eseguire
    n = 10  # Modifica il valore per aumentare le esecuzioni
    risultati = []
    
    
    # Creazione dei mazzi
    create_deck_ragingbolt(True)
    create_deck_charizard_t(True)
    
    
    nplayer = 1000
    array_di_player1 = [GameState() for _ in range(nplayer)]
    for i, player1 in enumerate(array_di_player1):
        player1.name = "Player 1"

        
    array_di_player2 = [GameState() for _ in range(nplayer)]
    for i, player2 in enumerate(array_di_player2):
        player2.name = "Player 2"

    
    print("array_di_player2")
    
    # Creazione del thread
    threads = [threading.Thread(target=esegui_gioco, args=(array_di_player1[i],array_di_player2[i],risultati,)) for i in range(0,nplayer)]
    
    for thread in threads:
        thread.start()
        
    for thread in threads:
        thread.join()
    
    # Calcolo della media dei risultati
    if risultati:
        media_rate = sum(risultati) / len(risultati)
        print(f"Risultati individuali: {risultati}")
        print(f"Media del rate: {media_rate:.2f}")
    else:
        print("Nessun risultato disponibile")
              
             
        
                  
