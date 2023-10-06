frappe.ui.form.on("Purchase Order",{
    supplier:function(frm){
        frappe.call({
            method:"go4fresh.go4fresh.custom.custom_purchase_receipt.hide_fields",
            args:{
                "s_user" : frappe.session.user
            },
            callback:function(r){
                if(r.message === 1){
                    cur_frm.set_df_property("get_items_from_open_material_requests","hidden","1");
                }
            }
        })
    },
    before_load:function(frm,cdt,cdn){
        frappe.call({
            method:"go4fresh.go4fresh.custom.custom_purchase_receipt.hide_fields",
            args:{
                "s_user" : frappe.session.user
            },
            callback:function(r){
                if(r.message === 1){
                    console.log("hello")
                    cur_frm.get_field("items").grid.editable_fields = [
                        {fieldname : 'item_name' , columns : 6},
                        {fieldname : 'rate' , columns : 4}
                    ]

                    // cur_frm.set_df_property("get_items_from_supplier_quotation","hidden","0");
                    cur_frm.set_df_property("get_items_from_material_request","hidden","0");

                    const main_doc = [ "apply_tds", "tax_withholding_category", "company", "schedule_date", "order_confirmation_no", "order_confirmation_date", "amended_from", "drop_ship", "customer", "customer_name", "customer_contact_person", "customer_contact_display", "customer_contact_mobile", "customer_contact_email", "section_addresses", "supplier_address", "supplier_gstin", "address_display", "contact_person", "contact_display", "contact_mobile", "contact_email", "shipping_address", "place_of_supply", "shipping_address_display", "company_gstin", "billing_address", "billing_address_display", "currency_and_price_list", "conversion_rate", "price_list_currency", "plc_conversion_rate", "ignore_pricing_rule", "sec_warehouse", "is_subcontracted", "col_break_warehouse", "supplier_warehouse", "before_items_section", "scan_barcode", "base_total", "base_net_total", "total_net_weight", "net_total", "pricing_rules", "raw_material_details", "set_reserve_warehouse", "supplied_items", "tax_category", "shipping_rule", "taxes_and_charges", "taxes", "sec_tax_breakup", "other_charges_calculation", "totals", "base_taxes_and_charges_added", "base_taxes_and_charges_deducted", "base_total_taxes_and_charges", "taxes_and_charges_added", "taxes_and_charges_deducted", "total_taxes_and_charges", "discount_section", "apply_discount_on", "base_discount_amount", "additional_discount_percentage", "discount_amount", "totals_section", "base_grand_total", "base_rounding_adjustment", "base_in_words", "base_rounded_total", "grand_total", "rounding_adjustment", "rounded_total", "disable_rounded_total", "in_words", "advance_paid", "payment_schedule_section", "payment_terms_template", "payment_schedule", "tracking_section", "status", "per_billed", "per_received", "terms_section_break", "tc_name", "terms", "column_break5", "letter_head", "select_print_heading", "language", "group_same_items", "subscription_section", "from_date", "to_date", "auto_repeat", "update_auto_repeat_reference", "more_info", "ref_sq", "column_break_74", "party_account_currency", "is_internal_supplier", "represents_company", "inter_company_order_reference"]
                    main_doc.forEach(function(entry){
                        cur_frm.set_df_property(entry,"hidden","1")
                    })                   
                    

                    const child_table = ["uom","supplier_part_no", "product_bundle", "schedule_date", "expected_delivery_date", "description", "gst_hsn_code", "is_nil_exempt", "is_non_gst", "conversion_factor", "stock_qty", "price_list_rate", "last_purchase_rate", "base_price_list_rate", "discount_and_margin_section", "margin_type", "margin_rate_or_amount", "rate_with_margin", "discount_percentage", "discount_amount", "base_rate_with_margin", "amount", "item_tax_template", "base_amount", "pricing_rules", "stock_uom_rate", "is_free_item", "net_rate", "net_amount", "base_net_rate", "base_net_amount", "warehouse_and_reference", "warehouse", "actual_qty", "company_total_stock", "material_request", "material_request_item", "sales_order", "sales_order_item", "sales_order_packed_item", "supplier_quotation", "supplier_quotation_item", "delivered_by_supplier", "against_blanket_order", "blanket_order", "blanket_order_rate", "item_group", "brand", "received_qty", "returned_qty", "billed_amt", "accounting_details", "expense_account", "manufacture_details", "manufacturer", "manufacturer_part_no", "bom", "include_exploded_items", "item_weight_details", "weight_per_unit", "total_weight", "weight_uom", "accounting_dimensions_section", "project", "cost_center", "is_fixed_asset", "item_tax_rate", "production_plan", "production_plan_item", "production_plan_sub_assembly_item", "page_break"]
                    child_table.forEach(function(entry){
                        var df=frappe.meta.get_docfield("Purchase Order Item", entry ,frm.doc.name);
                        df.hidden=1;
                    })
                    frm.refresh_fields();
                }
            }
        })
    },
    get_items_from_supplier_quotation:function(frm){
        if (!frm.doc.supplier) {
            frappe.throw({
                title: __("Mandatory"),
                message: __("Please Select a Supplier")
            });
        }
        erpnext.utils.map_current_doc({
            method: "erpnext.buying.doctype.supplier_quotation.supplier_quotation.make_purchase_order",
            source_doctype: "Supplier Quotation",
            target: me.frm,
            setters: {
                supplier: me.frm.doc.supplier,
                valid_till: undefined
            },
            get_query_filters: {
                docstatus: 1,
                status: ["not in", ["Stopped", "Expired"]],
            }
        })
    },
    get_items_from_material_request:function(frm){
        if (!frm.doc.supplier) {
            frappe.throw({
                title: __("Mandatory"),
                message: __("Please Select a Supplier")
            });
        }
        erpnext.utils.map_current_doc({
            method: "erpnext.stock.doctype.material_request.material_request.make_purchase_order",
            source_doctype: "Material Request",
            target: me.frm,
            setters: {
                schedule_date: undefined,
                status: undefined
            },
            get_query_filters: {
                material_request_type: "Purchase",
                docstatus: 1,
                status: ["!=", "Stopped"],
                per_ordered: ["<", 100],
                company: me.frm.doc.company,
            },
            allow_child_item_selection: true,
            child_fielname: "items",
            child_columns: ["item_code", "qty"]
        });
    }
})
frappe.ui.form.on("Purchase Order Item",{
    form_render:function(frm){
        var df = frappe.meta.get_docfield("Purchase Order Item","description",frm.doc.name)
        df.hidden=1;
        cur_frm.refresh_fields();
    }
})