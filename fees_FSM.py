from transitions import Machine
class fees_FSM(object):

    states=['inital','hostel','academics','mess','rooms','undergraduation','postgraduation','final']
    def __init__(self, name):
        self.name = name
        self.machine = Machine(model=self, states=fees_FSM.states, initial='initial')
        self.questions={
            "initial":"Would You like to Know Academics Fees or Hostel?: ",
            "hostel":"Would You like to Know Mess Fees or Rooms?: ",
            "academics":"Which Degree would you like to purse? UnderGraduation or PostGraduation?: ",
            "mess": "Fees for mess in VIT is #to be filled",
            "rooms" : "Here is what I found. You can compare all the rooms in this link",
            "undergraduation" : "Which one do you like to know? Btech,BSC,BCOM,BCA?",
            "postgraduation" : "Which one do you like to know? Mtech,MSC,MCA,MBA?",
            "btech" : "Fees for B.Tech is #TBF",
            "bcom" : "Fees for B.Com is #TBF",
            "bca" : "Fees for BCAis #TBF",
            "bsc" : "Fees for BSC is #TBF",
            "mtech" : "Fees for M.Tech is #TBF",
            "mcom" : "Fees for M.Com is #TBF",
            "msc" : "Fees for MSC is #TBF",
            "mba" : "Fees for MBA is #TBF",

        }
        self.possible_states={
            "initial":("hostel","academics"),
            "hostel":("mess","rooms"),
            "academics":("undergraduation","postgraduation"),
            "undergraduation":("btech","bsc","bcom","bca"),
            "postgraduation" : ("mtech","mcom","mca","mba")                        
        }
        
        self.machine.add_transition(trigger='hostel', source='initial', dest='hostel')
        self.machine.add_transition(trigger='academics', source='initial', dest='academics')
        self.machine.add_transition(trigger='mess', source='hostel', dest='final')
        self.machine.add_transition(trigger='rooms', source='hostel', dest='final')
        self.machine.add_transition(trigger='undergraduation', source='academics', dest='undergraduation')
        self.machine.add_transition(trigger='postgraduation', source='academics', dest='postgraduation')

        self.machine.add_transition(trigger='btech', source='undergraduation', dest='final')
        self.machine.add_transition(trigger='bsc', source='undergraduation', dest='final')
        self.machine.add_transition(trigger='bcom', source='undergraduation', dest='final')
        self.machine.add_transition(trigger='bca', source='undergraduation', dest='final')

        self.machine.add_transition(trigger='mtech', source='postgraduation', dest='final')
        self.machine.add_transition(trigger='mcom', source='postgraduation', dest='final')
        self.machine.add_transition(trigger='mca', source='postgraduation', dest='final')
        self.machine.add_transition(trigger='mba', source='postgraduation', dest='final')

    def dialouge(self):
        while(self.state!='final'):
            answer=raw_input(self.questions[str(self.state)])
            states=self.possible_states[self.state]
            for possible_answer in states:
                if possible_answer in answer:
                    eval("self."+possible_answer+"()")
                    if(self.state == 'final'):
                        print self.questions[str(answer)]
                    break
                
        
f=fees_FSM("fees")
f.dialouge()    