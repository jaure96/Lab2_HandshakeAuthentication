import struct

# buruan luzeria 4 da:  1 code + 1 id  + 2 lenght


def create_packet(code, identifier, data):
    data_len = len(data)
    packet_len = 4 + data_len

    # !(big endian) + B(integer) + B(integer) + B(integer) + __s(hainbat string karaktere)
    pack_format = '!BBH' + str(data_len) + 's'

    packet = struct.pack(pack_format, code, identifier, packet_len, data)

    return packet

def send_packet(my_socket, packet):
    try:
        my_socket.send(packet)
    except Exception as exp:
        print("ERROR: ", exp)


def receive_packet(sock):

    try:
        header = sock.recv(4)

        while len(header) < 4:
            moment_header = sock.recv(4 - len(header))
            header = header + moment_header
            if header == '':
                raise Exception("An error occurred receiving the packet")

        (code, identifier, length) = struct.unpack('!BBH', header)
        packet = header

        while len(packet) < length:
            chunk = sock.recv(length - len(packet))
            if chunk == '':
                raise Exception("An error occurred receiving the packet")
            packet = packet + chunk

        (code, identifier, length, data) = struct.unpack('!BBH' + str(length - 4) + 's', packet)

        return {'code': code,
                'identifier': identifier,
                'length': length,
                'data': data}
    except Exception as exp:
        print("ERROR: ", exp)