import pandas as pd,os,ctypes
from transitions import Machine
import nltk,pickle,websocket,time,thread,json,requests,logging
os.chdir(os.getcwd())
logging.basicConfig()
talkers={}
ls=[]
st=1
url="ws://54.245.5.208/"
botname="mad_bot"
key="OGU2M2NhODQtYTY2Zi00YWE1LWE5NjAtM2RjZjJlYjg4YWVjNTRkMGQwY2QtM2Fi"
def decodemsg(msgid,key):
    r = requests.session()
    r.headers["Content-Type"]="application/json; charset=utf-8"
    r.headers["Authorization"]="Bearer " + key
    response=r.get("https://api.ciscospark.com/v1/messages/"+msgid)
    response=json.loads(response.text)
    text=response["text"]
    sender=response["personId"]
    roomid=response["roomId"]
    return [text,sender,roomid,key]

def postmsg(room,text,key):  
    p = requests.session()
    p.headers["Content-Type"]="application/json; charset=utf-8"
    p.headers["Authorization"]="Bearer "+key
    payload={"text":str(text),"markdown":str(text),"roomId":str(room)}
    res=p.post("https://api.ciscospark.com/v1/messages/",json=payload)
    #print(res)
    #print(room,text,key)

def on_message(ws,message):
    try:
        data=json.loads(message)
        #print(data)
    except:
        data=""
        botname=""
        sender=""
    if data:
        flag=1
        botname=data["name"]
        sender=data["data"]["personEmail"]
        msgid=data["data"]["id"]
        decoded=decodemsg(msgid,key)
        message=str(decoded[0]).lower()
        sender=str(decoded[1])
        roomID=str(decoded[2])
        print("Message: "+message+ "\nSender:  " +sender+"\nRoom:   " +roomID+"\n key : " +decoded[3])	
        if sender not in talkers.keys():
            t1=fees_FSM(message,roomID)
            talkers[sender]=t1
        else:
            
            states=talkers[sender].possible_states[talkers[sender].state]
            for possible_answer in states:
                print(states)
                if possible_answer in message:
                    flag=0
                    print("matched",possible_answer)
                    print(talkers[sender].state)
                    talkers[sender].state=possible_answer
                    if(talkers[sender].state == 'final'):
                        postmsg(talkers[sender].room,talkers[sender].questions[talkers[sender].state],key)
                    else:                        
                        postmsg(talkers[sender].room,talkers[sender].questions[talkers[sender].state],key)
                        break
            if flag:
                talkers[sender].state="initial"
                print("state changed to fallback")
                print(talkers[sender])
                postmsg(talkers[sender].room,talkers[sender].questions[talkers[sender].state],key)

def on_error(ws, error):
    print error

def on_close(ws):
    print "### closed ###"

def on_open(ws):
    def run(*args):
        ws.send("subscribe:"+botname)
        while(1>0):
            time.sleep(30)
            ws.send("")
        ws.close()
        print("thread terminating...")
    thread.start_new_thread(run, ())

    def run(*args):
        ws.send("subscribe:"+botname)
        while(1>0):
            time.sleep(30)
            ws.send("")
        ws.close()
        print("thread terminating...")
    thread.start_new_thread(run, ())

class apiextraction():
	def __init__(self,filename="",load=""):
		if load!="":
			self.featuresets=self.load()
		else:
			self.filename=filename
			self.training_data=self.process_dataset()
			self.featuresets = [(self.process_sentence(n), intent) for (n, intent) in self.training_data]
			self.featuresets = [ (n, intent) for (n, intent) in self.featuresets if n]
		self.classifier= nltk.NaiveBayesClassifier.train(self.featuresets)
	def save(self):
		pickle.dump(self.featuresets, open( "featuresets", "wb" ) )
	def load(self):
		return pickle.load( open( "featuresets", "rb" ) )
	def process_dataset(self):
		df = pd.read_csv(self.filename)
		training_data = []
		for i in range(len(df)):
			training_data.append((df['Text'][i],df['Category'][i]))
		return training_data
	def bag_of_words(self,words):
		return dict([(word, True) for word in words])
	def process_sentence(self,x):
		words = nltk.tokenize.word_tokenize(x.lower()) 
		postag= nltk.pos_tag(words)
		stopwords = nltk.corpus.stopwords.words('english')
		lemmatizer = nltk.WordNetLemmatizer()
		processedwords=[]	
		for w in postag:
		    if "VB" in w[1]:
		        processedwords.append(lemmatizer.lemmatize(w[0].lower(),'v'))
		    else:
		        processedwords.append(lemmatizer.lemmatize(w[0],'n').lower())
		l=[]
		for w in processedwords:
		    if w.lower()=="not":
		        l.append(w)
		    elif w not in stopwords:
		        if (len(w)>2):
		            l.append(w)
		return self.bag_of_words(l)
	def score(self,input_sent):		
		input_sent = input_sent.lower()
		dist = self.classifier.prob_classify(self.process_sentence(input_sent))
		temp=[]
		for label in dist.samples():
		    temp.append((label, dist.prob(label)))
		return temp
	def intent(self,input_sent):
		print(input_sent)
		dist = self.classifier.classify(self.process_sentence(input_sent))
		prob = self.score(input_sent)
		prob = sorted(prob,key=lambda x:(-x[1],x[0]))
		if(prob[0][1]<0.5):
			return  "fallback"
		else:
			return dist
var1=apiextraction("dataset.csv")
#var1.save()

