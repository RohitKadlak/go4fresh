# Copyright (c) 2022, Mannlowe Information Services Pvt. Ltd. and contributors
# For license information, please see license.txt


import frappe
from frappe import _
from frappe.utils import date_diff, flt, getdate
import pandas as pd
import datetime


def execute(filters=None):
	columns = get_columns(filters)
	conditions = get_conditions(filters)

	data = get_data(conditions, filters)
	if not data:
		return [], [], None, []

	# data, chart_data,report_summary = prepare_data(data, filters)

	return columns, data #, None, chart_data,report_summary


def get_conditions(filters):
	conditions = ""
	if filters.get("created_from") and filters.get("created_to"):
		conditions += " and rdn.creation between %(created_from)s and %(created_to)s"
  
	return conditions

def get_data(conditions, filters):
		
	data = frappe.db.sql(
		"""
		SELECT
			rdn.name as unique_id,
			rdn.name as return_delivery_note,
			CONCAT(rdn.posting_date," ",rdn.posting_time) as return_created_date,
			dn.name as delivery_note,
			CONCAT(dn.posting_date," ",dn.posting_time) as created_date,
			rdn.posting_date as r_posting_date,
			dn.posting_date as posting_date

		FROM
			`tabDelivery Note` rdn
		LEFT JOIN `tabDelivery Note` dn
			ON  dn.name = rdn.return_against AND dn.is_return="0" AND dn.docstatus = "1"

		WHERE
			rdn.docstatus = "1"
			AND rdn.is_return ="1"
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
		print(a["return_created_date"])
		diff = datetime.datetime.strptime(a["return_created_date"],'%Y-%m-%d %H:%M:%S.%f')-datetime.datetime.strptime(a["created_date"],'%Y-%m-%d %H:%M:%S.%f') 
		print(diff.total_seconds())
		time = diff.total_seconds()
		day = time // (24 * 3600)
		time = time % (24 * 3600)
		hour = time // 3600
		time %= 3600
		minutes = time // 60
		time %= 60
		seconds = time
		# print("d:h:m:s-> %d:%d:%d:%d" % (day, hour, minutes, seconds))
		a["time_diff"] = str(int(day))+":Days "+str(int(hour))+":Hrs "+str(int(minutes))+":Min "+str(int(seconds))+":Sec"
	return data

def get_columns(filters):
	columns = [
		{
			"label": _("Unique ID"),
			"fieldname": "unique_id",
			"fieldtype": "Data",
			"width": 160
		},
		{
			"label": _("Returned Delivery Note"),
			"fieldname": "return_delivery_note",
			"fieldtype": "Link",
			"options": "Delivery Note",
			"width": 160,
		},
		{
			"label": _("Return Created Date"),
			"fieldname": "return_created_date",
			"fieldtype": "Date",
			"width": 160
		},
		{
			"label": _("Delivery Note"),
			"fieldname": "delivery_note",
			"fieldtype": "Link",
			"options": "Delivery Note",
			"width": 160,
		},
		{
			"label": _("Created Date"),
			"fieldname": "created_date",
			"fieldtype": "Date",
			"width": 160
		},
		{
			"label": _("Time Difference"),
			"fieldname": "time_diff",
			"fieldtype": "Data",
			"width": 160
		},
		{
			"label": _("Posting Date"),
			"fieldname": "posting_date",
			"fieldtype": "Date",
			"width": 160,
			"hidden":1
		},
		{
			"label": _("Return Posting Date"),
			"fieldname": "r_posting_date",
			"fieldtype": "Date",
			"width": 160,
			"hidden":1
		},
	]

	

	return columns
	
