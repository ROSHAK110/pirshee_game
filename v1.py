# ~/Documents/IDLE/pirshee_game
"""
Hra prší - v1.0
"""
#######################################################################
import random

#parameters
cards_marks= ["srdce", "žaludy", "kule", "zelený"]
card_nr= ["spodek", "filek", "král", "eso", "sedma", "osma", "devítka", "desítka"]

game_deck= []       #balíček karet
drawn_deck=[]       #karty, které už se hrály - není extra zahrnuto v herní logice
player_deck= []     #hráčovy karty
comp_deck= []       #karty počítače
played_card= ""     #karta na stole
#######################################################################
#functions

def create_deck(c_m: list, c_nr: list) -> None:
    """
    Zamíchání balíčku karet
    """
    for mark in c_m:
        for num in c_nr:
            game_deck.append(mark+"_"+num)

def first_lap(deck: list):
    """
    rozdělnení karet na začátku hry
    """
    global played_card
    for _ in range(4):
        #vybere kartu pro hráče + vymaže ji z balíčku
        p_choice= random.choice(deck)
        player_deck.append(p_choice)
        deck.remove(p_choice)

        # vybere kartu pro comp + vymaže ji z balíčku
        c_choice= random.choice(deck)
        comp_deck.append(c_choice)
        deck.remove(c_choice)

    played_card= random.choice(deck)
    drawn_deck.append(played_card)
    deck.remove(played_card)
    print(f"Začala hra")

def pirshee_logic(used_card:str) -> bool:
    """
    Vyhodnocení tahu karty
    """
    global played_card, comp_deck, game_deck
    #rozpad karet na znak + číslo
    moved_c = used_card.split("_")      #karta, kterou hrál hráč
    played_c= played_card.split("_")    #karta na stole

    #jde hrát tato karta?
    if moved_c[1] == "filek":
        #v plyed_card je pouze znak -> poz[0]
        played_card= input(f"Zadejte barvu {cards_marks}: ")
        return True
    elif (moved_c[0] == played_c[0]) or (moved_c[1] == played_c[1]):
        if moved_c[1] == "eso":
            played_card= used_card
            player_deck.remove(used_card)
            return False
        elif moved_c[1] == "sedma":
            print("Soupeř bere dvě")
            for _ in range(0,2):
                fine_card= random.choice(game_deck)
                comp_deck.append(fine_card)
                game_deck.remove(fine_card)
            played_card = used_card
            player_deck.remove(used_card)
            return False
        else:
            played_card = used_card
            return True
    else:
        print("Tuto kartu nemůžete hrát!")
        return False



def player_move():
    """
    herní tah
    """
    global played_card, player_deck, game_deck

    player_choice = input(f"Zadejte kartu, kterou chcete hrát\n{player_deck} / nebo 'líznout': ")
    if player_choice in player_deck:
        if pirshee_logic(player_choice):
            player_deck.remove(player_choice)
        else:
            if len(player_deck) > 0:
                player_move()
    elif player_choice == "líznout":
        load_card = random.choice(game_deck)
        player_deck.append(load_card)
        game_deck.remove(load_card)
    else:
        #pokud hráč hraje kartu, která není v jeho balíčku -> znovu player_move()
        print("Takto karta není ve Vašem balíčku!")
        player_move()

def comp_move():
    """
    tah počítače
    """
    global comp_deck, game_deck, played_card

    #rozložení balíčku karet počítače na znak + číslo + porovnání a hra
    played_m_plus_nr = played_card.split("_")
    comp_deck_m= []
    comp_deck_nr=[]
    card_index= 0
    for card in comp_deck:
        temp_card= card.split("_")
        comp_deck_m.append(temp_card[0])
        comp_deck_nr.append(temp_card[1])

    if (played_m_plus_nr[0] not in comp_deck_m) and (played_m_plus_nr[1] not in comp_deck_nr):
        if "filek" in comp_deck_nr:
            # počítač hraje filka
            # odebrání filka z balíčku soupeřových karet
            card_index= comp_deck_nr.index("filek")
            print(f"Počítač hrál {comp_deck[card_index]}")

            comp_deck_m.remove(comp_deck_m[card_index])
            comp_deck.remove(comp_deck[card_index])
            # vybrání barvy ze zbytku karet
            played_card= random.choice(comp_deck_m)
        else:
            #počítač líže kartu
            need_card= random.choice(game_deck)
            comp_deck.append(need_card)
            game_deck.remove(need_card)
            print("Soupeř lízal kartu")
    elif (played_m_plus_nr[0] in comp_deck_m) or (played_m_plus_nr[1] in comp_deck_nr):
        if played_m_plus_nr[0] in comp_deck_m:
            card_index= comp_deck_m.index(played_m_plus_nr[0])
        elif played_m_plus_nr[1] in comp_deck_nr:
            card_index= comp_deck_nr.index(played_m_plus_nr[1])
        print("============================")
        print(f"Počítač hrál: {comp_deck[card_index]}")
        played_card= comp_deck[card_index]
        comp_deck.remove(comp_deck[card_index])
        if comp_deck_nr[card_index] == "eso":
            if len(comp_deck) > 0:
                comp_move()
        elif comp_deck_nr[card_index] == "sedma":
            print("Berete dvě")
            for _ in range(0,2):
                fine_card= random.choice(game_deck)
                player_deck.append(fine_card)
                game_deck.remove(fine_card)
                if len(comp_deck) > 0:
                    comp_move()
        elif comp_deck_nr[card_index] == "filek":
            comp_deck_m.remove(comp_deck_m[card_index])
            comp_deck.remove(comp_deck[card_index])

            # vybrání barvy ze zbytku karet
            played_card= random.choice(comp_deck_m)

#######################################################################
#začátek hry
create_deck(c_m=cards_marks, c_nr=card_nr)
first_lap(game_deck)
#herní průběh
while True:
    #tah hráče
    print(f"Hrajte na: {played_card}")
    print("============================")
    player_move()
    if len(player_deck) == 0:
        break
    #Tah počítač
    comp_round= comp_move()
    print(f"Soupeři zbývá: {len(comp_deck)} karty")
    if len(comp_deck) == 0:
        break

#Vyhodnocení
print("============================")
if len(player_deck) == 0:
    print("Blahopřejeme k výhře")
else:
    print("Soupeř vyhrál")
print("Konec hry")
