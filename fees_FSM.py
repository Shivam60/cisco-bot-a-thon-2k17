from transitions import Machine
import random

class NarcolepticSuperhero(object):

    states=['inital','hostel','academics','mess','rooms','undergraduation','postgraduation']
    def __init__(self, name):
        self.name = name
        self.machine = Machine(model=self, states=NarcolepticSuperhero.states, initial='initial')
        self.machine.add_transition(trigger='hostel', source='initial', dest='hostel')
        self.machine.add_transition(trigger='academics', source='initial', dest='academics')
        self.machine.add_transition(trigger='mess', source='hostel', dest='mess')
        self.machine.add_transition(trigger='rooms', source='hostel', dest='rooms')
        self.machine.add_transition(trigger='undergraduate', source='academics', dest='undergraduaion')
        self.machine.add_transition(trigger='postgraduate', source='academics', dest='postgraduaion')
        