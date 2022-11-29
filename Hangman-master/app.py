from flask import Flask,render_template,redirect,request

app = Flask(__name__) 

secret_word = None
allwords = None
to_display = None
tries = None
blanks = None

import random

#This fucntion gets a random word from the Movies.txt and removes the spaces
def get_random_word():
    num_words_processed = 0
    c_word = None
    with open("dictionary/Movies.txt", 'r') as f:
        for word in f:
            word = word.strip().lower()
            num_words_processed += 1
            if random.randint(1, num_words_processed) == 1:
                c_word = word
    return c_word

@app.after_request
def set_response_headers(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

#Homepage, this give the basic details about the game
@app.route('/')
def hello_world():
    return render_template('home.html')

#Mainpage, this is the place where the whole game takes place
@app.route('/game')
def game():
	global secret_word
	global allwords
	global to_display
	global tries
	global blanks	
	secret_word = get_random_word()
	allwords = "abcdefghijklmnopqrstuvwxyz"
	blanks = 0
	to_display = []
	for i,charac in enumerate(secret_word):
		if charac == " ":
			to_display.append("#")
		else:
			to_display.append("_")
			blanks+=1

	tries = 0
	return render_template('game.html',to_display=to_display,allwords=allwords,tries="/static/img/hangman%d.png"%tries)

#removes the alphabets which are already entered from the allwords variable and displays it in the page
@app.route('/add_char',methods=["POST"])
def add_char():
	global secret_word
	global allwords
	global to_display
	global tries
	global blanks	

	letter = request.form["letter"]
	
	chance_lost = True
	for i,charac in enumerate(secret_word):
		if charac.lower()==letter.lower():
			chance_lost = False
			to_display[i] = letter.lower()
			blanks-=1

	allwords = allwords.replace(letter,'')
	print("blanks",blanks)
	if chance_lost==True:
		tries += 1
		if tries==6:
			return redirect('/game_lost')

	if blanks==0:
		return redirect('/game_won')

	return render_template('game.html',to_display=to_display,allwords=allwords,tries="/static/img/hangman%d.png"%tries)


#Page which pops when the player loses the game
@app.route('/game_lost')
def game_lost_landing():
	return render_template('game_lost.html', word=secret_word)


#Page which pops when the player wins the game
@app.route('/game_won')
def game_won_landing():
	return render_template('game_won.html', word=secret_word)

if __name__ == '__main__': 
    app.run() 