print("Algorithm Trained.") 
class fees_FSM(object):

    states=['initial','placement','fees','hostel','academics','mess','rooms','undergraduation','postgraduation','final','help']
    def __init__(self, message,room):
        self.message= message
        self.room=room
        self.st=1
        a="Here is a popular social media linke for your answer https://www.quora.com/What-is-the-total-4-year-fees-approx-of-VIT-for-a-student-of-rank-under-5k-10k-and-15k"
       # self.val=self.value
        self.machine = Machine(model=self, states=fees_FSM.states, initial='initial')
        self.questions={
            "initial1":"",
            "initial":"Hii, Let me get that for you. ",
            "fees":"Which fees would you like to know? Hostel(including the mess) or Academics ",
            "hostel":"Would You like to Know Mess Fees or Rooms?: ",
            "academics":"Which Degree would you like to purse? UnderGraduation or PostGraduation?: ",
            "mess": "Fees for mess in VIT is #to be filled, Here is the social link https://www.quora.com/What-is-the-hostel-fees-and-mess-charge-in-VIT-approximately",
            "rooms" : "Here is what I found. You can compare all the rooms in this link http://chennai.vit.ac.in/campus/hostelsfee",
            "undergraduation" : "Which one do you like to know? Btech,BSC,BCOM,BCA? "+str(a),
            "postgraduation" : "Which one do you like to know? Mtech,MSC,MCA,MBA? "+str(a),
            "btech" : "Fees for B.Tech "+str(a),
            "bcom" : "Fees for B.Com  "+str(a),
            "bca" : "Fees for BCAis "+str(a),
            "bsc" : "Fees for BSC  "+str(a),
            "mtech" : "Fees for M.Tech  "+str(a),
            "mcom" : "Fees for M.Com  "+str(a),
            "msc" : "Fees for MSC  "+str(a),
            "mba" : "Fees for MBA  "+str(a),
            "fallback":"Sorry, I didn't get you.",
            'placement':"Here is an excellent discussion on social media for that. https://www.quora.com/How-is-the-placement-in-VIT-Vellore-What-is-the-average-package", 
            "help" :"Welcome TO VIT bot. \n You can ask questions from following topics. \n Fees \n Placements \n Academics \n Exam \n Hostel \n "
        }
        self.possible_states={
            #"placement": ("initial","help","fees"),
            "initial":("hostel","academics","help","fees","undergraduation","postgraduation"),
            "fees":("hostel","academics","help"),
            "rooms":("help"),
            "hostel":("mess","rooms","help"),
            "academics":("undergraduation","postgraduation","help"),
            "undergraduation":("btech","bsc","bcom","bca","help"),
            "postgraduation" : ("mtech","mcom","mca","mba","help"),
            "help":("fees", "postgraduation","undergraduation","academics","hostel")                      
        }
        self.machine.add_transition(trigger='fallback', source='initial', dest='initial')
        self.machine.add_transition(trigger='fallback', source='fees', dest='fees')
        self.machine.add_transition(trigger='fallback', source='hostel', dest='hostel')
        self.machine.add_transition(trigger='fallback', source='academics', dest='academics')
        self.machine.add_transition(trigger='fallback', source='mess', dest='mess')
        self.machine.add_transition(trigger='fallback', source='rooms', dest='rooms')
        self.machine.add_transition(trigger='fallback', source='undergraduation', dest='undergraduation')
        self.machine.add_transition(trigger='fallback', source='postgraduation', dest='postgraduation')
        self.machine.add_transition(trigger='fallback', source='final', dest='final')

        self.machine.add_transition(trigger='hostel', source='fees', dest='hostel')
        self.machine.add_transition(trigger='academics', source='fees', dest='academics')
        self.machine.add_transition(trigger='mess', source='hostel', dest='final')
        self.machine.add_transition(trigger='rooms', source='hostel', dest='final')
        self.machine.add_transition(trigger='undergraduation', source='academics', dest='undergraduation')
        self.machine.add_transition(trigger='postgraduation', source='academics', dest='postgraduation')
        self.machine.add_transition(trigger='fees', source='initial', dest='fees')
        self.machine.add_transition(trigger='btech', source='undergraduation', dest='final')
        self.machine.add_transition(trigger='bsc', source='undergraduation', dest='final')
        self.machine.add_transition(trigger='bcom', source='undergraduation', dest='final')
        self.machine.add_transition(trigger='bca', source='undergraduation', dest='final')

        self.machine.add_transition(trigger='mtech', source='postgraduation', dest='final')
        self.machine.add_transition(trigger='mcom', source='postgraduation', dest='final')
        self.machine.add_transition(trigger='mca', source='postgraduation', dest='final')
        self.machine.add_transition(trigger='mba', source='postgraduation', dest='final')
        if 'help' in self.message.lower().split():
            print(self.state)
            postmsg(self.room,self.questions["help"],key)  

        if self.state=='initial':
            self.state=var1.intent(self.message.lower()).lower()
            if self.state=="fallback":
                self.state='initial'
            print(self.state)
            if self.state== "placement":
                self.state='initial'
                postmsg(self.room,self.questions["placement"],key)
                self.st+=1
            if self.state=="initial" and st!=1:
                postmsg(self.room,self.questions[self.state+"1"],key)
            else:
                postmsg(self.room,self.questions[self.state],key)
                self.st+=1


if __name__ == "__main__":
	ws = websocket.WebSocketApp("ws://54.245.5.208/",on_message = on_message,on_error = on_error,on_close = on_close)
	ws.on_open = on_open
	ws.run_forever()
