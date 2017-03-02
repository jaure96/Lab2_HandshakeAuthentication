import hashlib
import socket
import struct
import sys
import MyPacketManager
import ChapCodes


def get_config_values():
    config = {}
    try:

        config['authenticator'] = raw_input("Authenticator IP: ")
        config['port'] = raw_input("Port number: ")
        config['identity'] = raw_input("Identity: ")
        config['secret'] = raw_input("Secret: ")
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


def connect(config):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((config['authenticator'], int(config['port'])))
        return sock
    except Exception:
        print("\nERROR: Error opening the socket connection")


def process_challenge(challenge_packet):

    try:
        challenge_len = struct.unpack('!B', challenge_packet['data'][0])[0]
        challenge = challenge_packet['data'][1:challenge_len + 1]
        name = challenge_packet['data'][challenge_len + 1:]

        return {'identifier': challenge_packet['identifier'], 'challenge': challenge, 'name': name}

    except Exception as e:
        print("\nERROR: ", e)


def create_response(config, challenge):

    try:
        hash = hashlib.sha256(chr(challenge['identifier']) + config['secret'] + challenge['challenge'])
        response_value = hash.digest()
        response_value_size = struct.pack('!B', len(response_value))
        name = config['localname']
        data = response_value_size + response_value + name

        return MyPacketManager.create_packet(ChapCodes.RESPONSE, challenge['identifier'], data)

    except Exception as e:
        print("\nERROR: ", e)
