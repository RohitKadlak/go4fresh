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

	data, chart_data,report_summary = prepare_data(data, filters)

	return columns, data, None, chart_data,report_summary


def validate_filters(filters):
	from_date, to_date = filters.get("from_date"), filters.get("to_date")

	if not from_date and to_date:
		frappe.throw(_("From and To Dates are required."))
	elif date_diff(to_date, from_date) < 0:
		frappe.throw(_("To Date cannot be before From Date."))

def get_conditions(filters):
	conditions = ""
	if filters.get("from_date") and filters.get("to_date"):
		conditions += " and po.transaction_date between %(from_date)s and %(to_date)s"

	if filters.get("purchase_order"):
		conditions += " and po.name = %(purchase_order)s"

	if filters.get("supplier"):
		conditions += " and po.supplier = %(supplier)s"

	if filters.get("item_code"):
		conditions += " and poi.item_code = %(item_code)s"
	
	if filters.get("sales_order"):
		conditions += " and poi.sales_order = %(sales_order)s"

	if filters.get("purchase_receipt"):
		conditions += " and prr.name = %(purchase_receipt)s"

	if filters.get("created_from") and filters.get("created_to"):
			conditions += " and po.creation between %(created_from)s and %(created_to)s"

	if filters.get("modified_from") and filters.get("modified"):
		conditions += " and po.modified between %(modified_from)s and %(modified_to)s"

	return conditions

