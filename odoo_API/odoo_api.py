import json
from logging import exception
from flask import Flask, Response, jsonify, request
import xmlrpc.client
import random


dbData = ["url", "db", "dbusername", "dbpassword"]
global models
# odoo Connection Start
# odoo Connection End

app = Flask(__name__)
# get Data From Odoo
url_prefix = "/api/odoo/"

global authToken
global login_data
global uid


def authentication(auth):
    headerToken = request.headers.get('token')
    if (not headerToken):
        return "Token In Header is Required"
    for i in range(len(auth)):
        print(auth[i])
        if auth[i] == headerToken:
            return True
    return "Invalid Token"


def getUsers():
    db_url = request.args.get('db_url')
    db_name = request.args.get('db_name')
    req = request.get_json()
    name = req['name']
    password = req['password']
    global models
    global login_data
    global uid
    login_data = {dbData[2]: name, dbData[3]: password,
                  dbData[0]: db_url, dbData[1]: db_name}
    # odoo Connection
    common = xmlrpc.client.ServerProxy(
        '{}/xmlrpc/2/common'.format(login_data['url']))
    common.version()
    uid = common.authenticate(
        login_data['db'], login_data['dbusername'], login_data['dbpassword'], {})
    models = xmlrpc.client.ServerProxy(
        '{}/xmlrpc/2/object'.format(login_data['url']))
    if (not uid):
        print("User Does Not Exist")
        return "User Does Not Exist"

    return "User Login Successfully"



tokenList = []
@app.route('/', methods=['GET'])
def get():
    return "Hello"

@app.route(url_prefix + 'login', methods=['POST'])
def login():
    try:
        lower = 'qwertyuioplkjhgfdsazxcvbnmQWERTYUIOPLKJHGFDSAZXCVBNM'
        upper = 'QWERTYUIOPLKJHGFDSAZXCVBNMqwertyuioplkjhgfdsazxcvbnm'
        number = '0123456789'
        symbol = '!@#$%^&*?'
        all = lower+upper+number+symbol
        length = 100
        token = "".join(random.sample(all, length))
        resUid = getUsers()
        if not uid:
            print("invalid credentials")
            return Response("invalid credentials /" + " " + str(resUid), status=404, mimetype='application/json')

        global authToken
        tokenList.append(token)
        authToken = tokenList
        # print(authToken)
        return {'token': token, 'message': resUid}
    except Exception as ex:
        print("Some Thing want wrong", ex)
        return Response('Sorry, something went wrong!' + str(ex), status=400, mimetype='application/json')



@app.route(url_prefix + 'createCustomer', methods=['POST'])
def createSaleOrder():
    record = json.loads(request.data)
    try:
        global authToken
        res = authentication(authToken)
        if res == True:
            
            id = models.execute_kw(login_data['db'], uid, login_data['dbpassword'], 'res.partner', 'create', [{
                "customer_name":record['customer_name'],
                "name":record['customer_name'],
                "gender":record['gender'],
                "cnic_number":record['cnic_number'],
                "father_name":record['father_name'],
                "cnic_expiry_date":record['cnic_expiry_date'],
                "date_of_birth":record['date_of_birth'],
                "birth_place":record['birth_place'],
                "mailing_address":record['mailing_address'],
                "permanent_address":record['permanent_address'],
                "city":record['city'],
                "province":record['province'],
                "nature_of_business":record['nature_of_business'],
                "requestor_income":record['requestor_income'],
                "no_of_years":record['no_of_years'],
                "company_name":record['company_name'],
                "company_address":record['company_address'],
                "cnic_front":record['cnic_front'],
                "cnic_back":record['cnic_back'],
                "security_cheque":record['security_cheque'],
                "customer_image":record['customer_image'],
            }])
            print(id)
            return Response('Record created successfully! ', status=201, mimetype='application/json')
        else:
            return Response(res, status=400, mimetype='application/json')

    except NameError as ex:
        print(ex)
        return Response('Sorry, something went wrong!' + str(ex), status=400, mimetype='application/json')



@app.route(url_prefix + 'updateCustomer/<id>', methods=['POST'])
def updatesalesorder(id):
    record = json.loads(request.data)
    try:
        customer_id = int(id)
        global authToken
        res = authentication(authToken)
        if res == True:
            orderId = models.execute_kw(login_data['db'], uid, login_data['dbpassword'], 'res.partner', 'search', [
                [['id', '=', customer_id]]])
            if not orderId:
                return Response('Please Enter Correct Order Number!', status=400, mimetype='application/json')
            data = models.execute_kw(login_data['db'], uid, login_data['dbpassword'], 'res.partner', 'write', [[customer_id],record])
            if not data:
                return Response('Please Enter Correct Order Number!', status=400, mimetype='application/json')
            return Response('Record Update successfully!', status=201, mimetype='application/json')
        else:
            print("hello False")
            return Response(res, status=400, mimetype='application/json')
    except Exception as ex:
        print('Sorry, something went wrong!')
        return Response('Sorry, something went wrong!' + ' ' + str(ex), status=400, mimetype='application/json')


