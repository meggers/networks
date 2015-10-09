#!/usr/bin/python

import sys, socket, json, random

# UDP static info
UDP_HOSTNAME = "0.0.0.0"
UDP_PORT = 5000

# log of all actions script takes for file dump
actions = []

def main(argv):
    global UDP_HOSTNAME, UDP_PORT

    print_message("Starting Server")
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_HOSTNAME, UDP_PORT))

    request = listen_request(sock)

    print_message("Request message: " + request)
    send_response(sock, json.loads(request))

    dump_log()

def listen_request(sock):
    print_message("Listening for client...")

    while True:
        data, addr = sock.recvfrom(1024)
        if data:
            print_message("Request received.")
            return data

def send_response(sock, request):
    response = json.dumps({
        "hostname": socket.gethostname(),
        "moviename": request["moviename"],
        "moviestart": "00:00:01",
        "moviecost": 100,
        "password": random.randrange(0, 256)
    })

    print_message("Generated response: " + response)
    print_message("Sending response to client...")

    sock.sendto(response, ("10.10.2.2", 5000))

    print_message("Response sent.")

# dumps all actions to file
def dump_log():
    global actions

    print_message("Dumping actions to log file...")
    print_message("Exiting.")

    output = open("server_log.txt", "w")
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
