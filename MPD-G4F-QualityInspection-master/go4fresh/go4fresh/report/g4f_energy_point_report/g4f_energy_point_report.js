// Copyright (c) 2022, Mannlowe Information Services Pvt. Ltd. and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["G4F Energy Point Report"] = {
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
			"fieldname": "user",
			"label": __("User"),
			"fieldtype": "Link",
			"width": "80",
			"options": "User"
		},
		{
			"fieldname": "rule",
			"label": __("Rule"),
			"fieldtype": "Link",
			"width": "80",
			"options": "Energy Point Rule"
		},
	]
};
