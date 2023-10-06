frappe.ui.form.on("Delivery Note",{
    before_load:function(frm,cdt,cdn){
        frappe.call({
            method:"go4fresh.go4fresh.custom.custom_purchase_receipt.hide_fields",
            args:{
                "s_user" : frappe.session.user
            },
            callback:function(r){
                if(r.message === 1){

                    if(frm.doc.docstatus===1){
                        cur_frm.set_df_property("create_sales_return","hidden","0")    
                    }

                    cur_frm.set_df_property("get_items_from_sales_order","hidden","0");
                    const main_doc = ["company", "currency", "conversion_rate", "selling_price_list", "price_list_currency", "plc_conversion_rate", "ignore_pricing_rule", "set_warehouse", "set_target_warehouse", "scan_barcode", "pricing_rules", "packed_items", "product_bundle_help", "total_net_weight", "tax_category", "shipping_rule", "taxes_and_charges", "taxes", "other_charges_calculation", "base_total_taxes_and_charges", "total_taxes_and_charges", "apply_discount_on", "base_discount_amount", "additional_discount_percentage", "discount_amount", "tc_name", "terms", "project", "campaign", "source", "is_internal_customer", "represents_company", "inter_company_reference", "per_billed", "customer_group", "territory", "letter_head", "select_print_heading", "language", "print_without_amount", "group_same_items", "status", "per_installed", "installation_status", "per_returned", "excise_page", "instructions", "auto_repeat", "sales_partner", "amount_eligible_for_commission", "commission_rate", "total_commission", "sales_team", "ewaybill", "port_code", "shipping_bill_date", "shipping_bill_number"]
                    main_doc.forEach(function(entry){
                        cur_frm.set_df_property(entry,"hidden","1")
                    })
                    
                    frm.refresh_fields();
                }
            }
        })
    },
    create_sales_return:function(frm){
        frappe.model.open_mapped_doc({
			method: "erpnext.stock.doctype.delivery_note.delivery_note.make_sales_return",
			frm: cur_frm
		})
    },
    get_items_from_sales_order:function(frm){
        if (!frm.doc.customer) {
            frappe.throw({
                title: __("Mandatory"),
                message: __("Please Select a Customer")
            });
        }
        erpnext.utils.map_current_doc({
            method: "erpnext.selling.doctype.sales_order.sales_order.make_delivery_note",
            source_doctype: "Sales Order",
            target: me.frm,
            setters: {
                customer: me.frm.doc.customer,
            },
            get_query_filters: {
                docstatus: 1,
                status: ["not in", ["Closed", "On Hold"]],
                per_delivered: ["<", 99.99],
                company: me.frm.doc.company,
                project: me.frm.doc.project || undefined,
            }
        })
    }
})