// Copyright (c) 2022, Mannlowe Information Services Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('G4F Crop Planner', {
	// refresh: function(frm) {
	// 	if(frm.doc.crop_planner_details){
	// 		frappe.call({
	// 			method:"crop_update",
	// 			doc:frm.doc,
	// 			callback:function(r){
	// 				frm.refresh_field("crop_planner_details");
	// 				// frm.doc.reload();
	// 			}
	// 		})
	// 	}
	// },
	before_save:function(frm){
		if(frm.doc.supplier){
			frappe.call({
				method:"set_supplier_name",
				doc:frm.doc,
				callback:function(r){
					if(r.message === "Done"){
						frm.refresh_field("supplier_name")
					}
				}
			})
		}
	},
	supplier:function(frm){
		if(frm.doc.supplier){
			// frappe.model.get_value('Supplier', {'name': frm.doc.supplier}, 'supplier_name', function(d) { 
			// 	frm.set_value("supplier_name",d.supplier_name)
			// 	frm.refresh_field("supplier_name")
			// })
			frappe.call({
				method:"set_supplier_name",
				doc:frm.doc,
				callback:function(r){
					if(r.message === "Done"){
						frm.refresh_field("supplier_name")
					}
				}
			})
			frappe.call({
				method:"get_address",
				doc:frm.doc,
				callback:function(r){
					var address = r.message
					if(address){
						frm.set_value("supplier_address",address.name)
						frm.refresh_field("supplier_address")

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
	}
});
frappe.ui.form.on("G4F Crop Planner Details",{
	crop_name:function(frm,cdt,cdn){
		var d = locals[cdt][cdn]
		if(d.crop_name){
			frappe.call({
				method: "frappe.client.get",
				args: {
					doctype: "G4F Crop List",
					name: d.crop_name,
				},
				callback(r) {
					if(r.message) {
						var doc = r.message;
						d.tentative_yield_kgha = doc.tentative_yield_kgha;
						d.no_of_harvesting_or_plucking = doc.no_of_harvesting_or_plucking;
						d.number_of_harvests_per_week = doc.number_of_harvests_per_week;
						// frm.refresh_field("crop_planner_details");
						frappe.call({
							method:"get_data",
							doc:frm.doc,
							args:{"crop":d.crop_name},
							callback:function(r){
								d.frst_harvesting_or_plucking_from_planting_or_sowing_in_days = r.message;	
								d.tentative_yield_kgha = d.tentative_yield_kgha;
								d.no_of_harvesting_or_plucking = d.no_of_harvesting_or_plucking
								d.number_of_harvests_per_week = d.number_of_harvests_per_week;
								d.harvesting_or_plucking_from_planting_or_sowing = frappe.datetime.add_days(d.planting_date, d.frst_harvesting_or_plucking_from_planting_or_sowing_in_days)
								frappe.call({
									method:"cal_till_date",
									doc:frm.doc,
									args:{
										"frst_harvest":d.harvesting_or_plucking_from_planting_or_sowing,
										"total_harvest":d.no_of_harvesting_or_plucking,
										"per_week":d.number_of_harvests_per_week
									},
									callback:function(r){
										if(r.message){
											d.dates_of_harvest = r.message[0];
											d.lasts_harvesting_till = r.message[1];
											d.frst_harvesting_or_plucking_from_planting_or_sowing_in_days = d.frst_harvesting_or_plucking_from_planting_or_sowing_in_days
											d.tentative_yield_kgha = d.tentative_yield_kgha
											d.no_of_harvesting_or_plucking = d.no_of_harvesting_or_plucking
											d.number_of_harvests_per_week = d.number_of_harvests_per_week
											d.harvesting_or_plucking_from_planting_or_sowing = d.harvesting_or_plucking_from_planting_or_sowing
											frm.refresh_field("crop_planner_details");
										}
									}
								})
							}
						})
					}
				}
			});
		}
	},
	frst_harvesting_or_plucking_from_planting_or_sowing_in_days:function(frm,cdt,cdn){
		var d = locals[cdt][cdn]
		if(d.planting_date && d.frst_harvesting_or_plucking_from_planting_or_sowing_in_days){
			d.harvesting_or_plucking_from_planting_or_sowing = frappe.datetime.add_days(d.planting_date, d.frst_harvesting_or_plucking_from_planting_or_sowing_in_days)
			console.log(d.harvesting_or_plucking_from_planting_or_sowing,d.frst_harvesting_or_plucking_from_planting_or_sowing_in_days)
			frappe.call({
				method:"cal_till_date",
				doc:frm.doc,
				args:{
					"frst_harvest":d.harvesting_or_plucking_from_planting_or_sowing,
					"total_harvest":d.no_of_harvesting_or_plucking,
					"per_week":d.number_of_harvests_per_week
				},
				callback:function(r){
					if(r.message){
						d.dates_of_harvest = r.message[0];
						d.lasts_harvesting_till = r.message[1];
						d.harvesting_or_plucking_from_planting_or_sowing = d.harvesting_or_plucking_from_planting_or_sowing;
						frm.refresh_field("crop_planner_details");
					}
				}
			})
		}
	},
	planting_date:function(frm,cdt,cdn){
		var d = locals[cdt][cdn]
		if(d.planting_date && d.frst_harvesting_or_plucking_from_planting_or_sowing_in_days){
			d.harvesting_or_plucking_from_planting_or_sowing = frappe.datetime.add_days(d.planting_date, d.frst_harvesting_or_plucking_from_planting_or_sowing_in_days)
			frappe.call({
				method:"cal_till_date",
				doc:frm.doc,
				args:{
					"frst_harvest":d.harvesting_or_plucking_from_planting_or_sowing,
					"total_harvest":d.no_of_harvesting_or_plucking,
					"per_week":d.number_of_harvests_per_week
				},
				callback:function(r){
					if(r.message){
						d.harvesting_or_plucking_from_planting_or_sowing = d.harvesting_or_plucking_from_planting_or_sowing;
						d.dates_of_harvest = r.message[0];
						d.lasts_harvesting_till = r.message[1];
						frm.refresh_field("crop_planner_details");
					}
				}
			})
		}
	},
	planting_area_in_acreage_ha:function(frm,cdt,cdn){
		var d = locals[cdt][cdn];
		if(d.planting_area_in_acreage_ha){
			if(d.planting_area_in_acreage_ha && d.no_of_harvesting_or_plucking){ 
				d.per_harvest_supply_in_kg = Math.round(((d.planting_area_in_acreage_ha * d.tentative_yield_kgha)/2.5)/d.no_of_harvesting_or_plucking)
			}
			if(d.per_harvest_supply_in_kg && d.number_of_harvests_per_week){
				d.per_week_capacity = Math.round((((d.planting_area_in_acreage_ha * d.tentative_yield_kgha)/2.5)/d.no_of_harvesting_or_plucking) * d.number_of_harvests_per_week)
			}
			if(d.tentative_yield_kgha){
				d.total_capacity_in_plant_cycle_kg = Math.round((d.planting_area_in_acreage_ha * d.tentative_yield_kgha)/2.5)
			}
			frm.refresh_field("crop_planner_details");
		}
	},
	no_of_harvesting_or_plucking:function(frm,cdt,cdn){
		var d = locals[cdt][cdn];
		if(d.planting_area_in_acreage_ha){
			if(d.planting_area_in_acreage_ha && d.no_of_harvesting_or_plucking){ 
				d.per_harvest_supply_in_kg = Math.round(((d.planting_area_in_acreage_ha * d.tentative_yield_kgha)/2.5)/d.no_of_harvesting_or_plucking)
				frappe.call({
					method:"cal_till_date",
					doc:frm.doc,
					args:{
						"frst_harvest":d.harvesting_or_plucking_from_planting_or_sowing,
						"total_harvest":d.no_of_harvesting_or_plucking,
						"per_week":d.number_of_harvests_per_week
					},
					callback:function(r){
						if(r.message){
							d.dates_of_harvest = r.message[0];
							d.lasts_harvesting_till = r.message[1];
							d.per_harvest_supply_in_kg = d.per_harvest_supply_in_kg;
							if(d.per_harvest_supply_in_kg && d.number_of_harvests_per_week){
								d.per_week_capacity = Math.round((((d.planting_area_in_acreage_ha * d.tentative_yield_kgha)/2.5)/d.no_of_harvesting_or_plucking) * d.number_of_harvests_per_week)
							}
							if(d.tentative_yield_kgha){
								d.total_capacity_in_plant_cycle_kg = Math.round((d.planting_area_in_acreage_ha * d.tentative_yield_kgha)/2.5)
							}
							frm.refresh_field("crop_planner_details");
						}
					}
				})
			}
		}
	},
	tentative_yield_kgha:function(frm,cdt,cdn){
		var d = locals[cdt][cdn];
		if(d.planting_area_in_acreage_ha){
			if(d.planting_area_in_acreage_ha && d.no_of_harvesting_or_plucking){ 
				d.per_harvest_supply_in_kg = Math.round(((d.planting_area_in_acreage_ha * d.tentative_yield_kgha)/2.5)/d.no_of_harvesting_or_plucking)
			}
			if(d.per_harvest_supply_in_kg && d.number_of_harvests_per_week){
				d.per_week_capacity = Math.round((((d.planting_area_in_acreage_ha * d.tentative_yield_kgha)/2.5)/d.no_of_harvesting_or_plucking) * d.number_of_harvests_per_week)
			}
			if(d.tentative_yield_kgha){
				d.total_capacity_in_plant_cycle_kg = Math.round((d.planting_area_in_acreage_ha * d.tentative_yield_kgha)/2.5)
			}
			frm.refresh_field("crop_planner_details");
		}
	},
	number_of_harvests_per_week:function(frm,cdt,cdn){
		var d = locals[cdt][cdn];
		if(d.planting_area_in_acreage_ha){
			if(d.planting_area_in_acreage_ha && d.no_of_harvesting_or_plucking){ 
				d.per_harvest_supply_in_kg = Math.round(((d.planting_area_in_acreage_ha * d.tentative_yield_kgha)/2.5)/d.no_of_harvesting_or_plucking)
				frappe.call({
					method:"cal_till_date",
					doc:frm.doc,
					args:{
						"frst_harvest":d.harvesting_or_plucking_from_planting_or_sowing,
						"total_harvest":d.no_of_harvesting_or_plucking,
						"per_week":d.number_of_harvests_per_week
					},
					callback:function(r){
						if(r.message){
							d.dates_of_harvest = r.message[0];
							d.lasts_harvesting_till = r.message[1];
							d.per_harvest_supply_in_kg = d.per_harvest_supply_in_kg;
							if(d.per_harvest_supply_in_kg && d.number_of_harvests_per_week){
								d.per_week_capacity = Math.round((((d.planting_area_in_acreage_ha * d.tentative_yield_kgha)/2.5)/d.no_of_harvesting_or_plucking) * d.number_of_harvests_per_week)
							}
							if(d.tentative_yield_kgha){
								d.total_capacity_in_plant_cycle_kg = Math.round((d.planting_area_in_acreage_ha * d.tentative_yield_kgha)/2.5)
							}
							frm.refresh_field("crop_planner_details");
						}
					}
				})
			}
		}
	}
})
