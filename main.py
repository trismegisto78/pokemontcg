# main.py
from core.player import GameState
from core.play_turn_actions import esegui_turno
from env.setup_game import *
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
    
    char_deck = create_deck_charizard
    arch = create_deck_arch


    if g==0:#random.randint(0,1000)>=50:
        
        player1.reset(player2,arch)
        player2.reset(player1,char_deck)
        
        player2.setup_active_and_bench(char_deck)
        player1.setup_active_and_bench(arch)
        
    
    
        while True:
            esegui_turno(player1,player2)
            if check_vittory(player1,player2):
                return

            esegui_turno(player2,player1)
            if check_vittory(player2,player1):
                return
    else:
        player2.reset(player1,char_deck)
        player1.reset(player2,arch)
        
        player1.setup_active_and_bench(arch)
        player2.setup_active_and_bench(char_deck)
        
        
        while True:
            esegui_turno(player2,player1)
            if check_vittory(player2,player1):
                return  

            esegui_turno(player1,player2)
            if check_vittory(player1,player2):
                return            


if __name__ == "__main__":
    #while True:
        # Creazione dei mazzi
        create_deck_charizard(True)
        create_deck_arch(True)
        
        
        player1 = GameState()
        player1.name = "Player 1"
        
        player2 = GameState()
        player2.name = "Player 2"
    
        
        gioca(player1,player2,0)
   
              
             
        
                  
