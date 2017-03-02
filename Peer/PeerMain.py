import sys
import MyPeerFunctions

if __name__ == "__main__":
    try:
        print "============ Starting authentication process as peer ================"
        config = MyPeerFunctions.get_config_values('peer')
        MyPeerFunctions.peer(config)
    except EOFError:
        print "\nCannot continue: End of File detected. Exiting..."
        sys.exit()