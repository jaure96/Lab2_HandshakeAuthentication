import sys
import MyAuthFunctions
import MyPackeTManager
import ChapCodes

if __name__ == "__main__":
    try:
        print("***************************************************")
        print("               Server running....")
        print("***************************************************")

        config = MyAuthFunctions.get_config_values()

        sock = MyAuthFunctions.listen(config)
        packet = MyPackeTManager.receive_packet(sock)

        if packet['code'] == ChapCodes.AUTH_REQUEST:
            auth_request_data = MyAuthFunctions.process_authentication_request(packet)
            (packet, challenge_id, challenge) = MyAuthFunctions.create_challenge(config)
            MyPackeTManager.send_packet(sock, packet)
            packet = MyPackeTManager.receive_packet(sock)

            if packet['code'] == ChapCodes.RESPONSE:
                if packet['identifier'] == challenge_id:
                    response_data = MyAuthFunctions.process_response(packet)
                    if MyAuthFunctions.verify_response(response_data, auth_request_data['identity'], challenge_id, challenge):
                        code = ChapCodes.SUCCESS
                        data = ''
                    else:
                        code = ChapCodes.FAILURE
                        data = 'You are not registered'
                    packet = MyPackeTManager.createPacket(code, packet['identifier'], data)
                    MyPackeTManager.send_packet(sock, packet)

        sock.close()

    except EOFError:
        print ("\nCannot continue: End of File detected. Exiting...")
        sys.exit()