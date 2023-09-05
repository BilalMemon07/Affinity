odoo.define('sh_pos_fbr_connector.screens', function(require) {
    "use strict";
   
    const PosComponent = require('point_of_sale.PosComponent');
    var models = require('point_of_sale.models');
    var rpc = require('web.rpc');
    const ProductScreen = require('point_of_sale.ProductScreen');
    const PaymentScreen = require('point_of_sale.PaymentScreen');
    const { useListener } = require("@web/core/utils/hooks");
    const Registries = require('point_of_sale.Registries');
	var uid = 0;
	var checkuid = 0;
    var order_ref = '';
    var fbr_number = '';
    var exports = {};
    var receipt = {};  
    
    
    // models.load_fields("pos.order", ['invoice_number','post_data_fbr','fbr_respone']);
    
    // var _super_order = models.Order.prototype;
    // models.Order = models.Order.extend({
    //     initialize: function(attr, options){
    //         _super_order.initialize.call(this,attr,options);
    //         this.invoice_number = '';
    //         this.post_data_fbr = '';
    //         this.fbr_respone = '';
    //     },
    //     set_fbr_respone (fbr_respone) {
    //         this.fbr_respone = fbr_respone || null;
    //     },
    //     get_fbr_respone() {
    //         return this.fbr_respone
    //     },
    //     set_invoice_number(invoice_number) {
    //         this.invoice_number = invoice_number || null;
    //     },
    //     get_invoice_number() {
    //         // $("#fbrinvoice").text('Hello World');
    //         return this.invoice_number;
    //     },
    //     set_post_data_fbr(post_data_fbr) {
    //         this.post_data_fbr = post_data_fbr || null;
    //     },
    //     get_post_data_fbr() {
    //         return this.post_data_fbr
    //     },
    //     export_as_JSON() {
    //         var vals = _super_order.export_as_JSON.call(this, arguments);
    //         vals['invoice_number'] = this.get_invoice_number();
    //         vals['post_data_fbr'] = this.get_post_data_fbr();
    //         vals['fbr_respone'] = this.get_fbr_respone();
    //         console.log('test1: ', vals);
    //         return vals
    //     },
    //     export_for_printing: function () {
    //         //setTimeout(function(){
    //             var res = _super_order.export_for_printing.apply(this, arguments);
    //             res.invoice_number = this.get_invoice_number();
    //             console.log('res.invoice_number:', res.invoice_number);
    //             return res;
    //         //}, 3000);
    //     },
    // });


    const NewPaymentScreen = (PaymentScreen) =>
        class extends PaymentScreen {
            constructor(){
                super(...arguments);
            }
            async validateOrder(isForceValidate) {
                
                console.log('working');
                var validate_btn = document.querySelector('.button.next.validation');
                console.log('validate_btn');
                console.log(validate_btn);
                // MouseEvent.stopPropagation();
                // validate_btn.disabled = true;
                validate_btn.style.display = 'none';
                var loyalty = super.validateOrder(isForceValidate)
                var self = this;
                if (await this._isOrderValid(isForceValidate)) {
                    console.log('uid in ',uid);
                    var pos_order = this.env.pos.get_order();
                    // console.log('pos_order.amount_total', pos_order.get_total_with_tax());
                    var e_json = pos_order.export_as_JSON();
                    console.log('234234234234', e_json);
                    if(e_json.amount_total == 0){ 
                        // self._finalizeValidation(); 
                    }
                    else{
                        uid = pos_order.uid;
                        order_ref = e_json.name;
                        console.log('Order ref: ',order_ref);
                        console.log('uid after saving ',uid);
                        console.log('test3: ', pos_order);
                        //$('.receipt-screen').addClass('oe_wait');
                        if (uid != checkuid){
                          
                        rpc.query({
                                model: 'pos.order',
                                method: 'post_data_fbi',
                                args: [[pos_order.uid],[pos_order.export_as_JSON()]],
                            })
                            .then(function(data){
                                //setTimeout(function(){
                                console.log('test2: ', data)
                                var inv = data[0];
                                var resp = data[1];
                                fbr_number = data[0];
                                // if(data && data[0] && data[1]){
                                //     console.log('datadatadatadata: ',  data);
                                //     pos_order.set_invoice_number(data[0]);
                                //     pos_order.set_post_data_fbr(true);
                                //     pos_order.set_fbr_respone(data[1]); 
                                // }
                                //Asir
                                if(data && data[0] && data[1]){
                                    setTimeout(() => {
                                        validate_btn.style.display = 'block';
                                        rpc.query({
                                            model: 'pos.order',
                                            method: 'post_data_to_order',
                                            // args: [[pos_order.uid],[order_ref],inv,resp],
                                            args: [[pos_order.uid],[order_ref],inv,resp],
                                        })
                                        .then(function(rdata){
                                            if(rdata){
                                                console.log('rdata: '+rdata);
                                                var pos_id = rdata[0];
                                                var qr_code = rdata[1];
                                                // document.getElementById("fbrinvoiceno").innerHTML = inv;
                                                // document.getElementById("fbrposid").innerHTML = pos_id;
                                                // document.getElementById("fbrqrimg").src = "data:image/png;base64," + qr_code;
                                            }
                                        });
                                    },1000);
                                }                             
                            });
                            
                            // self._finalizeValidation();
                        }
                    }
                    console.log('checkuid in ',checkuid);
                    checkuid = pos_order.uid;
                    console.log('checkuid after saving ',checkuid);
                }

                return loyalty;
            }

        }
    Registries.Component.extend(PaymentScreen, NewPaymentScreen);


    // return NewPaymentScreen;
                                        // exports.Order = Backbone.Model.extend({
                                    //     var: receipt = {
                                    //         invoice_number: data[0],
                                    //     },
                                    //     getOrderReceiptEnv: function() {
                                    //         console.log('check2');
                                    //         var order = this.pos.get_order();
                                    //         console.log(fbr_number);
                                    //         return {
                                    //             widget: this,
                                    //             // pos: pos_check,
                                    //             order: order,
                                    //             invoicenumber :receipt.invoice_number,
                                    //             receipt: order.export_for_printing(),
                                    //             orderlines: order.get_orderlines(),
                                    //             paymentlines: order.get_paymentlines(),
                                    //         };
                                    //     },
                                    // });
    // var _super_order = models.Order.prototype;
    // models.Order = models.Order.extend({
    // 	initialize: function(attributes, options) {
    //         _super_order.initialize.apply(this, arguments);
    //         this.invoice_number = false;
    //         this.post_data_fbr = false;
	// 		this.fbr_respone = false;
    //     },
	// 	set_fbr_respone: function(fbr_respone) {
    //     	this.fbr_respone = fbr_respone || null;
    //     },
    //     get_fbr_respone: function() {
    //         return this.fbr_respone
    //     },
    //     set_invoice_number: function(invoice_number) {
    //     	this.invoice_number = invoice_number || null;
    //     },
    //     get_invoice_number: function() {
    //         return this.invoice_number
    //     },
    //     set_post_data_fbr: function(post_data_fbr) {
    //     	this.post_data_fbr = post_data_fbr || null;
    //     },
    //     get_post_data_fbr: function() {
    //         return this.post_data_fbr
    //     },
    //     export_as_JSON: function() {
    //         var vals = _super_order.export_as_JSON.apply(this, arguments);
    //         vals['invoice_number'] = this.get_invoice_number();
    //         vals['post_data_fbr'] = this.get_post_data_fbr();
	// 		vals['fbr_respone'] = this.get_fbr_respone();
    //         console.log('test1: ', vals)
    //         return vals
    //     },
    // });
    // payscreens.include({
    // 	validateOrder: function(isForceValidate) {
    //         console.log('check');
    // 		var self = this;
    //         if (this.order_is_valid(isForceValidate)) {
	// 			console.log('uid in ',uid);
    //             var pos_order = this.pos.get_order();
	// 			console.log('pos_order.amount_total', pos_order.amount_total);
	// 			var e_json = pos_order.export_as_JSON();
	// 			console.log('e_json', e_json);
	// 			if(e_json.amount_total == 0){ self._finalizeValidation(); }
	// 			else{
	// 				uid = pos_order.uid; 
	// 				console.log('uid after saving ',uid);
	// 				console.log('test3: ',  pos_order)
	// 				//$('.receipt-screen').addClass('oe_wait');
	// 				if (uid != checkuid){
	// 					rpc.query({
	// 						model: 'pos.order',
	// 						method: 'post_data_fbi',
	// 						args: [[pos_order.uid],[pos_order.export_as_JSON()]],
	// 					})
	// 					.then(function(data){
	// 						console.log('test2: ', data[1])
	// 						if(data && data[0] && data[1]){
	// 							pos_order.set_invoice_number(data[0]);
	// 							pos_order.set_post_data_fbr(true);
	// 							pos_order.set_fbr_respone(data[1]);
	// 						}
	// 						self._finalizeValidation();
	// 					});
	// 				}
	// 			}
	// 			console.log('checkuid in ',checkuid);
    //         	checkuid = pos_order.uid;
	// 			console.log('checkuid after saving ',checkuid);
    //         }
    //     },
    // });
    
    // var _super_order = models.Order.prototype;
    // models.Order = models.Order.extend({
    //  getOrderReceiptEnv: function() {
    //     console.log('check2');
    //     var order = this.pos.get_order();
    //     console.log(fbr_number);
    //     return {
    //         widget: this,
    //         // pos: pos_check,
    //         order: order,
    //         invoicenumber :fbr_number,
    //         receipt: order.export_for_printing(),
    //         orderlines: order.get_orderlines(),
    //         paymentlines: order.get_paymentlines(),
    //     };
    // },

    // orderscreens.include({
    //         getOrderReceiptEnv: function() {
    //             console.log('check2');
    //             var order = this.env.pos.get_order();
    //             return {
    //                 widget: this,
    //                 pos: this.pos,
    //                 order: order,
    //                 invoicenumber :this.get_invoice_number(),
    //                 receipt: order.export_for_printing(),
    //                 orderlines: order.get_orderlines(),
    //                 paymentlines: order.get_paymentlines(),
    //             };
    //         },
    // });
    
});

// odoo.define('sh_pos_fbr_connector.assets', function (require) {
//     'use strict';

//     require('point_of_sale.assets');
// });