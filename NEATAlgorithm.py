import copy
from main import play_game
from SimPlayers import NEATPlayer
from multiprocessing import Pool
import neat
import os
import pickle
import numpy as np
import random


class NEATAlgorithm:
    def __init__(self, config, games=10):
        self.config = config
        self.games = games

    def eval_genomes(self, genomes, conf):
        random.seed()
        random.shuffle(genomes)
        fitness = []
        while True:
            if len(genomes) % 6 == 0:
                genome_subtasks = [array for array in np.array_split(genomes, 6)]

                pool = Pool(processes=6)

                p1 = pool.apply_async(func=self.multiprocessing_eval, args=(genome_subtasks[0], conf))
                p2 = pool.apply_async(func=self.multiprocessing_eval, args=(genome_subtasks[1], conf))
                p3 = pool.apply_async(func=self.multiprocessing_eval, args=(genome_subtasks[2], conf))
                p4 = pool.apply_async(func=self.multiprocessing_eval, args=(genome_subtasks[3], conf))
                p5 = pool.apply_async(func=self.multiprocessing_eval, args=(genome_subtasks[4], conf))
                p6 = pool.apply_async(func=self.multiprocessing_eval, args=(genome_subtasks[5], conf))

                pool.close()
                pool.join()

                temp = []

                for i in [p1.get(), p2.get(), p3.get(), p4.get(), p5.get(), p6.get()]:
                    for j in i:
                        temp.append(j)

                for (genome_id, genome), (temp_genome_id, temp_genome) in zip(genomes, temp):
                    genome.fitness = temp_genome.fitness
                    fitness.append(genome.fitness)

                file = open("fitnessDataTest", 'a')
                file.write(str(max(fitness)) + "\n")
                file.close()
                break
            else:
                if len(genomes) != 0:
                    temp_fitness = []
                    for i, (genome_id, genome) in enumerate(genomes):
                        genome.fitness = 0 if genome.fitness is None else genome.fitness
                        temp_fitness.append(genome.fitness)
                    while len(genomes) % 6 != 0:
                        index = temp_fitness.index(min(temp_fitness))
                        temp_fitness.pop(index)
                        genomes.pop(index)

    def multiprocessing_eval(self, genomes, conf):
        count = 0
        playerGenomes = []
        for i, (genome_id, genome) in enumerate(genomes):
            genome.fitness = 0  # if genome.fitness is None else genome.fitness
            for j, (genome_id2, genome2) in enumerate(genomes[min(i + 1, len(genomes) - 1):]):
                playerGenomes.append(genome)
                genome2.fitness = 0
                playerGenomes.append(genome2)
                if len(playerGenomes) == 2:
                    count += 1
                    tally = [0, 0]
                    players = [
                        NEATPlayer("1", neat.nn.FeedForwardNetwork.create(playerGenomes[0], conf)),
                        NEATPlayer("2", neat.nn.FeedForwardNetwork.create(playerGenomes[1], conf)),
                    ]
                    for _ in range(0, int(self.games)):
                        game = play_game(players)

                        tally[0] += game[0]
                        tally[1] += game[1]

                        # print("=================================\n"
                        #       "Game {0}/{1} Summary\n"
                        #       "=================================\n"
                        #       "Total wins over {4} games:\n"
                        #       "=================================\n"
                        #       "Player 1: {2}\n"
                        #       "Player 2: {3}\n"
                        #       "=================================".format(count,
                        #                                                  int((len(genomes) * (len(genomes)) - 1) / 2),
                        #                                                  tally[0],
                        #                                                  tally[1],
                        #                                                  self.games))
                    playerGenomes[0].fitness += (((tally[0] - 5) / 5) / ((len(genomes) - 1) * self.games))
                    playerGenomes[1].fitness += (((tally[1] - 5) / 5) / ((len(genomes) - 1) * self.games))
                    playerGenomes.clear()
        return genomes

    def run_neat(self, name, generations):
        pop = neat.Population(self.config)
        pop.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        pop.add_reporter(stats)
        pop.add_reporter(neat.Checkpointer(1))

        best_genome = pop.run(self.eval_genomes, generations)
        with open(name, "wb") as file:
            pickle.dump(best_genome, file)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "NEATconfig4.txt")

    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)

    neatAlgo = NEATAlgorithm(config)
    neatAlgo.run_neat("NEATv3.0.1-100gen", 100)
