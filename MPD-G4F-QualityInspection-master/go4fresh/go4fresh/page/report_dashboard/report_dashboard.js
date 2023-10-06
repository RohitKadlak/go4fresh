frappe.pages['report-dashboard'].on_page_load = function(wrapper) {
	new ReportPage(wrapper);
}
ReportPage = Class.extend({
	init:function(wrapper){
		this.page = frappe.ui.make_app_page({
			parent: wrapper,
			// title: 'Dashboard',
			single_column: true
		})
		// this.make();
		// $(wrapper).removeClass('.page-form');
		// $(wrapper).remove('.page-head flex drop-shadow');
		$("div").remove('.page-head.flex');
		$("div").remove('.page-head.flex.drop-shadow');
		$("div").remove('.row.layout-main');
		let body = `
			<div class="page-form">
				<iframe 
					src="https://analytics.mannlowe.com:8088/superset/dashboard/11/?native_filters_key=EPe6v2IB2H8I_QzuxAV4TcWJbUY-Dnm_JyXVJk-LGDCY8_8uLANv1c1AtsaCswE2&standalone=true" 
					frameborder="0"
					width="100%"
					height="867"
					allowtransparency
				></iframe>
			</div>
		`;
		$(wrapper).append(body);
	},
	// make:function(){
	// 	let me = $(this)
	// 	// $(frappe.render_template(frappe.report_dashboard.body,this)).appendTo(this.page.main)
		
	// }
})

// let body = `
// 	<div class="page-form">
		
// 	</div>
// `;
// frappe.report_dashboard = {
// 	body : body
// }