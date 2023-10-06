frappe.ui.form.on("Stock Entry",{
    before_load:function(frm,cdt,cdn){
        frappe.call({
            method:"go4fresh.go4fresh.custom.custom_purchase_receipt.hide_fields",
            args:{
                "s_user" : frappe.session.user
            },
            callback:function(r){
                if(r.message === 1){

                    const main_doc = ["outgoing_stock_entry", "add_to_transit", "work_order", "delivery_note_no", "sales_invoice_no", "pick_list", "purchase_receipt_no", "inspection_required", "from_bom", "apply_putaway_rule", "bom_no", "fg_completed_qty", "use_multi_level_bom", "get_items", "source_warehouse_address", "source_address_display", "target_warehouse_address", "target_address_display", "scan_barcode", "total_incoming_value", "total_outgoing_value", "value_difference", "additional_costs", "total_additional_costs", "supplier", "supplier_name", "supplier_address", "address_display", "project", "select_print_heading", "letter_head", "is_opening", "remarks", "per_transferred", "total_amount", "job_card", "amended_from", "credit_note", "is_return"]
                    main_doc.forEach(function(entry){
                        cur_frm.set_df_property(entry,"hidden","1")
                    })
                    
                    frm.refresh_fields();
                }
            }
        })
    }
})