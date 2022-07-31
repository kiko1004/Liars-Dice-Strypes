from random import randint
from statistics import mode, mean

PLAYERS = 5
MANUAL_PLAYER = True


class Player:
    def __init__(self, player_number, manual=False):
        self.dices = 5
        self.bid = None
        self.player_number = player_number
        self.manual = manual

    def role_dice(self):
        self.hand = [randint(1, 6) for i in range(self.dices)]

    def make_bid(self, current_face, current_value, increase_by=0):
        self.challenge = False
        self.bid = {'face': current_face, "current_value": current_value + increase_by}

    def call_lie(self):
        self.challenge = True
        self.bid = None

    def lose(self):
        self.dices -= 1

    def make_move(self, last_bid=None):
        if not last_bid:
            self.make_bid(int(mean(self.hand)), 2)
        else:
            self.call_lie()

    @staticmethod
    def manual_input(initial=False):
        if initial:
            while True:
                try:
                    print("Your turn to make a bid!")
                    face_value = int(input("Choose face face_value: "))
                    numer_of_occurances = int(input("Number of occurances: "))
                    return face_value, numer_of_occurances
                except:
                    print('Please enter a valid number!')
                    continue
        else:
            while True:
                try:
                    numer_of_occurances_to_increase = int(input("Number of occurrences to increase by: "))
                    return numer_of_occurances_to_increase
                except:
                    print('Please enter a valid number!')
                    continue


_round = 1

print('Game starts!')
players = [Player(i + 1) for i in range(PLAYERS)]
if MANUAL_PLAYER:
    players[0].manual = True
print(f'You are player {players[0].player_number}!')

while True:
    print(f'Round {_round}')
    board = []
    for player in players:
        player.role_dice()
        board.extend(player.hand)
        if player.manual:
            print(f'Your hand is {player.hand}')
    challenge = False
    last_bid = None

    while not challenge:
        player_in_play = players.pop(0)
        print(f'Currently in play: Player {player_in_play.player_number}')
        if player_in_play.manual:
            if not last_bid:
                face_value, numer_of_occurances = player_in_play.manual_input(initial=True)
                player_in_play.make_bid(face_value, numer_of_occurances)
            else:
                while True:
                    print('Current bid is:')
                    print(last_bid)
                    print("Would you like to make a bid or call a lie?")
                    decision = input('Write "b" for bid and "l" for lie: ')
                    if decision == 'b':
                        number_to_increase_with = player_in_play.manual_input()
                        player_in_play.make_bid(
                            current_face=last_bid['face'], current_value=last_bid['current_value'],
                            increase_by=number_to_increase_with
                        )
                        break
                    elif decision == 'l':
                        player_in_play.call_lie()
                        break
                    else:
                        print('Please enter a valid number!')
                        continue

        else:
            player_in_play.make_move(last_bid=last_bid)
        challenge = player_in_play.challenge
        if player_in_play.bid:
            last_bid = player_in_play.bid
        players.append(player_in_play)
    print(f'Current Board: {board}')
    face_value = last_bid['face']
    suggested_count = last_bid['current_value']
    actual_count = board.count(face_value)
    print(f'Actual Count:{actual_count}, Bid:{suggested_count}')

    if actual_count >= suggested_count:
        print(f'Challenger loses. Player {players[-1].player_number}')
        player_lost = players.pop(-1)
        player_lost.lose()
    else:
        print(f'Bidder loses. Player {players[-2].player_number}')
        player_lost = players.pop(-2)
        player_lost.lose()

    print(f'Player {player_lost.player_number} left with {player_lost.dices} dices')
    if player_lost.dices > 0:
        players.insert(0, player_lost)
    else:
        print(f'Player {player_lost.player_number} eliminated')

    if len(players) > 1:
        _round += 1
        print('Current status:')
        for player in players:
            print(f"{player.player_number}: {player.dices} dices")
    else:
        break

print(f'We have a winner! Player: {players[0].player_number}')
