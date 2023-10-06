frappe.ready(function() {
	// bind events here
	document.querySelector('.page-header').innerHTML = `
		<h2 class='text-danger'></h2>
	`;

	frappe.web_form.after_load = (e) => {
		// $(`<div class="img_preview">
		// <img class="img-responsive" src="/files/slider2.jpg">
		// </div>`).insertAfter(".ql-editor");
		$('body').css({'background-color': '#CFD8DC'});
		// $(".navbar-brand").css('height','110px');
		$('#introduction').append(`<div class="img_preview">
			<img class="img-responsive" src="/files/slider2.jpg">
		</div>`);
		$(".web-footer").hide();
		$(".btn-primary").css('background-color','green');
		// init script here
		// $(".btn-primary").hide();
		// $(".btn-light").hide();
		// $("#second").hide();
		// frappe.web_form.set_df_property('supplier_group', 'hidden', 1);
		// frappe.web_form.set_df_property('supplier_name', 'hidden', 1);
		// frappe.web_form.set_df_property('email_id', 'hidden', 1);
		// frappe.web_form.set_df_property('pan', 'hidden', 1);
		// frappe.web_form.set_df_property('aadhar_card_no', 'hidden', 1);
		// frappe.web_form.set_df_property('attach_kyc_documents', 'hidden', 1);
		// frappe.web_form.set_df_property('primary_address', 'hidden', 1);
		// frappe.web_form.set_df_property('taluka', 'hidden', 1);
		// frappe.web_form.set_df_property('district', 'hidden', 1);
		// frappe.web_form.set_df_property('state', 'hidden', 1);
		// frappe.web_form.set_df_property('postal_code', 'hidden', 1);

		// $('.web-form-footer').after(`
		// 	<div id="form-step-footer" class="text-right">
		// 		<button class="btn btn-success btn-prev btn-sm ml-2">${__("PREV")}</button>
		// 		<button class="btn btn-success btn-next btn-sm ml-2">${__("NEXT")}</button>
		// 	</div>
		// `);
		// $(".btn-register").hide();
		// $('.btn-next').on('click', function () {

			
		// 	if (!(frappe.web_form.get_value("supplier_type","supplier_type"))) {
		// 		frappe.throw('Please enter Seller Type');
		// 		return false;
		// 	}
		// 	if (!(frappe.web_form.get_value("mobile_no","mobile_no"))) {
		// 		frappe.throw('Please enter Mobile No.');
		// 		return false;
		// 	}
			

		// 	$(".btn-next").hide();	
		// 	$("#first").hide();

		// 	frappe.web_form.set_df_property('supplier_type', 'hidden', 1);
		// 	frappe.web_form.set_df_property('mobile_no', 'hidden', 1);

		// 	$(".btn-register").show();
		// 	$(".btn-primary").show();
		// 	$("#second").show();
		// 	frappe.web_form.set_df_property('supplier_name', 'hidden', 0);
		// 	frappe.web_form.set_df_property('email_id', 'hidden', 0);
		// 	frappe.web_form.set_df_property('pan', 'hidden', 0);
		// 	frappe.web_form.set_df_property('aadhar_card_no', 'hidden', 0);
		// 	frappe.web_form.set_df_property('attach_kyc_documents', 'hidden', 0);
		// 	frappe.web_form.set_df_property('supplier_group', 'hidden', 0);
		// 	frappe.web_form.set_df_property('primary_address', 'hidden', 0);
		// 	frappe.web_form.set_df_property('taluka', 'hidden', 0);
		// 	frappe.web_form.set_df_property('district', 'hidden', 0);
		// 	frappe.web_form.set_df_property('state', 'hidden', 0);
		// 	frappe.web_form.set_df_property('postal_code', 'hidden', 0);
			
		// });
		// $('.btn-prev').on('click', function () {
		// 	$(".btn-next").show();	
		// 	$("#first").show();

		// 	frappe.web_form.set_df_property('supplier_type', 'hidden', 0);
		// 	frappe.web_form.set_df_property('mobile_no', 'hidden', 0);


		// 	$(".btn-primary").hide();
		// 	$("#second").hide();
		// 	frappe.web_form.set_df_property('supplier_name', 'hidden', 1);
		// 	frappe.web_form.set_df_property('email_id', 'hidden', 1);
		// 	frappe.web_form.set_df_property('pan', 'hidden', 1);
		// 	frappe.web_form.set_df_property('aadhar_card_no', 'hidden', 1);
		// 	frappe.web_form.set_df_property('attach_kyc_documents', 'hidden', 1);
		// 	frappe.web_form.set_df_property('supplier_group', 'hidden', 1);
		// 	frappe.web_form.set_df_property('primary_address', 'hidden', 1);
		// 	frappe.web_form.set_df_property('taluka', 'hidden', 1);
		// 	frappe.web_form.set_df_property('district', 'hidden', 1);
		// 	frappe.web_form.set_df_property('state', 'hidden', 1);
		// 	frappe.web_form.set_df_property('postal_code', 'hidden', 1);
			
		// });
		// $('.btn-register').on('click', function () {
			
		// 	if (!(frappe.web_form.get_value("supplier_type","supplier_type"))) {
		// 		frappe.throw('Please enter Supplier Type.');
		// 		return false;
		// 	}			

		// 	if (!(frappe.web_form.get_value("supplier_group","supplier_group"))) {
		// 		frappe.throw('Please enter Supplier Group');
		// 		return false;
		// 	}

		// 	let data = frappe.web_form.get_values();
		// 	// var contact = frappe.new_doc = ({ 
		// 	// 	"doctype": "Supplier",
		// 	// 	"supplier_name" : data.supplier_name,
		// 	// 	"mobile_no" : data.mobile_no,
		// 	// 	"email_id" : data.email_id,
		// 	// 	"pan" : data.pan,
		// 	// 	"aadhar_card_no" : data.aadhar_card_no,
		// 	// 	"supplier_type" : data.supplier_type,
		// 	// 	"supplier_group" : data.supplier_group,
		// 	// 	"primary_address" : data.primary_address,
		// 	// 	"taluka" : data.taluka,
		// 	// 	"district" : data.district,
		// 	// 	"country" : data.country,
		// 	// 	"cluster" : data.cluster,
		// 	// 	"disabled" : 1
		// 	// });
		// 	// console.log(contact);
		// 	// frappe.db.insert(contact);
		// 	frappe.call({
		// 		method: "go4fresh.api.create_seller",
		// 		args: {
		// 		"data": data
		// 		}, 
		// 		callback: function(r) {
		// 			if(r.message){

		// 				frappe.msgprint("You Successfully created supplier. Your reference number is "+r.message)
		// 				// window.location.reload();
		// 			}
		// 		}
		// 	});																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																	
		// });
	}

	frappe.web_form.after_save = () => {
		// window.location.href = "/login";
		// frappe.confirm("Your application is successfully submitted.",
		// () => {
		// 	window.location.href = "/index1.html";
		// })
		frappe.msgprint({
			title: __('Notification'),
			message: __('Your information is successfully submitted.'),
			primary_action:{
				'label' : 'OK',
				action(values) {
					window.location.href = "/index.html";
				}
			}
		});
	}
})