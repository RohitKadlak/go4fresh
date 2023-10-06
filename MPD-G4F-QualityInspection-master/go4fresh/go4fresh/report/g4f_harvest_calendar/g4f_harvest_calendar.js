// Copyright (c) 2022, Mannlowe Information Services Pvt. Ltd. and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["G4F Harvest Calendar"] = {
	"filters": [
		{
			"fieldname": "supplier",
			"label": __("Seller"),
			"fieldtype": "Link",
			"width": "80",
			"options": "Supplier"
		},
		{
			"fieldname": "crop",
			"label": __("Crop"),
			"fieldtype": "Link",
			"width": "80",
			"options": "G4F Crop List"
		},
		{
			"fieldname": "date",
			"label": __("Date"),
			"fieldtype": "Date",
			"width": "80"
		}
	]
};
