# Copyright (c) 2022, Mannlowe Information Services Pvt. Ltd. and contributors
# For license information, please see license.txt


from re import A
import frappe
from frappe.model.document import Document
from datetime import datetime
from frappe.utils import add_to_date
from frappe.model.document import Document
from frappe.contacts.doctype.address.address import get_address_display

class G4FFarmBook(Document):
	# pass
	def before_insert(self):
		if not self.seller_name:
			self.seller_name = frappe.db.get_value('Supplier', self.seller, 'supplier_name')
		if not self.seller_address:
			links = frappe.db.get_all("Dynamic Link", filters={'link_doctype':'Supplier','link_name': self.seller, 'parenttype': 'Address'},fields = ['parent'])
			address = ""
			if links:
				address = frappe.get_doc("Address",links[0].parent)
				if address!="":
					self.seller_address = address.name
					self.address_display = get_address_display(address_dict = address.name)
		
		if not self.total_cost:
			if len(self.g4f_farm_book_activities)!=0:
				a = 0
				for i in self.g4f_farm_book_activities:
					a=a+i.amount
				self.total_cost = a
				
	@frappe.whitelist()
	def get_address(self):
		links = frappe.db.get_all("Dynamic Link", filters={'link_doctype':'Supplier','link_name': self.seller, 'parenttype': 'Address'},fields = ['parent'])
		address = ""
		if links:
			address = frappe.get_doc("Address",links[0].parent)
			
		return address

	@frappe.whitelist()
	def set_supplier_name(self):
		if self.seller:
			self.seller_name = frappe.db.get_value('Supplier', self.seller, 'supplier_name')
			# self.save()

		return "Done"
