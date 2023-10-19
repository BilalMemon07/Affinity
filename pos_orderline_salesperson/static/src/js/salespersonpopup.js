odoo.define('pos_orderline_salesperson.SalesPersonPopup', function (require) {
"use strict";

    const AbstractAwaitablePopup = require('point_of_sale.AbstractAwaitablePopup');
    const Registries = require('point_of_sale.Registries');
    const { useAutoFocusToLast } = require('point_of_sale.custom_hooks');

    class SalesPersonPopup extends AbstractAwaitablePopup {
        constructor() {
            super(...arguments);            
            useAutoFocusToLast();
        }
        salespersonpopup(event){
            var order = this.props.pos.get_order();
            if (!this.props.orderline) {
                order.get_orderlines().forEach(function (orderline) {
                    orderline.set_salesperson(event.currentTarget.dataset);
                });
            }
            else{
                this.props.orderline.set_salesperson(event.currentTarget.dataset);
                this.props.orderline.trigger('change',this.props.orderline);
            }
            this.trigger('close-popup');
        }

    }
    SalesPersonPopup.template = 'SalesPersonPopup';
    SalesPersonPopup.defaultProps = {
        confirmText: 'Ok',
        cancelText: 'Cancel',
    };

    Registries.Component.add(SalesPersonPopup);
    return SalesPersonPopup;

});
