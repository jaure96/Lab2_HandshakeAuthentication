import sys
import ChapCodes
import MyPacketManager
import MyPeerFunctions

if __name__ == "__main__":
    try:
        print("***************************************************")
        print("               Peer running....")
        print("***************************************************")

        config = MyPeerFunctions.get_config_values()

        sock = MyPeerFunctions.connect(config)
        packet = MyPacketManager.create_packet(ChapCodes.AUTH_REQUEST, 0x00, config['identity'])
        MyPacketManager.send_packet(sock, packet)

        packet = MyPacketManager.receive_packet(sock)

        if packet['code'] == ChapCodes.CHALLENGE:
            challenge_data = MyPeerFunctions.process_challenge(packet)
            packet = MyPeerFunctions.create_response(config, challenge_data)
            MyPacketManager.send_packet(sock, packet)
            packet = MyPacketManager.receive_packet(sock)

            if packet['identifier'] == challenge_data['identifier']:

                if packet['code'] == ChapCodes.SUCCESS:
                    print("\nAUTHENTICATION WAS OK!")

                elif packet['code'] == ChapCodes.FAILURE:
                    print("\nAUTHENTICATION ERROR: ", packet['data'])

    except EOFError:
        print("\nCannot continue: End of File detected. Exiting...")
        sys.exit()
    finally:
        sock.close()
