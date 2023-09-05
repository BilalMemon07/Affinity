odoo.define('sh_pos_fbr_connector.fbr_product_customization', function (require) {
    "use strict";


    var models = require('point_of_sale.models');
    
    models.PosGlobalState.prototype.add_new_order = function () { 
        console.log('bialal'+this.company.id)
        if (this.company.id != 2){

            const order = this.createReactiveOrder();
            this.orders.add(order);
            this.selectedOrder = order;
            let fbr_product = this.env.pos.db.get_product_by_id(50)
            this.selectedOrder.add_product(fbr_product);
            //Asir checking order log
            console.log('add new order: '+this.selectedOrder);
            return order;
        }
        else{

            const order = this.createReactiveOrder();
            this.orders.add(order);
            this.selectedOrder = order;
            return order;
        }
    };

    return models;
});
