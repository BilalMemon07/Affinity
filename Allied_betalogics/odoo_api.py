import json
from logging import exception
import random
from datetime import timedelta ,datetime
from flask import Flask, Response, jsonify, request
from flask_jwt_extended import JWTManager
import xmlrpc.client
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY3NzgzODIzMywianRpIjoiNTBhN2QxNzItNDg4My00YzFjLTk4OTYtNWIyZjc4ZTRmZTgwIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6ImJpbGFsIiwibmJmIjoxNjc3ODM4MjMzLCJleHAiOjE2Nzc4MzgyOTN9.ECM0f-1TJgdAFELYF_yn3hGMZ2tmIfT-PNKHVt-CPSw'  # Change this!
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1800)
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=1800)
jwt = JWTManager(app)



dbData = ["url", "db", "dbusername", "dbpassword"]
global models
# odoo Connection Start
# odoo Connection End

# get Data From Odoo

global authToken
global login_data
global uid


@app.route('/', methods=['GET'])
def get():
    return "Hello"

@app.route('/login', methods=['POST'])
def login():
    
    db_url = "http://localhost:8069"
    db_name = "AES_Live"
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

@app.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)
    response = jsonify({'access_token': access_token})
    return response




@app.route('/createsalesorder', methods=['POST'])
@jwt_required()
def createSaleOrder():
    record = json.loads(request.data)
    # return request.data
    try:
        current_user = get_jwt_identity()
        sales_order_line = []
        #print(str(record))
        if record['customer']:
            state = models.execute_kw(current_user['db'], uid, current_user['dbpassword'], 'res.country.state', 'search_read', [
                                            [['name', '=', record['dropOff']['address']['state']]]])
            country = models.execute_kw(current_user['db'], uid, current_user['dbpassword'], 'res.country', 'search_read', [
                                            [['name', '=', record['dropOff']['address']['country']]]])
            customer = models.execute_kw(current_user['db'], uid, current_user['dbpassword'], 'res.partner', 'create', [{
                "name": str(record['customer']['firstName'])+ ' ' + str(record['customer']['lastName']),
                "phone" :record['customer']['phoneNumber'],               
                "email" :record['customer']['email'],               
                "street" :record['dropOff']['address']['unit'],
                "street2" :record['dropOff']['address']['street'],
                "city" : record['dropOff']['address']['city'],
                "state_id" : state[0]['id'],
                "zip": record['dropOff']['address']['zip'],
                "country_id": country[0]['id']            
            }])
            payment_type = ""
            if record['paymentType'] == 'Cash' or record['paymentType'] == 'Swipe Card':
                payment_type = "COD"
            elif record['paymentType'] == 'Credit Card':
                payment_type = "Prepaid"

            if customer:
                id = models.execute_kw(current_user['db'], uid, current_user['dbpassword'], 'sale.order', 'create', [{
                    # 'sale_order_type':record['sale_order_type'],
                    # 'sale_order_sub_type':record['sale_order_sub_type'],
                    'partner_id': customer,
                    'partner_invoice_id': customer,
                    'partner_shipping_id': customer,
                    'x_studio_platform_1':101138,
                    "sale_order_type":"fulfillment",
                    "sale_order_sub_type":"candyland",
                    # 'warehouse_id': warehouse_data[0]['id'],
                    # 'x_studio_street':record['x_studio_street'],
                    'candyland_order_number': record['orderId'],
                    'x_studio_shipping_amount': record['total']['deliveryCharges'],
                    # 'x_studio_city':record['x_studio_city'],
                    # 'x_studio_phone_no':record['x_studio_phone_no'],
                    'x_studio_payment_mode':payment_type,
                    'picking_policy': 'direct',
                    # 'amount_tax' :record['total']['tax'],
                    'discount_rate' :record['total']['discountedAmount'],
                    'x_studio_assigned_courier':33,
                    'x_delivery_address_fu': record['customer']['address'],
                    'latitude' : record['dropOff']['address']['latitude'],
                    'longitude' : record['dropOff']['address']['longitude']
                    
                }])
                if id:
                    if float(record['total']['deliveryCharges']) > 0:
                        sales_order_line.append((0,0,{
                            "product_id": 9497,
                            'price_unit': record['total']['deliveryCharges'],
                            'product_uom_qty': 1,

                        }))
                    for rec in record['items']:
                        tax = float(record['total']['tax']) / len(record['items'])
                        discount = float(record['total']['discountedAmount']) / len(record['items'])
                        
                        
                        data = models.execute_kw(current_user['db'], uid, current_user['dbpassword'], 'product.product', 'search_read', [
                                            [['x_studio_supplier_sku_code', '=', rec['sku']]]])
                    
                        if data:
                            sales_order_line.append((0, 0, {
                                'product_id': data[0]['id'],
                                'price_unit': float(rec['price']),
                                'product_uom_qty': rec['qty'],
                                'x_studio_tax_amount_tp': tax,
                                'x_studio_total_discount_amount':discount
                                # 'tax_id': [(4, 63)] 

                            }))
                    models.execute_kw(current_user['db'], uid, current_user['dbpassword'], 'sale.order', 'write', [
                        [id], {"order_line": sales_order_line}])
                    
                    order_data = models.execute_kw(current_user['db'], uid, current_user['dbpassword'], 'sale.order', 'search_read', [
                                            [['id', '=', id]]])

                    res_message ={
                        "Message" : "Sale Order Created Successfully",
                        "id" : id,
                        "orderNumber":order_data[0]['name']
                    }       
                    print(res_message)
                    return Response(json.dumps(res_message), status=201, mimetype='application/json')
    
    except Exception as ex:
        err_msg ={
            "Message" : str(ex),
            "status" : 404
        }
        return Response(json.dumps(err_msg), status=404, mimetype='application/json')
