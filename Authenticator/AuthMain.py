import sys
import MyAuthFunctions
import MyPacketManager
import GlobalVariables

if __name__ == "__main__":
    try:
        print("***************************************************")
        print("               Server running....")
        print("***************************************************")

        config = MyAuthFunctions.get_config_values()

        sock = MyAuthFunctions.listen(config)
        packet = MyPacketManager.receive_packet(sock)

        if packet['code'] == GlobalVariables.AUTH_REQUEST:
            auth_request_data = MyAuthFunctions.process_authentication_request(packet)
            (packet, challenge_id, challenge) = MyAuthFunctions.create_challenge(config)
            MyPacketManager.send_packet(sock, packet)
            packet = MyPacketManager.receive_packet(sock)

            if packet['code'] == GlobalVariables.RESPONSE:
                if packet['identifier'] == challenge_id:
                    response_data = MyAuthFunctions.process_response(packet)
                    if MyAuthFunctions.verify_response(response_data, auth_request_data['identity'], challenge_id, challenge):
                        code = GlobalVariables.SUCCESS
                        data = ''
                    else:
                        code = GlobalVariables.FAILURE
                        data = 'You are not registered'
                    packet = MyPacketManager.create_packet(code, packet['identifier'], data)
                    MyPacketManager.send_packet(sock, packet)

        sock.close()

    except EOFError:
        print("\nCannot continue: End of File detected. Exiting...")
        sys.exit()
