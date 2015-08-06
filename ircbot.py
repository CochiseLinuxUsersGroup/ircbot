#!/usr/bin/env python
#Written by paulbe,  github code written by elimisteve

import feedparser, socket, time, pywapi, string, random

#Connection info for IRC
USER = 'CLUG_INFO'  #set bot name
botname     = USER #+ "_bot"
network     = 'irc.freenode.net' #set irc network to connect to
chatchannel = '#cochiselinux' #set channel to connect to
port = 6667  #set port number
end = '\n'

#IRC setup
premess = 'PRIVMSG ' + chatchannel + ' :'
irc = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
irc.connect( ( network, port ) )
print irc.recv( 4096 )
irc.send( 'NICK ' + botname + end )
irc.send( 'USER ' + USER + 'bot botty bot bot: Python IRC' + end )
irc.send( 'JOIN ' + chatchannel + end )

bot_list = "hello".split()

# Helper Functions
def irc_msg(msg):
    """Sends msg to channel"""
    irc.send(premess + msg + end)
    return

def getuser():
    """Returns nick of current message author"""
    try:
        user = data.split()[0].split('!')[0].strip(':')
    except:
        user = data.split('!')[0].strip(':')
    return user
    
def content(keyword):
	return data.split(':!' + keyword + ' ')[1].strip('\r\n ')

#
# GitHub code from elimisteve, thanks!
#
account_name = 'cochiselinuxusersgroup'
branch = 'master'
repo_names = ['cochiselinuxusersgroup.github.io', 'projectcode', 'ircbot']
SLEEP_SECONDS = float(60*2.4)/len(repo_names)  # Check each repo once/couple minutes

# Check github for last change in each repo in repo_names
def force_check_github():
    old_version = {}
    for repo in repo_names:
        old_version[repo] = feedparser.parse(
            'https://github.com/' + account_name +
            '/' + repo + '/commits/' + branch + '.atom'
            )
            
    for repo in repo_names:
        new = feedparser.parse('https://github.com/' + account_name +
                               '/' + repo + '/commits/' + branch + '.atom')
        try:
			author = new.entries[0].author_detail.href.split('/')[-1]
			commit_msg = new.entries[0].title
			print '\n'
			print"[" + repo + "] " + author + ": " + commit_msg
			print '\n'
			irc_msg("[" + repo + "] " + author + ": " + commit_msg)
			
        except:
            print "GitHub fucked up, I think. Here's what they gave us:"
            print new
            
# Mail function    This needs testing, mailing list is too inactive at the moment to test   
def check_mail():
	new_mail = feedparser.parse("https://www.freelists.org/feed/cochiselinux")
	mail_msg = new_mail.entries[0].title
	irc_msg( mail_msg )
	return
	
# Calendar functions  This is a bit messy atm.  Would like to implement google-api at some point
def calendar():
	calendar = feedparser.parse("https://www.google.com/calendar/feeds/fp9et4ecr2c131rth7ftvfua1g%40group.calendar.google.com/public/basic")
	cal_short = "http://tinyurl.com/cochisecal"
	latest_ev = calendar.entries[0].title
	latest_sum = calendar.entries[0].summary
	if '&nbsp;' in latest_sum:
		print 'Stripping'
		stripped_sum = latest_sum.replace('&nbsp;', ' | For details: ' + cal_short)
		irc_msg( '[Next CLUG event]: ' + latest_ev + ' | ' + stripped_sum  )
	else:
		irc_msg( '[Next CLUG event]: ' + latest_ev + ' | ' + latest_sum + ' | ' + 'See Google calendar for details: ' + cal_short )
	return
	
			
# Weather function			
def check_weather():		
	weather = pywapi.get_weather_from_noaa('KFHU') #setup weather results ('location')
	irc_msg("Sierra Vista current weather: " + weather['temp_f'] + "F and " + weather['weather'])
	return
	
# Information function
def info():
	website = "CochiseLinuxUsersGroup.github.io"  #CLUG website
	mailing = "https://www.freelists.org/feed/cochiselinux" #CLUG mailing list feed
	clug_cal = "http://tinyurl.com/cochisecal"
	irc_msg( 'Website: ' + website )
	irc_msg( 'Mailing archive: ' + mailing )
	irc_msg( 'Calendar: ' + clug_cal )
	
# Help function
def irchelp():
	irc_msg( "Available commands: !info, !lastmail, !lastpush, !weather, !nextevent, !google <searchterm> (More to come!)")
	irc_msg( "Use !h <command> for more info ie !h info")
	return