# def createSaleOrder():
#     record = json.loads(request.data)
#     # return request.data
#     try:
#         current_user = get_jwt_identity()
#         sales_order_line = []
#         shipping_policy = False
#         if record['shipping_policy'] ==  "When all Products are ready":
#             shipping_policy  = 'one'
#         elif record['shipping_policy'] ==  "As soon as possible":
#             shipping_policy  = 'direct'
        
#         customer_id = models.execute_kw(current_user['db'], uid, current_user['dbpassword'], 'res.partner', 'create', [{
#             "name": record['customer']
#         }])
#         # courier_data = models.execute_kw(current_user['db'], uid, current_user['dbpassword'], 'courier_model', 'search_read', [
#         #                             [['name', '=', record['x_studio_assigned_courier']]]])
#         warehouse_data = models.execute_kw(current_user['db'], uid, current_user['dbpassword'], 'stock.warehouse', 'search_read', [
#                                     [['name', '=', record['warehouse_id']]]])
#         # check_order_number = models.execute_kw(current_user['db'], uid, current_user['dbpassword'], 'sale.order', 'search_read', [
#         #                         [['shopify_order_number', '=', record['shopify_order_number']]]])
#         # shopify_numbers_list =[]
#         # for check in  check_order_number:
#         #     shopify_numbers_list.append(check['shopify_order_number'])
#         #     print(check['shopify_order_number'])

        
#         # if record['shopify_order_number'] not in shopify_numbers_list:                                         
#         id = models.execute_kw(current_user['db'], uid, current_user['dbpassword'], 'sale.order', 'create', [{
#                 'sale_order_type':record['sale_order_type'],
#                 'sale_order_sub_type':record['sale_order_sub_type'],
#                 'partner_id': customer_id,
#                 'x_studio_platform_1':25475,
#                 'warehouse_id': warehouse_data[0]['id'],
#                 'x_studio_street':record['x_studio_street'],
#                 'x_studio_shipping_amount': record['x_studio_shipping_amount'],
#                 'x_studio_city':record['x_studio_city'],
#                 'x_studio_phone_no':record['x_studio_phone_no'],
#                 'x_studio_payment_mode':record['x_studio_payment_mode'],
#                 'picking_policy': shipping_policy,
#                 'x_studio_delivery_method': record['x_studio_delivery_method'],
#             }])
#         if id:
#             for rec in record['order_line']:

#                 data = models.execute_kw(current_user['db'], uid, current_user['dbpassword'], 'product.product', 'search_read', [
#                                     [['default_code', '=', rec['product_id']]]])
            
#                 if data:
#                     sales_order_line.append((0, 0, {
#                         'product_id': data[0]['id'],
#                         'price_unit': rec['price_unit'],
#                         'product_uom_qty': rec['product_uom_qty'],
#                     }))
#             models.execute_kw(current_user['db'], uid, current_user['dbpassword'], 'sale.order', 'write', [
#                 [id], {"order_line": sales_order_line}])
            
