from collections import defaultdict

from contracts import contract

from gridworld.generic_grid_world import GenericGridWorld
import numpy as np

from .constants import GridWorldsConstants
from .drawing import display_policy


__all__ = ['POGridWorld']



class POGridWorld(GenericGridWorld):
    """ 
        Partially observable problem. 
    
        The motion model fails with a certain probability, in which
        case you go in one of adjacent cells.
    
        The Observation model gives the current cell with probability p_loc,
        or one of the adjacent ones with probability (1-p_loc)/n.
     """

    @contract(map='array[HxW](int,(=0|=1))',
              p_fail='>=0,<=1',
              p_loc='>=0,<=1',
              bump_reward='<=0')
    def __init__(self, map, p_fail, p_loc, bump_reward, goal, start):  # @ReservedAssignment
        GenericGridWorld.__init__(self, goal=goal, start=start, grid=map)

        self._bump_reward = bump_reward
        self._goal = goal
        self._start = start

        self._p_loc = p_loc
        self._map = map

        self.motion_dist = get_motion_dist(p_fail)


    def actions(self, state):  # @UnusedVariable
        return list(GridWorldsConstants.action_to_displ.keys())

    def transition(self, state, action):
        # Goal is absorbing state
        if state in self._goal:
            return {state: 1.0}

        md = self.motion_dist[action]

        p = defaultdict(lambda:0.0)
        for motion, p_motion in md.items():
            s2 = self._grid.next_cell(state, motion)
            if self._grid.is_empty(s2):
                p[s2] += p_motion
            else:
                p[state] += p_motion
        p = dict(**p)
        return p

    def reward(self, state, action, state2):  # @UnusedVariable
        if state in self._goal:
            return 0.0
        else:
            if state == state2:  # bumped into wall
                return self._bump_reward

            (di, dj) = GridWorldsConstants.action_to_displ[action]
            length = np.hypot(di, dj)
            return -length


    def display_policy(self, pylab, det_policy):
        mm = main_motion()
        def a_to_motion(a):
            return mm[a]
            # must draw this action as an arrow
            
        display_policy(grid=self._grid, goal=self.get_goal(),
                       pylab=pylab, policy=det_policy, a_to_motion=a_to_motion)


def get_motion_dist(p_fail):
    p = 1.0 - p_fail
    q = p_fail / 2
    return {
       'r': {(-1, 0): p, (-1, +1): q, (-1, -1): q},
       'l': {(+1, 0): p, (+1, +1): q, (+1, -1): q},
       'd': {(0, -1): p, (-1, -1): q, (+1, -1): q},
       'u': {(0, +1): p, (-1, +1): q, (+1, +1): q},
       'rd': {(-1, -1): p, (-1, 0): q, (0, -1): q},
       'ld': {(+1, -1): p, (+1, 0): q, (0, -1): q},
       'ru': {(-1, +1): p, (-1, 0): q, (0, +1): q},
       'lu': {(+1, +1): p, (+1, 0): q, (0, +1): q},
    }

def main_motion():
    return {
       'r': (-1, 0),
       'l': (+1, 0),
       'd': (0, -1),
       'u': (0, +1),
       'rd': (-1, -1),
       'ld': (+1, -1),
       'ru': (-1, +1),
       'lu': (+1, +1),
    }
