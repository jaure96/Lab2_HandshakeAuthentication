import hashlib
import socket
import struct
import sys
import MyPackeTManager
import ChapCodes


def get_config_values(type):
    config = {}
    try:

        config['authenticator'] = raw_input("Enter the IP of the authenticator: ")
        config['port'] = raw_input("Enter the port to connect to: ")
        config['identity'] = raw_input("Enter the identity you want to authenticate with: ")
        config['secret'] = raw_input("Enter the secret you want to authenticate with: ")
        config['localname'] = raw_input("Enter the name of the local (peer) system: ")

        for setting in config:
            if (config[setting] == ''):
                raise Exception('Cannot continue: One or more settings are empty. Exiting...')

    except Exception as e:
        print "\nCannot continue: End of File detected. Exiting..."
        sys.exit()

    return config


def connect(config):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((config['authenticator'], int(config['port'])))
    return sock

def process_challenge(challenge_packet):
    challenge_len = struct.unpack('!B', challenge_packet['data'][0])[0]
    challenge = challenge_packet['data'][1:challenge_len + 1]
    name = challenge_packet['data'][challenge_len + 1:]
    print "Processing challenge with identifier:", challenge_packet['identifier'], "name:", name
    return {'identifier': challenge_packet['identifier'],
            'challenge': challenge,
            'name': name}

def create_response(config, challenge):
    hash = hashlib.sha256(chr(challenge['identifier']) + config['secret'] + challenge['challenge'])
    response_value = hash.digest()
    response_value_size = struct.pack('!B', len(response_value))
    name = config['localname']
    data = response_value_size + response_value + name
    print "Creating response with identifier:", challenge['identifier']
    return MyPackeTManager.createPacket(ChapCodes.RESPONSE, challenge['identifier'], data)

def peer(config):
    sock = connect(config)
    packet = MyPackeTManager.createPacket(ChapCodes.AUTH_REQUEST, 0x00, config['identity'])
    MyPackeTManager.send_packet(sock, packet)
    packet = MyPackeTManager.receive_packet(sock)
    if (packet['code'] == ChapCodes.CHALLENGE):
        challenge_data = process_challenge(packet)
        packet = create_response(config, challenge_data)
        MyPackeTManager.send_packet(sock, packet)
        packet = MyPackeTManager.receive_packet(sock)
        if (packet['identifier'] == challenge_data['identifier']):
            if (packet['code'] == ChapCodes.SUCCESS):
                print "AUTHENTICATION WAS OK!"
            elif ((packet['code'] == ChapCodes.FAILURE)):
                print "AUTHENTICATION ERROR: ", packet['data']

    sock.close()


