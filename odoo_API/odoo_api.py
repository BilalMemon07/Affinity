import json
from logging import exception
from flask import Flask, Response, jsonify, request
import xmlrpc.client
import random
from datetime import timedelta, datetime
from flask_jwt_extended import JWTManager

from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
app = Flask(__name__)
jwt = JWTManager(app)
app.config['JWT_SECRET_KEY'] = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY3NzgzODIzMywianRpIjoiNTBhN2QxNzItNDg4My00YzFjLTk4OTYtNWIyZjc4ZTRmZTgwIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImJpbGFsIiwibmJmIjoxNjc3ODM4MjMzLCJleHAiOjE2Nzc4MzgyOTN9.ECM0f-1TJgdAFELYF_yn3hGMZ2tmIfT-PNKHVt-CPSw'  # Change this!
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1800)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=1800)

dbData = ["url", "db", "dbusername", "dbpassword"]
global models
# odoo Connection Start
# odoo Connection End

# get Data From Odoo
url_prefix = "/api/odoo/"

# global authToken
global login_data
global uid


# def authentication(auth):
#     headerToken = request.headers.get('token')
#     if (not headerToken):
#         return "Token In Header is Required"
#     for i in range(len(auth)):
#         print(auth[i])
#         if auth[i] == headerToken:
#             return True
#     return "Invalid Token"


# def getUsers():
#     db_url = request.args.get('db_url')
#     db_name = request.args.get('db_name')
#     req = request.get_json()
#     name = req['name']
#     password = req['password']
#     global models
#     global login_data
#     global uid
#     login_data = {dbData[2]: name, dbData[3]: password,
#                   dbData[0]: db_url, dbData[1]: db_name}
#     # odoo Connection
#     common = xmlrpc.client.ServerProxy(
#         '{}/xmlrpc/2/common'.format(login_data['url']))
#     common.version()
#     uid = common.authenticate(
#         login_data['db'], login_data['dbusername'], login_data['dbpassword'], {})
#     models = xmlrpc.client.ServerProxy(
#         '{}/xmlrpc/2/object'.format(login_data['url']))
#     if (not uid):
#         print("User Does Not Exist")
#         return "User Does Not Exist"

#     return "User Login Successfully"



tokenList = []
@app.route('/', methods=['GET'])
def get():
    return "Hello"

# @app.route(url_prefix + 'login', methods=['POST'])
# def login():
#     try:
#         lower = 'qwertyuioplkjhgfdsazxcvbnmQWERTYUIOPLKJHGFDSAZXCVBNM'
#         upper = 'QWERTYUIOPLKJHGFDSAZXCVBNMqwertyuioplkjhgfdsazxcvbnm'
#         number = '0123456789'
#         symbol = '!@#$%^&*?'
#         all = lower+upper+number+symbol
#         length = 100
#         token = "".join(random.sample(all, length))
#         resUid = getUsers()
#         if not uid:
#             print("invalid credentials")
#             message = {
#                 "Message" : "invalid credentials /" + " " + str(resUid),
#             }
#             return Response(json.dumps(message), status=404, mimetype='application/json')
#             # return Response("invalid credentials /" + " " + str(resUid), status=404, mimetype='application/json')

#         global authToken
#         tokenList.append(token)
#         authToken = tokenList
#         # print(authToken)
#         return {'token': token, 'message': resUid}
#     except Exception as ex:
#         print("Some Thing want wrong", ex)
#         return Response('Sorry, something went wrong!' + str(ex), status=400, mimetype='application/json')

@app.route(url_prefix+'login', methods=['POST'])
def login():
    # username = request.json.get('username', None)
    # password = request.json.get('password', None)
    
    db_url = request.args.get('db_url')
    db_name = request.args.get('db_name')
    req = request.get_json()
    name = req['name']
    password = req['password']
    global models
    global login_data
    global uid
    login_data = {
            "dbusername": name,
            "dbpassword": password,
            "url": db_url,
            "db": db_name
        }
    
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

    
    access_token = create_access_token(identity= login_data)
    refresh_token = create_refresh_token(identity= login_data)
    response = jsonify({'access_token': access_token, 'refresh_token': refresh_token})
    return response



