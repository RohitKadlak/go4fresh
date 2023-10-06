frappe.ui.form.on("Pick List",{
    refresh:function(frm){
        cur_frm.fields_dict.parent_warehouse.get_query = function(doc,cdt,cdn) {
        	return {
        		filters:[
        			['company', '=', "FRESH PRODUCE VALUE CREATION SERVICES PRIVATE LIMITED"]
        		]
        	}
        }
    },
    before_load:function(frm,cdt,cdn){
        frappe.call({
            method:"go4fresh.go4fresh.custom.custom_purchase_receipt.hide_fields",
            args:{
                "s_user" : frappe.session.user
            },
            callback:function(r){
                if(r.message === 1){

                    cur_frm.set_df_property("get_items_from_sales_order","hidden","0")
                    cur_frm.set_df_property("group_same_items","hidden","1")
                    frm.refresh_fields();
                }
            }
        })
    },
    // before_save:function(frm){
    //     // console.log("Hello")
    //     frm.doc.locations.forEach(function(item){
    //         if(item.warehouse!=frm.doc.parent_warehouse){
    //             frappe.throw({
    //                 title: __("Mandatory"),
    //                 message: __("Insufficient Stock For Item "+item.item_code+" in "+frm.doc.parent_warehouse+" Warehouse.")
    //             });
    //         }
    //     })
    // },
    get_items_from_sales_order:function(frm){
        if (!frm.doc.customer) {
            frappe.throw({
                title: __("Mandatory"),
                message: __("Please Select a Customer")
            });
        }
        const days  = new Date(frappe.datetime.nowdate())
        days.setDate(days.getDate() - 2);
        console.log(days,frappe.datetime.nowdate())
        let get_query_filters = {
			docstatus: 1,
			per_delivered: ['<', 100],
			status: ['!=', ''],
            transaction_date : ["between",[days,frappe.datetime.nowdate()]],
			customer: frm.doc.customer
		};
        erpnext.utils.map_current_doc({
            method: 'erpnext.selling.doctype.sales_order.sales_order.create_pick_list',
            source_doctype: 'Sales Order',
            target: frm,
            setters: {
                company: frm.doc.company,
                customer: frm.doc.customer
            },
            date_field: 'transaction_date',
            get_query_filters: get_query_filters
        });
    },
})