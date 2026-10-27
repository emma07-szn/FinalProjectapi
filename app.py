from flask_cors import CORS
from flask import*
import pymysql
import pymysql.cursors
import os


app=Flask(__name__)
CORS(app)

app.config['UPLOAD_FOLDER'] = "static/images"


# SIGNUP
@app.route('/api/signup',methods=['POST'])
def signup():

    username=request.form['username']
    email=request.form['email']
    password=request.form['password']
    phone=request.form['phone']

    Connection=pymysql.connect(user="root",password="",host="localhost",database="Finalproject")

    cursor=Connection.cursor()

    sql="INSERT INTO Users(username,email,password,phone)VALUE(%s,%s,%s,%s)"

    data=(email,password,username,phone)

    cursor.execute(sql,data)

    Connection.commit()

    return jsonify({"Success":"Thank you for Signin up"})


# SIGNIN
@app.route('/api/signin',methods=['POST'])
def signin():
    
    email=request.form['email']
    password=request.form['password']


    Connection=pymysql.connect(user="root",password="",host="localhost",database="Finalproject")

    cursor=Connection.cursor(pymysql.cursors.DictCursor)

    sql='SELECT * From Users WHERE email= %s AND password = %s'

    data = (email,password)

    cursor.execute(sql,data)

    count =cursor.rowcount

    if count == 0:
        return jsonify({
            "message" : "Login failed"
        })
    else:
        user = cursor.fetchone()

        return jsonify({
            "message" : "login success",
            "user" : user
        })


#DELETE USER
@app.route('/api/delete-user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
        # 1. Establish database connection
    connection = pymysql.connect( user="root",password="", host="localhost",database="Finalproject")
        
        # 2. Open a cursor to perform the operation
    cursor=connection.cursor()
            # 3. Define the SQL query using %s placeholders to prevent SQL injection
    sql = "DELETE FROM Users WHERE user_id = %s"
            
            # 4. Execute the query
    cursor.execute(sql, (user_id,))
            
            # 5. Check if a row was actually deleted
    if cursor.rowcount == 0:
                return jsonify({
                    "message": "User not found"
                }), 404  # 404 Not Found status code
            
            # 6. Commit the changes to the database
    connection.commit()
            
    return jsonify({
            "message": "User deleted successfully"
        }), 200  # 200 OK status code

   

#UPDATE USER
@app.route('/api/update-user/<int:user_id>', methods=['PUT'])
def update_user(user_id):

        # 1. Get the updated data from the request form (matching your sign-in style)
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Validation: Ensure at least one field is provided to update
        if not email and not password:
            return jsonify({"message": "No data provided to update"}), 400

        # 2. Establish database connection
        connection = pymysql.connect(user="root", password="", host="localhost", database="Finalproject")
        
        # 3. Open a cursor to perform the operation
        with connection.cursor() as cursor:
            # 4. Build dynamic SQL depending on what fields the user sent
            if email and password:
                sql = "UPDATE Users SET email = %s, password = %s WHERE user_id = %s"
                data = (email, password, user_id)
            elif email:
                sql = "UPDATE Users SET email = %s WHERE user_id = %s"
                data = (email, user_id)
            else:
                sql = "UPDATE Users SET password = %s WHERE user_id = %s"
                data = (password, user_id)
            
            # 5. Execute the update query
            cursor.execute(sql, data)
            
            # 6. Check if any row was actually modified
            if cursor.rowcount == 0:
                return jsonify({"message": "User not found or no changes made"}), 404
            
            # 7. Commit changes to the database
            connection.commit()
            
        return jsonify({"message": "User updated successfully"}), 200


# ADD PRODUCTS
@app.route('/api/add_product',methods=['POST'])
def add_product():

    if request.method == 'POST':

        product_name = request.form['product_name']
        product_description = request.form['product_description']
        product_cost = request.form['product_cost']

        photo = request.files['product_photo']
        
        filename = photo.filename

        photo_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        photo.save(photo_path)

        Connection = pymysql.connect(host="localhost" , user="root",password="",database="Finalproject")

        cursor = Connection.cursor()
        cursor.execute('INSERT INTO Product_details(product_name,product_description,product_cost,product_photo) VALUES(%s,%s,%s,%s)', (product_name,product_description,product_cost,filename))

        Connection.commit()

        return jsonify({
            "Success": "Product details added successfully"
        })


# GET PRODUCTS
@app.route("/api/get_products_details", methods = ["GET"])
def get_product_details():

    Connection = pymysql.connect(host="localhost", user="root",password="", database="Finalproject")

    cursor = Connection.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM Product_details")

    product_details =cursor.fetchall()

    Connection.close()

    return jsonify(product_details)


# MPESA
#    importing mpesa
    # Mpesa Payment Route 
import requests
import datetime
import base64
from requests.auth import HTTPBasicAuth

@app.route('/api/mpesa_payment', methods=['POST'])
def mpesa_payment():
    if request.method == 'POST':
        # Extract POST Values sent
        amount = request.form['amount']
        phone = request.form['phone']

        # Provide consumer_key and consumer_secret provided by safaricom
        consumer_key = "GTWADFxIpUfDoNikNGqq1C3023evM6UH"
        consumer_secret = "amFbAoUByPV2rM5A"

        # Authenticate Yourself using above credentials to Safaricom Services, and Bearer Token this is used by safaricom for security identification purposes - Your are given Access
        api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"  # AUTH URL
        # Provide your consumer_key and consumer_secret 
        response = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
        # Get response as Dictionary
        data = response.json()
        # Retrieve the Provide Token
        # Token allows you to proceed with the transaction
        access_token = "Bearer" + ' ' + data['access_token']

        #  GETTING THE PASSWORD
        timestamp = datetime.datetime.today().strftime('%Y%m%d%H%M%S')  # Current Time
        passkey = 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919'  # Passkey(Safaricom Provided)
        business_short_codflask-cose = "174379"  # Test Paybile (Safaricom Provided)
        # Combine above 3 Strings to get data variable
        data = business_short_code + passkey + timestamp
        # Encode to Base64
        encoded = base64.b64encode(data.encode())
        password = encoded.decode()

        # BODY OR PAYLOAD
        payload = {
            "BusinessShortCode": "174379",
            "Password":password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": "1",  # uflask-cosse 1 when testing
            "PartyA": phone,  # change to your number
            "PartyB": "174379",
            "PhoneNumber": phone,
            "CallBackURL": "https://coding.co.ke/api/confirm.php",
            "AccountReference": "SokoGarden Online",
            "TransactionDesc": "Payments for Products"
        }

        # POPULAING THE HTTP HEADER, PROVIDE THE TOKEN ISSUED EARLIER
        headers = {
            "Authorization": access_token,
            "Content-Type": "application/json"
        }

        # Specify STK Push  Trigger URL
        url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"  
        # Create a POST Request to above url, providing headers, payload 
        # Below triggers an STK Push to the phone number indicated in the payload and the amount.
        response = requests.post(url, json=payload, headers=headers)
        print(response.text) # 
        # Give a Response
        return jsonify({"message": "An MPESA Prompt has been sent to Your Phone, Please Check & Complete Payment"})



    






# if __name__=='__main__':
#     app.run(debug=True)