#             # shopify_order = models.execute_kw(current_user['db'], uid, current_user['dbpassword'], 'sale.order', 'search_read', [
#             #                         [['id', '=', id]]],{'fields': ['name', 'shopify_order_number']})
#             res_message ={
#                 "Message" : "Sale Order Created Successfully",
#                 "id" : id,
#                 # "Shopify_Order_number": record['shopify_order_number']
#             }       
#             print(res_message)
#             # return 'Record created successfully! '+'Record Created ID is '+  id
#             return Response(json.dumps(res_message), status=201, mimetype='application/json')
#         # else:
#         #     res_message ={
#         #         "Message" : "Order Number must be unique",
#         #     }       
#         #     # return 'Record created successfully! '+'Record Created ID is '+  id
#         #     return Response(json.dumps(res_message), status=400, mimetype='application/json')
#             # else:
#             #     res_message ={
#             #             "Message" : "shopify Order Number is duplicated",
#             #         }       
#             #         # return 'Record created successfully! '+'Record Created ID is '+  id
#             #     return Response(json.dumps(res_message), status=400, mimetype='application/json')
       
    
#     except Exception as ex:
#         err_msg ={
#             "Message" : str(ex),
#             "status" : 404
#         }
#         return Response(json.dumps(err_msg), status=404, mimetype='application/json')









@app.route('/cancelOrder/<orderNumber>', methods=['POST'])
@jwt_required()
def cancelOrder(orderNumber):
    try:
        global authToken
        current_user = get_jwt_identity()
        orderNum = orderNumber
        orderId = models.execute_kw(current_user['db'], uid, current_user['dbpassword'], 'sale.order', 'search', [
            [['id', '=', orderNum]]])
        if not orderId:
            return Response('This Order Number Record Does not Exist in DB', status=400, mimetype='application/json')
        models.execute_kw(current_user['db'], uid, current_user['dbpassword'], 'sale.order', 'write', [
            [orderId[0]], {'state': 'cancel'}])
        msg = {
            "Message" :"Order Cancelled successfully!",
            "status" : 200
        }

        return Response(json.dumps(msg), status=201, mimetype='application/json')
    except Exception as ex:
        err_msg ={
            "Message" : str(ex),
            "status" : 400
        }
        return Response(json.dumps(err_msg), status=400, mimetype='application/json')


# @app.route('/getSaleOrder/<id>', methods=['GET'])
# def getQuotationByName(id):
#     try:
#         global authToken
#         res = authentication(authToken)
#         if res == True:
#             orderNum = int(id)
            
#             order_line_data_list = []
#             trasnfer_list = []
#             data = models.execute_kw(login_data['db'], uid, login_data['dbpassword'], 'sale.order', 'search_read', [
#                                         [['id', '=', orderNum]]])
#             sale_order_line = models.execute_kw(
#                 login_data['db'], uid, login_data['dbpassword'], 'sale.order.line', 'search_read', [[]], {'fields': ['name', 'order_id', 'product_id', 'product_uom_qty', 'product_uom', 'price_unit', 'tax_id']})
#             for rec in data:
#                 if rec['picking_ids'] != []:
#                     for picking in rec['picking_ids']:
#                         print(picking)
#                         stock = models.execute_kw(login_data['db'], uid, login_data['dbpassword'], 'stock.picking', 'search_read', [
#                                                 [['id', '=', picking]]])
#                         for st in stock:
#                             trasnfer_list.append(st)
#                 for line in sale_order_line:
#                     if rec['id'] == line['order_id'][0]:
#                         order_line_data_list.append(line)
#                         rec['order_line_data'] = order_line_data_list
#                         rec['tansfer_data'] = trasnfer_list
#                         # new key, so add
#                 # print(rec)
#             return jsonify(data)
#         else:
#             res_message = {
#                     "Message" : res,
#                 }
#             return Response(json.dumps(res_message), status=400, mimetype='application/json')
#     except Exception as ex:
#         err_msg ={
#             "Message" : str(ex),
#             "status" : 400
#         }
#         return Response(json.dumps(err_msg), status=400, mimetype='application/json')




if __name__ == '__main__':

    app.run(host="0.0.0.0", port="5000")



