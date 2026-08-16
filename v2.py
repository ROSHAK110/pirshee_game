# ~/Documents/IDLE/pirshee_game
"""
Hra prší v2.0 - class
Opraveno (vs v1): Když dojdou karty v hracím balíču + možné hratelné karty
"""
#########################################################
import random
from collections import Counter

class Game:
    """
    Třída pro hru prší
    """
    def __init__(self):
        #init data
        self.color= ["SRDCE", "ZELENÝ", "KULE", "ŽALUDY"]
        self.symbol= ["spodek", "filek", "král", "eso", "sedma", "osma", "devítka", "desítka"]
        #game data
        self.game_deck= []
        self.player_deck= []
        self.computer_deck= []
        self.discard= []
        self.played_color= ""
        self.move= 0 #1 - player; 2 - comp
        self.first_card = False

    #STATIC METHOD
    @staticmethod
    def most_often_card(defined: bool, filek: bool, deck: list, options: list) -> list:
        """zjistí nejčastější barvu v zadaném seznamu"""
        if defined:
            can_play_cards= [deck[i] for i in options]
        else:
            can_play_cards= [card for card in deck]
        counter = Counter(t[0] for t in can_play_cards)
        if filek:
            color = counter.most_common(1)[0][0]
            return color
        else:
            most_often_card = []
            for card in can_play_cards:
                if card[0] == counter.most_common(1)[0][0]:
                    index = deck.index(card)
                    most_often_card.append(index)
            return most_often_card

    @staticmethod
    def card_str(card: tuple) -> str:
        return f"{card[0]}_{card[1]}"

    #Instance method
    def init(self) -> None:
        """Inicializace herních hodnot"""
        self.game_deck= []
        self.player_deck= []
        self.computer_deck= []
        self.discard= []
        self.played_color= ""
        self.move= 0 #1 - player; 2 - comp
        # self.first_card = False

    def setup(self):
        self.init()
        self.move = random.randint(1, 2)
        self.deck()
        self.first_lap()

    def can_play(self, hand: list) -> list:
        # hraje se už dalš kolo?
        if len(self.discard) > 1:
            self.first_card= False

        possible_cards= []
        for i in range(len(hand)):
            if (hand[i][1] == "filek"
                    or (not self.first_card and self.discard[-1][1] == "filek" and hand[i][0] == self.played_color)
                    or ((hand[i][0] == self.discard[-1][0] or hand[i][1] == self.discard[-1][1]) and (
                            not self.discard[-1][1] == "filek" or self.first_card))):
                possible_cards.append(i)
        return possible_cards

    def print_hand(self) -> None:
        """Vypíše karty hráče"""
        print("Vaše karty:")
        for i, card in enumerate(self.player_deck):
            print(f"{i}:{self.card_str(card)}", end=" ")
        print("\n_____________________")

    def deck(self) -> None:
        """Vytvoření balíčku karet + první karta na stole"""
        for c in self.color:
            for s in self.symbol:
                card= c, s
                self.game_deck.append(card)
        random.shuffle(self.game_deck)

    def is_card_in_deck(self) -> bool:
        """Jsou stále karty v hracím balíčku?"""
        if len(self.game_deck) > 0:
            return True
        else:
            return False

    def shuffle_deck(self) -> None:
        """Znovu zamíchání hracího balíčku"""
        top_card= self.discard.pop()
        self.game_deck= self.discard.copy()
        random.shuffle(self.game_deck)
        self.discard= [top_card]

    def first_lap(self) -> None:
        """Rozdělení karet na začátku hry"""
        for _ in range(4):
            self.player_deck.append(self.game_deck.pop())
            self.computer_deck.append(self.game_deck.pop())
        # zvolí první hranou kartu
        self.discard.append(self.game_deck.pop())
        self.first_card = True
        print("ZAČALA HRA\n"
              f"Na stole leží {self.card_str(self.discard[-1])}\n"
              "====================")

    def draw(self, deck: list) -> None:
        """líznout kartu"""
        # došly karty v balíčku?
        if not self.game_deck:
            self.shuffle_deck()
            print("Balíček byl zamíchán")
        deck.append(self.game_deck.pop())

    def fine(self, player_deck: list) -> None:
        """sedma - bere dvě"""
        for _ in range(2):
            self.draw(player_deck)


    def lap_continue(self) -> bool:
        """Určí, zda je tah u konce (eso/sedma)"""
        if self.discard[-1][1] in ("eso", "sedma"):
            return True
        else:
            return False

    def is_finish(self) -> bool:
        """Běží stále hra?"""
        if not self.player_deck:
            print("Blahopřeji, VYHRÁL JSTE! 🎉")
            return False
        elif not self.computer_deck:
            print("Soupeř VYHRÁL! 💀")
            return False
        else:
            return True

    # test text
    def computer_move(self) -> None:
        """tah počítače"""
        if self.move == 2:
            _can_play = self.can_play(self.computer_deck)
            if _can_play:
                # kolik stejných barev je nejvíce?
                card_indexes= Game.most_often_card(defined=True, filek=False, deck=self.computer_deck, options=_can_play)
                self.discard.append(self.computer_deck.pop(random.choice(card_indexes)))
                print(f"Počítač hrál: {self.card_str(self.discard[-1])}")
                # byla poslední karta filek/sedma?
                if self.discard[-1][1] == "filek":
                    most_color= Game.most_often_card(defined=False,filek=True, deck=self.computer_deck, options=_can_play)
                    self.played_color= most_color
                    print(f"Zvolená barva je {self.played_color}")
                elif self.discard[-1][1] == "sedma":
                    self.fine(self.player_deck)
                    print("Berete dvě!")
                # je kolo u konce?
                _lap_cont= self.lap_continue()
                if not _lap_cont:
                    self.move = 1
            else:
                self.draw(self.computer_deck)
                self.move = 1
                print("Počítač lízal kartu")

    def player_move(self) -> None:
        """tah hráče"""
        print(f"Hrajete na {self.card_str(self.discard[-1])}")
        if self.move == 1:
            self.print_hand()
            _can_play = self.can_play(self.player_deck)
            print("Možné hrát: ", *_can_play)
            try:
                user_choice = input("Zadejte index, nebo enter pro líznout: ")
                if user_choice == "":
                    self.draw(self.player_deck)
                    self.move = 2
                elif int(user_choice) not in _can_play:
                    print("Nelze hrát!")
                else:
                    if self.player_deck[int(user_choice)][1] == "filek":
                        self.played_color = input("Zadejte barvu: ")
                    elif self.player_deck[int(user_choice)][1] == "sedma":
                        self.fine(self.computer_deck)
                        print("Soupeř bere dvě!")
                    self.discard.append(self.player_deck.pop(int(user_choice)))
                    # je kolo u konce?
                    _lap_cont = self.lap_continue()
                    if not _lap_cont:
                        self.move = 2
            except ValueError:
                print("Zadali jste nepodporovanou hodnotu")

    def run(self):
        """Hlavní herní smyčka"""
        game_run= True
        while game_run:
            self.setup()

            let_continue = True
            while let_continue:
                if self.move == 1:
                    self.player_move()
                    print(f"Počet vašich karet {len(self.player_deck)}", "\n====================")
                elif self.move == 2:
                    self.computer_move()
                    print(f"počet soupeřových karet {len(self.computer_deck)}", "\n====================")
                let_continue= self.is_finish()
            # ukončit hru?
            again = input("Chcete začít novou hru? ano/ne: ")
            if again == "ano":
                game_run= True
            elif again == "ne":
                game_run= False



if __name__ == "__main__":
    game = Game()
    game.run()

