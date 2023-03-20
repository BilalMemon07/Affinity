import json
from logging import exception
from flask import Flask, Response, jsonify, request
import xmlrpc.client
import random




app = Flask(__name__)
# get Data From Odoo



url = 'https://odoo-database.cpoui9kngi81.ap-south-1.rds.amazonaws.com:5432'
db = 'odoo-database'
username = 'postgres'
password = 'trukkr-user'

common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
# common.version()

uid = common.authenticate(db, username, password, {})

models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))



@app.route('/', methods=['GET'])
def createCustomer():
    record = json.loads(request.data)
    try:

            id = models.execute_kw(db, uid, password, 'res.partner', 'create', [{
                "name":record['name']
            }])
            res_message ={
                    "Message" : "Product Created Successfully",
                    "id" : "Customer Created Id is" + " " + str(id)
            }
            return Response(json.dumps(res_message), status=201, mimetype='application/json')

    except NameError as ex:
        print(ex)
        return Response('Sorry, something went wrong!' + str(ex), status=400, mimetype='application/json')



if __name__ == '__main__':

    app.run(host="0.0.0.0", port="5000")