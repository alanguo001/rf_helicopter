# Purpose: Script Defines the Directions that the Agent can move
#
#   Info: Scalable for 3-5 possible actions
#
#   Developed as part of the Software Agents Course at City University
#
#   Dev: Dan Dixey and Enrico Lopedoto
#
#
import logging


class agent_controls:

    def __init__(self):
        logging.debug("Loaded Agent Movements Function")

    @staticmethod
    def action_move(action, location):
        """
        Given an Action value and Location (x,y) apply the action

        :param action: int
        :param location: tuple(int, int)
        :return: tuple(int, int)
        """
        if action == 1:
            logging.debug("Move Up and Right One")
            return location[0] + 1, location[1] + 1

        elif action == 0:
            logging.debug("Move Right One")
            return location[0] + 1, location[1]

        elif action == 2:
            logging.debug("Move Down and Right One")
            return location[0] + 1, location[1] - 1

        elif action == 4:
            logging.debug("Move Up Twice and Right One")
            return location[0] + 1, location[1] + 2

        elif action == 3:
            logging.debug("Move Down Twice and Right One")
            return location[0] + 1, location[1] - 2

        else:
            assert 1 == 2, "Something went wrong!"

    @staticmethod
    def action_wind(wind_value, location):
        """
        Given an Wind value and Location (x,y) apply the action

        Wind values are taken from the Grid World

        :param action: int
        :param location: tuple(int, int)
        :return: tuple(int, int)
        """
        if wind_value == 1:
            logging.debug("No Change due to Wind")
            return location

        elif wind_value == 2:
            logging.debug("Weak Wind - Move Right One")
            return location[0] + 1, location[1]

        elif wind_value == 3:
            logging.debug("Strong Tail Wind - Move Right Two")
            return location[0] + 2, location[1]

        elif wind_value == 4:
            logging.debug("Weak Upward Wind - Move Up One")
            return location[0], location[1] + 1

        elif wind_value == 5:
            logging.debug("Strong Upward Wind - Move Up Two")
            return location[0], location[1] + 2

        elif wind_value == 6:
            logging.debug("Weak Downward Wind - Move Down One")
            return location[0], location[1] - 1

        elif wind_value == 7:
            logging.debug("Strong Downward Wind - Move Down Two")
            return location[0], location[1] - 2

        else:
            # Areas where Wind is greater than 7
            return location
