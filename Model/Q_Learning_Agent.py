# Purpose: Agent uses the Q-Learning Algorithm to Interact with the Environment
#
#   Info: Class that Implements the Q-Learning Algorithm
#
#   Developed as part of the Software Agents Course at City University
#
#   Dev: Dan Dixey and Enrico Lopedoto
#
#
import logging
import os
from random import choice, random

import numpy as np
from keras.layers.convolutional import Convolution1D, MaxPooling1D
from keras.layers.core import Dense, Dropout, Activation
from keras.layers.embeddings import Embedding
from keras.layers.recurrent import LSTM
from keras.models import Sequential
from keras.optimizers import RMSprop

# Logging Controls Level of Printing
logging.basicConfig(format='[%(asctime)s] : [%(levelname)s] : [%(message)s]',
                    level=logging.INFO)


class Q_Learning_Algorithm:
    """
    Basic Implementation of the Q-Learning Algorithm
    """

    def __init__(self, settings=None):
        """
        :param settings: dictionary of settings
        """
        self.q = {}
        assert settings is not None, 'Pass the Settings'
        self.actions = range(settings['nb_actions'])
        self.alpha = settings['alpha']
        self.epsilon = settings['epsilon']
        self.gamma = settings['gamma']

    def get_Qvalue(self, state, action):
        return self.q.get((state, action), 0.0)

    def learnQ(self, state, action, reward, value):
        old_value = self.q.get((state, action), None)
        if old_value is None:
            self.q[(state, action)] = reward
        else:
            self.q[(state, action)] = old_value + \
                self.alpha * (value - old_value)

    def choose_Action(self, state):
        if random() < self.epsilon:
            action = choice(self.actions)
        else:
            q = [self.get_Qvalue(state, a) for a in self.actions]
            maxQ = max(q)
            count = q.count(maxQ)
            if count > 1:
                best = [i for i in range(len(self.actions)) if q[i] == maxQ]
                i = choice(best)
            else:
                i = q.index(maxQ)
            action = self.actions[i]
        return action

    def learn(self, state1, action1, reward, state2):
        maxqnew = max([self.get_Qvalue(state2, a) for a in self.actions])
        self.learnQ(state1, action1, reward, reward + self.gamma * maxqnew)


class Q_Learning_Epsilon_Decay:
    """
    Epsilon Rate Decay - Over time Agent gets more responsibility for its own actions
    """

    def __init__(self, settings=None):
        """
        :param settings: dictionary of settings
        """
        self.q = {}
        assert settings is not None, 'Pass the Settings'
        self.actions = range(settings['nb_actions'])
        self.alpha = settings['alpha']
        self.epsilon = settings['epsilon']
        self.gamma = settings['gamma']
        self.decay = settings['epsilon_decay']
        self.rate = settings['epsilon_action']
        self.action_count = 0

    def get_Qvalue(self, state, action):
        return self.q.get((state, action), 0.0)

    def learnQ(self, state, action, reward, value):
        old_value = self.q.get((state, action), None)
        if old_value is None:
            self.q[(state, action)] = reward
        else:
            self.q[(state, action)] = old_value + \
                self.alpha * (value - old_value)

    def choose_Action(self, state):
        self.learn_decay()
        if random() < self.epsilon:
            action = choice(self.actions)
        else:
            q = [self.get_Qvalue(state, a) for a in self.actions]
            maxQ = max(q)
            count = q.count(maxQ)
            if count > 1:
                best = [i for i in range(len(self.actions)) if q[i] == maxQ]
                i = choice(best)
            else:
                i = q.index(maxQ)
            action = self.actions[i]
        self.action_count += 1
        return action

    def learn(self, state1, action1, reward, state2):
        maxqnew = max([self.get_Qvalue(state2, a) for a in self.actions])
        self.learnQ(state1, action1, reward, reward + self.gamma * maxqnew)

    def learn_decay(self):
        if self.action_count % self.rate == 0 and self.action_count > 0:
            self.epsilon = self.epsilon * self.decay