@app.route(url_prefix + 'createCustomer', methods=['POST'])
@jwt_required()
def createCustomer():
    record = json.loads(request.data)
    product_type = request.args.get('product_type')
    try:
        current_user = get_jwt_identity()
        
        customer_search = models.execute_kw(current_user['db'], uid, current_user['dbpassword'], 'res.partner', 'search', [
            [['phone', '=', record['phone']]]])
        if customer_search:
            return Response('User Already Exist, You Can not add This User 2nd Time', status=400, mimetype='application/json')
        if product_type == "BROKER_LENDING":
            id = models.execute_kw(current_user['db'], uid, current_user['dbpassword'], 'res.partner', 'create', [{
                "name":record['name'],
                "gender":record['gender'],
                "phone": record['phone'],
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
                "product_type":"1"
            }])
        else:
            id = models.execute_kw(current_user['db'], uid, current_user['dbpassword'], 'res.partner', 'create', [{
                "name":record['name'],
                "phone": record['phone'],
                "cnic_number":record['cnic_number'],
                "cnic_expiry_date":record['cnic_expiry_date'],
                "permanent_address":record['permanent_address'],
                "region": record['region'],
                # "city":record['city'],
                # "province":record['province'],
                "company_name":record['company_name'],
                "product_type":"2",
                'state': record['record']
            }])
        print(id)
        res_message = {
                "Message" : "Record created successfully!",
                "id" : id
            }
        return Response(json.dumps(res_message), status=201, mimetype='application/json')
        # return Response('Record created successfully! ', status=201, mimetype='application/json')
        
    except Exception as ex:
        print(ex)
        return Response('Sorry, something went wrong!' + str(ex), status=400, mimetype='application/json')




@app.route(url_prefix + 'getCustomer/<id>', methods=['GET'])
@jwt_required()
def getCustomerbyID(id):
    try:
        _id = int(id)
        current_user = get_jwt_identity()
        if not _id:
            return Response('Record Number Must be Required in Url ', status=404, mimetype='application/json')
        data = models.execute_kw(current_user['db'], uid, current_user['dbpassword'], 'res.partner', 'search_read', [
                                    [['id', '=', _id]]])
        return jsonify(data)
    except Exception as ex:
        print('Sorry, something went wrong!' , str(ex))
        return Response('Sorry, something went wrong!' + ' ' + str(ex), status=400, mimetype='application/json')



#  db_url = request.args.get('db_url')
#     db_name = request.args.get('db_name')

