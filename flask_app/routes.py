from flask import jsonify, abort, make_response, request
from .app import app
from model.user import User, InsufficientFundsError, InsufficientSharesError
from model.util import get_price


@app.route('/api/account_info/<api_key>', methods=["GET"])
def returnUser(api_key):
    user= User.api_authenticate(api_key)
    if user is None:
        abort(404)
    return jsonify(user.json())

@app.route("/api/get_api_key", methods=["POST"])
def web_login():
    """ accept a username and password in json data, return the user's api key """
    if not request.json or "username" not in request.json or 'password' not in request.json:
        return jsonify({"error": "deposit requires json with 'username' and 'password' key"}), 400
    username= request.json['username']
    password = request.json['password']
    user = User.login(username,password)
    if user is not None:
        return jsonify({
        "api_key": user.api_key
        })    
    return jsonify({"error": "no user found"}) 

@app.route('/api/create_account/', methods=["POST"])
def create_account():
    """ create an account with a username, realname, and password provided in
    a json POST request """
    if not request.json or "username" not in request.json or 'password' not in request.json or 'realname' not in request.json:
        return jsonify({"error": "deposit requires json with 'username', 'password', and 'realname' key"}), 400
    new_user = User(username= request.json['username'], password= request.json['password'], realname= request.json['realname'])
    password = request.json['password']
    new_user.hash_password(password)
    new_user.generate_api_key()
    new_user.save()
    return jsonify(new_user.json())

@app.route('/api/price/<ticker>', methods=["GET"])
def lookup_price(ticker):
    """ return the price of a given stock. no api authentication """
    price = get_price(ticker)
    return jsonify({
        "ticker": ticker,
        "price": price
    })

@app.route('/api/positions/<api_key>', methods=["GET"])
def get_positions(api_key):
    """ return a json list of dictionaries of the user's positions """
    user= User.api_authenticate(api_key)
    if user is None:
        abort(404)
    return jsonify({"positions":[ position.json() for position in user.all_positions()]})


@app.route('/api/position/<ticker>/<api_key>', methods=["GET"])
def get_position(ticker, api_key):
    """ return a json object of a user's position for a given stock symbol """
    user= User.api_authenticate(api_key)
    if user is None:
        abort(404)
    return jsonify({"positions":user.position_for_stock(ticker).json()})


@app.route('/api/trades/<api_key>', methods=["GET"])
def get_trades(api_key):
    """ return a json list of dictionaries representing all of a user's trades """
    user= User.api_authenticate(api_key)
    if user is None:
        abort(404)
    return jsonify({"trades":[ trade.json() for trade in user.all_trades()]})


@app.route('/api/trades/<ticker>/<api_key>', methods=["GET"])
def get_trades_for(ticker, api_key):
    """ return a json list of dictionaries representing all trades for a given stock """
    user= User.api_authenticate(api_key)
    if user is None:
        abort(404)
    return jsonify({"trades":[ trade.json() for trade in user.trades_for(ticker)]})


@app.route('/api/deposit/<api_key>', methods=["POST"])
def deposit(api_key):
    if not request.json or "amount" not in request.json:
        return jsonify({"error": "deposit requires json with 'amount' key"}), 400
    amount = request.json["amount"]
    user = User.api_authenticate(api_key)
    user.balance += amount
    user.save()
    return jsonify(user.json()), 201

@app.route('/api/buy/<api_key>', methods=["POST"])
def buy(api_key):
    """ buy a certain amount of a certain stock, amount & symbol provided in a json POST request """
    if not request.json or "ticker" not in request.json or 'amount' not in request.json:
        return jsonify({"error": "deposit requires json with 'ticker' and 'amount key"}), 400
    user= User.api_authenticate(api_key)
    if user is None:
        abort(404)
    user.buy(request.json['ticker'], request.json['amount'])
    return jsonify({"position": user.position_for_stock(request.json['ticker']).json()})


@app.route('/api/sell/<api_key>', methods=["POST"])
def sell(api_key):
    """ sell a certain amount of a certain stock, amount & symbol provided in a json POST request """
    if not request.json or "ticker" not in request.json or 'amount' not in request.json:
        return jsonify({"error": "deposit requires json with 'ticker' and 'amount key"}), 400
    user= User.api_authenticate(api_key)
    if user is None:
        abort(404)
    try:
        user.sell(request.json['ticker'], request.json['amount'])
    except InsufficientSharesError:
        return jsonify({"invalid": "amount"})
    if user.position_for_stock(request.json['ticker']) is None:
        return jsonify({"invalid": "amount"})
    return jsonify({"position": user.position_for_stock(request.json['ticker']).json()})

    

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)