@app.route(url_prefix + 'createProduct', methods=['POST'])
def CreateCRM_product():
    product_type = request.args.get('product_type')
    record = json.loads(request.data)
    try:
        global authToken
        res = authentication(authToken)
        if res == True:
            if product_type == "1":
                id = models.execute_kw(login_data['db'], uid, login_data['dbpassword'], 'crm.lead', 'create', [{
                    "name":record['name'],
                    "partner_id" : record['partner_id'],
                    "product_type":product_type,
                    "limit_request":record['limit_request'],
                    "requested_amount":record['requested_amount'],
                    "instrument_number":record['instrument_number'],
                    "facility_request_date":record['facility_request_date'],
                    "instrument_due_date":record['instrument_due_date'],
                    "attachment" : record['attachment'],
                }])
                res_message ={
                    "Message" : "Product Created Successfully",
                    "id" : "Prodcut Created Id is" + " " + str(id)
                }
                return res_message
            elif product_type == "2":
                id = models.execute_kw(login_data['db'], uid, login_data['dbpassword'], 'crm.lead', 'create', [{
                    "name":record['name'],
                    "partner_id" : record['partner_id'],
                    "product_type":product_type,
                    "requested_amount":record['requested_amount'],
                    "instrument_number":record['instrument_number'],
                    "facility_request_date":record['facility_request_date'],
                    "instrument_due_date":record['instrument_due_date'],
                    "attachment" : record['attachment'],
                }])
                res_message ={
                    "Message" : "Product Created Successfully",
                    "id" : "Prodcut Created Id is" + " " + str(id)
                }
                return res_message
            elif product_type == "3":
                id = models.execute_kw(login_data['db'], uid, login_data['dbpassword'], 'crm.lead', 'create', [{
                    "name":record['name'],
                    "partner_id" : record['partner_id'],
                    "product_type":product_type,
                    "facility_request_date":record['facility_request_date'],
                    "instrument_due_date": record['instrument_due_date'],
                    "select_party": record['select_party'],
                    "invoice_amount":record['invoice_amount'],
                    "tag_trip":record['tag_trip'],
                    "invoice_type":record['invoice_type'],
                    "description":record['description'],
                    "invoice_attachment":record['invoice_attachment']
                }])
                res_message ={
                    "Message" : "Product Created Successfully",
                    "id" : "Prodcut Created Id is" + " " + str(id)
                }
                return res_message
            else:
                return "Prduct type is not Exist"
    
    except Exception as ex:
        print('Sorry, something went wrong!')
        return Response('Sorry, something went wrong!' + ' ' + str(ex), status=400, mimetype='application/json')


@app.route(url_prefix + 'updateProduct/<id>', methods=['POST'])
def updateProduct(id):
    record = json.loads(request.data)
    try:
        product_id = int(id)
        global authToken
        res = authentication(authToken)
        if res == True:
            orderId = models.execute_kw(login_data['db'], uid, login_data['dbpassword'], 'crm.lead', 'search', [
                [['id', '=', product_id]]])
            if not orderId:
                return Response('Please Enter Correct Order Number!', status=400, mimetype='application/json')
            data = models.execute_kw(login_data['db'], uid, login_data['dbpassword'], 'crm.lead', 'write', [[product_id],record])
            if not data:
                return Response('Please Enter Correct Order Number!', status=400, mimetype='application/json')
            return Response('Record Update successfully!', status=201, mimetype='application/json')
        else:
            print("hello False")
            return Response(res, status=400, mimetype='application/json')
    except Exception as ex:
        print('Sorry, something went wrong!')
        return Response('Sorry, something went wrong!' + ' ' + str(ex), status=400, mimetype='application/json')



if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host="0.0.0.0", port="5000")
    # from waitress import serve
    # serve(app,host='0.0.0.0',port=5000)




# "gender":"male",
# "mobile":false,
# "cnic_number":"e1231eqweqwe",
# "father_name":"AKkkss",
# "cnic_expiry_date":false,
# "date_of_birth":false,
# "birth_place":"karachi",
# "mailing_address":"hello",
# "permanent_address":"dadasd",
# "city":"adadad",
# "province":"dasdasd",
# "nature_of_business":"dadasdasd",
# "requestor_income":false,
# "no_of_years":false,
# "company_name":"asd",
# "company_address":"dasda",
# "cnic_front":false,
# "cnic_back":false,
# "security_cheque":false,
# "customer_image":false