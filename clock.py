# Author: fe1w0
from utils import SSO, Clock

if __name__ == "__main__":
    username = ""
    password = ""
    xdu_sso = SSO(username=username, password=password)
    session_client = xdu_sso.create_client()
    own_clock = Clock(session_client=session_client)
    if own_clock.xidiandailyup_clock():
        print("[+] Finish")        