def get_data(conditions, filters):
	data = frappe.db.sql(
		"""
		SELECT
			po.creation as created_date,
			po.modified as modified_date,
			poi.name as purchase_order_item_name,
			poi.name as unique_id,
			po.transaction_date as date,
			po.name as purchase_order,
			po.supplier as supplier,
			po.supplier_name as supplier_name,
			poi.item_code as item_code,
			poi.item_name as item_name,
			IFNULL(poi.qty,0) as po_qty,
			IFNULL(poi.rate,0) as po_rate,
			IFNULL(poi.amount,0) as po_amount,
			poi.material_request as material_request,
			poi.sales_order as sales_order,
			pr.name as purchase_receipt,
			pr.posting_date as pr_date,
			pri.batch_no as batch_no,
			pri.warehouse as accepted_warehouse,
			IFNULL(pri.received_qty,0) as received_qty,
			IFNULL(pri.qty,0) as accepted_qty,
			IFNULL(pri.rejected_qty,0) as rejected_qty,
			IFNULL(poi.qty - IFNULL(pri.received_qty,0),0) as pending_qty,
			IFNULL((poi.qty - pri.received_qty)*poi.rate,0) as pending_amount,
			IF((prir.qty*-1)!=0,prr.name,"") as pr_return_no,
			IF((prir.qty*-1)!=0,prr.posting_date,"") as pr_return_date,
			IFNULL((prir.qty * -1),0) as supplier_return_qty,
			IFNULL((prir.amount * -1),0) as supplier_return_amount,
			IFNULL((((poi.qty - pri.received_qty)+(prir.qty*-1))),0) as total_pending_qty_po,
			IFNULL(((((poi.qty - pri.received_qty)*poi.rate)+(prir.amount*-1))),0) as total_pending_amount

		FROM
			`tabPurchase Order` po join
			`tabPurchase Order Item` poi

		LEFT JOIN `tabPurchase Receipt Item` pri
			ON pri.purchase_order_item = poi.name
		LEFT JOIN `tabPurchase Receipt` pr
			ON pri.parent = pr.name	AND pr.is_return!="1"

		LEFT JOIN `tabPurchase Receipt` prr
			ON pr.name = prr.return_against
		LEFT JOIN `tabPurchase Receipt Item` prir
			ON prir.parent = prr.name AND pri.purchase_order_item = prir.purchase_order_item
			
		WHERE
			poi.parent = po.name
			and po.status not in ('Stopped', 'Closed')
			and po.docstatus = 1
			{0}
		GROUP BY poi.name
		ORDER BY po.transaction_date ASC
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

def prepare_data(data, filters):
	total,accepted, pending, return_qty = 0, 0, 0, 0
	total_field = "po_qty"
	accepted_field = "accepted_qty"
	pending_field = "pending_qty"
	return_field = "supplier_return_qty"

	for row in data:
		# sum data for chart
		total += row[total_field]
		accepted += row[accepted_field]
		pending += row[pending_field]
		return_qty += row[return_field]
	
	chart_data = prepare_chart_data(total, accepted , pending,return_qty)
	report_summary = [
		{"label":"<b>PO QTY</b>","value":total,'indicator':'Blue'},
		{"label":"<b>Total Accepted QTY</b>","value":accepted,'indicator':'Green'},
		{"label":"<b>Total Pending QTY</b>","value":pending,'indicator':'Red'},
		{"label":"<b>Supplier Rejected Return QTY</b>","value":return_qty,'indicator':'Red'},
	]
	return data, chart_data,report_summary

def prepare_chart_data(total, accepted , pending, return_qty):
	labels = ["Total PO QTY", "Accepted QTY" , "Pending QTY", "Supplier Rejected Return QTY"]

	return {
		"data": {"labels": labels, "datasets": [{"values": [total, accepted , pending, return_qty]}]},
		"type": "donut",
		"height": 100,
		"colors": ['blue'],
	}



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
			"label": _("Purchase Order Item Name"),
			"fieldname": "purchase_order_item_name",
			"fieldtype": "Data",
			"width": 160,
		},

		{
			"label": _("Unique ID"),
			"fieldname": "unique_id",
			"fieldtype": "Data",
			"width": 160,
		},
		{"label": _("Date"), "fieldname": "date", "fieldtype": "Date", "width": 90},
		{
			"label": _("Purchase Order"),
			"fieldname": "purchase_order",
			"fieldtype": "Link",
			"options": "Purchase Order",
			"width": 160,
		},
  		{
			"label": _("Supplier"),
			"fieldname": "supplier",
			"fieldtype": "Link",
			"options": "Supplier",
			"width": 160,
		},
		{
			"label": _("Supplier Name"),
			"fieldname": "supplier_name",
			"fieldtype": "Data",
			"width": 160,
		},
		{
			"label": _("Item Code"),
			"fieldname": "item_code",
			"fieldtype": "Link",
			"options": "Item",
			"width": 100,
		},
		{
			"label": _("Item Name"),
			"fieldname": "item_name",
			"fieldtype": "Data",
			"width": 160,
		},
		{
			"label": _("PO Qty"),
			"fieldname": "po_qty",
			"fieldtype": "Float",
			"width": 120,
			"convertible": "po_qty",
		},
		{
			"label": _("PO Rate"),
			"fieldname": "po_rate",
			"fieldtype": "Currency",
			"width": 110,
			"options": "Company:company:default_currency",
			"convertible": "po_rate",
		},
		{
			"label": _("PO Amount"),
			"fieldname": "po_amount",
			"fieldtype": "Currency",
			"width": 110,
			"options": "Company:company:default_currency",
			"convertible": "po_amount",
		},
		{
			"label": _("Material Request"),
			"fieldname": "material_request",
			"fieldtype": "Link",
			"options": "Material Request",
			"width": 160,
		},
		{
			"label": _("Sales Order"),
			"fieldname": "sales_order",
			"fieldtype": "Link",
			"options": "Sales Order",
			"width": 160,
		},
		{
			"label": _("Purchase Receipt"),
			"fieldname": "purchase_receipt",
			"fieldtype": "Link",
			"options": "Purchase Receipt",
			"width": 160,
		},
		{"label": _("PR Date"), "fieldname": "pr_date", "fieldtype": "Date", "width": 90},
		{
			"label": _("Batch"),
			"fieldname": "batch_no",
			"fieldtype": "Link",
			"options": "Batch",
			"width": 160,
		},
		{
			"label": _("Accepted Warehouse"),
			"fieldname": "accepted_warehouse",
			"fieldtype": "Link",
			"options": "Warehouse",
			"width": 160,
		},
		{
			"label": _("Received Qty"),
			"fieldname": "received_qty",
			"fieldtype": "Float",
			"width": 120,
			"convertible": "received_qty",
		},
		{
			"label": _("Accepted Qty"),
			"fieldname": "accepted_qty",
			"fieldtype": "Float",
			"width": 120,
			"convertible": "accepted_qty",
		},
		{
			"label": _("Rejected Qty"),
			"fieldname": "rejected_qty",
			"fieldtype": "Float",
			"width": 120,
			"convertible": "rejected_qty",
		},
		{
			"label": _("Pending Qty"),
			"fieldname": "pending_qty",
			"fieldtype": "Float",
			"width": 120,
			"convertible": "pending_qty",
		},
		{
			"label": _("Pending Amount"),
			"fieldname": "pending_amount",
			"fieldtype": "Currency",
			"width": 110,
			"options": "Company:company:default_currency",
			"convertible": "pending_amount",
		},
		{
			"label": _("PR Return No"),
			"fieldname": "pr_return_no",
			"fieldtype": "Link",
			"options": "Purchase Receipt",
			"width": 160,
		},
		{"label": _("PR Return Date"), "fieldname": "pr_return_date", "fieldtype": "Date", "width": 90},
		{
			"label": _("Supplier Return Qty"),
			"fieldname": "supplier_return_qty",
			"fieldtype": "Float",
			"width": 120,
			"convertible": "supplier_return_qty",
		},
		{
			"label": _("Supplier Return Amount"),
			"fieldname": "supplier_return_amount",
			"fieldtype": "Currency",
			"width": 110,
			"options": "Company:company:default_currency",
			"convertible": "supplier_return_amount",
		},
		# {
		# 	"label": _("Total Accepted QTY in PO"),
		# 	"fieldname": "total_accepted_qty_po",
		# 	"fieldtype": "Float",
		# 	"width": 120,
		# 	"convertible": "total_accepted_qty_po",
		# },
		{
			"label": _("Total Pending QTY in PO"),
			"fieldname": "total_pending_qty_po",
			"fieldtype": "Float",
			"width": 120,
			"convertible": "total_pending_qty_po",
		},
		{
			"label": _("Total Pending Amount"),
			"fieldname": "total_pending_amount",
			"fieldtype": "Currency",
			"width": 110,
			"options": "Company:company:default_currency",
			"convertible": "total_pending_amount",
		}
	]

	

	return columns
	