odoo.define('pos_orderline_salesperson.orderline', function(require) {
    'use strict';

    const Orderline = require('point_of_sale.Orderline');
    const Registries = require('point_of_sale.Registries');

    const PosResOrderline = Orderline =>
        class extends Orderline {
            usericonclick(){
                this.showPopup('SalesPersonPopup',{
                    title: this.env._t('Select Salesperson'),
                    employees: this.env.pos.employees,
                    pos: this.env.pos,
                    orderline: this.props.line,
                });
           }

           removesalesperson(){
                this.props.line.salesperson = '';
                this.props.line.salesperson_id = 0.0;
                this.props.line.trigger('change',this.props.line);
           }
        };

    Registries.Component.extend(Orderline, PosResOrderline);

    return Orderline;
});
