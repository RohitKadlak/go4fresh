// Copyright (c) 2022, Mannlowe Information Services Pvt. Ltd. and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["G4F Farmer Onboarding Report"] = {
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
			"fieldname": "cluster",
			"label": __("Cluster"),
			"fieldtype": "Select",
			"width": "80",
			"options": ["","Ghoti","Otur"]
		},
		{
			"fieldname": "supplier_group",
			"label": __("Supplier Group"),
			"fieldtype": "Link",
			"width": "80",
			"options": "Supplier Group"
		},
	]
};
