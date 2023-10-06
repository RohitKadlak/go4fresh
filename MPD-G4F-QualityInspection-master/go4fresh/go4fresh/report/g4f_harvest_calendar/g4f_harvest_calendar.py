# Copyright (c) 2022, Mannlowe Information Services Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe import _
from frappe.utils import date_diff, flt, getdate


def execute(filters=None):
	# if not filters:
	# 	return [], []

	columns = get_columns(filters)
	conditions = get_conditions(filters)

	data = get_data(conditions, filters)
	if not data:
		return [], [], None, []

	# data, chart_data,report_summary = prepare_data(data, filters)

	return columns, data #, None, chart_data,report_summary


def get_conditions(filters):
	conditions = ""
	if filters.get("supplier"):
		conditions += " and cp.supplier = %(supplier)s"
		
	if filters.get("crop"):
		conditions += " and cpd.crop_name = %(crop)s"
  
	if filters.get("date"):
		conditions += " and %(date)s between cpd.frst_harvesting_or_plucking_from_planting_or_sowing_in_days AND cpd.lasts_harvesting_till"

	return conditions

def get_data(conditions, filters):
	data = frappe.db.sql(
		"""
		SELECT
    		DISTINCT(cpd.crop_name) as crop_name,
    		COALESCE(SUM(cpd.per_week_capacity),0) AS per_week_capacity
    	FROM
			`tabG4F Crop Planner Details` cpd
    	LEFT JOIN `tabG4F Crop Planner` cp
    		ON cp.name = cpd.parent
    		
		WHERE
			cp.name != ""
			{0}
	""".format(
			conditions
		),
		filters,
		as_dict=1,
	)
	# comp = ""
	# if frappe.defaults.get_global_default("company") == "FRESH PRODUCE VALUE CREATION SERVICES PRIVATE LIMITED":
	# 	comp = "G4F-Go4Fresh-"
	# 	data = data_manipulation(data,comp)
	# if frappe.defaults.get_global_default("company") == "Krishi Pragati Centre - Solan" :
	# 	comp = "G4F-Solan-"
	# 	data = data_manipulation(data,comp)

	return data

# def data_manipulation(data,comp):
# 	for a in data:
# 		a["unique_id"] = comp + a["unique_id"]
# 	return data

def get_columns(filters):
	columns = [
		{
			"label": _("Seller"),
			"fieldname": "seller",
			"fieldtype": "Link",
			"options": "Supplier",
			"width": 160,
		},
		{
			"label": _("Crop Name"),
			"fieldname": "crop_name",
			"fieldtype": "Link",
			"options": "G4F Crop List",
			"width": 160,
		},	
		{
			"label": _("Per week capacity in Kg"),
			"fieldname": "per_week_capacity",
			"fieldtype": "Float",
			"width": 160
		}			
	]

	

	return columns
	