frappe.ui.form.on("Supplier",{
    setup:function(frm){
        function getLocation() {
			if(navigator.geolocation) {
			    navigator.geolocation.getCurrentPosition(showPosition);
			} else { 
			    console.log("Error")
			}
		}
		function showPosition(position) {
            frm.set_value("latitude",position.coords.latitude);
            frm.set_value("longitude",position.coords.longitude)
            frm.refresh_field("latitude");
            frm.refresh_field("longitude");
        }
        getLocation();


        console.log(frappe.session.user)
        if(frappe.session.user === "ghoti@go4fresh.com"){
            frm.set_value("naming_series","FSM-.######");
            frm.set_value("supplier_group","Farmer Supplier-Maharashtra");
            frm.refresh_field("naming_series");
            frm.refresh_field("supplier_group");
        }
    },
    before_save:function(frm){
        if(frm.doc.farmer_reference_table){
            frm.set_value("calculated_number_of_farmers",frm.doc.farmer_reference_table.length);
            frm.refresh_field("calculated_number_of_farmers");
            var total_acreage = 0.00
            frm.doc.farmer_reference_table.forEach(function(entry){
                frappe.call({
                    method:"frappe.client.get",
                    args:{
                        "doctype":"Supplier",
                        "name":entry.supplier_code
                    },
                    callback:function(r){
                        var r = r.message;
                        total_acreage = total_acreage + parseFloat(r.total_farm_acreage);
                        frm.set_value("calculated_total_acreage",total_acreage);
                        frm.refresh_field("calculated_total_acreage");
                    }
                })
            })
        }
    }
})
frappe.ui.form.on("Farmer Reference",{
    supplier_code:function(frm,cdt,cdn){
        var child = locals[cdt][cdn];
        console.log(child.supplier_code)
        frappe.model.get_value("Supplier",{'name':child.supplier_code},"supplier_name",
            function(d){
                if(d.supplier_name){
                    child.supplier_name = d.supplier_name
                    frm.refresh_field("farmer_reference_table");
                }
        })
    }
})