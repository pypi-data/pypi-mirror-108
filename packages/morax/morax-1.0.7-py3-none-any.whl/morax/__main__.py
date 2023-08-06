import yaml
import os, subprocess, pathlib, time, string, random, requests, signal, click
from webbrowser import open_new
from auth.auth import renewAccessToken, getScope, app
from data import api, view, chart
from subprocess import Popen, PIPE

@click.command(hidden=True)
@click.option('--login', '-l', is_flag=True, help="Login into Coinbase account")
@click.option('--switch', '-s', is_flag=True, help = "Switch wallets")
@click.option('--wallet', '-w', is_flag=True, help = "For viewing wallet information")
@click.option('--refresh', '-r', is_flag=True, help = "Force refresh access token")
@click.option('--graph', '-g', is_flag=True, help = "For displaying the crypto. asset's price graph")
@click.option('--version', '-v', is_flag=True, help = "version number")
def start(login, switch, wallet, graph, refresh, version):
	if version:
		output("v1.0.7", "bright_white")
		return
	elif login:
		init()
		return
	elif switch:
		init()
		switchWallet()
		return
	elif wallet:
		init()
		userWallet()
		return
	elif graph:
		init()
		coinGraph()
		return
	elif refresh:
		init()
		tokenRefresh()
		return
	else:
		welcomeText()
		click.echo()
		click.echo("Enter morax --help to get a list of commmands")

def init():
	config = loadConfig()
	if config.get('LOGIN_STATE') == None:
		login()
	else:
		if config.get('TIME') == None:
			login()
		elif time.time() - float(config.get('TIME')) > 7200: 
			output("⚠️  Access token expired", "yellow")
			output("Redirecting you to login page to renew it", "yellow")
			time.sleep(2)					
			login()		
		else:
			refreshToken()

def userWallet():
	if verifyLogin():
		view.selectCoin(api.getCoin())
	else:
		output("Please login first 🥺", "bright_white")

def coinGraph():
	if verifyLogin():
		coin = api.getCoin()	
		chart.getChartData(api.getCoin())
	else:
		output("Please login first 🥺", "bright_white")

def tokenRefresh():
	if verifyLogin():
		try:
			refreshToken()
			output("Successfully renewed access token 👏",'green')
		except Exception as err:
			output("Failed to renewed access token, please login again", 'red')
			login()	
	else:
		output("Please login first 🥺", "bright_white")

def switchWallet():
	if verifyLogin():
		output("I'll need you to authorize me to switch wallets 😁", 'yellow')
		time.sleep(1)
		login()
	else:
		output("Please login first 🥺", "bright_white")
		
def verifyLogin():
	config = loadConfig()
	if config.get("ACCESS_TOKEN") != None and config.get("REFRESH_TOKEN") != None:
		return True
	else:
		return False

def output(inp, color):
	click.echo()
	click.echo(
				click.style(inp, fg=color, bold=True)
			)
	click.echo()

def login():
	config = loadConfig()

	#Kill any process running at PORT 6660
	removeProcess()
	output("In order to continue, you must login to your Coinbase account 💳", 'bright_white')
	output("I'm taking you to the login page right now", 'bright_white')
	time.sleep(2)

	AUTH_URI = ('https://www.coinbase.com/oauth/' 
		+ 'authorize?response_type=code&client_id=' + config.get('CLIENTID') + '&redirect_uri=' 
		+ config.get('REDIRECT_URL') + '&scope=' + getScope() +'&code=' + '302')
		
	open_new(AUTH_URI)
		
	#start the flask server for OAuth
	app.run(port=6660)

def refreshToken():
	config = loadConfig()
	#Fetch new access token using refresh token 
	if time.time() - float(config.get('TIME')) <= 7200:
		renewAccessToken()

def removeProcess():
	port = 6660
	process = Popen(["lsof", "-i", ":{0}".format(port)], stdout=PIPE, stderr=PIPE)
	stdout, stderr = process.communicate()
	for process in str(stdout.decode("utf-8")).split("\n")[1:]:       
		data = [x for x in process.split(" ") if x != '']
		if (len(data) <= 1):
			continue

		os.kill(int(data[1]), signal.SIGKILL)
	
def welcomeText():
	path = os.getcwd()
	p = str(pathlib.Path(__file__).parent.absolute())
	p1 = os.path.join(p,"data","assets")
	os.chdir(p1)
	txt = open(f"ascii.txt", 'r')
	txt = txt.readlines()
	for i in range(len(txt)):
		temp = txt[i].rstrip("\n")
		click.secho(temp, fg = "bright_white")
	os.chdir(path)

def loadConfig():
	path = os.getcwd()
	p = str(pathlib.Path(__file__).parent.absolute())
	os.chdir(p)
	with open("config.yaml", "r") as f:
		os.chdir(path)
		return yaml.safe_load(f)

def genState():
	return ''.join(random.choice(string.ascii_uppercase 
		+ string.ascii_lowercase + string.digits) for _ in range(16))

if __name__ == "__main__":
   start()