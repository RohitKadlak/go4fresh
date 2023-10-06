// Copyright (c) 2022, Mannlowe Information Services Pvt. Ltd. and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["G4F Sell Your Produce Report"] = {
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
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"width": "80"
		},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"width": "80"
		},
		{
			"fieldname": "check_date",
			"label": __("Check for particular Date"),
			"fieldtype": "Date",
			"width": "80"
		},
		{
			"fieldname": "crop",
			"label": __("Crop"),
			"fieldtype": "Link",
			"width": "80",
			"options": "G4F Crop List"
		},
		{
			"fieldname": "supplier",
			"label": __("Seller"),
			"fieldtype": "Link",
			"width": "80",
			"options": "Supplier"
		}
	]
};
