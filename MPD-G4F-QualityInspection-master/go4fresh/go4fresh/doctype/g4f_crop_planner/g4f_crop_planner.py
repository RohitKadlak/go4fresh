# Copyright (c) 2022, Mannlowe Information Services Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime,timedelta
from frappe.utils.data import add_days
from frappe.contacts.doctype.address.address import get_default_address,get_address_display

class G4FCropPlanner(Document):
	def before_insert(self):
		self.update_data()
					
	def on_update(self):
		self.update_data()
			
	@frappe.whitelist()
	def update_data(self):
		if not self.supplier_name and self.supplier and frappe.db.exists("Supplier",self.supplier):
			self.supplier_name = frappe.db.get_value('Supplier', self.supplier, 'supplier_name')
			
		if not self.supplier_address and self.supplier and frappe.db.exists("Dynamic Link", {'link_doctype':'Supplier','link_name': self.supplier, 'parenttype': 'Address'}):
			links = frappe.db.get_all("Dynamic Link", filters={'link_doctype':'Supplier','link_name': self.supplier, 'parenttype': 'Address'},fields = ['parent'])
			if links:
				self.supplier_address = links[0].parent
				if not self.address_display and links[0].parent:
					self.address_display = get_address_display(links[0].parent)
					
		if self.crop_planner_details:
			for entry in self.crop_planner_details:
				if not entry.harvesting_or_plucking_from_planting_or_sowing and entry.planting_date and entry.crop_name and entry.frst_harvesting_or_plucking_from_planting_or_sowing_in_days:
					entry.harvesting_or_plucking_from_planting_or_sowing = add_days(entry.planting_date, days=entry.frst_harvesting_or_plucking_from_planting_or_sowing_in_days)
				
				if not entry.per_harvest_supply_in_kg and entry.tentative_yield_kgha and entry.no_of_harvesting_or_plucking and entry.planting_area_in_acreage_ha:
					entry.per_harvest_supply_in_kg = round(((entry.planting_area_in_acreage_ha * entry.tentative_yield_kgha)/2.5)/entry.no_of_harvesting_or_plucking)
					if not entry.per_week_capacity and entry.number_of_harvests_per_week:
						entry.per_week_capacity = round(entry.per_harvest_supply_in_kg * entry.number_of_harvests_per_week)
				
				if not entry.total_capacity_in_plant_cycle_kg and entry.planting_area_in_acreage_ha and entry.tentative_yield_kgha:
					entry.total_capacity_in_plant_cycle_kg = round((entry.planting_area_in_acreage_ha * entry.tentative_yield_kgha)/2.5)
					
				if not entry.lasts_harvesting_till:
					entry.lasts_harvesting_till = add_days(entry.harvesting_or_plucking_from_planting_or_sowing,  ((entry.no_of_harvesting_or_plucking-1/entry.number_of_harvests_per_week)*7))
					
				if entry.harvesting_or_plucking_from_planting_or_sowing:
					frst_harvest = entry.harvesting_or_plucking_from_planting_or_sowing
					total_harvest = entry.no_of_harvesting_or_plucking-1
					per_week = entry.number_of_harvests_per_week
					weeks_harvest = 7/per_week
					final_list = [frst_harvest]
					if total_harvest>=1:
						last_harvest = datetime.strptime(frst_harvest, "%Y-%m-%d")+timedelta((total_harvest/per_week)*7)
						harvest = datetime.strptime(frst_harvest, "%Y-%m-%d")+timedelta(weeks_harvest)
						# final_list = [frst_harvest]
						final_list.append(harvest.date().strftime("%Y-%m-%d"))
						weeks1_harvest = weeks_harvest
						for i in range(1,total_harvest):
							weeks1_harvest = weeks1_harvest + weeks_harvest
							harvest = datetime.strptime(frst_harvest, "%Y-%m-%d")+timedelta(weeks1_harvest)
							final_list.append(harvest.date().strftime("%Y-%m-%d"))
				final_list.sort()
				entry.dates_of_harvest = str(final_list)
	
	@frappe.whitelist()
	def cal_till_date(self,frst_harvest,total_harvest,per_week):
		frst_harvest = frst_harvest
		total_harvest = total_harvest-1
		per_week = per_week
		weeks_harvest = 7/per_week
		final_list = [frst_harvest]
		if total_harvest>=1:
			last_harvest = datetime.strptime(frst_harvest, "%Y-%m-%d")+timedelta((total_harvest/per_week)*7)
			harvest = datetime.strptime(frst_harvest, "%Y-%m-%d")+timedelta(weeks_harvest)
			final_list.append(harvest.date().strftime("%Y-%m-%d"))
			weeks1_harvest = weeks_harvest
			for i in range(1,total_harvest):
				weeks1_harvest = weeks1_harvest + weeks_harvest
				harvest = datetime.strptime(frst_harvest, "%Y-%m-%d")+timedelta(weeks1_harvest)
				final_list.append(harvest.date().strftime("%Y-%m-%d"))
		final_list.sort()
		lst = str(final_list)
		last_date = str(final_list[-1])
		return lst,last_date
	
	@frappe.whitelist()
	def crop_update(self):
		for entry in self.crop_planner_details:
			if entry.planting_date and entry.crop_name:
				entry.harvesting_or_plucking_from_planting_or_sowing = add_days(entry.planting_date, days=frappe.db.get_value("G4F Crop List",entry.crop_name,"1st_harvesting_or_plucking_from_planting_or_sowing_in_days"))

			if entry.crop_name:
				doc = frappe.get_doc("G4F Crop List",entry.crop_name)
				if doc.tentative_yield_kgha and doc.no_of_harvesting_or_plucking and entry.planting_area_in_acreage_ha:
					# entry.per_harvest_supply_in_kg = round((doc.tentative_yield_kgha * entry.planting_area_in_acreage_ha)/doc.no_of_harvesting_or_plucking)
					entry.per_harvest_supply_in_kg = round(((entry.planting_area_in_acreage_ha * doc.tentative_yield_kgha)/2.5)/doc.no_of_harvesting_or_plucking)
					if doc.number_of_harvests_per_week:
						entry.per_week_capacity = round(entry.per_harvest_supply_in_kg * doc.number_of_harvests_per_week)
				
				if entry.planting_area_in_acreage_ha and doc.tentative_yield_kgha:
					# entry.total_capacity_in_plant_cycle_kg = round(entry.planting_area_in_acreage_ha * doc.tentative_yield_kgha)
					entry.total_capacity_in_plant_cycle_kg = round((entry.planting_area_in_acreage_ha * doc.tentative_yield_kgha)/2.5)
		# self.save()

	@frappe.whitelist()
	def get_address(self):
		links = frappe.db.get_all("Dynamic Link", filters={'link_doctype':'Supplier','link_name': self.supplier, 'parenttype': 'Address'},fields = ['parent'])
		address = ""
		if links:
			address = frappe.get_doc("Address",links[0].parent)
			
		return address

	@frappe.whitelist()
	def set_supplier_name(self):
		if self.supplier:
			self.supplier_name = frappe.db.get_value('Supplier', self.supplier, 'supplier_name')
			# self.save()

		return "Done"
		
	@frappe.whitelist()
	def get_data(self,crop):
		days = frappe.db.get_value("G4F Crop List",crop,"1st_harvesting_or_plucking_from_planting_or_sowing_in_days")
		if days:
			return days
		else:
			return 0