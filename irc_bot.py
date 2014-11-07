"""
For hackthissite programming challenge and IRC challenges.
"""
import socket
import time
import _thread
import os
import re

class InvalidCharacters(ValueError):
    "Invalid characters were encountered in the message"


class MessageTooLong(ValueError):
    "Message is too long"


class irc_bot:
    sock = None
    print_messages = True
    listener = None
    bot_name = "Icarus"
    version = 1.0
    description = "basic IRC bot for HTS missions"
    response_needed = None
    custom_listeners = {}   # dict of words to take some automated action on
    command_delay = .5 #min time to wait between sending commands

    def __init__(self, server, nick, password, port=6667, print_server_messages=True, version=1.0, allow_user_input=True):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((server, port))
        self.print_messages = print_server_messages
        user_string="USER " + nick + " " + server + " " + nick + " :" + str(version) + "\n"
        nick_string="NICK " + nick + "\n"
        _thread.start_new_thread(self.listen, ())
        self.send_command(nick_string)
        self.send_command(user_string)
        self.hold_for_response("PING")
        if allow_user_input:
            self.listen_for_user_input()
        print("PRIVMSG " + nick + "  :")
        self.add_listener("PRIVMSG " + nick + " :\x01VERSION",self.send_version) #not working - need to do some kind of pattern match instead

    def hold_for_response(self, response, timeout=3, freq=.2):
        """ensures that nothing happens in the main script until the response is read, or timeout is reached"""
        self.response_needed = response
        end_time = time.time() + timeout
        while self.response_needed is not None and time.time() < end_time:
            time.sleep(freq)

    def join_channel(self, channel):
        self.send_command("JOIN " + str(channel) + "\n")

    def ping(self, data):
        self.send_command("PONG :" + data +"\n")

    def priv_message(self, target, message):
        self.send_command("PRIVMSG " + target + " : " + message)

    def listen(self):
        sleep_time = .1
        while True:
            self.read_messages()
            time.sleep(sleep_time)

    def read_messages(self):
        # reads messages from the server
        time.sleep(.1)
        data = self.sock.recv(2048)
        data = str(data, encoding='UTF-8')
        if self.print_messages:
            for message in data.splitlines():
                print("< " + message)
        if self.response_needed is not None:
            if data.find(self.response_needed) != -1:
                self.response_needed = None
        if data.find("PING :") != -1:
            #respond if ping
            loc = data.find("PING :")
            self.ping(data[loc+6:-1])
        for term in self.custom_listeners.keys():
            if re.search(term, data):
                self.custom_listeners[term](data)
        return data

    def add_listener(self, string, handler):
        """a string to watch for in responses. When found, will call the handler function and pass the data"""
        self.custom_listeners[string] = handler

    def remove_listener(self, string):
        if string in self.custom_listeners.keys():
            del self.custom_listeners[string]

    def authenticate(self, password):
        self.priv_message("NickServ", "identify " + password)

    def send_command(self, command):
        #while self.last_command is not None and self.last_command + self.command_delay > time.time():
        #   time.sleep(.001)
        command = command + "\r\n"
        if self.print_messages:
            print("> " + command )
        self.sock.send(bytes(command, 'ascii'))
        #self.last_command = time.time()

    def notice(self, target, text):
        """Send a NOTICE command."""
        self.send_command("NOTICE %s :%s" % (target, text))

    def message(self, target, message):
        """Sends a message in the format of /msg"""
        command = ":/msg " + target + " " + message
        self.send_command(command)

    def send_version(self, data):
        version = self.bot_name + ":" + str(self.version) + ":" + self.description
        target = data[data.find(":")+1:data.find("!")]
        self.notice(target, "\x01VERSION " + version )

    def listen_for_user_input(self):
        """listens for commands entered by the user on the command line, and sends them to the irc server"""
        def listen():
            while True:
                cmd = input("# ")
                self.send_command(cmd)
                time.sleep(1)
        _thread.start_new_thread(listen, ())
