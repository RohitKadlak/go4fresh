// Copyright (c) 2022, Mannlowe Information Services Pvt. Ltd. and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["G4F Purchase Order Analysis"] = {
	"filters": [
		{
			"fieldname": "created_from",
			"label": __("Created From"),
			"fieldtype": "Date",
			"width": "80"
		},
		{
			"fieldname": "created_to",
			"label": __("Created To"),
			"fieldtype": "Date",
			"width": "80"
		},
		{
			"fieldname": "modified_from",
			"label": __("Modified From"),
			"fieldtype": "Date",
			"width": "80"
		},
		{
			"fieldname": "modified_to",
			"label": __("Modified To"),
			"fieldtype": "Date",
			"width": "80"
		},
		{
			"fieldname": "company",
			"label": __("Company"),
			"fieldtype": "Link",
			"width": "80",
			"options": "Company",
			"reqd": 1,
			"default": frappe.defaults.get_default("company")
		},
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"width": "80",
			"reqd": 1,
			"default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"width": "80",
			"reqd": 1,
			"default": frappe.datetime.get_today()
		},
		{
			"fieldname": "purchase_order",
			"label": __("Purchase Order"),
			"fieldtype": "Link",
			"width": "80",
			"options": "Purchase Order"
		},
		{
			"fieldname": "supplier",
			"label": __("Supplier"),
			"fieldtype": "Link",
			"width": "80",
			"options": "Supplier"
		},
		{
			"fieldname": "item_code",
			"label": __("Item Code"),
			"fieldtype": "Link",
			"width": "80",
			"options": "Item"
		},
		{
			"fieldname": "sales_order",
			"label": __("Sales Order"),
			"fieldtype": "Link",
			"width": "80",
			"options": "Sales Order"
		},
		{
			"fieldname": "purchase_receipt",
			"label": __("Purchase Receipt Return"),
			"fieldtype": "Link",
			"width": "80",
			"options": "Purchase Receipt",
			"get_query": () =>{
				return {
					filters: { "is_return": 1 }
				}
			}
		},
	]
};
