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
  
	if filters.get("created_from") and filters.get("created_to"):
		conditions += " and cpd.creation between %(created_from)s and %(created_to)s"
  
	if filters.get("modified_from") and filters.get("modified_to"):
		conditions += " and cpd.modified between %(modified_from)s and %(modified_to)s"

	return conditions

def get_data(conditions, filters):
		
	data = frappe.db.sql(
		"""
		SELECT
			cpd.creation as created_date,
			cpd.modified as modified_date,
			cp.name as crop_planner_name,
			cp.name as unique_id,
			cp.supplier as supplier,
			cp.supplier_name as supplier_name,
			cp.supplier_address as address,
			cp.address_display as supplier_address,
			cp.date as crop_registration_date,
			cpd.name as crop_planner_detail_name,
			cpd.crop_name as crop_name,
			cpd.planting_date as planting_date,
			cpd.planting_area_in_acreage_ha as planting_area_in_acre,
			cpd.per_harvest_supply_in_kg as per_harvest_supply,
			cpd.total_capacity_in_plant_cycle_kg as total_capacity_in_plant_cycle,
			cpd.per_week_capacity as per_week_capacity_in_kg,
			cpd.harvesting_or_plucking_from_planting_or_sowing as harvesting_or_plucking_from

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
	comp = ""
	if frappe.defaults.get_global_default("company") == "FRESH PRODUCE VALUE CREATION SERVICES PRIVATE LIMITED":
		comp = "G4F-Go4Fresh-"
		data = data_manipulation(data,comp)
	if frappe.defaults.get_global_default("company") == "Krishi Pragati Centre - Solan" :
		comp = "G4F-Solan-"
		data = data_manipulation(data,comp)

	return data

def data_manipulation(data,comp):
	for a in data:
		a["unique_id"] = comp + a["unique_id"]
	return data

def get_columns(filters):
	columns = [
		{
			"label": _("Created Date"),
			"fieldname": "created_date",
			"fieldtype": "Date",
			"width": 160
		},
		{
			"label": _("Modified Date"),
			"fieldname": "modified_date",
			"fieldtype": "Date",
			"width": 160
		},
		{
			"label": _("Crop Planner Name"),
			"fieldname": "crop_planner_name",
			"fieldtype": "Link",
			"options": "G4F Crop Planner",
			"width": 160,
		},
		{
			"label": _("Crop Planner"),
			"fieldname": "unique_id",
			"fieldtype": "Data",
			"width": 160,
		},
		{
			"label": _("Seller"),
			"fieldname": "supplier",
			"fieldtype": "Link",
			"options": "Supplier",
			"width": 160,
		},
		{
			"label": _("Seller Name"),
			"fieldname": "supplier_name",
			"fieldtype": "Data",
			"width": 160
		},
		{
			"label": _("Address"),
			"fieldname": "address",
			"fieldtype": "Link",
			"options": "Address",
			"width": 160,
		},
		{
			"label": _("Seller Address"),
			"fieldname": "supplier_address",
			"fieldtype": "Read Only",
			"width": 160
		},
		{
			"label": _("Crop Registration Date"),
			"fieldname": "crop_registration_date",
			"fieldtype": "Date",
			"width": 160
		},
		{
			"label": _("Crop Planner Detail Name"),
			"fieldname": "crop_planner_detail_name",
			"fieldtype": "Data",
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
			"label": _("Planting Date"),
			"fieldname": "planting_date",
			"fieldtype": "Date",
			"width": 160
		},
		{
			"label": _("Planting Area In Acre"),
			"fieldname": "planting_area_in_acre",
			"fieldtype": "Float",
			"width": 160
		},	
		{
			"label": _("1st Harvesting or Plucking from Planting or Sowing"),
			"fieldname": "harvesting_or_plucking_from",
			"fieldtype": "Int",
			"width": 160
		},
		{
			"label": _("Per Harvest Supply in Kg"),
			"fieldname": "per_harvest_supply",
			"fieldtype": "Int",
			"width": 160
		},	
		{
			"label": _("Per week capacity in Kg"),
			"fieldname": "per_week_capacity_in_kg",
			"fieldtype": "Int",
			"width": 160
		},
		{
			"label": _("Total Capacity in plant cycle (Kg)"),
			"fieldname": "total_capacity_in_plant_cycle",
			"fieldtype": "Int",
			"width": 160
		},			
	]

	

	return columns
	