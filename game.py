from .deck import Deck, Rank, Hand
from .players import Dealer, Player
    
class Game:
    round_in_progress: bool = False
    deck: Deck
    dealer: Dealer
    players: list[Player]
    # active_players: list[Player]
    

    def __init__(self, num_players: int):
        self.deck = Deck()
        self.dealer = Dealer(self.deck)
        self.players = [Player(i) for i in range(num_players)]

    def start_round(self):
        self.round_in_progress = True
        self.dealer.start_round()
        for player in self.players:
            hand = Hand()
            hand.draw(self.dealer.deal())
            hand.draw(self.dealer.deal())
            player.place_bet(hand, 10)

            if hand.total() == 21:
                print(f"Player {player} has blackjack!")
                player.balance += hand.bet * 2.5
                player.clear()

        self.show_table()

    def play_round(self):
        if not self.round_in_progress:
            raise Exception("Round not started")
        for player in self.players:
            player.play(self.dealer)
        self.dealer.play()
        self.show_table()

    def end_round(self):
        if not self.round_in_progress:
            raise Exception("Round not started")
        print(f"Dealer {self.dealer.reveal_hand()}")
        dealer_total = self.dealer.total_hand()
        for player in self.players:
            for hand in player.show_hands():
                hand_total = hand.total()
                if hand_total > 21:
                    print(f"Player {player} {hand} busts!")
                elif hand_total > 21 or hand_total > dealer_total:
                    print(f"Player {player} wins!")
                    player.balance += hand.bet * 2
                elif hand_total == dealer_total:
                    print(f"Player {player} pushes!")
                    player.balance += hand.bet
                else:
                    print(f"Player {player} loses!")
            player.clear()
        self.dealer.clear()
        self.round_in_progress = False

    def show_table(self):
        print(f"Dealer: {self.show_dealer_hand()}")

        for player in self.players:
            print(f"Player: {player} {player.show_hands()}")

    def show_dealer_hand(self):
        return self.dealer.show_hand()
