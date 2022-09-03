# Author: fe1w0
from utils import SSO, Clock
from config import user_id, password


if __name__ == "__main__":
    username = user_id
    password = password
    xdu_sso = SSO(username=username, password=password)
    session_client = xdu_sso.create_client()
    own_clock = Clock(session_client=session_client)
    if own_clock.xidiandailyup_clock():
        print("[+] Finish")        
