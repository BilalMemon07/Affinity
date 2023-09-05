import json
from logging import exception
import random
from datetime import timedelta ,datetime
from flask import Flask, Response, jsonify, request
from flask_jwt_extended import JWTManager
import xmlrpc.client
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity


from werkzeug.middleware.profiler import ProfilerMiddleware



app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY3NzgzODIzMywianRpIjoiNTBhN2QxNzItNDg4My00YzFjLTk4OTYtNWIyZjc4ZTRmZTgwIiwidHlwZSI6ImFeyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.jY2VzcyIsInN1YiI6ImJpbGFsIiwibmJmIjoxNjc3ODM4MjMzLCJleHAiOjE2Nzc4MzgyOTN9.ECM0f-1TJgdAFELYF_yn3hGMZ2tmIfT-PNKHVt-CPSw'  # Change this!
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
        sales_order_line = [
            (0,0,{
                'product_id': 9497,
                'price_unit': record['shipping_amount'],
                'product_uom_qty': 1,

            })
        ]
        shipping_policy = False
        if record['shipping_policy'] ==  "When all Products are ready":
            shipping_policy  = 'one'
        elif record['shipping_policy'] ==  "As soon as possible":
            shipping_policy  = 'direct'
        
        customer_id = models.execute_kw(current_user['db'], uid, current_user['dbpassword'], 'res.partner', 'create', [{
            "name": record['customer'],
            "street": record['delivery_address'],
            "city" : record['customer_city'],
            "phone": record['customer_phone_no']
        }])
        courier_data = models.execute_kw(current_user['db'], uid, current_user['dbpassword'], 'courier_model', 'search_read', [
                                    [['name', '=', record['assigned_courier']]]])
        warehouse_data = models.execute_kw(current_user['db'], uid, current_user['dbpassword'], 'stock.warehouse', 'search_read', [
                                    [['name', '=', record['warehouse']]]])
        check_order_number = models.execute_kw(current_user['db'], uid, current_user['dbpassword'], 'sale.order', 'search_read', [
                                [['shopify_order_number', '=', record['shopify_order_number']]]], {'fields': ['shopify_order_number'], 'limit': 1})
        print(check_order_number)
        shopify_numbers_list =[]
        # for check in  check_order_number:
        #     shopify_numbers_list.append(check['shopify_order_number'])
        #     print(check['shopify_order_number'])

        if len(check_order_number) < 0:
            for rec in record['order_line']:
                # shopify_numbers_list.append(check['shopify_order_number'])
                data = models.execute_kw(current_user['db'], uid, current_user['dbpassword'], 'product.product', 'search_read', [
                                            [['default_code', '=', rec['product']]]])    
                if data:
                    sales_order_line.append((0, 0, {
                        'product_id': data[0]['id'],
                        'price_unit': rec['price_unit'],
                        'product_uom_qty': rec['quantity'],
                    }))
        # if record['shopify_order_number'] not in shopify_numbers_list:
        if len(check_order_number) < 0:
            id = models.execute_kw(current_user['db'], uid, current_user['dbpassword'], 'sale.order', 'create', [{
                    'sale_order_type':str(record['sale_order_type']).lower(),
                    'sale_order_sub_type':str(record['sale_order_sub_type']).lower(),
                    'partner_id': customer_id,
                    'x_studio_platform_1':25475,
                    'warehouse_id': warehouse_data[0]['id'],
                    # 'x_studio_street':record['street'],
                    "shopify_order_number" : record['shopify_order_number'],
                    'x_studio_shipping_amount': record['shipping_amount'],
                    'x_studio_city':record['customer_city'],
                    'x_studio_phone_no':record['customer_phone_no'],
                    'x_studio_payment_mode':record['payment_mode'],
                    'picking_policy': shipping_policy,
                    'x_studio_assigned_courier':courier_data[0]['id'],
                    "x_studio_gift_note":record['gift_note'],
                    "order_line" : sales_order_line
                    # "x_delivery_address_fu": record['delivery_address_file_upload']
                }])
            if id:
                # for rec in record['order_line']:

                #     data = models.execute_kw(current_user['db'], uid, current_user['dbpassword'], 'product.product', 'search_read', [
                #                         [['default_code', '=', rec['product']]]])
                
                #     if data:
                #         sales_order_line.append((0, 0, {
                #             'product_id': data[0]['id'],
                #             'price_unit': rec['price_unit'],
                #             'product_uom_qty': rec['quantity'],
                #         }))
                # models.execute_kw(current_user['db'], uid, current_user['dbpassword'], 'sale.order', 'write', [
                #     [id], {"order_line": sales_order_line}])
                
                # shopify_order = models.execute_kw(current_user['db'], uid, current_user['dbpassword'], 'sale.order', 'search_read', [
                #                         [['id', '=', id]]],{'fields': ['name', 'shopify_order_number']})
                res_message ={
                    "Message" : "Sale Order Created Successfully",
                    "id" : id,
                    "Shopify_Order_number": record['shopify_order_number']
                }       
                print(res_message)
                # return 'Record created successfully! '+'Record Created ID is '+  id
                return Response(json.dumps(res_message), status=201, mimetype='application/json')
        else:
            res_message ={
                    "Message" : "shopify Order Number is duplicated",
                }       
                # return 'Record created successfully! '+'Record Created ID is '+  id
            return Response(json.dumps(res_message), status=400, mimetype='application/json')
    
    
    except Exception as ex:
        err_msg ={
            "Message" : str(ex),
            "status" : 404
        }
        return Response(json.dumps(err_msg), status=404, mimetype='application/json')


@app.route('/getSaleOrder/<shopify_order_number>', methods=['GET'])
@jwt_required()       
def getQuotationByName(shopify_order_number):
    print("0 Step Complete")

    try:
        order_line_data_list = []
        current_user = get_jwt_identity()
        print("0.1 Step Complete")

        
        

        trasnfer_list = []
        data = models.execute_kw(current_user['db'], uid, current_user['dbpassword'], 'sale.order', 'search_read', [
                                    [['shopify_order_number', '=', shopify_order_number]]])
        print("0.0.1 step complete")
        print("1 Step Complete")
        for rec in data:
            sale_order_line = models.execute_kw(
                current_user['db'], uid, current_user['dbpassword'], 'sale.order.line', 'search_read', [[['order_id', '=', rec['id']]]], {'fields': ['name', 'order_id', 'product_id', 'product_uom_qty', 'product_uom', 'price_unit', 'tax_id']})

            if rec['picking_ids'] != []:
                for picking in rec['picking_ids']:
                    print(picking)
                    stock = models.execute_kw(current_user['db'], uid, current_user['dbpassword'], 'stock.picking', 'search_read', [
                                            [['id', '=', picking]]])
                    for st in stock:
                        trasnfer_list.append(st)
                    print("2 Step Complete")
            for line in sale_order_line:
                if rec['id'] == line['order_id'][0]:
                    order_line_data_list.append(line)
                    rec['order_line_data'] = order_line_data_list
                    rec['tansfer_data'] = trasnfer_list
                    print("3 Step Complete")
                    # new key, so add
            # print(rec)
            print("4 Step Complete")   
        # return jsonify(data)
        return Response(json.dumps(data), status=201, mimetype='application/json')

       
    except Exception as ex:
        err_msg ={
            "Message" : str(ex),
            "status" : 400
        }
        print(str(ex))
        return Response(json.dumps(err_msg), status=400, mimetype='application/json')



if __name__ == '__main__':
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app)
    app.run(host="0.0.0.0", port="5001")