@app.route(url_prefix + 'searchLead', methods=['GET'])
@jwt_required()
def getLeadbysearch():
    try:
        current_user = get_jwt_identity()
        customer =  models.execute_kw(current_user['db'], uid, current_user['dbpassword'], 'res.partner', 'search', [[]])

        product_list = ['1','2','3']
        status_list =  ['pending','approve','reject']
        product_type = False
        customer_id = False
        status = False
        to_date = str(datetime(2000, 1, 1))
        # from_date = str(datetime.datetime.now()).split(" ")[0]
        customer_id = request.args.get('customer_id')
        if customer_id:
            customer =  [int(customer_id)]
        product_type = request.args.get('product_type')
        if product_type == 'BROKER_LENDING':
            product_list = ['1']
        elif product_type == 'DRIVE_THROUGH_LENDING':
            product_list = ['2']
        elif product_type == 'INVOICE_DISCOUNTING':
            product_list = ['3']
        status = request.args.get('status')
        if status:
            status_list = [status]
        requested_date = False
        requested_date = request.args.get('requestedDate')
        if requested_date:
            to_date = requested_date

        # status = request.args.get('status')
        _product_type = product_list
        _customer_id = customer
        _status = status_list
        _requested_date_to = to_date
        print(_requested_date_to)
        
        count = 0
        print(_customer_id)
        list_data = []
        invoice_list = []
        # for abc in _product_type:
        # data = models.execute_kw(current_user['db'], uid, current_user['dbpassword'], 'crm.lead', 'search_read', [[['partner_id','in',_customer_id],['product_type','in',_product_type],['state','in',_status],['create_date','>=', _requested_date_to]]],{'fields': ['create_date','product_type','state','requested_amount','amount']})
        record_id = models.execute_kw(current_user['db'], uid, current_user['dbpassword'], 'crm.lead', 'search', [[['partner_id','in',_customer_id],['product_type','in',_product_type],['state','in',_status],['create_date','>=', _requested_date_to]]])
        for rec in record_id:
            record = models.execute_kw(current_user['db'], uid, current_user['dbpassword'], 'crm.lead', 'read', [rec],{'fields': ['id', 'amount', 'display_name', 'state','invoice_state','disbursement_state','requested_amount','product_type','facility_request_date','instrument_due_date','create_date','name','partner_id','partner_name','stage_id','won_status','invoice_id','phone']})
            for reco in record:
                if reco['invoice_id']:
                    invoice_rec = models.execute_kw(current_user['db'], uid, current_user['dbpassword'], 'account.move', 'search_read', [[['id','=', reco['invoice_id'][0]]]],{'fields': ['id', 'payment_state', 'crm_id']})
                    for inv in invoice_rec:
                        if reco['id'] == inv['crm_id'][0]:
                            print('bilal Testing Here') 
                            # invoice_list.append(inv)
                            reco['invoice_data'] =inv

            list_data.append(record)
        print(list_data)
        return jsonify(list_data)
        # {'fields': ['create_date','product_type','state','requested_amount','amount']}
    except Exception as ex:
        print('Sorry, something went wrong!')
        return Response('Sorry, something went wrong!' + ' ' + str(ex), status=400, mimetype='application/json')
# payment_state
# ['facility_request_date','>=', _requested_date_to],['instrument_due_date','<=', __due_date_from]


@app.route(url_prefix + 'getLeads/<id>', methods=['GET'])
@jwt_required()
def getLeadbyProductType(id):
    try:
        _id = int(id)
        current_user = get_jwt_identity()
        if not _id:
            return Response('Record Number Must be Required in Url ', status=404, mimetype='application/json')
       
        data = models.execute_kw(current_user['db'], uid, current_user['dbpassword'], 'crm.lead', 'search_read', [
                                    [['id', '=', _id]]])
        return jsonify(data)
        
    except Exception as ex:
        print('Sorry, something went wrong!')
        return Response('Sorry, something went wrong!' + ' ' + str(ex), status=400, mimetype='application/json')



@app.route(url_prefix + 'updateCustomer/<id>', methods=['POST'])
@jwt_required()
def updateCustomer(id):
    record = json.loads(request.data)
    try:
        customer_id = int(id)
        current_user = get_jwt_identity()
        
        orderId = models.execute_kw(current_user['db'], uid, current_user['dbpassword'], 'res.partner', 'search', [
            [['id', '=', customer_id]]])
        if not orderId:
            return Response('Please Enter Correct Order Number!', status=400, mimetype='application/json')
        data = models.execute_kw(current_user['db'], uid, current_user['dbpassword'], 'res.partner', 'write', [[customer_id],record])
        if not data:
            res_message = {
                "Message" : "Please Enter Correct Order Number!",
            }
            return Response(json.dumps(res_message), status=404, mimetype='application/json')
            # return Response('Please Enter Correct Order Number!', status=400, mimetype='application/json')
        message = {
            "Message" : "Record Update successfully!",
            "id":data
        }
        return Response(json.dumps(message), status=201, mimetype='application/json')
       
       
    except Exception as ex:
        print('Sorry, something went wrong!')
        return Response('Sorry, something went wrong!' + ' ' + str(ex), status=400, mimetype='application/json')


