// Copyright (c) 2022, Mannlowe Information Services Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Excel Upload Tool', {
	extract_data: function(frm) {
		if(frm.doc.attach_pdf_or_image){
			frappe.call({
				method:"extract_data",
				doc:frm.doc,
				callback:function(r){

					frm.refresh_field("not_found_items");
					frm.refresh_field("found_items");
					// console.log("done")
					// frm.set_df_property("upload","read_only",1)
				}
			})
		}
	},
	attach_pdf_or_image:function(frm){
		frm.save();
	},
	create_quotation:function(frm){
		frappe.call({
			method:"update_info",
			doc:frm.doc,
			callback:function(r){
				frm.refresh_field("not_found_items");
				frm.refresh_field("found_items");

				if(r.message){
					frappe.confirm(
						'Are you sure you have to Create Quotation with '+r.message+' Items?',
						
						function(){
							console.log("confirmed")
							frappe.call({
								method:"create_qt",
								doc : frm.doc,
								callback:function(r){
									if(r.message){
										show_alert(r.message)
									}
								}
							})
						},
						function(){
							window.close();
						},
					)
				}
			}
		})
	}
});
