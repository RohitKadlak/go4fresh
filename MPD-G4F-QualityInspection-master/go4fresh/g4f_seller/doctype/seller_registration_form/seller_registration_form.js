// Copyright (c) 2022, Mannlowe Information Services Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Seller Registration Form', {
	refresh: function(frm) {
		if(frm.doc.supplier){
			$('.btn-supplier').hide();
		}
		$('.btn-supplier').on('click', function () {
			frappe.call({
				method:"supplier_automation",
				doc:frm.doc,
				callback:function(r){
					if(r.message){
						var res = r.message;
						if(res.supplier){
							frm.doc.supplier=res.supplier;
							frm.refresh_field("supplier");
						}
						if(res.user){
							frm.doc.user=res.user;
							frm.refresh_field("user");
						}
						frm.save();
					}
				}
			})
		})
		$('.btn-user').on('click', function () {
			frappe.call({
				method:"aggre_automation",
				doc:frm.doc,
				callback:function(r){
					if(r.message){
						var res = r.message;
						// if(res.supplier){
						// 	frm.doc.supplier=res.supplier;
						// 	frm.refresh_field("supplier");
						// }
						if(res.user){
							frm.doc.user=res.user;
							frm.refresh_field("user");
						}
						frm.save();
					}
				}
			})
		})
	}
});
