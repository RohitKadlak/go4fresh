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

		// frappe.web_form.add_button_to_footer("test", "submit", ()=>{alert('Hello World')})
		frappe.web_form.set_df_property('forecast_for_you_section', 'hidden', 1);
		frappe.web_form.set_df_property('estimated_yield', 'hidden', 1);
		frappe.web_form.set_df_property('total_sales', 'hidden', 1);
		frappe.web_form.set_df_property('net_income', 'hidden', 1);
		
		frappe.web_form.on('seed',(field,value) => {
			let data = frappe.web_form.get_values();
			let r = data.seed+data.fertigation+data.crop_protection+data.interculture+data.harvesting+data.irrigation+data.transport+data.other_expenses
			// console.log(r)
			frappe.web_form.set_value('total_cost', r);
			
		});
		frappe.web_form.on('fertigation',(field,value) => {
			let data = frappe.web_form.get_values();
			let r = data.seed+data.fertigation+data.crop_protection+data.interculture+data.harvesting+data.irrigation+data.transport+data.other_expenses
			frappe.web_form.set_value('total_cost', r);
		});
		frappe.web_form.on('crop_protection',(field,value) => {
			let data = frappe.web_form.get_values();
			let r = data.seed+data.fertigation+data.crop_protection+data.interculture+data.harvesting+data.irrigation+data.transport+data.other_expenses
			frappe.web_form.set_value('total_cost', r);
		});
		frappe.web_form.on('interculture',(field,value) => {
			let data = frappe.web_form.get_values();
			let r = data.seed+data.fertigation+data.crop_protection+data.interculture+data.harvesting+data.irrigation+data.transport+data.other_expenses
			frappe.web_form.set_value('total_cost', r);
		});
		frappe.web_form.on('harvesting',(field,value) => {
			let data = frappe.web_form.get_values();
			let r = data.seed+data.fertigation+data.crop_protection+data.interculture+data.harvesting+data.irrigation+data.transport+data.other_expenses
			frappe.web_form.set_value('total_cost', r);
		});
		frappe.web_form.on('irrigation',(field,value) => {
			let data = frappe.web_form.get_values();
			let r = data.seed+data.fertigation+data.crop_protection+data.interculture+data.harvesting+data.irrigation+data.transport+data.other_expenses
			frappe.web_form.set_value('total_cost', r);
		});
		frappe.web_form.on('transport',(field,value) => {
			let data = frappe.web_form.get_values();
			let r = data.seed+data.fertigation+data.crop_protection+data.interculture+data.harvesting+data.irrigation+data.transport+data.other_expenses
			frappe.web_form.set_value('total_cost', r);
		});
		frappe.web_form.on('other_expenses',(field,value) => {
			let data = frappe.web_form.get_values();
			let r = data.seed+data.fertigation+data.crop_protection+data.interculture+data.harvesting+data.irrigation+data.transport+data.other_expenses
			frappe.web_form.set_value('total_cost', r);
		});

		$('.web-form-footer').after(`
			<div id="form-step-footer" class="text-left">
				<a href="/seller-registration-form" style="color:green;">Register to save the Result...</a><br>
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
								if(!data.total_cost){
									data.total_cost = 0.00;
								}
								frappe.web_form.set_value('estimated_yield', (data.area*0.404686)*r.message);
								frappe.web_form.set_value('total_sales', ((data.area*0.404686)*r.message)*data.average_pricekg);
								// console.log(data.total_sales,data.total_cost)
								frappe.web_form.set_value('net_income', ((data.area*0.404686)*r.message)*data.average_pricekg - data.total_cost);
								frappe.web_form.set_df_property('forecast_for_you_section', 'hidden', 0);
								frappe.web_form.set_df_property('estimated_yield', 'hidden', 0);
								frappe.web_form.set_df_property('average_pricekg', 'hidden', 0);
								frappe.web_form.set_df_property('total_sales', 'hidden', 0);
								frappe.web_form.set_df_property('net_income', 'hidden', 0);
							}
						}
					});
				}
			}
		});
	}
})