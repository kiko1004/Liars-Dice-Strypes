from random import randint
from statistics import mode, mean

PLAYERS = 2


class Player:
    def __init__(self, player_number):
        self.dices = 5
        self.bid = None
        self.player_number = player_number

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

    def make_move(self, last_bid = None):
        if not last_bid:
            self.make_bid(int(mean(self.hand)), 2)
        else:
            self.call_lie()


_round = 1

print('Game starts!')
players = [Player(i+1) for i in range(PLAYERS)]

while True:
    print(f'Round {_round}')
    board = []
    for player in players:
        player.role_dice()
        board.extend(player.hand)
    challenge = False
    last_bid = None

    while not challenge:
        player_in_play = players.pop(0)
        player_in_play.make_move(last_bid=last_bid)
        challenge = player_in_play.challenge
        if player_in_play.bid:
            last_bid = player_in_play.bid
        players.append(player_in_play)

    face_value = last_bid['face']
    suggested_count = last_bid['current_value']
    actual_count = board.count(face_value)
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
    else:
        break

print(f'We have a winner! Player: {players[0].player_number}')






