import sys
import MyAuthFunctions

if __name__ == "__main__":
    try:

        config = MyAuthFunctions.get_config_values('authenticator')
        print "============ Starting authentication process as authenticator ================"
        MyAuthFunctions.authenticator(config)

    except EOFError:
        print "\nCannot continue: End of File detected. Exiting..."
        sys.exit()