import neat
import os

class NNSystem:

    config : neat.Config = None
    genome_count = 0

    @staticmethod
    def init():
        
        file_path = os.path.dirname(__file__)
        config_path = os.path.join(file_path, '../neuralnet/config.txt')
        NNSystem.config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)
    
    @staticmethod
    def get_starting_genome():
        genome = neat.DefaultGenome(NNSystem.genome_count)
        NNSystem.genome_count += 1

        genome.configure_new(NNSystem.config.genome_config)

        return genome

    @staticmethod
    def get_net(genome: neat.DefaultGenome):
        return neat.nn.FeedForwardNetwork.create(genome, NNSystem.config)
    
    @staticmethod
    def get_actions(net: neat.nn.FeedForwardNetwork, energy: float, sight: list[tuple[int]]) -> list[float]:
        sight_inputs = []
        for input in sight:
            sight_inputs.append(input[0])
            sight_inputs.append(input[1])

        outputs = net.activate((energy, *sight_inputs))
        actions = [output > 0.5 for output in outputs]
        return actions

        