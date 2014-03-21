from tutum.api.auth import authenticate, is_authenticated
from tutum.api.container import list_containers

def main():
    success = authenticate('admin', 'XXXXXX')
    if not success:
        print "Invalid login."
    else:
        print "Login successful. Listing your containers:"
        containers = list_containers()
        for c in containers:
            print c.uuid

if __name__ == "__main__":
    main()