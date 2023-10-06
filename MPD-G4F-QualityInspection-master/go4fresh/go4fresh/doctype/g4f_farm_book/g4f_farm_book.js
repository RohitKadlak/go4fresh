// Copyright (c) 2022, Mannlowe Information Services Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('G4F Farm Book', {
	// refresh: function(frm) {

	// }
	seller:function(frm){
		if(frm.doc.seller){
			// frappe.model.get_value('Supplier', {'name': frm.doc.supplier}, 'supplier_name', function(d) { 
			// 	frm.set_value("supplier_name",d.supplier_name)
			// 	frm.refresh_field("supplier_name")
			// })
			frappe.call({
				method:"set_supplier_name",
				doc:frm.doc,
				callback:function(r){
					if(r.message === "Done"){
						frm.refresh_field("seller_name")
					}
				}
			})
			frappe.call({
				method:"get_address",
				doc:frm.doc,
				callback:function(r){
					var address = r.message
					if(address){
						frm.set_value("seller_address",address.name)
						frm.refresh_field("seller_address")

						if(address.name)
						{
							frappe.call({
								method: "frappe.contacts.doctype.address.address.get_address_display",
								args:{
									"address_dict": address.name
								},
								callback: function(r) {
									if(r.message){
										frm.set_value("address_display", r.message);							   
									}
								}
							});
						}
					}
				}
			})
		}
	},
	before_save:function(frm){
		if(frm.doc.g4f_farm_book_activities){
			var sum = 0;
			frm.doc.g4f_farm_book_activities.forEach(function(item){
				sum += item.amount;
			});
			frm.set_value("total_cost",sum)
			frm.refresh_field("total_cost")
		}
	}
});
