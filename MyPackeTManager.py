import struct

header_len = 4

def createPacket(code, identifier, data):
    data_len = len(data)
    packet_len = header_len + data_len

    # Packing format:
    #    ! ==> use network byte order
    #    B ==> encode as a C unsigned char (8 bit character == octect)
    #    s ==> encode as a string character (in particular NNs => encode NN characters)
    #
    pack_format = '!BBH' + str(data_len) + 's'

    packet = struct.pack(pack_format, code, identifier, packet_len, data)

    return packet

def send_packet(sock, packet):
    totalsent = 0
    while totalsent < len(packet):
        sent = sock.send(packet[totalsent:])
        if sent == 0:
            raise RuntimeError("socket connection broken")
        totalsent = totalsent + sent


def receive_packet(sock):
    header = sock.recv(header_len)

    while len(header) < header_len:
        print "paket: " + header
        print len(header)
        momentHeader = sock.recv(header_len - len(header))
        header = header + momentHeader
        if header == '':
            raise RuntimeError("socket connection broken")

    print "paket: " + header
    print len(header)
    (code, identifier, length) = struct.unpack('!BBH', header)
    packet = header

    while len(packet) < length:
        chunk = sock.recv(length - len(packet))
        if chunk == '':
            raise RuntimeError("socket connection broken")
        packet = packet + chunk

    (code, identifier, length, data) = struct.unpack('!BBH' + str(length - header_len) + 's', packet)
    return {'code': code,
            'identifier': identifier,
            'length': length,
            'data': data}
