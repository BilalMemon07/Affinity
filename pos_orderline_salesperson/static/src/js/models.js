odoo.define('pos_orderline_salesperson.modelsorderline', function (require) {
"use strict";

    var models = require('point_of_sale.models');

    var _super_orderline = models.Orderline.prototype;

    models.Orderline = models.Orderline.extend({
        initialize: function(attr, options) {
            _super_orderline.initialize.call(this,attr,options);
            this.salesperson = this.salesperson || "";
            this.salesperson_id = this.salesperson_id || 0.0;
        },
        set_salesperson: function(salesperson){
            this.salesperson = salesperson.value;
            this.salesperson_id = salesperson.id;
            this.trigger('change',this);
        },
        get_salesperson: function(salesperson){
            return this.salesperson;
        },
        can_be_merged_with: function(orderline) {
            if (orderline.get_salesperson() !== this.get_salesperson()) {
                return false;
            } else {
                return _super_orderline.can_be_merged_with.apply(this,arguments);
            }
        },
        clone: function(){
            var orderline = _super_orderline.clone.call(this);
            orderline.salesperson = this.salesperson;
            orderline.salesperson_id = this.salesperson_id;
            return orderline;
        },
        export_as_JSON: function(){
            var json = _super_orderline.export_as_JSON.call(this);
            json.salesperson = this.salesperson;
            json.salesperson_id = this.salesperson_id;
            return json;
        },
        init_from_JSON: function(json){
            _super_orderline.init_from_JSON.apply(this,arguments);
            this.salesperson = json.salesperson;
            this.salesperson_id = json.salesperson_id;
        },
    });

});
