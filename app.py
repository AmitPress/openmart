from flask import Flask, request, render_template, redirect, session
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson import ObjectId
from flask_cors import CORS
#### DATABASE ####
# client = MongoClient('localhost', 27017)
# db = client['openmart']

uri = "mongodb+srv://amit2000:amit2000@cluster0.rjrwa3v.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client['openmart']

profiles    = db['profiles'] # collection
products    = db['products'] # collection
carts       = db['carts'] # collection
mailbox     = db['mailbox'] # collection


#### APP ####
app = Flask(__name__, static_url_path='/static')
app.secret_key = "amit"
CORS(app)
#### ROUTES ####
@app.route('/', methods=["GET"])
def index():
    if("logged_in" in session and session["logged_in"] == True):
        return redirect("/buyerprofile")
    else:
        return render_template("login.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        if("logged_in" in session and session["logged_in"] == True):
            return redirect("/buyerprofile")
        else:
            return render_template("login.html")
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["pass"]
        profile = profiles.find_one({"email": email})
        if profile and profile["password"] == password:
            session["profile_id"] = str(profile["_id"])
            session["logged_in"] = True
            return redirect("/buyerprofile")
        else:
            message = "Incorrect email or password"
            return render_template("login.html", **locals())


@app.route("/logout", methods=["GET"])
def logout():
    session.clear()
    return redirect("/login")
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "GET":
        if "logged_in" in session and session["logged_in"] == True:
            return redirect("/buyerprofile")
        else:
            return render_template("signup.html")
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        if profiles.find_one({"email": email}):
            return render_template("signup.html", message="Email already exists")
        password = request.form["pass"]
        profile = profiles.insert_one({"username": username, "email": email, "password": password})
        cart = carts.insert_one({"profile": profile.inserted_id})
        mail = mailbox.insert_one({"profile": profile.inserted_id})
        return redirect("/login")

@app.route('/buyerprofile', methods=["GET"])
def buyer():
    if request.method == "GET":
        if "logged_in" in session and session["logged_in"] == True:
            buyer = profiles.find_one({"_id": ObjectId(session["profile_id"])})
            cart = carts.find_one({'profile': ObjectId(session['profile_id'])})
            if cart:
                items = cart.get('products')
                if items:
                    total = len(items)
                    count = {id: items.count(id) for id in set(items)}
                    real_products = []
                    for id in set(items):
                        real_products.append((products.find_one({"_id": ObjectId(id)}), count[id]))
            return render_template('buyerprofile.html', **locals())
        else:
            return redirect('/login')

@app.route('/sellerprofile', methods=["GET", "POST"])
def seller():
    if request.method == "GET":
        if "logged_in" in session and session["logged_in"] == True:
            profile = profiles.find_one({"_id": ObjectId(session['profile_id'])})
            all_products = products.find({'vendor_id': session['profile_id']})
            return render_template('sellerprofile.html', **locals())
        else:
            return redirect('/login')
    if request.method == "POST":
        profile = profiles.find_one({"_id": ObjectId(session['profile_id'])})
        pname = request.form['pname']
        ptype = request.form['ptype']
        qty   = request.form['qty']
        price = request.form['price']
        vendor = profile['username']
        vendor_id = session['profile_id']
        products.insert_one({'pname':pname, 'ptype': ptype, 'qty': qty, 'price': price, 'vendor': vendor, 'vendor_id': vendor_id})
        return redirect('/sellerprofile')

    

@app.route('/marketplace', methods=["GET"])
def marketplace():
    if request.method == "GET":
        if("logged_in" in session and session["logged_in"] == True):
            all_products = products.find()
            return render_template('marketplace.html', **locals())
        else:
            return redirect('/login')

# @app.route('/add_product/<string:product_id>', methods=["GET"])
# def add_product(product_id):
#     cart = carts.find_one({'profile': ObjectId(session['profile_id'])})
#     if 'products' in cart:
#         p = cart['products']
#         p.append(product_id)
#         carts.update_one({'profile': ObjectId(session['profile_id'])}, {'products':p})
#     else:
#         p = []
#         p.append(product_id)
#         carts.insert_one({'profile': ObjectId(session['profile_id']), 'products':p})
#     return redirect('/marketplace')

@app.route('/add_product/<string:product_id>', methods=["GET"])
def add_product(product_id):
    cart = carts.find_one({'profile': ObjectId(session['profile_id'])})
    if cart:
        p = cart.get('products', [])
        p.append(product_id)
        carts.update_one({'_id': cart['_id']}, {'$set': {'products': p}})
    else:
        p = [product_id]
        carts.insert_one({'profile': ObjectId(session['profile_id']), 'products': p})
    return redirect('/marketplace')

@app.route('/remove_product/<string:product_id>', methods=["GET"])
def remove_product(product_id):
    cart = carts.find_one({'profile': ObjectId(session['profile_id'])})
    if cart:
        p = cart.get('products')
        p.remove(product_id)
        carts.update_one({'_id': cart['_id']}, {'$set': {'products': p}})
    return redirect('/buyerprofile')
if __name__=="__main__":
    # from waitress import serve
    # serve(app, host="0.0.0.0", port=8080)
    app.run()