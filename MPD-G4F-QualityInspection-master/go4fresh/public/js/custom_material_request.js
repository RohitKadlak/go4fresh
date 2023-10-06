frappe.ui.form.on("Material Request",{
    before_load:function(frm,cdt,cdn){
        cur_frm.set_df_property("get_items_from_sales_order","hidden","0");
        frappe.call({
            method:"go4fresh.go4fresh.custom.custom_purchase_receipt.hide_fields",
            args:{
                "s_user" : frappe.session.user
            },
            callback:function(r){
                if(r.message === 1){
                    
                    // cur_frm.set_df_property("get_items_from_sales_order","hidden","0");
                    const main_doc = ["letter_head","select_print_heading","tc_name","terms"]
                    main_doc.forEach(function(entry){
                        cur_frm.set_df_property(entry,"hidden","1")
                    })
                    
                    frm.refresh_fields();
                }
            }
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
			method: "erpnext.selling.doctype.sales_order.sales_order.make_material_request",
			source_doctype: "Sales Order",
			target: frm,
			setters: {
				customer: frm.doc.customer || undefined,
				delivery_date: undefined,
			},
			get_query_filters: {
				docstatus: 1,
				status: ["not in", ["Closed", "On Hold"]],
				per_delivered: ["<", 99.99],
				company: frm.doc.company
			}
		});
    },
    before_save:function(frm){
        frm.doc.items.forEach(function(item){
            item.rate = 0
            item.amount = 0
        })
        frm.refresh_fields("items");
    }
})