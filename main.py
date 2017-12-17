import pandas as pd,os,ctypes
from transitions import Machine
import nltk,pickle,websocket,time,thread,json,requests,logging
os.chdir(os.getcwd())
logging.basicConfig()
talkers={}
ls=[]
d2={}  
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
        botname=data["name"]
        sender=data["data"]["personEmail"]
        msgid=data["data"]["id"]
        decoded=decodemsg(msgid,key)
        message=str(decoded[0])
        sender=str(decoded[1])
        roomID=str(decoded[2])
        print("Message: "+message+ "\nSender:  " +sender+"\nRoom:   " +roomID+"\n key : " +decoded[3])	
        if sender not in talkers.keys():
            t1=fees_FSM(message,roomID)
            talkers[sender]=t1
        else:
            states=talkers[sender].possible_states[talkers[sender].state]
            for possible_answer in states:
                if possible_answer in message:
                    talkers[sender].state=possible_answer
                    if(talkers[sender].state == 'final'):
                        print talkers[sender].questions['academics']
                        break
                    else:
                        
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
'''
class FSM(object):
    states=['fallback','final','hostel','academics','placements','fees','start','exam']
    def __init__(self,room,roomID):
         self.room=roomID
         self.machine = Machine(model=self, states=FSM.states, initial='start')
         self.ans=""
         self.questions={
             'start':'Let me get That for you',
             'help':"Sorry, I can't seem to understandyou. Would you like to know the categories I deal with?",
             'academics':"Here is what I found, academics fees is 1.5k",
             "placements" : "Here is what I found for VIT placements. Please refer to this link : https://www.quora.com/How-is-the-placement-in-VIT-Vellore-What-is-the-average-package",
             "exams":"VITEEE 2018 - Vellore Institute of Technology has released VITEEE 2018 application form in online and offlne mode. The last date to submit both online and offline application form of VITEEE is February 28, 2018. VIT will conduct VITEEE 2018 in online mode from April 4 to April 15, 2018. Please refer to this link for more details : https://engineering.careers360.com/articles/viteee"
         }
         self.possible_states={
             'start':('academics','placements','fees','exam','hostel','help'),
             'help':('academics','placements','fees','exam','hostel')
         }
         self.machine.add_transition(trigger='academics', source='start', dest='final')
         self.machine.add_transition(trigger='placements', source='start', dest='final')
         self.machine.add_transition(trigger='fees', source='start', dest='fees')
         self.machine.add_transition(trigger='exam', source='start', dest='final')
         self.machine.add_transition(trigger='hostel', source='start', dest='final')
         self.machine.add_transition(trigger='help', source='start', dest='academics')
         self.dialouge()
    def dialouge(self):
        if self.state=='start':
            postmsg(self.room,self.questions[self.state],key)
            postmsg(self.room,'fees?',key) 
''' 
class fees_FSM(object):

    states=['inital','fees','hostel','academics','mess','rooms','undergraduation','postgraduation','final']
    def __init__(self, message,room):
        self.message= message
        self.room=room
       # self.val=self.value
        self.machine = Machine(model=self, states=fees_FSM.states, initial='initial')
        self.questions={
            "initial":"Let me get that for you. ",
            "fees":"Which fees would you like to know? hostel,academics ",
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
            "fees":("hostel","academics"),
            "hostel":("mess","rooms"),
            "academics":("undergraduation","postgraduation"),
            "undergraduation":("btech","bsc","bcom","bca"),
            "postgraduation" : ("mtech","mcom","mca","mba")                        
        }
        
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
        if self.state=='initial':
            print("self."+var1.intent(self.message.lower()).lower()+"()")
            eval("self."+var1.intent(self.message.lower()).lower()+"()")
            print(self.state)
            postmsg(self.room,self.questions[self.state],key)  

        '''
        while(self.state!='final'):
            answer=raw_input(self.questions[str(self.state)])
            states=self.possible_states[self.state]
            for possible_answer in states:
                if possible_answer in answer:
                    eval("self."+possible_answer+"()")
                    if(self.state == 'final'):
                        print self.questions[str(answer)]
                    break
        '''
'''
        while(self.state!='final'):
            postmsg(self.room,self.questions[self.state],key)
            states=self.possible_states[self.state]
            for possible_answer in states:
                if possible_answer in answer:
                    eval("self."+possible_answer+"()")
                    if(self.state == 'final'):
                        print self.questions[str(answer)]
                        break

    class fees_FSM(object):

        states=['inital','hostel','academics','mess','rooms','undergraduation','postgraduation','final']
        def __init__(self, name):
            self.name = name
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
            self.machine = Machine(model=self, states=fees_FSM.states, initial='initial')
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
            self.dialouge()
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

'''

'''
class bot():
	def __init__(self,botname,key,url):
		self.botname=botname
		self.key=key
		self.url=url
		self.name={}
		self.var1=apiextraction("","yes")		
		print("Algorithm Trained.")
		#self.var1.save()
		self.ws = websocket.WebSocketApp(self.url,on_message = self.on_message,on_error = self.on_error,
		on_close = self.on_close,on_open=self.on_open)
		print("Bot Running")
		self.ws.run_forever()

	def decodemsg(self,msgid):
		r=requests.session()
		r.headers["Content-Type"]="application/json; charset=utf-8"
		r.headers["Authorization"]="Bearer " + self.key
		response=r.get("https://api.ciscospark.com/v1/messages/"+msgid)
		response=response.json()
		text=response["text"].encode('utf-8')		
		sender=response["personId"].encode('utf-8')
		roomid=response["roomId"].encode('utf-8')		
		return [text,sender,roomid]	
	def postmsg(self,room,text):
		p = requests.session()
		p.headers["Content-Type"]="application/json; charset=utf-8"
		p.headers["Authorization"]="Bearer "+self.key
		payload={"text":str(text),"markdown":str(text),"roomId":str(room)}
		res=p.post("https://api.ciscospark.com/v1/messages/",json=payload)	
	def on_error(self,ws,error):
		print(error)
	def on_close(self,ws):
		print("Bot Stopped")		
	def on_message(self,ws,message):
		try:
			data=json.loads(message)
		except:
			data=""
			botname=""
			sender=""
		finally:
			if data:
				botname=data["name"]
				sender=data["data"]["personEmail"]
				msgid=data["data"]["id"]
				decoded=self.decodemsg(msgid)

				message=str(decoded[0])
				sender=str(decoded[1])
				room=str(decoded[2])
				print("Message: "+message+ "\nSender:  " +sender+"\nRoom:   " +room)
				#self.postmsg(decoded[2],self.var1.intent(decoded[0]))
				if sender in self.name.keys:
					pass
				else:
					self.name[sender]='start'
					mach=FSM()
	def on_open(self,ws):
		def run(*args):
			ws.send("subscribe:"+self.botname)
			while(1):
				time.sleep(30)
				ws.send("")
			ws.close()
			print("thread terminating...")
		thread.start_new_thread(run, ())

'''


if __name__ == "__main__":
	ws = websocket.WebSocketApp("ws://54.245.5.208/",on_message = on_message,on_error = on_error,on_close = on_close)
	ws.on_open = on_open
	ws.run_forever()
