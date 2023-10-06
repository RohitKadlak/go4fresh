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
	if filters.get("user"):
		conditions += " and e.user = %(user)s"
	
	if filters.get("created_from") and filters.get("created_to"):
		conditions += " and e.creation between %(created_from)s and %(created_to)s"

	if filters.get("rule"):
		conditions += " and e.rule = %(rule)s"

	return conditions

def get_data(conditions, filters):
	data = frappe.db.sql(
		"""
		SELECT
			e.name as id,
			e.name as unique_id,
			e.creation as date,
			e.user as user,
			u.full_name as user_name,
			e.type as type,
			e.points as point,
			e.rule as rule,
			e.reference_doctype as ref_doctype,
			e.reference_name as reference_name

		FROM
			`tabEnergy Point Log` e
		LEFT JOIN `tabUser` u
			ON e.user = u.name

		WHERE
			e.points != 0
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
			"label": _("ID"),
			"fieldname": "id",
			"fieldtype": "Link",
			"options": "Energy Point Log",
			"width": 160,
		},
		{
			"label": _("Unique ID"),
			"fieldname": "unique_id",
			"fieldtype": "Link",
			"options": "Energy Point Log",
			"width": 160,
		},
		{
			"label": _("Date"),
			"fieldname": "date",
			"fieldtype": "Date",
			"width": 160,
      	},
		{
			"label": _("User"),
			"fieldname": "user",
			"fieldtype": "Link",
			"options": "User",
			"width": 160,
		},
		{
			"label": _("User Name"),
			"fieldname": "user_name",
			"fieldtype": "Data",
			"width": 160,
		},
		{
			"label": _("Type"),
			"fieldname": "type",
			"fieldtype": "Data",
			"width": 160,
		},
		{
			"label": _("Point"),
			"fieldname": "point",
			"fieldtype": "Data",
			"width": 160,
		},
		{
			"label": _("Rule"),
			"fieldname": "rule",
			"fieldtype": "Link",
			"options": "Energy Point Rule",
			"width": 160,
		},
		{
			"label": _("Reference Document Type"),
			"fieldname": "ref_doctype",
			"fieldtype": "Link",
			"options": "DocType",
			"width": 160,
		},
		{
			"label": _("Reference Name"),
			"fieldname": "reference_name",
			"fieldtype": "Data",
			"width": 160,
		}
	]

	

	return columns
	