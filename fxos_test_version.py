import fxos  # FXOS Management
import sys
import logging
import urllib3

logger = logging.getLogger(__name__)

def main():
    """
    Test FXOS REST API.
    """
    logging.basicConfig(
        # filename='/path/to/fxos/output.txt',
        stream=sys.stdout,
        level=logging.INFO,  # DEBUG, INFO, WARNING, ERROR, CRITICAL
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
    server_url = 'https://fxos.example.com'
    if len(sys.argv) > 3:
        server_url = sys.argv[3]

    with fxos.FXOS(url=server_url, username=username, password=password) as lab_fxos:
        lab_fxos.get_version()
    # End of with block

    print("Done running...")
    return

# Output:
# [04/03/2018 10:39:42 PM-INFO]: https://fxos.example.com: Login Successful!
# [04/03/2018 10:39:43 PM-INFO]: FXOS Software https://fxos.example.com Version is 2.1(1.85)
# [04/03/2018 10:39:44 PM-INFO]: https://fxos.example.com: Logout Successful!
# Done running...


# Standard boilerplate to call main() function.
if __name__ == "__main__":
    main()
