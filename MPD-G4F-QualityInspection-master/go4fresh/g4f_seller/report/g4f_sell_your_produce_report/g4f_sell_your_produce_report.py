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
	if filters.get("check_date"):
		conditions += " and syp.posting_date = %(check_date)s"
	
	if filters.get("supplier"):
		conditions += " and syp.supplier = %(supplier)s"
		
	if filters.get("crop"):
		conditions += " and syp.crop = %(crop)s"
  
	if filters.get("created_from") and filters.get("created_to"):
		conditions += " and sypi.creation between %(created_from)s and %(created_to)s"
  
	if filters.get("modified_from") and filters.get("modified_to"):
		conditions += " and sypi.modified between %(modified_from)s and %(modified_to)s"
		
	if filters.get("from_date") and filters.get("to_date"):
		conditions += " and sypi.posting_date between %(from_date)s and %(to_date)s"

	return conditions

def get_data(conditions, filters):
		
	data = frappe.db.sql(
		"""
		SELECT
			sypi.creation as created_date,
			sypi.modified as modified_date,
			syp.name as sell_your_produce_name,
			sypi.name as unique_id,
			syp.supplier as seller,
			syp.supplier_name as seller_name,
			syp.address as address,
			syp.address_display as address_display,
			syp.posting_date as posting_date,
			syp.crop as crop,
			sypi.grade_name as grade,
			sypi.item_code as item_code,
			sypi.item_name as item_name,
			sypi.uom as uom,
			sypi.qty as qty
			

		FROM
			`tabG4F Sell Your Produce Item` sypi
		LEFT JOIN `tabG4F Sell Your Produce` syp
			ON syp.name = sypi.parent

		WHERE
			syp.name != ""
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
			"label": _("Sell Your Produce Name"),
			"fieldname": "sell_your_produce_name",
			"fieldtype": "Link",
			"options": "G4F Sell Your Produce",
			"width": 160,
		},
		{
			"label": _("Unique ID"),
			"fieldname": "unique_id",
			"fieldtype": "Data",
			"width": 160
		},
		{
			"label": _("Seller"),
			"fieldname": "seller",
			"fieldtype": "Link",
			"options": "Supplier",
			"width": 160,
		},
		{
			"label": _("Seller Name"),
			"fieldname": "seller_name",
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
			"fieldname": "address_display",
			"fieldtype": "Read Only",
			"length": 500,
			"width": 160
		},
		{
			"label": _("Sell Your Produce Date"),
			"fieldname": "posting_date",
			"fieldtype": "Date",
			"width": 160
		},
		{
			"label": _("Crop Name"),
			"fieldname": "crop",
			"fieldtype": "Link",
			"options": "G4F Crop List",
			"width": 160,
		},
		{
			"label": _("Grade"),
			"fieldname": "grade",
			"fieldtype": "Link",
			"options": "G4F Grade",
			"width": 160,
		},
		{
			"label": _("Item Code"),
			"fieldname": "item_code",
			"fieldtype": "Link",
			"options": "Item",
			"width": 160,
		},
		{
			"label": _("Item Name"),
			"fieldname": "item_name",
			"fieldtype": "Data",
			"width": 160,
		},
		{
			"label": _("UOM"),
			"fieldname": "uom",
			"fieldtype": "Link",
			"options": "UOM",
			"width": 160,
		},
		{
			"label": _("Qty"),
			"fieldname": "qty",
			"fieldtype": "Float",
			"width": 160
		}			
	]

	

	return columns