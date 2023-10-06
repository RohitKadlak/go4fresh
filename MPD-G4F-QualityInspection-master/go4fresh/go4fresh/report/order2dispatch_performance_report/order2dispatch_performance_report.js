// Copyright (c) 2022, Mannlowe Information Services Pvt. Ltd. and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Order2Dispatch Performance Report"] = {
	"filters": [
		{
			"fieldname": "sales_order",
			"label": __("Sales Order"),
			"fieldtype": "Link",
			"width": "80",
			"options": "Sales Order"
		},
	]
};
