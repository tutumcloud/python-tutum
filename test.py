from tutum.api.auth import authenticate, is_authenticated
from tutum.api.container import Container
from tutum.api.application import Application

def main():
    if is_authenticated():
        print "Listing containers:"
        print Container.list()
        print "Listing applications:"
        print Application.list()
    else:
        print """
        You are not authenticated. Either set TUTUM_USER and TUTUM_APIKEY
        in your environment, or use tutum.api.auth.authenticate.
        """

if __name__ == "__main__":
    main()