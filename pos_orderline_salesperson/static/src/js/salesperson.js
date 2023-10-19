odoo.define('pos_orderline_salesperson.OrderlineSalespersonButton', function(require) {
    'use strict';

    const PosComponent = require('point_of_sale.PosComponent');
    const ProductScreen = require('point_of_sale.ProductScreen');
    const { useListener } = require('web.custom_hooks');
    const Registries = require('point_of_sale.Registries');

    class OrderlineSalespersonButton extends PosComponent {
        constructor() {
            super(...arguments);
            useListener('click', this.onClick);
        }

        async onClick() {
            this.showPopup('SalesPersonPopup', {
                title: this.env._t('Select Salesperson'),
                employees: this.env.pos.employees,
                pos: this.env.pos,
            });

        }
    }
    OrderlineSalespersonButton.template = 'OrderlineSalespersonButton';

    ProductScreen.addControlButton({
        component: OrderlineSalespersonButton,
        condition: function() {
            return this.env.pos.config.allow_orderline_user;
        },
    });

    Registries.Component.add(OrderlineSalespersonButton);

    return OrderlineSalespersonButton;
});
