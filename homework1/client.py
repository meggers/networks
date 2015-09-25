#!/usr/bin/python

import sys, getopt, socket, json

# UDP static info
UDP_HOSTNAME = "localhost"
UDP_PORT = 5000

actions = [] # log of all actions script takes for file dump

def main(argv):
    global actions

    username = ""
    moviename = ""
    starttime = ""

    # parse our command line arguments
    try:
      opts, args = getopt.getopt(argv, "u:m:s:", ["username=","moviename=","starttime="])
    except getopt.GetoptError:
      print 'client.py -u <username> -m <moviename> -s <starttime>'
      sys.exit(2)
    for opt, arg in opts:
        if opt in ("-u", "--username"):
            username = arg
        elif opt in ("-m", "--moviename"):
            moviename = arg
        elif opt in ("-s", "--starttime"):
            starttime = arg

    # Main
    actions.append("Starting Client")
    send_request(json.dumps({"username":username, "moviename":moviename, "starttime":starttime}))
    response = get_response()
    actions.append("Reponse: " + response)
    dump_response()

# sends text over udp using global udp info
def send_request(json_message):
    global UDP_HOSTNAME, UDP_PORT

    print_message("Request message: " + json_message)
    print_message("Sending request to server...")

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(json_message, (UDP_HOSTNAME, UDP_PORT))

    print_message("Request sent.")

# listens on udp port for any response
def get_response():
    global UDP_HOSTNAME, UDP_PORT

    print_message("Listening for server response...")

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_HOSTNAME, UDP_PORT))

    while True:
        data, addr = sock.recvfrom(1024)
        if data:
            print_message("Response received.")
            sock.close()
            return data

# dumps all actions to file
def dump_response():
    global actions

    print_message("Dumping actions to log file...")
    print_message("Exiting.")

    output = open("client_log.txt", "w")
    output.truncate()
    output.write("\n".join(actions))
    output.close()

# utility function to print action and keep log of them
def print_message(message):
    global actions

    print message
    actions.append(message)

if __name__ == "__main__":
   main(sys.argv[1:])