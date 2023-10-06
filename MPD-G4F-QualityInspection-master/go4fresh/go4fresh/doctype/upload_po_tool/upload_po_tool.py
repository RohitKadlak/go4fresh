
# Copyright (c) 2022, Mannlowe Information Services Pvt. Ltd. and contributors
# For license information, please see license.txt


import os                    
import requests
import frappe
from frappe.model.document import Document

class UploadPOTool(Document):
	@frappe.whitelist()
	def update_info(self):
		not_found = []
		for i in self.not_found_items:
			if i.item:
				self.append("found_items",{
					"item_code" : i.item_code,
					"item" : i.item,
					"qty" : i.qty,
					"rate" : i.rate,
					"description" : i.description
				})
			else:
				not_found.append({
					"item_code" : i.item_code,
					"item" : i.item,
					"qty" : i.qty,
					"rate" : i.rate,
					"description" : i.description
				})
		self.not_found_items = []
		if not_found:
			for i in not_found:
				self.append("not_found_items",{
					"item_code" : i["item_code"],
					"item" : i["item"],
					"qty" : i["qty"],
					"rate" : i["rate"],
					"description" : i["description"]
				})
		self.save()
		return len(self.found_items)
	
	@frappe.whitelist()
	def update_so(self):
		print("called")
		doc = frappe.get_doc("Sales Order",self.so_no)
		print(doc.name)
		doc.items = []
		for i in  self.found_items:
			doc.append("items",{
				"item_code" : i.item ,
				"rate" : i.rate ,
				"qty" : i.qty
			})
		doc.save()
		doc.reload()
		return "Successfully Updated Sales Order "+self.so_no+" Items.."

				


	@frappe.whitelist()
	def upload_data(self):
		# frappe.throw(self.attach_pdf_or_image)
		if(self.attach_pdf_or_image):
			url = 'https://sds.mannlowe.com/backend/api/auth/login/'
			obj = {"email":"shrikant.pawar@mannlowe.com" , "password":"s_pawar@123"}
			res = requests.post(url,data=obj)
			res = res.json()
			if res.get("access"):
				out = upload_file(self.attach_pdf_or_image,res.get("access"),self.name,self.customer_name)
				if out:	
					if out.status_code == 201:
						frappe.msgprint({
							"title": 'Notification',
							"indicator": 'green',
							"message": 'Document updated successfully'
						})
					else:
						frappe.throw("File Not Uploaded... Subscription not Valid/Expired.")

def upload_file(file,tok,docname,customer_name):
	url = "https://sds.mannlowe.com/backend/api/sds/upload/"
	headers = {
	'Authorization': 'Bearer ' + tok
	}
	data = {"docname":docname,"group":"Go4Fresh","customer_name":customer_name}
	file_path = frappe.get_site_path()+"/public"+file
	if ((frappe.get_site_path()+"/public"+file).endswith(".png")):
		files = {'image': (os.path.basename(frappe.get_site_path()+"/public"+file), open(frappe.get_site_path()+"/public"+file, 'rb'), 'application/octet-stream')}
		r2 = requests.post(url, files=files, headers=headers,data = data)
		if r2.status_code == 201:
				return r2
		else :
			frappe.throw("File Not Uploaded... Subscription not Valid/Expired.")
		# return r2
	elif ((frappe.get_site_path()+"/public"+file).endswith(".pdf")):
		files  = {'file': (os.path.basename(frappe.get_site_path()+"/public"+file), open(frappe.get_site_path()+"/public"+file, 'rb'), 'application/octet-stream')}
		r2 = requests.post(url, files=files, headers=headers,data = data)
		if r2.status_code == 201:
			return r2
		else :
			frappe.throw("File Not Uploaded... Subscription not Valid/Expired.")
		# return r2
	else:
		frappe.throw("Unsupported File")
	# if os.path.isfile(file_path):
	# 	file_extension = os.path.splitext(file_path)[1]
	# 	print(file_extension,"*"*40)
	# 	if file_extension.lower() == ".png":
	# 		files = {'image': (os.path.basename(frappe.get_site_path()+"/public"+file), open(frappe.get_site_path()+"/public"+file, 'rb'), 'application/octet-stream')}
	# 		r2 = requests.post(url, files=files, headers=headers,data = data)
	# 		return r2
	# 	elif file_extension.lower() == ".pdf":
	# 		files  = {'file': open(frappe.get_site_path()+"/public"+file, 'rb')}
	# 		r2 = requests.post(url, files=files, headers=headers,data = data)
	# 		return r2
	# 	else:
	# 		frappe.throw("Unsupported File")

	# files = {'image': (os.path.basename(frappe.get_site_path()+"/public"+file), open(frappe.get_site_path()+"/public"+file, 'rb'), 'application/octet-stream')}
	# r2 = requests.post(url, files=files, headers=headers,data = data)
	