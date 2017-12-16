from transitions import Machine
import re
class fees_FSM(object):

    states=['inital','hostel','academics','mess','rooms','undergraduation','postgraduation','final']
    def __init__(self, name):
        self.name = name
        self.questions={
            "initial":"Would You like to Know Academics Fees or Hostel?: ",
            "hostel":"Would You like to Know Mess Fees or Room?: ",
            "academics":"Which Degree would you like to purse? UnderGraduation or PostGraduation?: "
        }
        self.possible_states={
            "initial":(" hostel "," academics "),
            "hostel":(" mess "," rooms "),
            "academics":(" undergraduation "," postgraduation ")
        }
        self.machine = Machine(model=self, states=NarcolepticSuperhero.states, initial='initial')
        self.machine.add_transition(trigger='hostel', source='initial', dest='hostel')
        self.machine.add_transition(trigger='academics', source='initial', dest='academics')
        self.machine.add_transition(trigger='mess', source='hostel', dest='mess')
        self.machine.add_transition(trigger='rooms', source='hostel', dest='rooms')
        self.machine.add_transition(trigger='undergraduate', source='academics', dest='undergraduation')
        self.machine.add_transition(trigger='postgraduate', source='academics', dest='postgraduayion')
    def dialouge(self):
        while(self.state!='final'){
            answer=str(input(self.questions[self.state]))
            states=self.possible_states[self.state]
            for possible_state in states:
                if(re.match(i,ans)):
                    print(i)
        }
f=fees_FSM
f.dialouge()