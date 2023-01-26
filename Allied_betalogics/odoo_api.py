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


# @app.route('/checkingData', methods=['POST'])
# def checkingData():
#     return data
tokenList = []


@app.route('/login', methods=['POST'])
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



@app.route('/createCustomer', methods=['POST'])
def createCustomer():
    record = json.loads(request.data)
    try:
        global authToken
        res = authentication(authToken)
        if res == True:
            # customer_search = models.execute_kw(login_data['db'], uid, login_data['dbpassword'], 'res.partner', 'search', [
            #     [['mobile', '=', record['mobile']]]])
            # if customer_search:
            #     return Response('User Already Exist, You Can not add This User 2nd Time', status=400, mimetype='application/json')
            id = models.execute_kw(login_data['db'], uid, login_data['dbpassword'], 'res.partner', 'create', [{
                "name":record['name']
            }])
            res_message ={
                    "Message" : "Product Created Successfully",
                    "id" : "Customer Created Id is" + " " + str(id)
            }
            return Response(json.dumps(res_message), status=201, mimetype='application/json')
        else:
            return Response(res, status=400, mimetype='application/json')

    except NameError as ex:
        print(ex)
        return Response('Sorry, something went wrong!' + str(ex), status=400, mimetype='application/json')



@app.route('/createsalesorder', methods=['POST'])
def createSaleOrder():
    record = json.loads(request.data)
    print(record)
    # return request.data
    try:
        global authToken
        res = authentication(authToken)
        if res == True:
            sales_order_line = []
            courier_data = models.execute_kw(login_data['db'], uid, login_data['dbpassword'], 'courier_model', 'search_read', [
                                        [['name', '=', rec['x_studio_assigned_courier']]]])
            id = models.execute_kw(login_data['db'], uid, login_data['dbpassword'], 'sale.order', 'create', [{
                # 'name': record['name'],
                # 'pricelist_id': record['pricelist_id'],
                'sale_order_type':'fulfillment',
                'sale_order_sub_type':'shopify',
                'shopify_order_number':record['	shopify_order_number'],
                'partner_id': record['partner_id'],
                'x_studio_platform_1':1230,
                'x_studio_street':record['x_studio_street'],
                'x_studio_shipping_amount': record['x_studio_shipping_amount'],
                'x_studio_city':record['x_studio_city'],
                'x_studio_phone_no':record['x_studio_phone_no'],
                'x_studio_assigned_courier':courier_data[0]['id']       
                # 'payment_term_id': record['payment_term_id'],
            }])
            if id:
                for rec in record['order_line']:

                    data = models.execute_kw(login_data['db'], uid, login_data['dbpassword'], 'product.product', 'search_read', [
                                        [['default_code', '=', rec['product_id']]]])
                  
                    if data:
                        sales_order_line.append((0, 0, {
                            'name': rec['name'],
                            'product_id': data[0]['id'],
                            'price_unit': rec['price_unit'],
                            'product_uom_qty': rec['product_uom_qty'],
                            # 'tax_id': rec['tax_id'],
                        }))
                        models.execute_kw(login_data['db'], uid, login_data['dbpassword'], 'sale.order', 'write', [
                            [id], {"order_line": sales_order_line}])

                        print('Record created successfully!')
                res_message ={
                    "Message" : "Sale Order Created Successfully",
                    "id" : "Sale Order Created Id is" + " " + str(id)
                }       
                # return 'Record created successfully! '+'Record Created ID is '+  id
                return Response(json.dumps(res_message), status=201, mimetype='application/json')
            else:
                return Response('Record is not created! ', status=201, mimetype='application/json')

        else:
            return Response(res, status=400, mimetype='application/json')

    except Exception as ex:
        print(ex)
        return Response('Sorry, something went wrong!' + str(ex), status=400, mimetype='application/json')


@app.route('/getQuotationByName/<orderNumber>', methods=['GET'])
def getQuotationByName(orderNumber):
    try:
        orderNum = orderNumber
        global authToken
        res = authentication(authToken)
        if not orderNum:
            return Response('Record Number Must be Required in Url ', status=404, mimetype='application/json')
        if res == True:
            order_line_data_list = []
            data = models.execute_kw(login_data['db'], uid, login_data['dbpassword'], 'sale.order', 'search_read', [
                                     [['name', '=', orderNum]]])
            sale_order_line = models.execute_kw(
                login_data['db'], uid, login_data['dbpassword'], 'sale.order.line', 'search_read', [[]], {'fields': ['name', 'order_id', 'product_id', 'product_uom_qty', 'product_uom', 'price_unit', 'tax_id']})
            for rec in data:
                for line in sale_order_line:
                    if rec['id'] == line['order_id'][0]:
                        order_line_data_list.append(line)
                        rec['order_line_data'] = order_line_data_list
                        # new key, so add
                # print(rec)
            print(order_line_data_list)
            return jsonify(data)
        else:
            print("hello False")
            return Response(res, status=400, mimetype='application/json')
    except Exception as ex:
        print('Sorry, something went wrong!')
        return Response('Sorry, something went wrong!' + ' ' + str(ex), status=400, mimetype='application/json')


