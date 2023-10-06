# Copyright (c) 2022, Mannlowe Information Services Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.website.website_generator import WebsiteGenerator
from frappe.model.document import Document
from frappe.core.doctype.user.user import generate_keys

class SellerRegistrationForm(WebsiteGenerator):
	pass

class SellerRegistrationForm(Document):    
	@frappe.whitelist( allow_guest=True )
	def update_form(self,addr,sel_doc):
		doc = frappe.get_doc('Address', addr)
		# doc.links = []
		# doc.append('links', {
		# 	'link_doctype': 'Supplier',
		# 	'link_name': sel_doc
		# })
		# doc.save()
		# com =frappe.db.sql(""" select dl.parent from `tabDynamic Link` dl where dl.link_doctype = 'Supplier' and dl.parenttype = 'Contact' and dl.link_name = '{s}' """.format(s=sel_doc), as_dict=True)
		# print(com)
		# for i in com:
		# 	print(i["parent"])
		# 	if frappe.get_doc('Contact', i["parent"]) :
		# 		doc1 = frappe.get_doc('Contact', i["parent"])
		# 		if self.company:
		# 			doc1.company=self.company
		# 			doc1.abbr= self.abbr
		# 		if self.supplier_type == "Farmer":
		# 			doc1.first_name = self.supplier_name
		# 		else:
		# 			doc1.first_name = self.contact_person_name
		# 		doc1.links=[]
		# 		doc1.append("links",{
		# 			"link_doctype":"Seller",
		# 			"link_name":sel_doc
		# 		})
		# 		doc1.save()

	@frappe.whitelist()
	def supplier_automation(self):
		result =  {"supplier":"","user":""}
		if self.supplier_type=="Farmer":
			supplier_doc = frappe.new_doc("Supplier")
			supplier_doc.update({
				'supplier_type' : "Individual" ,
				'company':self.company,
				'abbr':self.abbr,
				# 'mobile_no' : self.mobile_no ,
				'supplier_group' : self.farmer_sub_type ,
				'supplier_name' : self.supplier_name ,
				# 'email_id' : self.email_id ,
				'aadhar_card_no' : self.aadhar_card_no ,
				'attach_kyc_documents' : self.attach_kyc_documents ,
				# // 'primary_address' : self.primary_address ,
				# "supplier_primary_address" : doc1.name,
				'longitude_and_latitude' : self.latitude ,
				# // 'longitude' : self.longitude ,
				'pin_code' : self.postal_code ,
				'tehsil' : self.taluka ,
				'district' : self.district ,
				'state' : self.state ,
				'total_farm_acreage' : self.total_farm_area ,
				'nearest_market' : self.narest_market ,
				'gender' : self.gender ,
				'education' : self.education ,
				'years_in_farming' : self.years_in_farming ,
				'farm_type' : self.farm_type ,
				'total_family_members' : self.total_family_members ,
				'no_of_farm_labour_required' : self.no_of_farm_labour_required ,
				# 'owned_vehicle_types' : self.owned_vehicle_types ,
				'total_owned_vehicles' : self.total_owned_vehicles ,
				'non_f_and_v_crops_cultivated' : self.non_fv_crops_cultivated ,
				'source_of_irrigation' : self.source_of_irrigation ,
				'bank_name' : self.bank_name ,
				'bank_ac_no' : self.bank_ac_no ,
				'ifsc_code' : self.ifsc_code ,
				'type_of_loans' : self.type_of_loans ,
				'total_loan_amount' : self.total_loan_amount ,
				'other_income_sources' : self.other_income_sources ,
				'total_other_income' : self.total_other_income ,
				'packhouse_area' : self.packhouse_area,
				'conneted_transporter_name' :  self.transporter_name,
				'connected_contractor_contact_number' :  self.transporter_contact_number,
				'current_supply_markets' :  self.current_supply_markets,
				'remark_if_any' :  self.remark_if_any,
				'seller_registration_form':self.name,
				'farm_linkage_associate':self.farm_linkage_associate,
				'center_incharge':self.farm_linkage_associate
			})
			supplier_doc.save()

			addr_doc = frappe.new_doc("Address")
			addr_doc.update({
				"address_title" : self.supplier_name,
				"address_type" : "Billing",
				'company':self.company,
				'abbr':self.abbr,
				"address_line1" : self.primary_address,
				"city" :  self.taluka,
				"county" : self.district ,
				"state" : self.state ,
				"pincode" : self.postal_code
			})
			addr_doc.append("links",{
				"link_doctype":"Supplier",
				"link_name":supplier_doc.name,
			})
			addr_doc.save()
			email = ""
			if self.email_id:
				email=self.email_id
			else:
				email = str(self.mobile_no)+"@gmail.com"

			con_doc= frappe.new_doc("Contact")
			con_doc.update({
				'first_name' : self.supplier_name,
				'company':self.company,
				'abbr':self.abbr,
			})
			con_doc.append("email_ids",{
				"email_id":email,
				"is_primary":1
			})
			con_doc.append("phone_nos",{
				"phone":self.mobile_no,
				"is_primary_mobile_no":1
			})
			con_doc.append("links",{
				"link_doctype":"Supplier",
				"link_name":supplier_doc.name,
			})
			con_doc.save()
			
			user_doc = frappe.new_doc("User")
			user_doc.update({
				"first_name" : self.supplier_name,
				"email" : email,
				"mobile_no" : self.mobile_no,
				"role_profile_name" : "Website Seller",
				"user_type" : "System User",
				"module_profile":"Website Seller",
				"new_password":self.supplier_name.split()[0]+"@123"
			})
			user_doc.save()


			user_n = frappe.get_doc("User",{'name':user_doc.name})		
			user_n.user_type = "System User"	
			user_n.save()

			user_perm_doc=frappe.new_doc("User Permission")
			user_perm_doc.update({
				"user":user_doc.name,
				"allow":"Supplier",
				"for_value":supplier_doc.name,
				"apply_to_all_doctypes":1
			})
			user_perm_doc.save()
			
			gene_api=generate_keys(user_doc.name)
			self.supplier = supplier_doc.name
			self.user = user_doc.name
			self.save()
			frappe.msgprint(f'{supplier_doc.doctype} {supplier_doc.name} created on {supplier_doc.creation} & {user_doc.doctype} {user_doc.name} created on {user_doc.creation}')
			result = {"supplier":supplier_doc.name,"user":user_doc.name}
		
	@frappe.whitelist()
	def aggre_automation(self):
		result =  {"user":""}
		if self.supplier_type=="Company/Traders" or self.supplier_type=="Farmer Group":
			# sup_type = ""
			# members = ""
			# if self.supplier_type=="Company/Traders":
			# 	sup_type = self.company_sub_type
			# 	members = self.no_of_vendors
			# elif self.supplier_type=="Farmer Group":
			# 	sup_type = self.farmer_group_sub_type
			# 	members = self.no_of_member_farmers
			# else:
			# 	sup_type = ""
			# 	members = ""
			# supplier_doc = frappe.new_doc("Supplier")
			# supplier_doc.update({
			# 	'supplier_type' : "Company" ,
			# 	'company':self.company,
			# 	'abbr':self.abbr,
			# 	'total_farm_acreage' : self.total_farm_area ,
			# 	'mobile_no' : self.alternate_mobile_no ,
			# 	'supplier_group' : sup_type ,
			# 	'supplier_name' : self.supplier_name ,
			# 	'email_id' : self.email_id ,
			# 	'pan' : self.pan ,
			# 	'contact_person_name' : self.contact_person_name ,
			# 	'alternate_mobile_no' : self.alternate_mobile_no ,
			# 	'gst_no' : self.gst_no ,
			# 	'attach_kyc_documents' : self.attach_kyc_documents ,
			# 	'longitude_and_latitude' : self.latitude ,
			# 	'pin_code' : self.postal_code ,
			# 	'tehsil' : self.taluka ,
			# 	'district' : self.district ,
			# 	'state' : self.state ,
			# 	'total_farm_acreage' : self.total_farm_area ,
			# 	'nearest_market' : self.narest_market ,
			# 	'company_type' : self.company_type ,
			# 	'trade_experience' : self.trade_experience ,
			# 	'annual_volume' : self.annual_volume ,
			# 	'annual_sales_value' : self.annual_sales_value ,
			# 	'digital_platform' : self.digital_platform ,
			# 	'no_of_vendors' : members ,
			# 	'team_size' : self.team_size ,
			# 	'total_owned_vehicles' : self.total_owned_vehicles ,
			# 	'contract_staff' : self.contract_staff ,
			# 	'office_type' : self.office_type ,
			# 	'warehouse' : self.warehouse ,
			# 	'no_of_warehouses' : self.no_of_warehouses ,
			# 	'processing_unit' : self.processing_unit ,
			# 	'farm_infrastructure' : self.farm_infrastructure ,
			# 	# 'rental_equipments' : self.rental_equipments ,
			# 	'number_of_cattle' : self.number_of_cattle ,
			# 	'packhouse_area' : self.packhouse_area,
			# 	'conneted_transporter_name' :  self.transporter_name,
			# 	'connected_contractor_contact_number' :  self.transporter_contact_number,
			# 	'current_supply_markets' :  self.current_supply_markets,
			# 	'remark_if_any' :  self.remark_if_any,
			# 	'bank_name' : self.bank_name ,
			# 	'bank_ac_no' : self.bank_ac_no ,
			# 	'ifsc_code' : self.ifsc_code ,
			# 	'seller_registration_form':self.name,
			# 	'farm_linkage_associate':self.farm_linkage_associate,
			# 	'center_incharge':self.farm_linkage_associate
			# })
			# print(supplier_doc.naming_series)
			# supplier_doc.save()

			# addr_doc = frappe.new_doc("Address")
			# addr_doc.update({
			# 	"address_title" : self.supplier_name,
			# 	"address_type" : "Billing",
			# 	'company':self.company,
			# 	'abbr':self.abbr,
			# 	"address_line1" : self.primary_address,
			# 	"city" :  self.taluka,
			# 	"county" : self.district ,
			# 	"state" : self.state ,
			# 	"pincode" : self.postal_code
			# })
			# addr_doc.append("links",{
			# 	"link_doctype":"Supplier",
			# 	"link_name":supplier_doc.name,
			# })
			# addr_doc.save()
			email = ""
			if self.email_id:
				email=self.email_id
			else:
				email = str(self.mobile_no)+"@gmail.com"
				
			# con_doc= frappe.new_doc("Contact")
			# con_doc.update({
			# 	'first_name' : self.contact_person_name if self.contact_person_name else self.supplier_name,
			# 	'company':self.company,
			# 	'abbr':self.abbr,
			# })
			# con_doc.append("email_ids",{
			# 	"email_id":email,System User
			# 	"is_primary":1
			# })
			# con_doc.append("phone_nos",{
			# 	"phone":self.mobile_no,
			# 	"is_primary_mobile_no":1
			# })
			# con_doc.append("links",{
			# 	"link_doctype":"Supplier",
			# 	"link_name":supplier_doc.name,
			# })
			# con_doc.save()
			
			user_doc = frappe.new_doc("User")
			# user_doc.update({
			# 	"first_name" : self.supplier_name,
			# 	"email" : email,
			# 	"mobile_no" : self.mobile_no,
			# 	"role_profile_name" : "Aggregator",
			# 	"user_type" : "System User",
			# 	"module_profile":"Aggregator Module",
			# 	"new_password":self.supplier_name.split()[0]+"@123"
			# })
			user_doc.first_name = self.supplier_name
			user_doc.email=email
			user_doc.mobile_no = self.mobile_no
			user_doc.role_profile_name = "Aggregator"
			# user_doc.user_type = "System User"
			user_doc.module_profile = "Aggregator Module"
			user_doc.new_password = self.supplier_name.split()[0]+"@123"
			user_doc.save()

			user_n = frappe.get_doc("User",{'name':user_doc.name})		
			user_n.user_type = "System User"	
			user_n.save()
			# user_perm_doc=frappe.new_doc("User Permission")
			# user_perm_doc.update({
			# 	"user":user_doc.name,
			# 	"allow":"Supplier",
			# 	"for_value":supplier_doc.name,
			# 	"apply_to_all_doctypes":1
			# })
			# user_perm_doc.save()
			
			# gene_api=generate_keys(user_doc.name)
			
			# self.supplier = supplier_doc.name
			# self.user = user_doc.name
			# self.save()

			# frappe.msgprint(f'{supplier_doc.doctype} {supplier_doc.name} created on {supplier_doc.creation} & {user_doc.doctype} {user_doc.name} created on {user_doc.creation}')
			frappe.msgprint(f'{user_doc.doctype} {user_doc.name} created on {user_doc.creation}')
			result = {"user":user_doc.name}  #"supplier":supplier_doc.name,

		return result