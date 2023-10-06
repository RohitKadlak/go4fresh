# Copyright (c) 2022, Mannlowe Information Services Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.contacts.doctype.address.address import get_address_display
class G4FSellYourProduce(Document):
	def before_save(self):
		if self.supplier and not self.address:
			sup_name = frappe.get_value("Supplier",self.supplier,"supplier_name")
			self.supplier_name = sup_name
			addr =frappe.db.sql(""" SELECT dl.parent FROM `tabDynamic Link` dl WHERE dl.link_doctype = 'Supplier' AND dl.parenttype = 'Address' AND dl.link_name = '{s}' """.format(s=self.supplier), as_dict=True)
			if addr:
				self.address= addr[0]["parent"]
				if self.address:
					self.address_display=get_address_display(self.address)
			
	@frappe.whitelist()
	def fetch_data(self):
		sup_name = frappe.get_value("Supplier",self.supplier,"supplier_name")
		self.supplier_name = sup_name
		addr =frappe.db.sql(""" SELECT dl.parent FROM `tabDynamic Link` dl WHERE dl.link_doctype = 'Supplier' AND dl.parenttype = 'Address' AND dl.link_name = '{s}' """.format(s=self.supplier), as_dict=True)
		if addr:
			return addr[0]["parent"]
			
	@frappe.whitelist()
	def copy_data(self):
		crop = frappe.get_doc("G4F Crop List",self.crop)
		if crop:
			if crop.map_items:
				print("running")
				self.items = []
				for i in crop.map_items:
					self.append("items",{
						"grade_name":i.grade_name,
						"item_code":i.item_code,
						"item_name":i.item_name,
						"uom":i.uom
					})
	
	@frappe.whitelist()
	def calculate(self):
		total = 0.00
		for i in self.items:
			total = total + i.qty
		self.total_qty = total