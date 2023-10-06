frappe.ui.form.on("Purchase Receipt",{
    
    refresh:function(frm){
        // if(frm.doc.items[0].purchase_order){
        //     frm.set_value("purchase_order",frm.doc.items[0].purchase_order)
        //     cur_frm.set_df_property("purchase_order","hidden","0")
        // }        

        // frm.doc.items.forEach(function(row) {
        //     if(row.purchase_order){
        //         frappe.call({
        //             method: "frappe.client.get",
        //             args: {
        //                 doctype: "Purchase Order",
        //                 name: row.purchase_order,
        //             },
        //             callback(r) {
        //                 if(r.message) {
        //                     var po = r.message;
        //                     $.each(po.items || [], function(v, entry) {
        //                         if(entry.item_code === row.item_code){
        //                             row.po_qty = entry.qty
        //                             frm.refresh_fields();
        //                         }
        //                     })    
        //                 }
        //             }
        //         })
        //     }
        // })
        // set_css(frm);
    },

    before_load:function(frm,cdt,cdn){
        frappe.call({
            method:"go4fresh.go4fresh.custom.custom_purchase_receipt.hide_fields",
            args:{
                "s_user" : frappe.session.user
            },
            callback:function(r){  
                if(r.message === 1){
                    if(frm.doc.docstatus===1){
                        cur_frm.set_df_property("create_purchase_return","hidden","0")    
                    }
                    cur_frm.get_field("items").grid.editable_fields = [
                        {fieldname : 'item_code' , columns : 6},
                        {fieldname : 'item_name' , columns : 4}
                    ]

                    cur_frm.set_df_property("get_items_from_purchase_order","hidden","0")

                    // set_css(frm);
                    const main_doc = ["rejected_warehouse","set_warehouse","supplier_delivery_note","supplier_delivery_note_date", "company", "set_posting_time", "apply_putaway_rule", "is_return", "return_against", "section_addresses", "supplier_address", "supplier_gstin", "contact_person", "address_display", "contact_display", "contact_mobile", "contact_email", "shipping_address", "place_of_supply", "shipping_address_display", "company_gstin", "billing_address", "billing_address_display", "currency_and_price_list", "currency", "conversion_rate", "buying_price_list", "price_list_currency", "plc_conversion_rate", "ignore_pricing_rule", "set_from_warehouse", "is_subcontracted", "supplier_warehouse", "scan_barcode", "base_total", "base_net_total", "total_net_weight", "net_total", "pricing_rule_details", "pricing_rules", "raw_material_details", "get_current_stock", "supplied_items", "tax_category", "shipping_rule", "taxes_and_charges", "taxes", "sec_tax_breakup", "other_charges_calculation", "base_taxes_and_charges_added", "base_taxes_and_charges_deducted", "base_total_taxes_and_charges", "taxes_and_charges_added", "taxes_and_charges_deducted", "total_taxes_and_charges", "section_break_42", "apply_discount_on", "base_discount_amount", "additional_discount_percentage", "discount_amount", "base_grand_total", "base_rounding_adjustment", "base_in_words", "base_rounded_total", "grand_total", "rounding_adjustment", "rounded_total", "in_words", "disable_rounded_total", "terms_section_break", "tc_name", "terms", "bill_no", "bill_date", "quality_insepection", "qc_status", "lot_qty", "lot_accepted_qty", "lot_rejected_qty", "remark", "accounting_details_section", "provisional_expense_account", "more_info", "project", "status", "amended_from", "range", "column_break4", "per_billed", "per_returned", "is_internal_supplier", "inter_company_reference", "represents_company", "subscription_detail", "auto_repeat", "printing_settings", "letter_head", "language", "instructions", "select_print_heading", "other_details", "remarks", "group_same_items", "transporter_info", "transporter_name", "lr_no", "lr_date"]
                    main_doc.forEach(function(entry){
                        cur_frm.set_df_property(entry,"hidden","1")
                    })
                    const child_table = ["uom","received_stock_qty","stock_qty","weight_per_unit","total_weight","weight_uom","gst_hsn_code","description","is_nil_exempt", "is_non_gst", "conversion_factor", "price_list_rate", "amount", "base_rate", "base_amount", "pricing_rules", "stock_uom_rate", "is_free_item", "net_rate", "net_amount", "item_tax_template", "base_net_rate", "base_net_amount", "valuation_rate", "item_tax_amount", "rm_supp_cost", "landed_cost_voucher_amount", "billed_amt", "allow_zero_valuation_rate", "bom", "serial_no", "rejected_serial_no", "manufacturer", "manufacturer_part_no", "project", "cost_center", "page_break"]                    
                    child_table.forEach(function(entry){
                        var df=frappe.meta.get_docfield("Purchase Receipt Item", entry ,frm.doc.name);
                        df.hidden=1;
                    })
                    frm.refresh_fields();
                }
            }
        })
    },
    
    get_items_from_purchase_order:function(frm){
        
        if (!frm.doc.supplier) {
            frappe.throw({
                title: __("Mandatory"),
                message: __("Please Select a Supplier")
            });
        }
        const days  = new Date(frappe.datetime.nowdate())
        days.setDate(days.getDate() - 2);
        erpnext.utils.map_current_doc({
            method: "erpnext.buying.doctype.purchase_order.purchase_order.make_purchase_receipt",
            source_doctype: "Purchase Order",
            target: frm,
            setters: {
                supplier: frm.doc.supplier,
                schedule_date: undefined
            },
            get_query_filters: {
                docstatus: 1,
                status: ["not in", ["Closed", "On Hold"]],
                per_received: ["<", 99.99],
                company: me.frm.doc.company,
                transaction_date : ["between",[days,frappe.datetime.nowdate()]]
            },
        })
        // setTimeout(() => {  frm.save() }, 10000);
        
        frm.fields_dict["items"].grid.add_custom_button(__('SELECT'), 
			function() {
                let selected = frm.get_selected()
                frappe.call({
                    method:"go4fresh.go4fresh.custom.custom_purchase_receipt.select_items",
                    args:{
                        "sel":selected.items,
                        "doc":frm.doc.name
                    },
                    callback:function(r){
                        frm.reload_doc()
                    }
                }) 
        });
        frm.fields_dict["items"].grid.grid_buttons.find('.btn-custom').removeClass('btn-default').addClass('btn-primary');
    },
    create_purchase_return:function(frm){
        frappe.model.open_mapped_doc({
			method: "erpnext.stock.doctype.purchase_receipt.purchase_receipt.make_purchase_return",
			frm: cur_frm
		})
    }
})

var set_css = function (frm) {
    let el = document.querySelectorAll("[data-fieldname='get_items_from_purchase_order']")[1].style.backgroundColor ="#4287f5";
    let fl = document.querySelectorAll("[data-fieldname='get_items_from_purchase_order']")[1].style.color ="white";
}
