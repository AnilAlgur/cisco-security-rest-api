import asa  # ASA REST API
import sys
import logging
import urllib3

logger = logging.getLogger(__name__)

def main():
    """
    Test ASA REST API.
    """
    logging.basicConfig(
        # filename='/path/to/fxos/output.txt',
        stream=sys.stdout,
        level=logging.DEBUG,  # DEBUG, INFO, WARNING, ERROR, CRITICAL
        # format="[%(levelname)8s]:  %(message)s",
        format='[%(asctime)s-%(levelname)s]: %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p')
    urllib3.disable_warnings()

    # Get server, username and password from CLI
    username = 'username'
    if len(sys.argv) > 1:
        username = sys.argv[1]
    password = 'password'
    if len(sys.argv) > 2:
        password = sys.argv[2]
    server_url = 'https://asa.example.com'
    if len(sys.argv) > 3:
        server_url = sys.argv[3]

    with asa.ASA(url=server_url, username=username, password=password) as lab_asa:
        lab_asa.get_version()
        cmds = ['show clock', 'show rest-api agent']
        lab_asa.get_cli(cmds)
    # End of with block

    print("Done running...")
    return


"""
CSCvh72007: Username and privilege display are incorrect when x-auth-token is used for REST API

Symptom:
syslog will show username as 15 instead of the actual username when using rest-api

JSON Response
{
    "response": [
        "Command authorization failed\n"
    ]
}

Conditions:
have ASA with rest-api installed
use tacacs authentication and authorization configurations on the ASA
use the X-AUTH_TOKEN header on your REST client 

Workaround:
use basic authentication header instead of X-AUTH-TOKEN
"""

"""
[04/11/2018 12:55:11 PM-DEBUG]: https://asa.example.com/api/tokenservices
[04/11/2018 12:55:11 PM-DEBUG]: Starting new HTTPS connection (1): asa.example.com
[04/11/2018 12:55:13 PM-DEBUG]: https://asa.example.com:443 "POST /api/tokenservices HTTP/1.1" 204 0
[04/11/2018 12:55:13 PM-INFO]: https://asa.example.com: Login Successful!
[04/11/2018 12:55:13 PM-DEBUG]: REST API Server Auth token: 23D70D@4096@E26E@7742A4E9C3F4D8CBDB457BCF5F16D708794F0C88
[04/11/2018 12:55:13 PM-DEBUG]: POST data: {"commands": ["show version | in Version"]}
[04/11/2018 12:55:13 PM-DEBUG]: Requesting POST for https://asa.example.com/api/cli
[04/11/2018 12:55:13 PM-DEBUG]: Resetting dropped connection: asa.example.com
[04/11/2018 12:55:13 PM-DEBUG]: https://asa.example.com:443 "POST /api/cli HTTP/1.1" 200 213
[04/11/2018 12:55:13 PM-DEBUG]: JSON Response
[04/11/2018 12:55:13 PM-DEBUG]: {
    "response": [
        "Cisco Adaptive Security Appliance Software Version 9.6(4)3 \nDevice Manager Version 7.9(1)\nREST API Agent Version 1.3.2.200\nBaseboard Management Controller (revision 0x1) Firmware Version: 2.4\n"
    ]
}
[04/11/2018 12:55:13 PM-INFO]: ASA Version is
Cisco Adaptive Security Appliance Software Version 9.6(4)3
Device Manager Version 7.9(1)
REST API Agent Version 1.3.2.200
Baseboard Management Controller (revision 0x1) Firmware Version: 2.4

[04/11/2018 12:55:13 PM-DEBUG]: POST data: {"commands": ["show clock", "show rest-api agent"]}
[04/11/2018 12:55:13 PM-DEBUG]: Requesting POST for https://asa.example.com/api/cli
[04/11/2018 12:55:13 PM-DEBUG]: Resetting dropped connection: asa.example.com
[04/11/2018 12:55:14 PM-DEBUG]: https://asa.example.com:443 "POST /api/cli HTTP/1.1" 200 92
[04/11/2018 12:55:14 PM-DEBUG]: JSON Response
[04/11/2018 12:55:14 PM-DEBUG]: {
    "response": [
        "16:53:28.095 UTC Wed Apr 11 2018\n",
        "REST API agent is currently enabled.\n"
    ]
}
[04/11/2018 12:55:14 PM-INFO]: Command: show clock
Output is
16:53:28.095 UTC Wed Apr 11 2018

[04/11/2018 12:55:14 PM-INFO]: Command: show rest-api agent
Output is
REST API agent is currently enabled.

[04/11/2018 12:55:14 PM-DEBUG]: DELETE data: None
[04/11/2018 12:55:14 PM-DEBUG]: Requesting DELETE for https://asa.example.com/api/tokenservices/23D70D@4096@E26E@7742A4E9C3F4D8CBDB457BCF5F16D708794F0C88
[04/11/2018 12:55:14 PM-DEBUG]: Resetting dropped connection: asa.example.com
[04/11/2018 12:55:15 PM-DEBUG]: https://asa.example.com:443 "DELETE /api/tokenservices/23D70D@4096@E26E@7742A4E9C3F4D8CBDB457BCF5F16D708794F0C88 HTTP/1.1" 204 0
[04/11/2018 12:55:15 PM-INFO]: https://asa.example.com: Logout Successful!
Done running...
"""

# Standard boilerplate to call main() function.
if __name__ == "__main__":
    main()