@app.route('/updatesalesorder/<orderNumber>', methods=['POST'])
def updatesalesorder(orderNumber):
    record = json.loads(request.data)
    try:
        orderNum = orderNumber
        global authToken
        res = authentication(authToken)
        if res == True:
            orderId = models.execute_kw(login_data['db'], uid, login_data['dbpassword'], 'sale.order', 'search', [
                [['name', '=', orderNum]]])
            if not orderId:
                return Response('Please Enter Correct Order Number!', status=400, mimetype='application/json')
            
            data = models.execute_kw(login_data['db'], uid, login_data['dbpassword'], 'sale.order', 'write', [[orderId[0]], record])
            if not data:
                return Response('Please Enter Correct Order Number!', status=400, mimetype='application/json')

            return Response('Record Update successfully!', status=201, mimetype='application/json')
        else:
            print("hello False")
            return Response(res, status=400, mimetype='application/json')
    except Exception as ex:
        print('Sorry, something went wrong!')
        return Response('Sorry, something went wrong!' + ' ' + str(ex), status=400, mimetype='application/json')


@app.route('/deleteOrder/<orderNumber>', methods=['DELETE'])
def deleteOrder(orderNumber):
    try:
        global authToken
        res = authentication(authToken)
        if res == True:
            orderNum = orderNumber
            orderId = models.execute_kw(login_data['db'], uid, login_data['dbpassword'], 'sale.order', 'search', [
                [['name', '=', orderNum]]])
            if not orderId:
                return Response('This Order Number Record Does not Exist in DB', status=400, mimetype='application/json')
            odoores = models.execute_kw(
                login_data['db'], uid, login_data['dbpassword'], 'sale.order', 'unlink', [[orderId[0]]])
            print(odoores)
            return Response('Record Delete successfully!', status=201, mimetype='application/json')
        else:
            return Response(res, status=400, mimetype='application/json')
    except Exception as ex:
        print('Sorry, something went wrong!')
        return Response('Sorry, something went wrong!' + ' ' + str(ex), status=400, mimetype='application/json')


@app.route('/cancelOrder/<orderNumber>', methods=['POST'])
def cancelOrder(orderNumber):
    try:
        global authToken
        res = authentication(authToken)
        if res == True:
            orderNum = orderNumber
            orderId = models.execute_kw(login_data['db'], uid, login_data['dbpassword'], 'sale.order', 'search', [
                [['name', '=', orderNum], ['name', '=', orderNum]]])
            if not orderId:
                return Response('This Order Number Record Does not Exist in DB', status=400, mimetype='application/json')
            models.execute_kw(login_data['db'], uid, login_data['dbpassword'], 'sale.order', 'write', [
                [orderId[0]], {'state': 'cancel'}])
            return Response('Order Cancel successfully!', status=201, mimetype='application/json')
        else:
            return Response(res, status=400, mimetype='application/json')
    except Exception as ex:
        print('Sorry, something went wrong!')
        return Response('Sorry, something went wrong!' + ' ' + str(ex), status=400, mimetype='application/json')


@app.route('/getProduct', methods=['GET'])
def getProduct():
    try:
        global authToken
        res = authentication(authToken)
        if res == True:
            data = models.execute_kw(login_data['db'], uid, login_data['dbpassword'], 'product.template', 'search_read', [
                []])
            return jsonify(data)
        else:
            return Response(res, status=400, mimetype='application/json')
    except NameError:
        print('Sorry, something went wrong!')
        return Response('Sorry, something went wrong!' + str(NameError), status=400, mimetype='application/json')


@app.route('/getPartner', methods=['GET'])
def getPartner():
    try:
        global authToken
        res = authentication(authToken)
        if res == True:
            data = models.execute_kw(login_data['db'], uid, login_data['dbpassword'], 'res.partner', 'search_read', [
                []])
            return jsonify(data)
        else:
            return Response(res, status=400, mimetype='application/json')
    except NameError:
        print('Sorry, something went wrong!')
        return Response('Sorry, something went wrong!' + str(NameError), status=400, mimetype='application/json')


@app.route('/getTaxes', methods=['GET'])
def getTaxes():
    try:
        global authToken
        res = authentication(authToken)
        if res == True:
            data = models.execute_kw(login_data['db'], uid, login_data['dbpassword'], 'account.tax', 'search_read', [
                []])
            return jsonify(data)
        else:
            return Response(res, status=400, mimetype='application/json')
    except Exception as ex:
        print('Sorry, something went wrong!')
        return Response('Sorry, something went wrong!' + ' ' + str(ex), status=400, mimetype='application/json')

# pricelist_id


@app.route('/getPricelist', methods=['GET'])
def getPricelist():
    try:
        global authToken
        print(authToken)
        res = authentication(authToken)
        if res == True:
            data = models.execute_kw(login_data['db'], uid, login_data['dbpassword'], 'product.pricelist', 'search_read', [
                                     []])
            price_list_line = models.execute_kw(
                login_data['db'], uid, login_data['dbpassword'], 'product.pricelist.item', 'search_read', [[]])
            pricelist_data_list = []
            for i, rec in enumerate(data):
                for line in price_list_line:
                    if rec['id'] == line['pricelist_id'][0]:
                        pricelist_data_list.append(line)
                        # new key, so add
                        rec['pricelist_line_data'] = pricelist_data_list
                    else:
                        rec['pricelist_line_data'] = []
                print(rec)
            print(uid)
            return jsonify(data)
        else:
            return Response(res, status=400, mimetype='application/json')
    except Exception as ex:
        print('Sorry, something went wrong!')
        return Response('Sorry, something went wrong!' + ' ' + str(ex), status=400, mimetype='application/json')




if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host="0.0.0.0", port="5000")
    # from waitress import serve
    # serve(app,host='127.0.0.1',port=5000)



