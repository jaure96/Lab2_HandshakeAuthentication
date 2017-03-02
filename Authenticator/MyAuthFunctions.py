import hashlib
import socket
import struct
import random
import time
import sys
import MyPackeTManager
import ChapCodes


def get_config_values(type):
    config = {}
    try:
        config['port'] = raw_input("Enter the port to listen to: ")
        config['localname'] = raw_input("Enter the name of the local (authenticator) system: ")

        for setting in config:
            if (config[setting] == ''):
                raise Exception('Cannot continue: One or more settings are empty. Exiting...')

    except Exception as e:

        print "\nCannot continue: End of File detected. Exiting..."

        sys.exit()

    return config

def listen(config):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', int(config['port'])))  # Host == '' means any local IP address
    print "Waiting for incoming authentication requests..."
    sock.listen(1)
    (conn, addr) = sock.accept()
    return conn

def verify_response(response_data, identity, identifier, challenge):
    print "Verifying response for identifier:", identifier

    # This is the list of valid identities and associated secrets
    identities = {}
    identities['jaure'] = '123';

    if (identity in identities):
        secret = identities[identity]
        hash = hashlib.sha256(chr(identifier) + secret + challenge)
        our_value = hash.digest()
        if (our_value == response_data['response']):
            return 1
        else:
            return 0
    else:
        return 0

def process_authentication_request(auth_request_packet):
    identity = auth_request_packet['data']
    print "Processing authentication request for identity:", identity
    return {'identifier': auth_request_packet['identifier'],
            'identity': identity}

def create_challenge(config, auth_request_data):
    identifier = random.randint(0, 255)
    # Create some random challenge, using the hash of a string
    # composed of 60 random integer number in the range
    # [1,100000000]
    hash = hashlib.sha256(''.join(str(random.sample(xrange(10000000), 60))))
    challenge_value = hash.digest()
    challenge_value_size = struct.pack('!B', len(challenge_value))
    name = config['localname']
    data = challenge_value_size + challenge_value + name
    print "Creating challenge with identifier:", identifier
    packet = MyPackeTManager.createPacket(ChapCodes.CHALLENGE, identifier, data)
    return (packet, identifier, challenge_value)

def process_response(response_packet):
    response_len = struct.unpack('!B', response_packet['data'][0])[0]
    response = response_packet['data'][1:response_len + 1]
    name = response_packet['data'][response_len + 1:]
    print "Processing response with identifier:", response_packet['identifier'], "name:", name
    return {'identifier': response_packet['identifier'],
            'response': response,
            'name': name}


def authenticator(config):
    sock = listen(config)
    packet = MyPackeTManager.receive_packet(sock)
    if (packet['code'] == ChapCodes.AUTH_REQUEST):
        auth_request_data = process_authentication_request(packet)
        (packet, challenge_identifier, challenge) = create_challenge(config, auth_request_data)
        MyPackeTManager.send_packet(sock, packet)
        packet = MyPackeTManager.receive_packet(sock)
        if (packet['code'] == ChapCodes.RESPONSE):
            if (packet['identifier'] == challenge_identifier):
                response_data = process_response(packet)
                if (verify_response(response_data, auth_request_data['identity'], challenge_identifier, challenge)):
                    code = ChapCodes.SUCCESS
                    data = ''
                else:
                    code = ChapCodes.FAILURE
                    data = 'You are not registered'
                packet = MyPackeTManager.createPacket(code, packet['identifier'], data)
                MyPackeTManager.send_packet(sock, packet)

    time.sleep(1)
    sock.close()
