A Basic IRC robot
==========

A simple to use, basic IRC client for created bots. Specifically, I created this to complete the programming 8 and IRC missions on [hackthissite.org] (https://www.hackthissite.org)

Don't read this if you actually want to complete the mission! This will spoil it for you.

I made it general enough that it is easy to have the bot auto-respond to new commands, and enventually I plan to expand it to compete in their IRC takeover competition.

connecting to IRC channels
------------------------------------

connecting is as simple as sending the information needed:

    from irc_bot import irc_bot
    irc = irc_bot(server, nick=nick, password=irc_password)
    irc.message("nickserv", "identify " + irc_password)
    irc.send_command("JOIN " + channel)

creating new commands for the bot
----------------------------------------------

Adding a new command that the bot will respond to is simple. First, create a custom listener, then attach it to the bot. In the challenge, the bot in the room asks you to create an MD5 hash of a random string, so I created this listener to reply with the hash. It isn't a very good listener because it is extremely specific to the mission, but it illustrates the proper way to create one:

    def reflect_md5(data):
        global irc
        md5 = hashlib.md5()
        md5.update(bytes(data[data.find("!md5 ")+5:-2], 'ascii'))
        irc.notice("moo", "!perm8-result " + md5.hexdigest())

Then you have to register it, along with the pattern that will trigger the listener to be run:

    irc.add_listener("!md5",reflect_md5)

and that's it! Now, when the bot sees any data coming from the channel including "!md5", it will immediately call reflect_md5 and send it the data. See hts8.py for the full example.