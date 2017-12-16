from transitions import Machine
import random

class FeesStates(object):

    states=['fees','hostel','academics','mess','rooms','undergraduation','postgraduation']
    def __init__(self, name):
        self.name = name
        questions={
            "fees":"Would You like to Know Academics Fees or Hostel?"
            "hostel_fees":"Would You like to Know Mess Fees or Room?"


        }
        self.machine = Machine(model=self, states=FeesStates.states, initial='fees')
        self.machine.add_transition(trigger='hostel', source='fees', dest='hostel',
            before='get_hostel_fees')
        self.machine.add_transition(trigger='mess', source='hostel', dest='mess',
            before="get_mess_fees")
        self.machine.add_transition(trigger='rooms', source='hostel', dest='rooms',before="get_rooms_fees")

        self.machine.add_transition(trigger='academics', source='fees', dest='academics', before="get_academics_fees")
        self.machine.add_transition(trigger='undergraduate', source='academics', dest='undergraduaion', before="get_undergraduate_fees")
        self.machine.add_transition(trigger='postgraduate', source='academics', dest='postgraduaion', before="get_postgraduate_fees")
        
        self.machine.add_transition(trigger='btech', source='undergraduaion', dest='btech', before="get_btech_fees")
        self.machine.add_transition(trigger='bsc', source='undergraduaion', dest='bsc')
        self.machine.add_transition(trigger='bcom', source='undergraduaion', dest='bcom')
        self.machine.add_transition(trigger='bca', source='undergraduaion', dest='bca')

        self.machine.add_transition(trigger='mtech', source='postgraduaion', dest='mtech',before="get_mtech_fees")
        self.machine.add_transition(trigger='mcom', source='postgraduaion', dest='mcom')
        self.machine.add_transition(trigger='mca', source='postgraduaion', dest='mca')
        self.machine.add_transition(trigger='mba', source='postgraduaion', dest='mba')

        def get_hostel_fees(self):
            print "Would You like to Know Mess Fees or Room?"

        def get_mess_fees(self):
            print "Here is what I found"

        def get_rooms_fees(self):
            print "Here is what I found"

        def get_academics_fees(self):
            print "Would you like to know undergraduation fees or postgraduation fees?"

        def get_undergraduate_fees(self):
            print "Which one you like to know? Btech,BSC,BCOM,BCA?"

        def get_btech_fees(self):
            print "Here is what I found"

        #Similarly for others

        def get_postgraduate_fees(self):
            print "Which one you like to know? Mtech,MSC,MCA,MBA?"

        def get_mtech_fees(self):
            print "Here is what I found"

        #Similarly for others.

    def dialouge(self):
