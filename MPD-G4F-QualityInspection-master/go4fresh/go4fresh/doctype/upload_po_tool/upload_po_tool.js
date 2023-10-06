// Copyright (c) 2022, Mannlowe Information Services Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Upload PO Tool', {
	// refresh: function(frm) {
	// 	frm.get_field("preview_html").$wrapper.html(`<div class="img_preview">
	// 		<img class="img-responsive" src="${frm.doc.file_url}" onerror="cur_frm.toggle_display('preview', false)" />
	// 	</div>`);		
	// },
	attach_pdf_or_image:function(frm){
		frm.set_df_property("upload","hidden",0)
		frm.save();
	},
	upload:function(frm){
		frappe.call({
			method:"upload_data",
			doc:frm.doc,
			callback:function(r){
				// console.log("done")
				frm.set_df_property("upload","hidden",1)
			}
		})
	},
	// sample:function(frm){
	// 	var data = {
	// 		"belongs_to": "Go4Fresh",
	// 		"unique_document_id": "Go4Fresh",
	// 		"document_type": "Receipt",
	// 		"created_at": "2022-04-13T16:18:45.491095+05:30",
	// 		"id": 309,
	// 		"image": "/media/images/sds_image_3090j1mnf.jpg",
	// 		"status": "Processed",
	// 		"sync_status": "Not Attempted",
	// 		"sync_details": {
	// 			"docname":"POT-22-00003"},
	// 		"misc_data": {
	// 			"po_date": "2022-04-15T02:52:00",
	// 			"po_number": "1459510000782",
	// 			"net_amount": 14247.0,
	// 			"po_bar_code": "1459510000782",
	// 			"po_currency": "INR",
	// 			"customer_cin": "U51909DL2015FTC285808",
	// 			"customer_pan": "AADCH7038R",
	// 			"total_amount": 14247.0,
	// 			"customer_name": "HANDS ON TRADES PRIVATE LIMITED",
	// 			"payment_terms": ":7",
	// 			"customer_contact": "7304500852",
	// 			"po_delivery_date": "2022-04-17T23:59:00",
	// 			"total_line_items": "27",
	// 			"customer_contact_person": "PAN",
	// 			"customer_shipping_address": "Super Store Pune F&V CPC (HOT) HANDS ON TRADES PRIVATE LIMITED, A/P Sate, Vadgaon, Pune Mumbai Highway, NH-4, Tal.Maval, Distt, Pune, 412106"
	// 		},
	// 		"table_data": [
	// 			{
	// 				"id": 1900,
	// 				"parent_document": 309,
	// 				"data": {
	// 					"quantity": 39,
	// 					"item_code": "1001143",
	// 					"total_amount": 390.0,
	// 					"basic_cost_price": 10.0,
	// 					"product_description": "Beetroot (Chukan dar)"
	// 				},
	// 				"received": "true"
	// 			},
	// 			{
	// 				"id": 1901,
	// 				"parent_document": 309,
	// 				"data": {
	// 					"quantity": 31,
	// 					"item_code": "10098514",
	// 					"total_amount": 775.0,
	// 					"basic_cost_price": 25.0,
	// 					"product_description": "gm) Lady Finger - Organica grown"
	// 				},
	// 				"received": "true"
	// 			},
	// 			{
	// 				"id": 1902,
	// 				"parent_document": 309,
	// 				"data": {
	// 					"quantity": 86,
	// 					"item_code": "1006522",
	// 					"total_amount": 1032.0,
	// 					"basic_cost_price": 12.0,
	// 					"product_description": "Chilli (100 g"
	// 				},
	// 				"received": "true"
	// 			},
	// 			{
	// 				"id": 1903,
	// 				"parent_document": 309,
	// 				"data": {
	// 					"quantity": 6,
	// 					"item_code": "10075157",
	// 					"total_amount": 132.0,
	// 					"basic_cost_price": 22.0,
	// 					"product_description": "Fenugre ( Methi ) - Organica Ily Grown - Exclusiv e Offer (250 g)"
	// 				},
	// 				"received": "true"
	// 			},
	// 			{
	// 				"id": 1904,
	// 				"parent_document": 309,
	// 				"data": {
	// 					"quantity": 22,
	// 					"item_code": "10004111",
	// 					"total_amount": 374.0,
	// 					"basic_cost_price": 17.0,
	// 					"product_description": "Varikatri Brinjal (500 gm"
	// 				},
	// 				"received": "true"
	// 			},
	// 			{
	// 				"id": 1905,
	// 				"parent_document": 309,
	// 				"data": {
	// 					"quantity": 17,
	// 					"item_code": "10098515",
	// 					"total_amount": 765.0,
	// 					"basic_cost_price": 45.0,
	// 					"product_description": "Lemon Organica grown 250 g)"
	// 				},
	// 				"received": "true"
	// 			},
	// 			{
	// 				"id": 1906,
	// 				"parent_document": 309,
	// 				"data": {
	// 					"quantity": 17,
	// 					"item_code": "10098516",
	// 					"total_amount": 357.0,
	// 					"basic_cost_price": 21.0,
	// 					"product_description": "Onion - Organica Ily grown (500 g)"
	// 				},
	// 				"received": "true"
	// 			},
	// 			{
	// 				"id": 1907,
	// 				"parent_document": 309,
	// 				"data": {
	// 					"quantity": 8,
	// 					"item_code": "10098510",
	// 					"total_amount": 176.0,
	// 					"basic_cost_price": 22.0,
	// 					"product_description": "Gree Cucumb er - Organica"
	// 				},
	// 				"received": "true"
	// 			},
	// 			{
	// 				"id": 1908,
	// 				"parent_document": 309,
	// 				"data": {
	// 					"quantity": 20,
	// 					"item_code": "10098",
	// 					"total_amount": 360.0,
	// 					"basic_cost_price": 18.0,
	// 					"product_description": "Ily grown (500 g) French Beans - Organica"
	// 				},
	// 				"received": "true"
	// 			},
	// 			{
	// 				"id": 1909,
	// 				"parent_document": 309,
	// 				"data": {
	// 					"quantity": 21,
	// 					"item_code": "10098512",
	// 					"total_amount": 168.0,
	// 					"basic_cost_price": 3.0,
	// 					"product_description": "(250 g) Garlic - Srg Organica grown"
	// 				},
	// 				"received": "true"
	// 			},
	// 			{
	// 				"id": 1910,
	// 				"parent_document": 309,
	// 				"data": {
	// 					"quantity": 21,
	// 					"item_code": "10098513",
	// 					"total_amount": 231.0,
	// 					"basic_cost_price": 11.0,
	// 					"product_description": "Ginger (Adtak) - Organica Ily grown 100 g)"
	// 				},
	// 				"received": "true"
	// 			},
	// 			{
	// 				"id": 1911,
	// 				"parent_document": 309,
	// 				"data": {
	// 					"quantity": 45,
	// 					"item_code": "1000405",
	// 					"total_amount": 720.0,
	// 					"basic_cost_price": 16.0,
	// 					"product_description": "Bottle Gourd 1 unit Lauki) (400- 600 gm)"
	// 				},
	// 				"received": "true"
	// 			},
	// 			{
	// 				"id": 1912,
	// 				"parent_document": 309,
	// 				"data": {
	// 					"quantity": 12,
	// 					"item_code": "10078",
	// 					"total_amount": 216.0,
	// 					"basic_cost_price": 18.0,
	// 					"product_description": "Raw Papaya (1 unit (400 g - 600 g))"
	// 				},
	// 				"received": "true"
	// 			},
	// 			{
	// 				"id": 1913,
	// 				"parent_document": 309,
	// 				"data": {
	// 					"quantity": 30,
	// 					"item_code": "10094647",
	// 					"total_amount": 540.0,
	// 					"basic_cost_price": 18.0,
	// 					"product_description": "White Cucumb er (500 g)"
	// 				},
	// 				"received": "true"
	// 			},
	// 			{
	// 				"id": 1914,
	// 				"parent_document": 309,
	// 				"data": {
	// 					"quantity": 40,
	// 					"item_code": "10004983",
	// 					"total_amount": 1480.0,
	// 					"basic_cost_price": 37.0,
	// 					"product_description": "Papaya 10.75- 1.25 kall"
	// 				},
	// 				"received": "true"
	// 			},
	// 			{
	// 				"id": 1915,
	// 				"parent_document": 309,
	// 				"data": {
	// 					"quantity": 39,
	// 					"item_code": "252",
	// 					"total_amount": 780.0,
	// 					"basic_cost_price": 20.0,
	// 					"product_description": "Green (250 g)"
	// 				},
	// 				"received": "true"
	// 			},
	// 			{
	// 				"id": 1916,
	// 				"parent_document": 309,
	// 				"data": {
	// 					"quantity": 11,
	// 					"item_code": "10098499",
	// 					"total_amount": 286.0,
	// 					"basic_cost_price": 26.0,
	// 					"product_description": "Bitter Gourd (Karela)"
	// 				},
	// 				"received": "true"
	// 			},
	// 			{
	// 				"id": 1917,
	// 				"parent_document": 309,
	// 				"data": {
	// 					"quantity": 20,
	// 					"item_code": "10098498",
	// 					"total_amount": 320.0,
	// 					"basic_cost_price": 16.0,
	// 					"product_description": "Organica grown 250 g Beetroot (Chukan dar)- Organica HYOW grown 250 g)"
	// 				},
	// 				"received": "true"
	// 			},
	// 			{
	// 				"id": 1918,
	// 				"parent_document": 309,
	// 				"data": {
	// 					"quantity": 12,
	// 					"item_code": "10017850",
	// 					"total_amount": 336.0,
	// 					"basic_cost_price": 28.0,
	// 					"product_description": "Potato - Organica Ily Grown (1 kg)"
	// 				},
	// 				"received": "true"
	// 			},
	// 			{
	// 				"id": 1919,
	// 				"parent_document": 309,
	// 				"data": {
	// 					"quantity": 62,
	// 					"item_code": "10061325",
	// 					"total_amount": 496.0,
	// 					"basic_cost_price": 8.0,
	// 					"product_description": "Ginger Adrak) 250 g"
	// 				},
	// 				"received": "true"
	// 			},
	// 			{
	// 				"id": 1920,
	// 				"parent_document": 309,
	// 				"data": {
	// 					"quantity": 32,
	// 					"item_code": "10098521",
	// 					"total_amount": 704.0,
	// 					"basic_cost_price": 22.0,
	// 					"product_description": "Green Peas - Organica Ily growIn"
	// 				},
	// 				"received": "true"
	// 			},
	// 			{
	// 				"id": 1921,
	// 				"parent_document": 309,
	// 				"data": {
	// 					"quantity": 23,
	// 					"item_code": "10098520",
	// 					"total_amount": 506.0,
	// 					"basic_cost_price": 22.0,
	// 					"product_description": "Tomato Organica Ily grown (500 a)"
	// 				},
	// 				"received": "true"
	// 			},
	// 			{
	// 				"id": 1922,
	// 				"parent_document": 309,
	// 				"data": {
	// 					"quantity": 25,
	// 					"item_code": "10098509",
	// 					"total_amount": 400.0,
	// 					"basic_cost_price": 16.0,
	// 					"product_description": "Chilli - Organica Ily grown"
	// 				},
	// 				"received": "true"
	// 			},
	// 			{
	// 				"id": 1923,
	// 				"parent_document": 309,
	// 				"data": {
	// 					"quantity": 11,
	// 					"item_code": "10004205",
	// 					"total_amount": 132.0,
	// 					"basic_cost_price": 12.0,
	// 					"product_description": "Spinach (Palak) - Organica HYOWI grown"
	// 				},
	// 				"received": "true"
	// 			},
	// 			{
	// 				"id": 1924,
	// 				"parent_document": 309,
	// 				"data": {
	// 					"quantity": 25,
	// 					"item_code": "10096625",
	// 					"total_amount": 1075.0,
	// 					"basic_cost_price": 13.0,
	// 					"product_description": "Guava Premium (500 g)"
	// 				},
	// 				"received": "true"
	// 			},
	// 			{
	// 				"id": 1925,
	// 				"parent_document": 309,
	// 				"data": {
	// 					"quantity": 28,
	// 					"item_code": "10007292",
	// 					"total_amount": 560.0,
	// 					"basic_cost_price": 20.0,
	// 					"product_description": "Ash Gourd (Petha) 500 g)"
	// 				},
	// 				"received": "true"
	// 			},
	// 			{
	// 				"id": 1926,
	// 				"parent_document": 309,
	// 				"data": {
	// 					"quantity": 26,
	// 					"item_code": "1001866",
	// 					"total_amount": 936.0,
	// 					"basic_cost_price": 36.0,
	// 					"product_description": "Papaya Organica Grown (1 unit (900 g - 1.1 kg))"
	// 				},
	// 				"received": "true"
	// 			}
	// 		]
	// 	}
		
	// 	frappe.call({
	// 		"method":"go4fresh.api.create_so",
	// 		args: {
	// 			data : data,
	// 		},
	// 		callback:function(r){
	// 			console.log("Done")
	// 		}
	// 	})
	// },
	upload_in_so:function(frm){
		frappe.call({
			method:"update_info",
			doc:frm.doc,
			callback:function(r){
				frm.refresh_field("not_found_items");
				frm.refresh_field("found_items");

				if(r.message){
					frappe.confirm(
						'Are you sure you have to update Sales Order '+frm.doc.so_no+' with '+r.message+' ?',
						
						function(){
							console.log("confirmed")
							frappe.call({
								method:"update_so",
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
frappe.ui.form.on("Upload Items", "item", function(frm, cdt, cdn){
    var child = locals[cdt][cdn];
    frappe.call({
        method: "frappe.client.get",
        args: {
            doctype: "Item",
            name: child.item,
        },
        callback(r) {
			frm.refresh_field("not_found_items");
			frm.refresh_field("found_items");
        }
    });
});