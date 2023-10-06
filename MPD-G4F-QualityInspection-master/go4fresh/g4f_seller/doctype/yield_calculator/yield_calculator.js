// Copyright (c) 2022, Mannlowe Information Services Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Yield Calculator', {
	crop: function(frm) {
		if(frm.doc.crop){
			frappe.db.get_value('G4F Crop List', frm.doc.crop, 'tentative_yield_kgha')
				.then(r => {
					frm.set_value("seed_yield",r.message.tentative_yield_kgha);
					frm.refresh_field("seed_yield");
				})
		}
	},
	area: function(frm){
		if(frm.doc.seed_yield){
			if(frm.doc.area!=0){
				frm.set_value("estimated_yield",(frm.doc.area*0.404686)*frm.doc.seed_yield);
				frm.refresh_field("estimated_yield");
				frm.set_value("average_pricekg",12.50);
				frm.refresh_field("average_pricekg");
				frm.set_value("total_sales",(frm.doc.average_pricekg*frm.doc.estimated_yield))
				frm.refresh_field("total_sales")
			}
		}
	}
});
