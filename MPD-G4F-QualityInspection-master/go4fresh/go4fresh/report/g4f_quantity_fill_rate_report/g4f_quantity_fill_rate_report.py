# Copyright (c) 2022, Mannlowe Information Services Pvt. Ltd. and contributors
# For license information, please see license.txt

import copy

import frappe
from frappe import _
from frappe.utils import date_diff, flt, getdate


def execute(filters=None):
	if not filters:
		return [], []

	validate_filters(filters)

	columns = get_columns(filters)
	conditions = get_conditions(filters)

	data = get_data(conditions, filters)
	if not data:
		return [], [], None, []

	return columns, data


def validate_filters(filters):
	from_date, to_date = filters.get("from_date"), filters.get("to_date")
	
	if from_date:
		if from_date and not to_date:
			frappe.throw(_("To Date are required."))
		elif date_diff(to_date, from_date) < 0:
			frappe.throw(_("To Date cannot be before From Date."))
	elif to_date:
		if not from_date and to_date:
			frappe.throw(_("From Date are required."))
		elif date_diff(to_date, from_date) < 0:
			frappe.throw(_("To Date cannot be before From Date."))

def get_conditions(filters):
	conditions = ""
	if filters.get("from_date") and filters.get("to_date"):
		conditions += " and so.transaction_date between %(from_date)s and %(to_date)s"
	
	if filters.get("sales_order"):
		conditions += " and so.name = %(sales_order)s"

	if filters.get("customer"):
		conditions += " and so.customer = %(customer)s"

	if filters.get("created_from") and filters.get("created_to"):
			conditions += " and so.creation between %(created_from)s and %(created_to)s"

	if filters.get("modified_from") and filters.get("modified"):
		conditions += " and so.modified between %(modified_from)s and %(modified_to)s"

	return conditions

def get_data(conditions, filters):
	data = frappe.db.sql(
		"""
		SELECT
			so.creation as created_date,
			so.modified as modified_date,
			so.name as so_no,
			so.name as unique_id,
			so.transaction_date as so_date,
			so.customer as customer,
			so.customer_name as customer_name,
			so.total_qty as so_qty,
			so.rounded_total as so_amount,
			(SELECT SUM(dn.total_qty) FROM `tabDelivery Note` dn WHERE dn.is_return!=1 AND so.po_no = dn.po_no) AS dn_qty,
			(SELECT SUM(dn.rounded_total) FROM `tabDelivery Note` dn WHERE dn.is_return!=1 AND so.po_no = dn.po_no) AS dn_amount,
			(SELECT SUM(dn.total_qty) FROM `tabDelivery Note` dn WHERE dn.is_return!=1 AND so.po_no = dn.po_no) AS si_qty,
			(SELECT SUM(dn.rounded_total) FROM `tabDelivery Note` dn WHERE dn.is_return!=1 AND so.po_no = dn.po_no) AS si_amount,
			so.total_qty-(SELECT SUM(dn.total_qty) FROM `tabDelivery Note` dn WHERE dn.is_return!=1 AND so.po_no = dn.po_no) AS dn_short_qty,
			so.rounded_total-(SELECT SUM(dn.rounded_total) FROM `tabDelivery Note` dn WHERE dn.is_return!=1 AND so.po_no = dn.po_no) AS dn_short_qty_amount,
			(SELECT SUM(dn.total_qty) FROM `tabDelivery Note` dn WHERE dn.is_return=1 AND so.po_no = dn.po_no)*-1 AS sales_return_qty,
			(SELECT SUM(dn.rounded_total) FROM `tabDelivery Note` dn WHERE dn.is_return=1 AND so.po_no = dn.po_no)*-1 AS sales_return_amount,
			((SELECT SUM(dn.total_qty) FROM `tabDelivery Note` dn WHERE dn.is_return!=1 AND so.po_no = dn.po_no)/so.total_qty)*100 as fill_rate,
			((SELECT SUM(dn.total_qty) FROM `tabDelivery Note` dn WHERE dn.is_return=1 AND so.po_no = dn.po_no)*-1/(SELECT SUM(total_qty) FROM `tabDelivery Note` dn WHERE dn.is_return!=1 AND so.po_no = dn.po_no))*100 as return_per
   
		FROM
			`tabSales Order` so   
		WHERE
			so.status not in ('Cancelled', 'On Hold')
			and so.docstatus = 1
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
			"label": "SO No",
			"fieldname": "so_no",
			"fieldtype": "Link",
			"options": "Sales Order",
			"width": 160
		},
		{
			"label": _("Unique ID"),
			"fieldname": "unique_id",
			"fieldtype": "Data",
			"width": 160,
		},
		{
			"label": "SO Date",
			"fieldname": "so_date",
			"fieldtype": "Date",
			"width": 160
		},
		{
			"label": "Customer",
			"fieldname": "customer",
			"fieldtype": "Link",
			"options": "Customer",
			"width": 160
		},
  		{
			"label": "Customer Name",
			"fieldname": "customer_name",
			"fieldtype": "Data",
			"width": 160
		},
		{
			"label": "SO Qty",
			"fieldname": "so_qty",
			"fieldtype": "Float",
			"width": 160
		},
		{
			"label": "SO Amount",
			"fieldname": "so_amount",
			"fieldtype": "Currency",
			"width": 160
		},
		{
			"label": "DN Qty",
			"fieldname": "dn_qty",
			"fieldtype": "Float",
			"width": 160
		},
		{
			"label": "DN Amount",
			"fieldname": "dn_amount",
			"fieldtype": "Currency",
			"width": 160
		},
		{
			"label": "SI Qty",
			"fieldname": "si_qty",
			"fieldtype": "Float",
			"width": 160
		},
		{
			"label": "SI Amount",
			"fieldname": "si_amount",
			"fieldtype": "Currency",
			"width": 160
		},
		{
			"label": "DN Short Qty",
			"fieldname": "dn_short_qty",
			"fieldtype": "Float",
			"width": 160
		},{
			"label": "DN Short Qty Amount",
			"fieldname": "dn_short_qty_amount",
			"fieldtype": "Currency",
			"width": 160
		},
		{
			"label": "Sales Return Qty",
			"fieldname": "sales_return_qty",
			"fieldtype": "Float",
			"width": 160
		},
		{
			"label": "Sales Return Amount",
			"fieldname": "sales_return_amount",
			"fieldtype": "Currency",
			"width": 160
		},
		{
			"label": "Fill Rate",
			"fieldname": "fill_rate",
			"fieldtype": "Float",
			"width": 160
		},
		{
			"label": "Return %",
			"fieldname": "return_per",
			"fieldtype": "Float",
			"width": 160
		}
	]

	

	return columns
	