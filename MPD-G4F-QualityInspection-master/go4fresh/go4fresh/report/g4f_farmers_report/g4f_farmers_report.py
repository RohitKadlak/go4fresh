# Copyright (c) 2022, Mannlowe Information Services Pvt. Ltd. and contributors
# For license information, please see license.txt

import copy

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
	if filters.get("cluster"):
		conditions += " and s.cluster = %(cluster)s"

	if filters.get("supplier_group"):
		conditions += " and s.supplier_group = %(supplier_group)s"

	if filters.get("created_from") and filters.get("created_to"):
			conditions += " and s.creation between %(created_from)s and %(created_to)s"

	if filters.get("modified_from") and filters.get("modified"):
		conditions += " and s.modified between %(modified_from)s and %(modified_to)s"

	return conditions

def get_data(conditions, filters):
	data = frappe.db.sql(
		"""
		SELECT
			s.creation as created_date,
			s.modified as modified_date,
			s.name as name,
			s.name as unique_id,
			s.disabled as docstatus,
			s.supplier_name as seller_name,
			s.supplier_group as seller_group,
			s.country as country,
			s.division as district,
			s.cluster as cluster,
			s.nearest_cp as nearest_collection_point,
			s.supplier_type as seller_type,
			s.aadhar_card_no as adhar_card_no,
			s.fcc_distance as cp_distance,
			s.total_farmer_linked as total_farmer_linked,
			s.pan as pan,
			s.total_farm_acreage as total_farm_acreage,
			s.any_relationship_with_other_organizations_ as any_relationship_with_other_organizations,
			s.crops_to_go4_fresh_and_qty as crops_to_go4fresh_and_qty,
			s.expectation_from_go4_fresh as expectation_from_go4fresh,
			s.calculated_number_of_farmers as calculated_number_of_farmers,
			s.total_farm_acreage as calculate_total_acreage,
			s.supplier_primary_address as seller_primary_address,
			s.supplier_primary_contact as seller_primary_contact
			
		FROM
			`tabSupplier` s

		WHERE
			s.disabled != 1
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

# def prepare_data(data, filters):
# 	total,accepted, pending, return_qty = 0, 0, 0, 0
# 	total_field = "po_qty"
# 	accepted_field = "accepted_qty"
# 	pending_field = "pending_qty"
# 	return_field = "supplier_return_qty"

# 	for row in data:
# 		# sum data for chart
# 		total += row[total_field]
# 		accepted += row[accepted_field]
# 		pending += row[pending_field]
# 		return_qty += row[return_field]
	
# 	chart_data = prepare_chart_data(total, accepted , pending,return_qty)
# 	report_summary = [
# 		{"label":"<b>PO QTY</b>","value":total,'indicator':'Blue'},
# 		{"label":"<b>Total Accepted QTY</b>","value":accepted,'indicator':'Green'},
# 		{"label":"<b>Total Pending QTY</b>","value":pending,'indicator':'Red'},
# 		{"label":"<b>Supplier Rejected Return QTY</b>","value":return_qty,'indicator':'Red'},
# 	]
# 	return data, chart_data,report_summary

# def prepare_chart_data(total, accepted , pending, return_qty):
# 	labels = ["Total PO QTY", "Accepted QTY" , "Pending QTY", "Supplier Rejected Return QTY"]

# 	return {
# 		"data": {"labels": labels, "datasets": [{"values": [total, accepted , pending, return_qty]}]},
# 		"type": "donut",
# 		"height": 100,
# 		"colors": ['blue'],
# 	}


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
			"label": _("Name"),
			"fieldname": "name",
			"fieldtype": "Link",
			"options": "Supplier",
			"width": 160,
		},
		{
			"label": _("Unique ID"),
			"fieldname": "unique_id",
			"fieldtype": "Data",
			"width": 160,
		},
		{
			"label": _("Docstatus"),
			"fieldname": "docstatus",
			"fieldtype": "Int",
			"width": 160,
		},
		{
			"label": _("Seller Name"),
			"fieldname": "seller_name",
			"fieldtype": "Data",
			"width": 160,
		},
		{
			"label": _("Seller Group"),
			"fieldname": "seller_group",
			"fieldtype": "Link",
			"options": "Supplier Group",
			"width": 160,
		},
		{
			"label": _("Country"),
			"fieldname": "country",
			"fieldtype": "Data",
			"width": 160,
		},
		{
			"label": _("District"),
			"fieldname": "district",
			"fieldtype": "Data",
			"width": 160,
		},
		{
			"label": _("Cluster"),
			"fieldname": "cluster",
			"fieldtype": "Data",
			"width": 160,
		},
		{
			"label": _("Nearest Collection Point"),
			"fieldname": "nearest_collection_point",
			"fieldtype": "Data",
			"width": 160,
		},
		{
			"label": _("Seller Type"),
			"fieldname": "seller_type",
			"fieldtype": "Data",
			"width": 160,
		},
		{
			"label": _("Adhar Card No."),
			"fieldname": "adhar_card_no",
			"fieldtype": "Data",
			"width": 160,
		},
		{
			"label": _("CP Distance (KM)"),
			"fieldname": "cp_distance",
			"fieldtype": "Data",
			"width": 160,
		}, 
		{
			"label": _("Total Farmer Linked"),
			"fieldname": "total_farmer_linked",
			"fieldtype": "Data",
			"width": 160,
		},
		{
			"label": _("PAN"),
			"fieldname": "pan",
			"fieldtype": "Data",
			"width": 160,
		}, 
		{
			"label": _("Total Farm Acreage"),
			"fieldname": "total_farm_acreage",
			"fieldtype": "Data",
			"width": 160,
		},
		{
			"label": _("Any Relationship with Other Organizations"),
			"fieldname": "any_relationship_with_other_organizations",
			"fieldtype": "Data",
			"width": 160,
		},
		{
			"label": _("Crops to Go4Fresh and Qty"),
			"fieldname": "crops_to_go4fresh_and_qty",
			"fieldtype": "Data",
			"width": 160,
		},
		{
			"label": _("Expectation From Go4Fresh"),
			"fieldname": "expectation_from_go4fresh",
			"fieldtype": "Data",
			"width": 160,
		},
		{
			"label": _("Calculated Number Of Farmers"),
			"fieldname": "calculated_number_of_farmers",
			"fieldtype": "Int",
			"width": 160,
		},
		{
			"label": _("Calculated Total Acreage"),
			"fieldname": "calculate_total_acreage",
			"fieldtype": "Float",
			"width": 160,
		},
		{
			"label": _("Seller Primary Address"),
			"fieldname": "seller_primary_address",
			"fieldtype": "Data",
			"width": 160,
		},
		{
			"label": _("Seller Primary Contact"),
			"fieldname": "seller_primary_contact",
			"fieldtype": "Data",
			"width": 160,
		},
	]

	

	return columns
	