from . import __version__ as app_version

app_name = "go4fresh"
app_title = "Go4Fresh"
app_publisher = "Mannlowe Information Services Pvt. Ltd."
app_description = "Vegetables Supply"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "shrikant.pawar@mannlowe.com"
app_license = "Man@Mannlowe Information Services Pvt. Ltd."

# Includes in <head>
# ------------------

# fixtures = [
#     {"dt": "DocType", "filters": [
#         [
#             "name", "in", [
#                 "Doctype1Name",
#                 "Doctype2Name"
#             ]
#         ]
#     ]},
#     {"dt": "Custom Field", "filters": [
#         [
#             "name", "in", [
#                 "CustomFieldName"
#             ]
#         ]
#     ]}
# ]
fixtures = [
    	# {"dt":"Custom Field", "filters": [["fieldname", "in", ("release_fence", "search_mode", "priority", "size_minimum", "size_maximum", "customer_pricing_rule_id", "planning_parameters", "column_break_16", "alternate_selection", "column_break_25", "type", "post_op_time", "postop_time", "size_minimum", "size_multiple", "size_maximum", "planning_parameters", "release_fence", "duration", "duration_per_unit", "column_break_66", "search_mode", "priority", "alternate_selection", "type", "c", "location", "available", "type", "column_break_5", "minimum_calendar", "min_interval", "location", "column_break_7", "priority", "fence", "effective_start", "effective_end", "size_minimum", "size_multiple", "size_maximum", "section_break_2", "resource", "resource_quantity", "lead_time", "type", "release_plan", "release_plan_wo", "frepple_po_ref", "column_break_2", "calendar", "release_plan_wo", "frepple_mo_ref", "section_break_15", "warehouse", "type", "constrained", "column_break_21", "efficiency", "maximum_calendar", "available", "maximum", "max_early", "efficiency_calendar")]]}, 
    	# {"dt":"Custom Field", "filters": [["fieldname", "in", ("taluka")]]},
		{"dt": "Custom Field", "filters": [
         	[
            	"name", "like", "Supplier-%"
         	]
 		]}
    ]

# include js, css files in header of desk.html
# app_include_css = ["/assets/go4fresh/css/custom.css"]
# app_include_js = "/assets/go4fresh/js/go4fresh.js"

# base_template = "www/index.html"
# base_template = {
#     r"login.*": "www/index.html"
# }

# include js, css files in header of web template
# web_include_css = "/assets/go4fresh/css/go4fresh.css"
web_include_css = "/assets/go4fresh/css/custom_css.css"
# web_include_js = "/assets/go4fresh/js/go4fresh.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "go4fresh/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}

doctype_js = {
	"Purchase Receipt" : "public/js/custom_purchase_receipt.js",
	"Purchase Order" : "public/js/custom_purchase_order.js",
	"Stock Entry" : "public/js/custom_stock_entry.js",
	"Pick List" : "public/js/custom_pick_list.js",
	"Delivery Note" : "public/js/custom_delivery_note.js",
	"Material Request" : "public/js/custom_material_request.js",
	"Quality Inspection" : "public/js/custom_quality_inspection.js",
	"Supplier" : "public/js/custom_supplier.js"
}

# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "home_landing_page.html"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "go4fresh.install.before_install"
# after_install = "go4fresh.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "go4fresh.uninstall.before_uninstall"
# after_uninstall = "go4fresh.uninstall.after_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "go4fresh.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }
override_doctype_class = {
	# "ToDo": "custom_app.overrides.CustomToDo"
	"Pick List" : "go4fresh.go4fresh.custom_pick_list.MPickList"
}

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"go4fresh.tasks.all"
# 	],
# 	"daily": [
# 		"go4fresh.tasks.daily"
# 	],
# 	"hourly": [
# 		"go4fresh.tasks.hourly"
# 	],
# 	"weekly": [
# 		"go4fresh.tasks.weekly"
# 	]
# 	"monthly": [
# 		"go4fresh.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "go4fresh.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "go4fresh.event.get_events"
# }
override_whitelisted_methods = {
	"erpnext.e_commerce.shopping_cart.cart.place_order": "go4fresh.go4fresh.custom.custom_cart.place_order"
}
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "go4fresh.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

user_data_fields = [
	{
		"doctype": "{doctype_1}",
		"filter_by": "{filter_by}",
		"redact_fields": ["{field_1}", "{field_2}"],
		"partial": 1,
	},
	{
		"doctype": "{doctype_2}",
		"filter_by": "{filter_by}",
		"partial": 1,
	},
	{
		"doctype": "{doctype_3}",
		"strict": False,
	},
	{
		"doctype": "{doctype_4}"
	}
]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"go4fresh.auth.validate"
# ]

