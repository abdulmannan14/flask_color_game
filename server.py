import math
from flask import (
    Flask, request, jsonify, g, redirect, url_for, render_template,
    session
)
import game as Game
from datetime import timedelta

SESSION_EXPIRY = 5      # a session will live for 5 mins

server = Flask(__name__, static_folder='static')

@server.route('/play', methods=['GET', 'POST'])
def play():
    print(request.args)
    if request.method == 'GET':
        # render the template
        return render_template('game_setup.html')
    elif request.method == 'POST':
        url = url_for(
            'playMastermind',
            numCol=request.form.get('numCol'),
            codeLength=request.form.get('codeLength'),
            duplicate=request.form.get('duplicate')
        )
        
        return redirect(url)

@server.get('/playMastermind')
def playMastermind():
    i = 0
    numCol = int(request.args.get('numCol', None))
    codeLength = int(request.args.get('codeLength', None))
    duplicate = request.args.get('duplicate', None)
    duplicate = True if duplicate and duplicate == 'yes' else False

    if not numCol or not codeLength:
        # error
        return { 'error': 'Bad Arguments' }, 400

    code = Game.createCode(numCol, codeLength, duplicate)

    #print('numCol', numCol)
    #print('codeLength', codeLength)
    #print('duplicate', duplicate)
    #print('code', code)

    # generate the required number of unique
    # colors for each unique digit in code
    # create a map and use that in the template
    colors = {}
    for digit in code:
        if not digit in colors:
            colors['{}'.format(digit)] = Game.getRandomColor(digit)

    if numCol > codeLength and not duplicate:
        # in this case you need to add extra colors
        # in the palette
        for i in range(1, 6):
            if not i in code:
                colors['{}'.format(i)] = Game.getRandomColor(i)

    
    
    # add the code in HTTP only cookie
    # this will add the cookie to every request
    # and can be checked against later
    session['code'] = code
    session['numCols'] = numCol
    session['duplicate'] = duplicate
    session['codeLength'] = codeLength

    isOdd = True if codeLength % 2 != 0 else False
    hintRows = math.ceil(codeLength/2)

    return render_template(
        'game.html',
        numCol=numCol,
        codeLength=codeLength,
        duplicate=duplicate,
        rows=12,
        colors=colors,
        hintRows=hintRows,
        isOdd=isOdd
    )

@server.post('/check')
def check_guess():
    # checks a guess submitted by the user
    if not 'code' in session or \
        not 'numCols' in session or \
            not 'codeLength' in session:
                return { 'error': 'No session', }

    guess = request.json.get('guess')
    #print('guess', guess)
    codeLength = session['codeLength']
    code = session['code']
    #print('code', code)
    numCols = session['numCols']

    if not guess:
        return { 'error': 'Bad Request' }
    
    #if numCols > codeLength:
        # remove the extra
    #    guess = list(filter(lambda g: g > 0, guess))
    #    print('corrected_guess', guess) 

    blacks, whites = Game.check_guess(guess, code)
    #print('code', code, 'guess', guess)
    #print('blacks', blacks, 'whites', whites)
    res = {}

    # the game logic was slightly misunderstood;
    # it should be the number of blacks being equal
    # to code length when correct and whites zero
    # based on this comment from input.py
    # "blacks is the length of correct positions"
    if blacks == codeLength:
        # guessed correctly
        res['result'] = 'correct'
    else:
        res['result'] = 'incorrect'
    
    res['whites'] = whites
    res['blacks'] = blacks

    return res

@server.get('/hint')
def hint():
    codeLength = session['codeLength']
    numCols = session['numCols']
    
    try:
        lastHints = session['hints']
    except KeyError:
        lastHints = None

    print('lastHints', lastHints)
    s = Game.createS(codeLength, numCols)
    h = None
    
    if lastHints:
        # this hint was already provided
        # so remove it from S so it is not repeated
        for k in range(len(lastHints)):
            lastHint = lastHints[k]
            #print('removing {} from s'.format(lastHint))
            found = True
            for idx, code in enumerate(s):
                #print('code', code)
                for i in range(len(code)):
                    if code[i] != lastHint[i]:
                        found = False
                        break
                if found:
                    #print('found {} at {}'.format(lastHint, idx))
                    s.pop(idx)
                    break
                else:
                    found = True
        
        h = Game.giveHint(S=s)
        lastHints.append(h)
        session['hints'] = list(lastHints)

    else:
        h = Game.giveHint(S=s)
        session['hints'] = [h]

    return {
        'hint': h
    }

@server.get('/solution')
def solution():
    # return the solution to the code
    pass


server.secret_key = 'SECReT'
server.config['SESSION_TYPE'] = 'filesystem'
server.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=SESSION_EXPIRY)

if __name__ == '__main__':
    server.run(
        host='127.0.0.1',
        port=8080
    )