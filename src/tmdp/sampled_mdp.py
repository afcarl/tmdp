from memos import memoize_instance
from tmdp import SimpleMDP
from contracts import contract


__all__ = ['SampledMDP']


class SampledMDP(SimpleMDP):

    @contract(start_dist='ddist')
    def __init__(self, states, state2actions, state2action2transition, state2action2state2reward,
                 start_dist):
        self._states = states
        self.state2actions = state2actions
        self.state2action2transition = state2action2transition
        self.state2action2state2reward = state2action2state2reward
        
        self.start_dist = start_dist
        self.check_correct()
        
    def check_correct(self):
        # check everything is correctly defined
        # check all states
        states = set(self._states)
        assert states == set(self.state2actions)
        assert states == set(self.state2action2transition)
        assert states == set(self.state2action2state2reward)

        # check all states have all actions
        actions = set()
        for s in states:
            actions.update(self.state2actions[s])

        for s in states:
            assert actions == set(self.state2actions[s]), (actions, self.state2actions[s])
            # check transitions defined for all actions
            assert actions == set(self.state2action2transition[s])
            assert actions == set(self.state2action2state2reward[s])
            
            # check state dist
            for a in actions:
                self.is_state_dist(self.state2action2transition[s][a])
                s2s = set(self.state2action2transition[s][a])
                # reward for all
                for s2 in s2s:
                    assert s2 in self.state2action2state2reward[s][a]
                    reward = self.state2action2state2reward[s][a][s2]
                    # assert number

    def get_start_dist(self):
        return self.start_dist

    @memoize_instance
    def states(self):
        return list(self._states)

    @memoize_instance
    def actions(self, state):
        return list(self.state2actions[state])

    @memoize_instance
    def transition(self, state, action):
        return dict(**self.state2action2transition[state][action])

    @memoize_instance
    def reward(self, state, action, state2):
        return self.state2action2state2reward[state][action][state2]

    def display_state_dist(self, pylab, state_dist):
        """ 
            dist: hash states -> value >= 0 
        """
        pass

    def display_state_values(self, pylab, state_values):
        pass

    def display_policy(self, pylab, det_policy):
        pass
