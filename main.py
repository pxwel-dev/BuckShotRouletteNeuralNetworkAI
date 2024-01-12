import random
import neat
import pickle
from SimItems import HandSaw, HandCuffs, Cigarette, Soda, MagnifyingGlass, Shotgun
from SimPlayers import Player, HumanPlayer, NEATPlayer

MAX_ITEMS = 8
ITEMS_PER_ROUND = 4
ALL_ITEMS = [HandSaw('Saw'), HandCuffs('Cuffs'), Cigarette('Cigs'), Soda('Soda'), MagnifyingGlass('Glass')]


def play_game(players: list[Player]):
    player1 = players[0]
    player2 = players[1]
    player1.opponent = player2
    player2.opponent = player1
    gun = Shotgun()
    player1.reset_player()
    player2.reset_player()
    rnd = 0
    while not player1.has_lost() and not player2.has_lost():
        rnd += 1
        # print('===================================')
        # print('Round: ', rnd)
        while gun.live_shells == 0 or gun.blank_shells == 0:
            gun.reset_gun()
            gun.load_chamber()
        # print('Shotgun has been loaded.')
        # print('===================================')
        for player in players:
            # print('===================================')
            for i in range(0, 4):
                random.shuffle(ALL_ITEMS)
                if len(player.items) != MAX_ITEMS:
                    player.get_item(ALL_ITEMS)
                else:
                    break
            player.is_cuffed = False
            player.cuff_count = 0
            # print('===================================')

        while len(gun.chamber) != 0 and not player1.has_lost() and not player2.has_lost():
            for player in players:
                if player.has_lost():
                    # print('Player {0} has lost the game!'.format(player.name))
                    break
                if player.opponent.has_lost():
                    # print('Player {0} has lost the game!'.format(player.opponent.name))
                    break
                if player.is_cuffed and player.cuff_count == 1:
                    player.get_cuffed(False)
                elif player.is_cuffed and player.cuff_count != 1:
                    player.cuff_count += 1
                if not player.is_cuffed:
                    # print("Player {0}'s turn!".format(player.name))
                    gun.reset_damage()
                    player.nextShell = None
                    while True:
                        if len(gun.chamber) == 0:
                            break
                        if player.nextShell != gun.chamber[0]:
                            player.nextShell = None
                        # print('===================================')
                        # print('Live shells:', gun.live_shells)
                        # print('Blank shells:', gun.blank_shells)
                        # print('===================================')
                        # print('HP:', player.health)
                        # print('Items:', [item.name for item in player.items])
                        # print('===================================')
                        player.liveShells = gun.live_shells
                        player.blankShells = gun.blank_shells
                        player.shotgunDamage = gun.damage
                        move = player.make_move()
                        if move == 1:
                            # print("Player {0} decides to shoot Player {1}!".format(player.name, player.opponent.name))
                            gun.fire_gun(player.opponent)
                            break
                        elif move == 2:
                            # print("Player {0} decides shoot to themselves!".format(player.name))
                            if gun.fire_gun(player):
                                break
                            else:
                                pass
                                # print("Player {0} got lucky and gets another turn!".format(player.name))
                        else:
                            if isinstance(move, Soda):
                                move.use_item(gun)
                            elif isinstance(move, MagnifyingGlass):
                                move.use_item(player, gun)
                            elif isinstance(move, HandSaw):
                                move.use_item(gun)
                            elif isinstance(move, Cigarette):
                                move.use_item(player)
                            elif isinstance(move, HandCuffs):
                                move.use_item(player.opponent)
                            else:
                                print("ISSUE ", move)
    return [int(not player1.has_lost()), int(not player2.has_lost())]


# config_path = 'NEATconfig3.txt'
# config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
#                      neat.DefaultSpeciesSet, neat.DefaultStagnation,
#                      config_path)
#
# config_path = 'NEATconfig4.txt'
# config2 = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
#                      neat.DefaultSpeciesSet, neat.DefaultStagnation,
#                      config_path)

# f = open("NEATv3.0.1-100gen", "rb")
# best_player = pickle.load(f)
# f2 = open("NEATv3.1-100gen", "rb")
# best_player2 = pickle.load(f2)
#
# tally = [0, 0]
# for i in range(0, 10000):
#     score = play_game([NEATPlayer('1', neat.nn.FeedForwardNetwork.create(best_player2, config)), NEATPlayer('2', neat.nn.FeedForwardNetwork.create(best_player, config2))])
#     tally[0] += score[0]
#     tally[1] += score[1]
#     print(tally)
