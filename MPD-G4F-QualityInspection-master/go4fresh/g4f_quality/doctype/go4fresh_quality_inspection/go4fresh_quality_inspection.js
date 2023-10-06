// Copyright (c) 2022, Mannlowe Information Services Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.provide("location")
frappe.ui.form.on('Go4Fresh Quality Inspection', {
	before_load:function(frm){

		if(frm.doc.docstatus != 1 && !frm.doc.amended_from){
			var a=["total_samples","qi_sample","lot_no","total_gross_weight","total_defect","average_defect"]
			a.forEach(function(entry){
				frm.set_df_property(entry,"hidden","1")
			})
			frm.disable_save();
		}
	},
	
	enter_sample_data:function(frm){
		if(frm.doc.product_name){
			frm.save()
			var det = ["consignee_name","vehicle_no","container_no","no_of_bags","cluster","order_size","order_packing_size","packaging_bag","pulp_temp","remarks","grn_number","grn_quantity","vendor_name","lot_no","sowing_date","days_since_sowing","select_destination","source_address","destination_address","distance_between_source_and_destination","receipt_date","inspection_date","qc_officer","supervisor","enter_sample_data","color","texture","patti_dry_layer","machanical_damage","test","product_type","dry_roots_available"]
			det.forEach(function(entry){
				frm.set_df_property(entry,"hidden","1")
			})
			if(frm.doc.product_name==="Onion"){
				var sam = ["attach_image","product_image","done","sample_details","product_name","submit_sample","create_new_lot","package_size_for_sampling","gross_weight","net_weightkg","size","small_size","without_pattikg","black_smugs","dry_roots","injury","rotten","sprouting"];
				sam.forEach(function(entry){
					frm.set_df_property(entry,"hidden","0")
				})
			}else if(frm.doc.product_name==="Watermelon"){
				var sam = ["attach_image","product_image","done","sample_details","product_name","submit_sample","create_new_lot","minimum_weight","shape","outer_color","whitish_power_texture_present","outer_skin_is_thick_and_tight","pulp_colour","fly_infestation","physical_damage","sunburnt","bottle_shape","caterpillar_infestaion_patches"];
				sam.forEach(function(entry){
					frm.set_df_property(entry,"hidden","0")
				})
			}else{
				frappe.throw("Product Not Found...")
			}
			frm.disable_save();
		}else{
			frappe.throw("Please Select Product....")
		}
	},
	
	refresh:function(frm){

		set_css(frm);

		if(frm.doc.name){
			frm.set_value("lot_no",frm.doc.name)
			frm.refresh_field("lot_no")
			
			if(frm.doc.qi_sample){
				frm.set_value("sample_no",frm.doc.qi_sample.length+1);
			}else{
				frm.set_value("sample_no",1);
			}
			frm.refresh_field("sample_no");
			
			var sample_details = "Lot - " + frm.doc.name + ' Sample - ' + frm.doc.sample_no.toString();
			frm.set_value("sample_details",sample_details)
			frm.refresh_field("sample_details")
		}
	},
	
	submit_sample:function(frm){	
		if(frm.doc.product_name==="Onion"){	
			var d = frm.doc
			var row = frm.add_child("qi_sample");
			row.lot_no = d.lot_no
			row.sample_no = d.sample_no 
			row.sample_details = d.sample_details 
			row.product_name = d.product_name 
			row.attach_image = d.attach_image
			
			row.package_size_for_sampling = d.package_size_for_sampling
			row.gross_weight = d.gross_weight 
			row.net_weightkg = d.net_weightkg
			row.size = d.size
			row.without_patti = d.without_pattikg
			row.rotten = d.rotten
			row.injury = d.injury
			row.dry_roots = d.dry_roots
			row.black_smugs = d.black_smugs
			row.sprouting = d.sprouting
			row.small_size = d.small_size

			row.injury_in_percentage = (d.injury/d.gross_weight)*100 
			row.without_patti_in_percentage = (d.without_pattikg/d.gross_weight)*100
			row.rotten_in_percentage = (d.rotten/d.gross_weight)*100
			row.dry_roots_in_percentage = (d.dry_roots/d.gross_weight)*100
			row.black_smugs_in_percentage = (d.black_smugs/d.gross_weight)*100 
			row.sprouting_in_percentage = (d.sprouting/d.gross_weight)*100 
			row.small_size_in_percentage = (d.small_size/d.gross_weight)*100 
			row.total_defects = d.without_pattikg + d.injury + d.dry_roots + d.rotten + d.black_smugs + d.sprouting + d.small_size
			row.total_defects_percentage = ((d.without_pattikg + d.injury + d.dry_roots + d.rotten + d.black_smugs + d.sprouting + d.small_size)/d.gross_weight)*100
			
			frm.refresh_field("qi_sample");
			
			frm.save();

			frm.set_value("sample_no","");
			frm.set_value("package_size_for_sampling","")
			frm.set_value("attach_image","");
			frm.set_value("size","");
			frm.set_value("sample_details","")
			frm.set_value("gross_weight",1.0);
			frm.set_value("net_weightkg",0.0);
			frm.refresh_field("net_weightkg");
			frm.refresh_field("package_size_for_sampling")
			frm.refresh_field("attach_image");
			frm.refresh_field("gross_weight");
			frm.refresh_field("size");
			frm.refresh_field("sample_no");
			frm.refresh_field("sample_details");

			var sam = ["rotten","dry_roots","size","injury","black_smugs","sprouting","small_size","without_pattikg"];
			sam.forEach(function(entry){
				frm.set_value(entry,"");
				frm.refresh_field(entry)
			})
		}else if(frm.doc.product_name==="Watermelon"){
			var d = frm.doc
			var row = frm.add_child("qi_sample");

			var data = ["lot_no","sample_no","attach_image","sample_details","product_name","minimum_weight","shape","outer_color","whitish_power_texture_present","outer_skin_is_thick_and_tight","pulp_colour","fly_infestation","physical_damage","sunburnt","bottle_shape","caterpillar_infestaion_patches"]
			data.forEach(function(entry){
				row[entry] = d[entry]
			})
			frm.refresh_field("qi_sample");
			frm.save();
			var data1=["sample_no","attach_image","sample_details","shape","outer_color","whitish_power_texture_present","outer_skin_is_thick_and_tight","pulp_colour","fly_infestation","physical_damage","sunburnt","bottle_shape"]
			data1.forEach(function(entry){
				frm.set_value(entry,"");
				frm.refresh_field(entry);
			})
			var data2 = ["minimum_weight","caterpillar_infestaion_patches"]
			data2.forEach(function(entry){
				frm.set_value(entry,0.0);
				frm.refresh_field(entry);
			})
		}else{
			frappe.throw("Please Select Product...")
		}

		
		if(frm.doc.qi_sample){
			frm.set_value("sample_no",frm.doc.qi_sample.length+1);
		}else{
			frm.set_value("sample_no",1);
		}
		frm.refresh_field("sample_no");
		
		var sample_details = "lot - " + frm.doc.name + " sample - " + frm.doc.sample_no.toString();
		frm.set_value("sample_details",sample_details)
		frm.refresh_field("sample_details")
	},
	create_new_lot:function(frm){
		frappe.confirm(__("Do you really want to create New Lot?"), 
		function () {
			if(frm.doc.product_name==="Onion"){
				var det = ["consignee_name","vehicle_no","container_no","no_of_bags","pulp_temp","remarks","grn_number",
					"grn_quantity",
					"vendor_name",
					"lot_no",
					"sowing_date","days_since_sowing","select_destination","source_address","destination_address","distance_between_source_and_destination",
					"receipt_date",
					"inspection_date",
					"qc_officer",
					"supervisor",
				]
				det.forEach(function(entry){
					frm.set_df_property(entry,"hidden","0")
					frm.set_df_property(entry,"read_only","1")
				})
				var sam = ["attach_image","product_image","done","sample_details","product_name","submit_sample","create_new_lot","gross_weight","package_size_for_sampling","net_weightkg","without_pattikg","rotten","dry_roots","size","injury","black_smugs","sprouting","small_size","submit_sample","create_new_lot"];
				sam.forEach(function(entry){
					frm.set_df_property(entry,"hidden","1")
					frm.set_df_property(entry,"read_only","1")
				})
				frm.set_df_property("qi_sample","hidden","0")
				frm.set_df_property("total_samples","hidden","0")
				frm.set_df_property("total_gross_weight","hidden","0")
				frm.set_df_property("total_defect","hidden","0")
				frm.set_df_property("average_defect","hidden","0")
				// frm.save()
				frappe.call({
					"method": "frappe.client.submit",
					"args": {
						"doctype": "Go4Fresh Quality Inspection",
						"doc": frm.doc
					},
					callback:function(r){
						if(r.message){
							frm.reload_doc();
							frm.refresh();
						}
					}
				})
			}else if(frm.doc.product_name==="Watermelon"){
				var det = ["consignee_name","vehicle_no","container_no","no_of_bags","grn_number",
					"grn_quantity",
					"vendor_name",
					"lot_no",
					"sowing_date","days_since_sowing","select_destination","source_address","destination_address","distance_between_source_and_destination",
					"receipt_date",
					"inspection_date",
					"qc_officer",
					"supervisor",
				]
				det.forEach(function(entry){
					frm.set_df_property(entry,"hidden","0")
					frm.set_df_property(entry,"read_only","1")
				})
				var sam = ["sample_no","attach_image","product_image","sample_details","shape","outer_color","whitish_power_texture_present","outer_skin_is_thick_and_tight","pulp_colour","fly_infestation","physical_damage","sunburnt","bottle_shape","caterpillar_infestaion_patches","minimum_weight"]
				sam.forEach(function(entry){
					frm.set_df_property(entry,"hidden","1")
					frm.set_df_property(entry,"read_only","1")
				})
				frm.set_df_property("qi_sample","hidden","0")
				frappe.call({
					"method": "frappe.client.submit",
					"args": {
						"doctype": "Go4Fresh Quality Inspection",
						"doc": frm.doc
					},
					callback:function(r){
						if(r.message){
							frm.reload_doc();
							frm.refresh();
						}
					}
				})
			}else{
				frappe.throw("Please Select Product...")
			}
			frappe.new_doc("Go4Fresh Quality Inspection",{"inspection_date":frappe.datetime.get_today()})
		},
		function (){
			frappe.show_alert("OK")
		})
	},

	done:function(frm){
		if(frm.doc.product_name==="Onion"){
			// var det = ["consignee_name","vehicle_no","container_no","no_of_bags","grn_number",
			// 	"grn_quantity",
			// 	"vendor_name",
			// 	"lot_no",
			// 	"sowing_date","days_since_sowing","select_destination","source_address","destination_address","distance_between_source_and_destination",
			// 	"receipt_date",
			// 	"inspection_date",
			// 	"qc_officer",
			// 	"supervisor",
			// ]
			var det = ["consignee_name","vehicle_no","container_no","no_of_bags","cluster","order_size","order_packing_size","packaging_bag","pulp_temp","remarks","grn_number","grn_quantity","vendor_name","lot_no","sowing_date","days_since_sowing","select_destination","source_address","destination_address","distance_between_source_and_destination","receipt_date","inspection_date","qc_officer","supervisor","enter_sample_data","color","texture","patti_dry_layer","machanical_damage","test","product_type","dry_roots_available"]
			det.forEach(function(entry){
				frm.set_df_property(entry,"hidden","0")
				frm.set_df_property(entry,"read_only","1")
			})
			var sam = ["attach_image","product_image","done","sample_details","product_name","submit_sample","create_new_lot","gross_weight","package_size_for_sampling","net_weightkg","without_pattikg","rotten","dry_roots","size","injury","black_smugs","sprouting","small_size","submit_sample","create_new_lot"];
			sam.forEach(function(entry){
				frm.set_df_property(entry,"hidden","1")
				frm.set_df_property(entry,"read_only","1")
			})
			frm.set_df_property("qi_sample","hidden","0")
			frm.refresh_field("qi_sample");
			frm.set_df_property("total_samples","hidden","0")
			frm.set_df_property("total_gross_weight","hidden","0")
			frm.set_df_property("total_defect","hidden","0")
			frm.set_df_property("average_defect","hidden","0")
			// frm.save();
			frappe.call({
				"method": "frappe.client.submit",
				"args": {
					"doctype": "Go4Fresh Quality Inspection",
					"doc": frm.doc
				},
				callback:function(r){
					if(r.message){
						frm.reload_doc();
						frm.refresh();
					}
				}
			})
		}else if(frm.doc.product_name === "Watermelon"){
			var det = ["consignee_name","vehicle_no","container_no","no_of_bags","grn_number",
					"grn_quantity",
					"vendor_name",
					"lot_no",
					"sowing_date","days_since_sowing","select_destination","source_address","destination_address","distance_between_source_and_destination",
					"receipt_date",
					"inspection_date",
					"qc_officer",
					"supervisor",
				]
			det.forEach(function(entry){
				frm.set_df_property(entry,"hidden","0")
				frm.set_df_property(entry,"read_only","1")
			})
			var sam = ["sample_no","attach_image","product_image","sample_details","shape","outer_color","whitish_power_texture_present","outer_skin_is_thick_and_tight","pulp_colour","fly_infestation","physical_damage","sunburnt","bottle_shape","caterpillar_infestaion_patches","minimum_weight"]
			sam.forEach(function(entry){
				frm.set_df_property(entry,"hidden","1")
				frm.set_df_property(entry,"read_only","1")
			})
			frm.set_df_property("qi_sample","hidden","0")
			frm.refresh_field("qi_sample");
			frappe.call({
				"method": "frappe.client.submit",
				"args": {
					"doctype": "Go4Fresh Quality Inspection",
					"doc": frm.doc
				},
				callback:function(r){
					if(r.message){
						frm.reload_doc();
						frm.refresh();
					}
				}
			})
		}else{
			frappe.throw("Please Select Product...")
		}
	},
	sowing_date:function(frm){
		frm.set_value("days_since_sowing",frappe.datetime.get_day_diff(frm.doc.inspection_date,frm.doc.sowing_date));
		frm.refresh_field("days_since_sowing")
	},
	select_destination:function(frm){
		function getLocation() {
			if(navigator.geolocation) {
			navigator.geolocation.getCurrentPosition(showPosition);
			} else { 
			console.log("Error")
			}
		}
		
		function showPosition(position) {
			console.log(position.coords.latitude); 
			console.log(position.coords.longitude);
			var lat = position.coords.latitude
			var lng = position.coords.longitude

			fetch('http://maps.google.com/maps/api/js?sensor=false', {
				mode: 'no-cors',
				credentials: 'include'
			})
			.then(data =>{
				console.log(data)
				var geocoder = new google.maps.Geocoder();
			})
			
			// var latlng = new google.maps.LatLng(lat, lng);
			// // This is making the Geocode request
			// var geocoder = new google.maps.Geocoder();
			// geocoder.geocode({ 'latLng': latlng },  (results, status) =>{
			// 	if (status !== google.maps.GeocoderStatus.OK) {
			// 		alert(status);
			// 	}
			// 	// This is checking to see if the Geoeode Status is OK before proceeding
			// 	if (status == google.maps.GeocoderStatus.OK) {
			// 		console.log(results);
			// 		var address = (results[0].formatted_address);
			// 		frm.set_value("source_address",address);
			// 		frm.refresh_field("source_address");
			// 	}
			// });
			// function getReverseGeocodingData(lat, lng) {
			// 	// fetch('src="https://maps.google.com/maps/api/js?sensor=false"').then(result => result.json())
			// 	// fetch('https://api.opencagedata.com/geocode/v1/json?q='+latitude+'+'+longitude+'&key=de1bf3be66b546b89645e500ec3a3a28')
			// 	// 	.then(response => response.json())
			// 	// 	.then(data => {
			// 	// 		console.log(data);
			// 	// 	})
				
			// 	fetch('http://maps.googleapis.com/maps/api/geocode/json?latlng=40.714224,-73.961452&sensor=true/false').then(result => {
			// 		console.log(result);
			// 	})


				
			// }
			// getReverseGeocodingData(lat,lng);
		}
		getLocation();
	}
});

var set_css = function (frm) {
    let el = document.querySelectorAll("[data-fieldname='enter_sample_data']")[1].style.backgroundColor ="#4287f5";
    let fl = document.querySelectorAll("[data-fieldname='enter_sample_data']")[1].style.color ="white";
}