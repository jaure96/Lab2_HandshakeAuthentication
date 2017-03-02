import hashlib
import socket
import struct
import random
import sys
import uuid
import MyPackeTManager
import ChapCodes


def get_config_values():
    config = {}
    try:
        config['port'] = raw_input("Port number: ")
        config['localname'] = raw_input("System name: ")

        if not check_config_values_are_filled(config):
            raise Exception('Configuration is not filled!')

    except Exception as e:
        print("\nERROR: ", e)
        sys.exit()

    return config


def check_config_values_are_filled(config):
    for c in config:
        if config[c] == '':
            return False
    return True


def listen(config):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', int(config['port'])))
    print("Waiting for incoming authentication requests...")
    sock.listen(5)  # 5 = zenbat entzule ipintzen dian kolan
    (conn, addr) = sock.accept()
    return conn


def verify_response(response_data, identity, identifier, challenge):

    secret = check_identity_in_database(identity)
    if not secret == '':
        hash = hashlib.sha256(chr(identifier) + secret + challenge)
        our_value = hash.digest()
        if our_value == response_data['response']:
            return 1
        else:
            return 0
    else:
        return 0


def process_authentication_request(packet):
    identity = packet['data']
    return {'identity': identity, 'identifier': packet['identifier']}


def create_challenge(config):

    identifier = random.randint(0, 255)

    # Hash-a bakarra izanbiada orduan string aleatorio bat sotzen dot
    hash = hashlib.sha256(generate_random_string())

    challenge_value = hash.digest()
    challenge_value_size = struct.pack('!B', len(challenge_value))
    name = config['localname']
    data = challenge_value_size + challenge_value + name
    print ("Creating challenge with identifier:", identifier)
    packet = MyPackeTManager.createPacket(ChapCodes.CHALLENGE, identifier, data)
    return packet, identifier, challenge_value


def process_response(response_packet):
    response_len = struct.unpack('!B', response_packet['data'][0])[0]
    response = response_packet['data'][1:response_len + 1]
    name = response_packet['data'][response_len + 1:]
    print("Processing response with identifier:", response_packet['identifier'], "name:", name)

    return {'identifier': response_packet['identifier'], 'response': response, 'name': name}


def generate_random_string():
    return str(uuid.uuid4())


def check_identity_in_database(identity):
    identities = {}
    identities['jaure'] = '123'

    if identity in identities:
        return identities[identity]
    else:
        return ''