# class Q_Learning_Algorithm_Temporal_Difference:
#     """
#     Implements Temporal Difference weighting of the Q-Values
#
#     Remove old value from observations and replace with new
#
#     Would sit in the Helicopter Function
#     """
#
#     def __init__(self, actions, epsilon=0.1, alpha=0.1, gamma=0.1, lambda=0.5):
#         """
#         :param actions: Possible Number of Moves
#         :param epsilon: Randomness of Action Selection
#         :param alpha: Learning Rate
#         :param gamma: Discount factor
#         """
#         self.q = {}
#         self.epsilon = epsilon
#         self.alpha = alpha
#         self.gamma = gamma
#         self.lambda = lambda
#         self.actions = actions
#         logging.debug("Loaded TD({}) Backward view Q-Learning Algorithm".format(self.lambda))
#
#     def get_Qvalue(self, state, action):
#         return self.q.get((state, action), 0.0)
#
#     def learnQ(self, state, action, reward, value):
#         old_value = self.q.get((state, action), None)
#         if old_value is None:
#             self.q[(state, action)] = reward
#         else:
#             self.q[(state, action)] = old_value + \
#                 self.alpha * (value - old_value)
#
#     def choose_Action(self, state):
#         logging.debug("Deciding on an Action")
#         if random() < self.epsilon:
#             logging.debug("Random Action")
#             action = choice(self.actions)
#         else:
#             logging.debug("Agent Chosen Action")
#             q = [self.get_Qvalue(state, a) for a in self.actions]
#             maxQ = max(q)
#             count = q.count(maxQ)
#             if count > 1:
#                 best = [i for i in range(len(self.actions)) if q[i] == maxQ]
#                 i = choice(best)
#             else:
#                 i = q.index(maxQ)
#             action = self.actions[i]
#         return action
#
#     def learn(self, state1, action1, reward, state2):
#         maxqnew = max([self.get_Qvalue(state2, a) for a in self.actions])
#         self.learnQ(state1, action1, reward, reward + self.gamma * maxqnew)
#
#     def history_weighting(self, x):
#         """
#         Temporal Difference Weighting - Works for any given length list
#
#         (gamma*lambda)*(reward[t-1] + gamma*(q[t-1])-q[t])
#
#         tuple = (reward, q-value)
#
#         """
#         y = np.empty(len(x), float)
#         y[0] = x[0] * (1 - self.gamma)
#         for i in xrange(1, len(x)):
#             y[i] = x[i] * (1 - self.gamma) * (self.gamma)**i
#         return np.sum(y)


