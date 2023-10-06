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
	if filters.get("sales_order"):
		conditions += " and so.sales_order = %(sales_order)s"
  
	return conditions

def get_data(conditions, filters):
	data = frappe.db.sql(
		"""
		SELECT DISTINCT
			so.name as sales_order,
			so.name as unique_id,
			so.creation as so_created,
			po.name as purchase_order,
			po.creation as po_created,
			pr.name as purchase_receipt,
			pr.creation as pr_created,
			dn.name as delivery_note,
			dn.creation as dn_created,
			so.customer as customer,
			so.customer_name as customer_name

		FROM
			`tabSales Order` so
		JOIN `tabPurchase Order Item` poi
			ON poi.sales_order = so.name
		JOIN `tabPurchase Order` po
			ON poi.parent = po.name AND po.status != "Cancelled"
		JOIN `tabPurchase Receipt Item` pri
			ON pri.purchase_order = po.name
		JOIN `tabPurchase Receipt` pr
			ON pri.parent = pr.name AND pr.is_return!=1
		JOIN `tabDelivery Note Item` dni
			ON dni.against_sales_order = so.name
		JOIN `tabDelivery Note` dn
			ON dni.parent = dn.name AND dn.is_return!=1

		WHERE
			so.status != "Cancelled"
			{0}
		GROUP BY
			so.name
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
			"label": _("Sales Order"),
			"fieldname": "sales_order",
			"fieldtype": "Link",
			"options": "Sales Order",
			"width": 160,
		},
		{
			"label": _("Unique ID"),
			"fieldname": "unique_id",
			"fieldtype": "Data",
			"width": 160,
		},
  		{
			"label": _("Sales Order Date"),
			"fieldname": "so_created",
			"fieldtype": "Data",
			"width": 160,
		},
		{
			"label": _("Purchase Order"),
			"fieldname": "purchase_order",
			"fieldtype": "Link",
			"options": "Purchase Order",
			"width": 160,
		},
  		{
			"label": _("Purchase Order Date"),
			"fieldname": "po_created",
			"fieldtype": "Data",
			"width": 160,
		},
		{
			"label": _("Purchase Receipt"),
			"fieldname": "purchase_receipt",
			"fieldtype": "Link",
			"options": "Purchase Receipt",
			"width": 160,
		},
  		{
			"label": _("Purchase Receipt Date"),
			"fieldname": "pr_created",
			"fieldtype": "Data",
			"width": 160,
		},
		{
			"label": _("Delivery Note"),
			"fieldname": "delivery_note",
			"fieldtype": "Link",
			"options": "Delivery Note",
			"width": 160,
		},
  		{
			"label": _("Delivery Note Date"),
			"fieldname": "dn_created",
			"fieldtype": "Data",
			"width": 160,
		},
		{
			"label": _("Customer"),
			"fieldname": "customer",
			"fieldtype": "Link",
			"options": "Delivery Note",
			"width": 160,
		},
		{
			"label": _("Customer Name"),
			"fieldname": "customer_name",
			"fieldtype": "Data",
			"width": 160,
		}
	]	

	return columns
	