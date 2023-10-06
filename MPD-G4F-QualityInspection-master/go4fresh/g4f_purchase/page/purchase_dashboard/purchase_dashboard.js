frappe.pages['purchase-dashboard'].on_page_load = function(wrapper) {
	new ReportPage(wrapper);
}
ReportPage = Class.extend({
	init:function(wrapper){
		this.page = frappe.ui.make_app_page({
			parent: wrapper,
			single_column: true
		})
		$("div").remove('.page-head.flex');
		$("div").remove('.page-head.flex.drop-shadow');
		$("div").remove('.row.layout-main');
		let body = `
			<div class="page-form">
				<iframe 
					src="https://analytics.mannlowe.com:8088/superset/dashboard/27/?preselect_filters=%7B%7D&standalone=true" 
					frameborder="0"
					width="100%"
					height="867"
					allowtransparency
				></iframe>
			</div>
		`;
		$(wrapper).append(body);
	}
})