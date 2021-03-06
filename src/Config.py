import datetime
import os
import configparser
import logging
import random
import math


class Config:
    """
    The Config class imports a configuration from file and prepares python classes which will be used at various points.
    """

    # Constructor for new model
    def __init__(self, configFileName: str):
        self.configuration = configparser.ConfigParser()
        # Get absolute path to config file -> they need to be in /src/config_files/
        pathToConfigFile = os.path.join(os.path.dirname(__file__), 'config_files/', configFileName + '.ini')
        try:
            # Load configuration from file
            self.configuration.read(pathToConfigFile)
            # generate config objects from file
            self.__extractConfigFromDict()

        except FileNotFoundError:
            print("Error in RunConfig.init(): File with path ", pathToConfigFile, " not found.")

        # set default values or get values from config
        environment_section = self.configuration['environment']
        self.env_use_default = environment_section.getboolean('env_use_default')
        if self.env_use_default:
            self.__set_default_values()
        else:
            self.__extractConfigFromDict()

    def __set_default_values(self):
        # env
        self.env_nbr_merchants = 5
        self.env_size = 10
        self.env_nbr_enemies = 5
        self.env_epsilon_start = 1
        self.env_epsilon_end = 1
        self.env_epsilon_decay = 0.99
        self.env_move_enemies_merchants = False
        self.pirate_depth_of_view = 2
        self.env_frozen_lake_state = False

        # agent
        self.agent_discount_factor_gamma = 0.9
        self.agent_stepsize_alpha = 0.1

        # experiment
        self.exp_nbr_game_per_exp = 100
        self.exp_max_nbr_of_steps = 100

    def __extractConfigFromDict(self):
        """
        Store infos from config file to variables in Config object.
        :return: Nothing
        """
        # Environment section
        environment_section = self.configuration['environment']
        self.env_size = environment_section.getint('env_size')                                 # side length of square map
        self.env_nbr_enemies = environment_section.getint('env_nbr_enemies')
        self.env_nbr_merchants = environment_section.getint('env_nbr_merchants')
        self.env_epsilon_start = environment_section.getfloat('env_epsilon_start')    # probability that action will be random
        self.env_epsilon_end = environment_section.getfloat('env_epsilon_end')
        self.env_epsilon_decay = environment_section.getfloat('env_epsilon_decay')
        self.env_random_map = environment_section.getboolean('env_random_map')                     # size, nbr of enemies and merchants is random
        self.env_random_enemies = environment_section.getboolean('env_random_enemies')            # only nbr of enemies is random
        self.env_random_merchants = environment_section.getboolean('env_random_merchants')         # only nbr of merchants is random        ## environment
        self.env_move_enemies_merchants = environment_section.getboolean('env_move_enemies_merchants')  # indicatates if other ships shall move (or stay always at the same place)
        self.env_action_success_prob = environment_section.getfloat('env_action_success_prob')

        # compute state_size basing on visibility of agent
        self.pirate_depth_of_view = environment_section.getint('env_pirate_depth_of_view')      # how far the pirate is able to see (defines statesize)
        self.state_size = (self.pirate_depth_of_view*2+1)**2

        self.env_frozen_lake_state = environment_section.getboolean('env_frozen_lake_state')  # if this is true, env returns always the whole map as state (not only a square around the pirate)
        if self.env_frozen_lake_state:
            self.state_size = self.env_size**2  # in this case just return the side length of the map ** 2

        # set random values if specified in config
        if self.env_random_map:
            self.__set_random_map()
        if self.env_random_enemies:
            self.__set_random_enemies()
        if self.env_random_merchants:
            self.__set_random_merchants()

        # Agent section
        agent_section = self.configuration['agent']
        self.agent_discount_factor_gamma = agent_section.getfloat('agent_discount_factor_gamma')
        self.agent_stepsize_alpha = agent_section.getfloat('agent_stepsize_alpha')
        self.agent_buffer_size = agent_section.getint('agent_buffer_size')
        self.agent_batch_size = agent_section.getint('agent_batch_size')
        self.agent_gamma = agent_section.getfloat('agent_gamma')
        self.agent_tau = agent_section.getfloat('agent_tau')
        self.agent_learning_rate = agent_section.getfloat('agent_learning_rate')
        self.agent_update_nn_every = agent_section.getint('agent_update_nn_every')
        self.agent_update_mem_every = agent_section.getint('agent_update_mem_every')
        self.agent_update_mem_par_every = agent_section.getint('agent_update_mem_par_every')
        self.agent_experiences_per_sampling = math.ceil(self.agent_batch_size * self.agent_update_mem_every / self.agent_update_nn_every)
        self.agent_uniform_sampling = agent_section.getboolean('agent_uniform_sampling')

        # Experiment section
        experiment_section = self.configuration['experiment']
        self.exp_max_nbr_of_steps = experiment_section.getint('exp_max_nbr_of_steps')
        self.exp_nbr_episodes = experiment_section.getint('exp_nbr_episodes')

        # Replay buffer section
        buffer_section = self.configuration['buffer']
        self.buf_alpha = buffer_section.getfloat('buf_alpha')
        self.buf_alpha_decay = buffer_section.getfloat('buf_alpha_decay')
        self.buf_beta = buffer_section.getfloat('buf_beta')
        self.buf_beta_growth = buffer_section.getfloat('buf_beta_growth')

        # Persistence options
        # self.load_model_name = self.configuratio['load_model_name']   # enter name if you want to load an existing model


    def __set_random_merchants(self):
        """
        :return: random number between 1 and the side length of the map
        """
        self.env_nbr_merchants = random.randint(1,self.env_size)

    def __set_random_enemies(self):
        """
        :return: random number between 1 and the side length of the map
        """
        self.env_nbr_merchants = random.randint(1,self.env_size)

    def __set_random_map(self):
        self.env_size = random.randint(5, 100)
        self.__set_random_merchants()
        self.__set_random_enemies()


