# Copyright (c) 2022, Mannlowe Information Services Pvt. Ltd. and contributors
# For license information, please see license.txt

import re
from pymysql import NULL            
import requests
import frappe
import pandas as pd
import warnings
warnings.simplefilter('ignore')
from frappe.model.document import Document

class ExcelUploadTool(Document):
	@frappe.whitelist()
	def extract_data(self):
		if self.customer_name == "Ankapali":
			df=pd.read_excel(frappe.get_site_path()+"/public"+self.attach_pdf_or_image,header=4)
			data=pd.read_excel(frappe.get_site_path()+"/public"+self.attach_pdf_or_image,usecols=[1,4,6])

			df=df[["NAME OF VEGETABLE","QUANTITY","UNIT"]].dropna(axis = 0, how ='all')
			df['PROJECT NAME']=data.iloc[1,0].split(":-")[1]
			df['DELIVERY DATE']=data.iloc[1,1].split(":-")[1]
			df["CAMP NAME"]=data.iloc[1,2].split(":")[1]
			# print(df["NAME OF VEGETABLE"].str.replace('[^a-zA-Z0-9]', ''))
			# print(df)
			for index, row in df.iterrows():
				sys_item = frappe.db.sql(""" select parent from `tabItem Customer Detail` where ref_code = '{0}' """.format(re.sub("[^a-zA-Z0-9]+", "",row["NAME OF VEGETABLE"])),as_dict = True)
				if sys_item and row["QUANTITY"] !=None and row["QUANTITY"] != 0:
					self.append("found_items",{
						"item_code" : re.sub("[^a-zA-Z0-9]+", "",row["NAME OF VEGETABLE"]),
						"item" : sys_item[0].get("parent") if sys_item else "",
						"qty" : row["QUANTITY"],
					})
				else:
					if row["QUANTITY"] != 0 and type(row["NAME OF VEGETABLE"])==str:
						self.append("not_found_items",{
							"item_code" : re.sub("[^a-zA-Z0-9]+", "",row["NAME OF VEGETABLE"]),
							"item" : sys_item[0].get("parent") if sys_item else "",
							"qty" : row["QUANTITY"],
						})			
			self.save()
			self.reload()

		if self.customer_name == "Nighali Coal Mines":
			df3=pd.read_excel(frappe.get_site_path()+"/public"+self.attach_pdf_or_image,usecols=[2,4,5,6,7,8,9,10,11],header=2).dropna(axis = 0, how ='all')
			# with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
				# print(df3["ITEM"])
				
			for index, row in df3.iterrows():
				sys_item = frappe.db.sql(""" select parent from `tabItem Customer Detail` where ref_code = '{0}' """.format(row["ITEM"] if type(row["ITEM"]) == str else "a"),as_dict = True)
				if sys_item and row["TOTAL \nQUANTITY"] !=None and row["TOTAL \nQUANTITY"] != 0:
					self.append("found_items",{
						"item_code" : row["ITEM"] if type(row["ITEM"]) == str else "",
						"item" : sys_item[0].get("parent") if sys_item else "",
						"qty" : row["TOTAL \nQUANTITY"] if row["TOTAL \nQUANTITY"]!= "NaN" else "",
					})
				else:
					if row["TOTAL \nQUANTITY"] != 0 and type(row["ITEM"])==str:
						self.append("not_found_items",{
							"item_code" : row["ITEM"] if type(row["ITEM"]) == str else "",	
							"item" : sys_item[0].get("parent") if sys_item else "",
							"qty" : row["TOTAL \nQUANTITY"] if row["TOTAL \nQUANTITY"]!= "NaN" else "",
						})			
			self.save()
			self.reload()

		if self.customer_name == "Gagangoor":
			# df2=pd.read_excel(frappe.get_site_path()+"/public"+self.attach_pdf_or_image,usecols=[1,6,11],header=None)
			d1=pd.read_excel(frappe.get_site_path()+"/public"+self.attach_pdf_or_image,usecols=[1,2,3],header=1).dropna(axis = 0, how ='all')
			# d2=pd.read_excel(frappe.get_site_path()+"/public"+self.attach_pdf_or_image,usecols=[6,7,8],header=1).dropna(axis = 0, how ='all')
			# d3=pd.read_excel(frappe.get_site_path()+"/public"+self.attach_pdf_or_image,usecols=[11,12,13],header=1).dropna(axis = 0, how ='all')

			# d1["CAMP NAME"]=df2.iloc[0,0].split(" ",1)[1]
			# d2["CAMP NAME"]=df2.iloc[0,1]
			# d3["CAMP NAME"]=df2.iloc[0,2]

			# d2.columns=d1.columns
			# d3.columns=d1.columns

			# df_new=d1.append(d2, ignore_index=True).append(d3, ignore_index=True)
			df_new = d1
			print(df_new)
   
			for index, row in df_new.iterrows():
				sys_item = frappe.db.sql(""" select parent from `tabItem Customer Detail` where ref_code = '{0}' """.format(row["ITEM"]),as_dict = True)
				if sys_item and row["QTY"] !=None and row["QTY"] != 0:
					self.append("found_items",{
						"item_code" : row["ITEM"],
						"item" : sys_item[0].get("parent") if sys_item else "",
						"qty" : row["QTY"],
                        # "rate" : row["Prices"],
					})
				else:
					if row["QTY"] != 0 and row["ITEM"]!="TOTAL QTY":
						self.append("not_found_items",{
							"item_code" : row["ITEM"],
							"item" : sys_item[0].get("parent") if sys_item else "",
							"qty" : row["QTY"],
						})			
			self.save()
			self.reload()

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
		self.reload()
		return len(self.found_items)

	@frappe.whitelist()
	def create_qt(self):
		doc = frappe.new_doc("Quotation")
		doc.party_name = self.customer
		doc.items = []
		for i in  self.found_items:
			doc.append("items",{
				"item_code" : i.item ,
				"rate" : i.rate ,
				"qty" : i.qty
			})
		self.quotation = doc.name
		doc.save()
		doc.reload()
		self.quotation = doc.name
		self.quotation_date = doc.transaction_date
		self.save()
		self.reload()
		return "Successfully Created Quotation "+doc.name