@app.route(url_prefix + 'createProduct', methods=['POST'])
@jwt_required()
def CreateCRM_product():
    product_type = request.args.get('product_type')
    record = json.loads(request.data)
    try:
        current_user = get_jwt_identity()
       
        if product_type == "BROKER_LENDING":
            id = models.execute_kw(current_user['db'], uid, current_user['dbpassword'], 'crm.lead', 'create', [{
                "name":record['name'],
                "partner_id" : record['partner_id'],
                "product_type":"1",
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
            return Response(json.dumps(res_message), status=201, mimetype='application/json')
        elif product_type == "DRIVE_THROUGH_LENDING":
            id = models.execute_kw(current_user['db'], uid, current_user['dbpassword'], 'crm.lead', 'create', [{
                "name":record['name'],
                "partner_id" : record['partner_id'],
                "product_type":"2",
                "requested_amount":record['requested_amount'],
                "instrument_number":record['instrument_number'],
                "facility_request_date":record['facility_request_date'],
                "instrument_due_date":record['instrument_due_date'],
                "attachment" : record['attachment'],
            }])
            res_message = {
                'Message' : 'Product Created Successfully',
                'id' : 'Prodcut Created Id is' + ' ' + str(id)
            }
            return Response(json.dumps(res_message), status=201, mimetype='application/json')
        elif product_type == "INVOICE_DISCOUNTING":
            id = models.execute_kw(current_user['db'], uid, current_user['dbpassword'], 'crm.lead', 'create', [{
                "name":record['name'],
                "partner_id" : record['partner_id'],
                "product_type":"3",
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
            return Response(json.dumps(res_message), status=201, mimetype='application/json')
        else:
            message ={
                "Message" : "This Product Is Not Exist",
            }
            return Response(json.dumps(message), status=404, mimetype='application/json')
        
    except Exception as ex:
        print('Sorry, something went wrong!')
        return Response('Sorry, something went wrong!' + ' ' + str(ex), status=400, mimetype='application/json')


@app.route(url_prefix + 'updateProduct/<id>', methods=['POST'])
@jwt_required()
def updateProduct(id):
    record = json.loads(request.data)
    try:
        product_id = int(id)
        current_user = get_jwt_identity()
        orderId = models.execute_kw(current_user['db'], uid, current_user['dbpassword'], 'crm.lead', 'search', [
            [['id', '=', product_id]]])
        if not orderId:
            return Response('Please Enter Correct Order Number!', status=400, mimetype='application/json')
        data = models.execute_kw(current_user['db'], uid, current_user['dbpassword'], 'crm.lead', 'write', [[product_id],record])
        if not data:
            return Response('Please Enter Correct Order Number!', status=400, mimetype='application/json')
        return Response('Record Update successfully!', status=201, mimetype='application/json')
        
    except Exception as ex:
        print('Sorry, something went wrong!')
        return Response('Sorry, something went wrong!' + ' ' + str(ex), status=400, mimetype='application/json')

@app.route(url_prefix + 'searchCustomer', methods=['POST'])
@jwt_required()
def SearchCutomer():
    record = json.loads(request.data)
    try:
        current_user = get_jwt_identity()
        cusId = models.execute_kw(current_user['db'], uid, current_user['dbpassword'], 'res.partner', 'search_read', [
                                    [['phone', '=', record['phone']]]])
        # cusId = models.execute_kw(current_user['db'], uid, current_user['dbpassword'], 'res.partner', 'search', [
        #         [["phone",' =' ,record['phone']]]])
        res_message ={}
        if cusId:
            res_message = {
                "Message" : "Customer Is Already Exits",
                "id" : "Customer Name is" + " " + str(cusId[0]['name'])
            }
            return Response(json.dumps(res_message), status=201, mimetype='application/json')
        else:
            res_message = {
                "Message" : "Customer is Not Exits",
                # "id" : "Customer Name is" + " " + str(res_message.name)
            }
            return Response(json.dumps(res_message), status=404, mimetype='application/json')
       

    except Exception as ex:
        print('Sorry, something went wrong!')
        return Response('Sorry, something went wrong!' + ' ' + str(ex), status=400, mimetype='application/json')



if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host="0.0.0.0", port="5000")
    # from waitress import serve
    # serve(app,host='0.0.0.0',port=5000)