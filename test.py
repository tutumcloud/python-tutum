from tutum.api import auth, container

def main():

    username = "admin"
    password = "XXXXX"

    apikey = auth.get_apikey(username, password)

    if apikey:

        print "Success!"
        print "Listing your containers:"
        containers = container.list_containers(username, apikey)
        for c in containers:
            print c.uuid
    else:
        print "Invalid username or password, please try again."

if __name__ == "__main__":
    main()