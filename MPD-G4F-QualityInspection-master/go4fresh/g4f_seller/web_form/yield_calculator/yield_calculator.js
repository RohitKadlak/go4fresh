frappe.ready(function() {
	// bind events here
	document.querySelector('.page-header').innerHTML = `
		<h2 class='text-danger'></h2>
	`;

	frappe.web_form.after_load = (e) => {
		// init script here

		$(".btn-primary").remove();
		$(".btn-light").remove();

		$('.web-form-footer').after(`
			<div id="form-step-footer" class="text-right">
				<button class="btn btn-success btn-next btn-sm ml-2">${__("Calculate")}</button>
			</div>
		`);

		frappe.web_form.set_df_property('forecast_for_you_section', 'hidden', 1);
		frappe.web_form.set_df_property('estimated_yield', 'hidden', 1);
		// frappe.web_form.set_df_property('average_pricekg', 'hidden', 1);
		frappe.web_form.set_df_property('total_sales', 'hidden', 1);
		$('.web-form-footer').after(`
			<div id="form-step-footer" class="text-left">
				<a href="/seller-registration-form" style="color:green;">Register to save the Result...</a><br>
				<a href="/detailed-yield-calculator">Click Here to Calculate net Income...</a>
			</div>
		`);
		$('.btn-next').on('click', function () {
			let data = frappe.web_form.get_values();
			if (!data.crop) {
				frappe.throw('Please select crop First...');
				return false;
			}else{
				if(data.area<=0){
					frappe.throw('Area must be grater than 0...');
					return false;
				} else if(data.average_pricekg<0){
					frappe.throw('Average price must be grater than 0...');
					return false;
				}else{
					frappe.call({
						method: "go4fresh.api.calculate_values",
						args: {
						"data": data
						}, 
						callback: function(r) {
							if(r.message){
								if(!data.area){
									data.area = 0.00;
								}
								if(!data.average_pricekg){
									data.average_pricekg = 0.00;
								}
								frappe.web_form.set_value('estimated_yield', (data.area*0.404686)*r.message);
								// frappe.web_form.set_value('average_pricekg', 12.50);
								frappe.web_form.set_value('total_sales', ((data.area*0.404686)*r.message)*data.average_pricekg);
								frappe.web_form.set_df_property('forecast_for_you_section', 'hidden', 0);
								frappe.web_form.set_df_property('estimated_yield', 'hidden', 0);
								// frappe.web_form.set_df_property('average_pricekg', 'hidden', 0);
								frappe.web_form.set_df_property('total_sales', 'hidden', 0);
							}
						}
					});
				}
			}
		});

		// frappe.web_form.on('area',(field,value) => {
		// 	let data = frappe.web_form.get_values();
		// 	if (!data.crop) {
		// 		frappe.throw('Please select crop First...');
		// 		return false;
		// 	}else{
		// 		if(data.area<=0){
		// 			frappe.throw('Area must be grater than 0...');
		// 			return false;
		// 		} else if(data.average_pricekg<0){
		// 			frappe.throw('Average price must be grater than 0...');
		// 			return false;
		// 		}else{
		// 			frappe.call({
		// 				method: "go4fresh.api.calculate_values",
		// 				args: {
		// 				"data": data
		// 				}, 
		// 				callback: function(r) {
		// 					if(r.message){
		// 						frappe.web_form.set_value('estimated_yield', (data.area*0.404686)*r.message);
		// 						// frappe.web_form.set_value('average_pricekg', 12.50);
		// 						frappe.web_form.set_value('total_sales', ((data.area*0.404686)*r.message)*data.average_pricekg);
		// 						frappe.web_form.set_df_property('forecast_for_you_section', 'hidden', 0);
		// 						frappe.web_form.set_df_property('estimated_yield', 'hidden', 0);
		// 						// frappe.web_form.set_df_property('average_pricekg', 'hidden', 0);
		// 						frappe.web_form.set_df_property('total_sales', 'hidden', 0);
		// 					}
		// 				}
		// 			});
		// 		}
		// 	}			
		// });
		
	}	
})