# Google function	
def g_search():
	q_google = content('google').replace(' ', '+')
	s_google = "http://www.google.com/search?q=" + q_google
	irc_msg(s_google)


# Simple rock, paper, scissors game, played vs the bot	
def rps():
	player_score = 0
	computer_score = 0
	tie = 0
	# Handles player choice
	if ':!rock' in data.lower():
		player = 'rock'
	elif ':!paper' in data.lower():
		player = 'paper'
	elif ':!scissors' in data.lower():
		player = 'scissors'

	# Random choice for computer
	computer = random.randint(0,2);
	if (computer == 0):
		computer = "rock";
	elif (computer == 1):
		computer = "paper";
	elif (computer == 2):
		computer = "scissors";
	else:
		computer = "error";
		
	#Round handler
	if (player == computer):
		tie += 1;
		print("Draw");
		irc_msg( 'Player: ' + player + ' , Bot: ' + computer + ' Tie!' )
	elif (player == 'rock'):
		if (computer == 'paper'):
			computer_score += 1;
			print("Computer Wins");
			irc_msg('Player: ' + player + ' , Bot: ' + computer + ' Computer Wins!' )
		else:
			player_score += 1;
			print("Player Wins");
			irc_msg('Player: ' + player + ' , Bot: ' + computer + ' Player Wins!' )
	elif (player == 'paper'):
		if (computer == 'rock'):
			player_score += 1;
			print ("Player Wins");
			irc_msg('Player: ' + player + ' , Bot: ' + computer + ' Player Wins!' )
		else:
			computer_score += 1;
			print ("Computer Wins");
			irc_msg('Player: ' + player + ' , Bot: ' + computer + ' Computer Wins!' )
	elif (player == 'scissors'):
		if (computer == 'rock'):
			computer_score += 1;
			print ("Computer Wins");
			irc_msg('Player: ' + player + ' , Bot: ' + computer + ' Computer Wins!' )
		else:
			player_score += 1;
			print ("Player Wins");
			irc_msg('Player: ' + player + ' , Bot: ' + computer + ' Player Wins!' )
				
# Main Loop
while True:
	data = irc.recv ( 4096 )
	datasp = data.split(' :')[0]
	datasp = str(datasp)

	username = getuser()

	if 'PING' in data:
		irc.send( 'PONG ' + data.split()[1] + end )

	if ':!info' in data.lower(): #Display info for website and mailing list
		print data
		info()
		
	if ':!help' in data.lower(): #Display help functions, list available commands
		print data
		irchelp()
#Help functions
	if ':!h info' in data.lower():
		irc_msg( "!info - Show website and mailing information")
	if ':!h lastmail' in data.lower():
		irc_msg( "!lastmail - Show the title of the latest email to the mailing list")
	if ':!h lastpush' in data.lower():
		irc_msg( "!lastpush - Show the last commits to github repos")
	if ':!h weather' in data.lower():
		irc_msg( "!weather - Show current weather in sierra vista")
	if ':!h nextevent' in data.lower():
		irc_msg( "!nextevent - Show the next calendar event")
	if ':!h google' in data.lower():
		irc_msg( "!google <searchterm> - Return a google search (link) in irc")
#End help functions
			
	if ':!lastmail' in data.lower(): # Lastmail function
		print data
		check_mail()
	
	if ':!lastpush' in data.lower(): # Lastpush function
		print data
		force_check_github()
		
	if ':!weather' in data.lower(): # Weather function
		print data
		check_weather()
		
	if ':!nextevent' in data.lower(): # Calendar function
		print data
		calendar()
	
	if ':!google' in data.lower(): # Google search function
		print data
		g_search()

#rock,paper,scissors	
	if ':!rock' in data.lower():
		rps()
	if ':!paper' in data.lower():
		rps()
	if ':!scissors' in data.lower():
		rps()
#end rock,paper,scissors

	# Bot's manners
	if not username.lower().endswith('INFO'):
		if 'good' and 'morning' in data.lower():
			irc_msg( 'Good Morning ' + username )
		if 'good' and 'afternoon' in data.lower():
			irc_msg( 'Good afternoon ' + username)
		if 'good' and 'evening' in data.lower():
			irc_msg( 'Good evening ' + username)
		for word in bot_list: # Add words to bot_list to add more triggers
			if word.lower() in data.lower():
				irc_msg( 'hello ' + username)
				break

