// Copyright (c) 2022, Mannlowe Information Services Pvt. Ltd. and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Delivery Note and Return Summary Report"] = {
	"filters": [
		{
			"fieldname": "created_from",
			"label": __("Created From"),
			"fieldtype": "Date",
			"width": "80",
			"default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),
		},
		{
			"fieldname": "created_to",
			"label": __("Created To"),
			"fieldtype": "Date",
			"width": "80",
			"default": frappe.datetime.get_today()
		}
	],
	"formatter": function(value, row, column, data, default_formatter) {
        value = default_formatter(value, row, column, data);
		// console.log((data.time_diff.split(":")[0]))
        // if((data.time_diff.split(":")[0])!=0){
        //     value = '<b style="color: red;">'+value+'</b>';
        // }else{
		// 	value = '<b style="color: green;">'+value+'</b>';
		// }
		// var a = frappe.db.get_value("Delivery Note",data.return_delivery_note,"posting_date")
		if(data.posting_date === data.r_posting_date){
			value = '<b style="color: green;">'+value+'</b>';
		}else{
			value = '<b style="color: red;">'+value+'</b>';
		}
        return value;
    },
};
