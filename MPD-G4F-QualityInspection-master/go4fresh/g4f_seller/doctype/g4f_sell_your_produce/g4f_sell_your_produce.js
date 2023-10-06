// Copyright (c) 2022, Mannlowe Information Services Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('G4F Sell Your Produce', {
	supplier: function(frm) {
		if(frm.doc.supplier){
			frappe.call({
				method:"fetch_data",
				doc:frm.doc,
				callback:function(r){
					var d = r.message
					if(d)
					{
						frm.refresh_field("supplier_name");
						frm.set_value("address",d)
						return frm.call({
							method: "frappe.contacts.doctype.address.address.get_address_display",
							args: {
							   "address_dict": d
							},
							callback: function(r) {
							var l = r.message
							if(l)
								frm.set_value("address_display", l);
							   
							}
						});
					}
					else{
						frm.set_value("address_display", "");
					}					
				}
			})
		}
	},
	crop:function(frm){
		if(frm.doc.crop){
			frappe.call({
				method:"copy_data",
				doc:frm.doc,
				callback:function(r){
					frm.refresh_field("items");
				}
			})
		}
	},
	before_save:function(frm){
		if(frm.doc.supplier){
			if(!frm.doc.address){
				frappe.call({
					method:"fetch_data",
					doc:frm.doc,
					callback:function(r){
						var d = r.message
						if(d)
						{
							frm.set_value("address",d)
							return frm.call({
								method: "frappe.contacts.doctype.address.address.get_address_display",
								args: {
								   "address_dict": d
								},
								callback: function(r) {
								var l = r.message
								if(l)
									frm.set_value("address_display", l);
								   
								}
							});
						}
						else{
							frm.set_value("full_address_field", "");
						}					
					}
				})
			}
		}
		if(frm.doc.crop){
			if(!frm.doc.items){
				frappe.call({
					method:"copy_data",
					doc:frm.doc,
					callback:function(r){
						frm.refresh_field("items");
					}
				})
			}
		}
		if(frm.doc.items){
			frappe.call({
				method:"calculate",
				doc:frm.doc,
				callback:function(r){
					frm.refresh_field("total_qty");
				}
			})
		}
	}
});
