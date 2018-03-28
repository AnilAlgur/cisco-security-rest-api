import ise21  # Cisco Identity Services Engine (ISE) 2.1
import sys
import logging

logger = logging.getLogger(__name__)

def main():
    """
    Demo script for ISE REST API.
    """
    logging.basicConfig(
        stream=sys.stdout,  # filename='/full/path/to/file',
        level=logging.DEBUG, # DEBUG, INFO, WARNING, ERROR, CRITICAL
        format='[%(asctime)s-%(levelname)s]: %(message)s',
        datefmt='%m/%d/%Y %I:%M:%S %p')

    # Get server, username and password from CLI
    username = 'username'
    if len(sys.argv) > 1:
        username = sys.argv[1]
    password = 'password'
    if len(sys.argv) > 2:
        password = sys.argv[2]
    server_url = 'https://ise.example.com:9060'
    if len(sys.argv) > 3:
        server_url = sys.argv[3]

    count = 0
    with ise21.ISE(server_url, username, password) as lab_ise:
        for XML_resp in lab_ise.getAllEndpoints(filter="mac.EQ.11:11:11:11:11:12"):  # filter='?filter=mac.EQ.11:11:11:11:11:12' 'groupId.EQ.a4a97d40-b4cb-11e5-8ffd-005056903ad0'
            for rsrc in XML_resp.iter('{ers.ise.cisco.com}resource'):
                logger.info(rsrc.attrib['name'] + ' --> ' + rsrc.attrib['id'])
                lab_ise.getEndpoint(mac_addr=rsrc.attrib['name'])
                endpt_xml = lab_ise.getEndpointById(rsrc.attrib['id'])
                logger.info(str(count) + ". " + rsrc.attrib['name'] + ' --> ' + rsrc.attrib['id'] + ' Group ID[' + endpt_xml.find('groupId').text + ']')
                count = count + 1
        # lab_ise.getAllEndpoints(filter='?filter=groupId.EQ.a4a97d40-b4cb-11e5-8ffd-005056903ad0')
        lab_ise.getEndpointById('719854a0-e26d-11e6-b433-005056926a52')
        # lab_ise.getAllEndpointIdGroups(filter='name.EQ.TEST-GROUP')
        lab_ise.getEndpointIdGroupById('a4a97d40-b4cb-11e5-8ffd-005056903ad0')
        lab_ise.getInternalUser('internaluser')

    return

# Standard boilerplate to call main() function.
if __name__ == "__main__":
    main()
