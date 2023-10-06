// Copyright (c) 2022, Mannlowe Information Services Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('G4F Crop List', {
	// refresh: function(frm) {

	// }
});
frappe.ui.form.on("G4F Sell Your Produce Item",{
	item_code:function(frm,cdt,cdn){
		var d = locals[cdt][cdn]
		if(d.item_code){
			frappe.call({
				method: "frappe.client.get",
				args: {
					doctype: "Item",
					name: d.item_code,
				},
				callback(r) {
					if(r.message) {
						var doc = r.message;
						d.item_name = doc.item_name;
						frm.refresh_field("map_items");
					}
				}
			});
		}
	}
})