class Q_Neural_Network:

    def __init__(self, settings=None, track_height=None):
        """
        :param settings: dictionary of settings
        """
        self.q = {}
        assert settings is not None, 'Pass the Settings'
        assert track_height is not None, 'Pass the track height'
        self.actions = range(settings['nb_actions'])
        self.alpha = settings['alpha']
        self.epsilon = settings['epsilon']
        self.gamma = settings['gamma']
        self.max_track = track_height

        self.convert_rewards(settings)

        self.observations = []
        self.directory = os.path.join(os.getcwd(), 'NN_Model/')

        # Neural Network Parameters
        config = self.config()
        self.batch_size = config['batch_size']
        self.dropout = config['dropout']
        self.neurons = config['hidden_units']
        self.embedding_size = config['embedding_size']
        self.input_dim = config['input_dim']
        self.filter_length = config['filter_length']
        self.nb_filter = config['nb_filter']
        self.pool_length = config['pool_length']
        self.obs_size = config['obs_size']

        self.old_state_m1 = None
        self.action_m1 = None
        self.reward_m1 = None

        self.model = self.create_neural_network_rnn()

        self.updates = 0

    def config(self):
        """
            Neural Network (RNN) Configuration Settings
        """
        c = dict(batch_size=4,
                 dropout=0.3,
                 hidden_units=512,
                 obs_size=2400,
                 embedding_size=30,
                 input_dim=34,
                 filter_length=3,
                 nb_filter=32,
                 pool_length=2)
        return c

    def create_neural_network_rnn(self):

        model = Sequential()

        emb_n = self.max_track + 6

        model.add(Embedding(emb_n, self.embedding_size,
                            input_length=self.input_dim))
        model.add(Dropout(self.dropout))
        model.add(Convolution1D(nb_filter=self.nb_filter,
                                filter_length=self.filter_length,
                                border_mode='valid',
                                activation='relu',
                                subsample_length=1))
        model.add(MaxPooling1D(pool_length=self.pool_length))
        model.add(LSTM(self.neurons))
        model.add(Dropout(self.dropout))
        model.add(Dense(len(self.actions)))
        model.add(Activation('linear'))
        model.compile(loss='mse', optimizer=RMSprop())

        # Print Model Summary
        print(model.summary())

        return model

    def choose_Action(
            self,
            state=None,
            pstate=None,
            paction=None,
            preward=None):

        if random() < self.epsilon or len(
                self.observations) < self.obs_size or pstate is None:
            action = np.random.randint(0, len(self.actions))
        else:
            state = np.concatenate(
                (list(pstate), [paction], [
                    self.reward_change[preward]], list(state))) + 1
            state = np.asarray(state).reshape(1, self.input_dim)
            qval = self.model.predict(state, batch_size=1)
            action = (np.argmax(qval))

        return action

    def update_train(self, p_state, action, p_reward, new_state, terminal):

        self.observations.append((p_state, action, p_reward, new_state))

        self.updates += 1

        # Train Model once enough history and every seven actions...
        if len(self.observations) >= self.obs_size and self.updates % 20 == 0:

            if len(self.observations) > self.obs_size:
                self.observations.pop(0)

            X_train, y_train = self.process_minibatch(terminal)

            self.model.fit(X_train,
                           y_train,
                           batch_size=self.batch_size,
                           nb_epoch=1,
                           verbose=0)

            if self.updates % 1000 == 0 and self.updates > 0:
                self.epsilon = self.epsilon * (1 - 1e-2)

    def process_minibatch(self, terminal_rewards):
        X_train = []
        y_train = []
        val = 0
        for memory in self.observations:
            if val == 0:
                val += 1
                old_state_m1, action_m1, reward_m1, new_state_m1 = memory
            else:
                # Get stored values.
                old_state_m, action_m, reward_m, new_state_m = memory
                # Get prediction on old state.
                input = np.concatenate(
                    (list(old_state_m1), [action_m1], [
                        self.reward_change[reward_m1]], list(old_state_m))) + 1
                old_state_m = input.reshape(1, self.input_dim)
                old_qval = self.model.predict(old_state_m,
                                              batch_size=1,
                                              verbose=0)
                # Get prediction on new state.
                input2 = np.concatenate((old_state_m[
                                        0][-16:], [action_m], [self.reward_change[reward_m1]], list(new_state_m))) + 1
                new_state_m = input2.reshape(1, self.input_dim)
                newQ = self.model.predict(new_state_m,
                                          batch_size=1,
                                          verbose=0)
                maxQ = np.max(newQ)
                y = np.zeros((1, len(self.actions)))
                y[:] = old_qval[:]

                # Check for terminal state.
                if reward_m not in terminal_rewards:
                    update = (reward_m + (self.gamma * maxQ))
                else:
                    update = reward_m

                y[0][action_m] = update
                X_train.append(old_state_m.reshape(self.input_dim,))
                y_train.append(y.reshape(len(self.actions),))
                self.old_state_m1, self.action_m1, self.reward_m1, new_state_m1 = memory

        X_train = np.array(X_train[-self.obs_size:])
        y_train = np.array(y_train[-self.obs_size:])

        return X_train, y_train

    def save_model(self, name):
        json_string = self.model.to_json()
        open(
            self.directory +
            name +
            '_architecture.json',
            'w').write(json_string)
        self.model.save_weights(self.directory + name + '_weights.h5',
                                overwrite=True)

    def convert_rewards(self, settings):
        names = ['completed', 'crashed', 'open']
        self.reward_change = dict()
        for val, each_name in enumerate(names):
            self.reward_change[settings[each_name]] = self.max_track + val + 1