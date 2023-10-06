from urllib.error import HTTPError
import frappe
import json
from frappe import auth
from pkg_resources import yield_lines
from frappe.client import insert
from datetime import datetime,timedelta


@frappe.whitelist(allow_guest=True)
def get_crop_details(crop):
	data = frappe.db.sql(
		"""
			SELECT
				c.name AS name,
				c.tentative_yield_kgha AS tentative_yield_kgha,
				c.no_of_harvesting_or_plucking AS no_of_harvesting_or_plucking,
				c.1st_harvesting_or_plucking_from_planting_or_sowing_in_days AS 1st_harvesting_or_plucking_from_planting_or_sowing_in_days,
				c.number_of_harvests_per_week AS number_of_harvests_per_week,
				"" AS map_items
			FROM
				`tabG4F Crop List` c
			WHERE 
				c.name = '{0}'
		""".format(crop),as_dict=1)
	for i in data:
		i["map_items"]=[]
		it = frappe.db.sql(
			"""
			SELECT
				it.grade_name as grade_name,
				it.item_code as item_code,
				it.item_name as item_name,
				it.uom as uom
	
			FROM
				`tabG4F Sell Your Produce Item` it
			
			WHERE
				it.parent = '{0}'
			ORDER BY
				it.idx
		""".format(
				i["name"]
			),
			as_dict=1
		)
		for k in it:	
			i["map_items"].append(k)
	return data

@frappe.whitelist(allow_guest=True)
def get_crop_data():
	crop = frappe.db.sql(
		"""
			SELECT 
				c.name as crop_name,
				c.tentative_yield_kgha as tantative_yield,
				c.no_of_harvesting_or_plucking as no_of_harvesting_or_plucking,
				c.1st_harvesting_or_plucking_from_planting_or_sowing_in_days as first_harvesting_or_plucking_from_planting_or_sowing_in_days,
				c.number_of_harvests_per_week as number_of_harvests_per_week,
				"" as map_items
			FROM
				`tabG4F Crop List` c
		""",as_dict=1)
	for i in crop:
		i["map_items"]=[]
		it = frappe.db.sql(
			"""
			SELECT
				it.grade_name as grade_name,
				it.item_code as item_code,
				it.item_name as item_name,
				it.uom as uom
	
			FROM
				`tabG4F Sell Your Produce Item` it
			
			WHERE
				it.parent = '{0}'
			ORDER BY
				it.idx
		""".format(
				i["crop_name"]
			),
			as_dict=1
		)
		for k in it:	
			i["map_items"].append(k)
	return crop
	
@frappe.whitelist(allow_guest=True)
def sell_your_produce(seller):
	data = frappe.db.sql(
		"""
		SELECT
			syp.creation as created_date,
			syp.modified as modified_date,
			syp.name as sell_your_produce_name,
			syp.supplier as seller,
			syp.supplier_name as seller_name,
			syp.address as address,
			syp.address_display as seller_address,
			syp.crop as crop,
			"" as items,
			syp.posting_date as sell_your_produce_date

		FROM
			`tabG4F Sell Your Produce` syp

		WHERE
			syp.name != "" AND
			syp.supplier = '{0}'
		
		ORDER BY
			syp.creation DESC
	""".format(
			seller
		),
		as_dict=1
	)
	for i in data:
		i["items"] = []
		fba = frappe.db.sql(
			"""
			SELECT
				sypi.grade_name as grade_name,
				sypi.item_code as item_code,
				sypi.item_name as item_name,
				sypi.uom as uom,
				sypi.qty as qty
	
			FROM
				`tabG4F Sell Your Produce Item` sypi
			
			WHERE
				sypi.parent = '{0}'
			ORDER BY
				sypi.idx
		""".format(
				i["sell_your_produce_name"]
			),
			as_dict=1
		)
		for k in fba:	
			i["items"].append(k)
	
		i["sell_your_produce_date"] = (i["sell_your_produce_date"]).strftime('%d/%m/%Y')
	return data

@frappe.whitelist(allow_guest=True)
def farm_book(seller):
	data = frappe.db.sql(
		"""
		SELECT
			fb.creation as created_date,
			fb.modified as modified_date,
			fb.name as farm_book_name,
			fb.seller as seller,
			fb.seller_name as seller_name,
			fb.seller_address as address,
			fb.address_display as seller_address,
			fb.crop as crop,
			"" as farm_book_activity,
			fb.date as farm_book_creation_date,
			fb.planting_date as planting_date

		FROM
			`tabG4F Farm Book` fb

		WHERE
			fb.name != "" AND
			fb.seller = '{0}'
		ORDER BY
			fb.creation DESC
	""".format(
			seller
		),
		as_dict=1
	)
	for i in data:
		i["farm_book_activity"] = []
		fba = frappe.db.sql(
			"""
			SELECT
				fba.name as farm_book_activity_name,
				fba.activity as activity,
				fba.particulars as particulars,
				fba.quantity as quantity,
				fba.uom as uom,
				fba.amount as amount
	
			FROM
				`tabG4F Farm Book Activities` fba
			
			WHERE
				fba.parent = '{0}'
			ORDER BY
				fba.idx
		""".format(
				i["farm_book_name"]
			),
			as_dict=1
		)
		for k in fba:	
			i["farm_book_activity"].append(k)
	
		i["farm_book_creation_date"] = (i["farm_book_creation_date"]).strftime('%d/%m/%Y')
	return data



	# if crop and for_date and seller:
	#     for_date = (datetime.strptime(for_date, '%d/%m/%Y')).strftime('%Y-%m-%d')
	#     data = frappe.db.sql(
	# 		"""
	# 		SELECT
	# 			cpd.crop_name as crop_name,
	# 			COALESCE(SUM(cpd.per_week_capacity),0) AS per_week_capacity
	# 		FROM
	# 			`tabG4F Crop Planner Details` cpd
	# 		LEFT JOIN `tabG4F Crop Planner` cp
	# 			ON cp.name = cpd.parent
	
	# 		WHERE
	# 			cp.supplier = '{0}' AND
	# 			cpd.crop_name = '{1}' AND
	# 			'{2}' between cpd.frst_harvesting_or_plucking_from_planting_or_sowing_in_days AND cpd.lasts_harvesting_till
	# 	""".format(
	# 			seller,crop,for_date
	# 		),
	# 		as_dict=1
	# 	)
	#     return data
@frappe.whitelist(allow_guest=True)
def track_harvesting(crop,for_date,seller):    
	if crop and for_date and seller:
		for_date = (datetime.strptime(for_date, '%d/%m/%Y')).strftime('%Y-%m-%d')
		for_date = (datetime.strptime(for_date, '%Y-%m-%d'))
		dict_obj = [
						{"date":(for_date - timedelta(1)).strftime('%Y-%m-%d'),"yield":0},
						{"date":(for_date).strftime('%Y-%m-%d'),"yield":0},
						{"date":(for_date + timedelta(1)).strftime('%Y-%m-%d'),"yield":0}
					]
		data = frappe.db.sql(
			"""
			SELECT
				cp.name as name,
				cp.supplier as seller,
				cpd.crop_name as crop_name,
				cpd.per_harvest_supply_in_kg AS per_harvest_supply_in_kg,
				cpd.dates_of_harvest as dates_of_harvest
			FROM
				`tabG4F Crop Planner Details` cpd
			LEFT JOIN `tabG4F Crop Planner` cp
				ON cp.name = cpd.parent
	
			WHERE
				cp.supplier = '{0}' AND
				cpd.crop_name = '{1}' AND
				'{2}' between cpd.frst_harvesting_or_plucking_from_planting_or_sowing_in_days AND cpd.lasts_harvesting_till
		""".format(
				seller,crop,for_date
			),
			as_dict=1
		)
		date_lst = [a["date"] for a in dict_obj]
		for i in data:
			if i["dates_of_harvest"] and len(i["dates_of_harvest"])>2:
				dates_of_harvest = i["dates_of_harvest"].replace("'","").strip("][").split(', ')
				for j in date_lst:
					if j in dates_of_harvest:
						for k in dict_obj:
							if j == k["date"]:
								k["yield"] = k["yield"] + i["per_harvest_supply_in_kg"]
		for i in dict_obj:
			i["date"] = (datetime.strptime(i["date"], '%Y-%m-%d')).strftime('%d/%m/%Y')
		return dict_obj
		# 				dict_obj[j] = dict_obj[j] + i["per_harvest_supply_in_kg"]
		# return {(datetime.strptime(a, '%Y-%m-%d')).strftime('%d/%m/%Y'):b for a, b in dict_obj.items()}  #dict_obj


@frappe.whitelist(allow_guest=True)
def crop_planner_details(seller):
	data = frappe.db.sql(
		"""
		SELECT
			cpd.creation as created_date,
			cpd.modified as modified_date,
			cp.name as crop_planner_name,
			cp.name as unique_id,
			cp.supplier as supplier,
			cp.supplier_name as supplier_name,
			cp.supplier_address as address,
			cp.address_display as supplier_address,
			cp.date as crop_registration_date,
			cpd.name as crop_planner_detail_name,
			cpd.crop_name as crop_name,
			cpd.planting_date as planting_date,
			cpd.planting_area_in_acreage_ha,
			cpd.tentative_yield_kgha,
			cpd.no_of_harvesting_or_plucking,
			cpd.frst_harvesting_or_plucking_from_planting_or_sowing_in_days,
			cpd.number_of_harvests_per_week,
			cpd.per_harvest_supply_in_kg,
			cpd.total_capacity_in_plant_cycle_kg as total_capacity_in_plant_cycle,
			cpd.per_week_capacity as per_week_capacity_in_kg,
			cpd.harvesting_or_plucking_from_planting_or_sowing as harvesting_or_plucking_from

		FROM
			`tabG4F Crop Planner Details` cpd
		LEFT JOIN `tabG4F Crop Planner` cp
			ON cp.name = cpd.parent

		WHERE
			cp.name != "" AND
			cp.supplier = '{0}'
		ORDER BY
			cpd.creation DESC
	""".format(
			seller
		),
		as_dict=1
	)
	return data
	
@frappe.whitelist(allow_guest=True)
def farm_book_details(seller):
	data = frappe.db.sql(
		"""
		SELECT
			fba.creation as created_date,
			fba.modified as modified_date,
			fb.name as farm_book_name,
			fb.name as unique_id,
			fb.seller as seller,
			fb.seller_name as seller_name,
			fb.seller_address as address,
			fb.address_display as seller_address,
			fb.crop as crop,
			fb.date as farm_book_creation_date,
			fba.name as farm_book_activity_name,
			fba.activity_name as activity,
			fba.particulars as particulars,
			fba.quantity as quantity,
			fba.uom as uom,
			fba.amount as amount

		FROM
			`tabG4F Farm Book Activities` fba
		LEFT JOIN `tabG4F Farm Book` fb
			ON fb.name = fba.parent

		WHERE
			fb.name != "" AND
			fb.seller = '{0}'
		ORDER BY
			fba.creation DESC
	""".format(
			seller
		),
		as_dict=1
	)
	return data

 
@frappe.whitelist(allow_guest=True)
def calculate_values(data):
	data = json.loads(data)
	value = frappe.db.get_value('G4F Crop List', data["crop"], 'tentative_yield_kgha')
	return value


@frappe.whitelist( allow_guest=True )
def user_login(usr, pwd):
	try:
		login_manager = frappe.auth.LoginManager()
		login_manager.authenticate(user=usr, pwd=pwd)
		login_manager.post_login()
	except frappe.exceptions.AuthenticationError:
		frappe.clear_messages()
		frappe.local.response['http_status_code'] = 404
		frappe.local.response["message"] = {
			"success_key":0,
			"message":"Authentication Error!"
		}

		return

	api_generate = generate_keys(frappe.session.user)
	user = frappe.get_doc('User', frappe.session.user)
	# print(user.api_key,api_generate,"*"*40)
	seller = None
	aggregator_details=[]
	if user.mobile_no:
		if frappe.db.exists("Seller Registration Form",user.mobile_no) :
			sel_reg = frappe.get_doc("Seller Registration Form",user.mobile_no)
			if sel_reg:
				if sel_reg.status == "Verified Seller":
					if sel_reg.supplier:
						seller = sel_reg.supplier
						sel_form = frappe.get_doc("Supplier",seller)
						if sel_form.farmer_reference_table:
							for i in sel_form.farmer_reference_table:
								aggregator_details.append({
									"aggregator_code":i.supplier_code,
									"aggregator_name":i.supplier_name,
									"aggregator_company":frappe.get_value("Supplier",i.supplier_code,"company") if frappe.db.exists("Supplier",i.supplier_code) else "",
									"aggregator_mobile_no":frappe.get_value("Supplier",i.supplier_code,"mobile_no") if frappe.get_value("Supplier",i.supplier_code,"mobile_no") else get_contact_number(i.supplier_code)
								})				
		elif frappe.db.exists("Supplier",{"mobile_no":user.mobile_no}):
			sel_form = frappe.get_doc("Supplier",{"mobile_no":user.mobile_no})
			if sel_form:
				seller = sel_form.name
			if sel_form.farmer_reference_table:
				for i in sel_form.farmer_reference_table:
					aggregator_details.append({
						"aggregator_code":i.supplier_code,
						"aggregator_name":i.supplier_name,
						"aggregator_company":frappe.get_value("Supplier",i.supplier_code,"company") if frappe.db.exists("Supplier",i.supplier_code) else "",
						"aggregator_mobile_no":frappe.get_value("Supplier",i.supplier_code,"mobile_no") if frappe.get_value("Supplier",i.supplier_code,"mobile_no") else get_contact_number(i.supplier_code)
					})
		else:
			con_no = frappe.db.sql(""" select parent from `tabContact Phone` where phone = '{0}' """.format(user.mobile_no),as_dict = True)
			# print(con_no[0].get("parent"))
			if frappe.db.exists("Contact",con_no[0].get("parent")):
				con_doc = frappe.get_doc("Contact",con_no[0].get("parent"))
				for i in con_doc.links:
					if i.link_doctype == "Supplier":
						seller = i.link_name
						sel_form = frappe.get_doc("Supplier",seller)
						if sel_form.farmer_reference_table:
							for i in sel_form.farmer_reference_table:
								aggregator_details.append({
									"aggregator_code":i.supplier_code,
									"aggregator_name":i.supplier_name,
									"aggregator_company":frappe.get_value("Supplier",i.supplier_code,"company") if frappe.db.exists("Supplier",i.supplier_code) else "",
									"aggregator_mobile_no":frappe.get_value("Supplier",i.supplier_code,"mobile_no") if frappe.get_value("Supplier",i.supplier_code,"mobile_no") else get_contact_number(i.supplier_code)
								})	
					else:
						pass           
				
	frappe.response["message"] = {
		"success_key":1,
		"message":"Authentication success",
		"sid":frappe.session.sid,
		"api_key":user.api_key,
		"api_secret":api_generate,
		"username":user.full_name,
		"email":user.email,
		"mobile_no":user.mobile_no,
		"seller":seller,
		"aggregator_details":aggregator_details
	}

def get_contact_number(seller):
	print("running"*100,seller)
	mobile_number=""
	if  frappe.db.exists('Dynamic Link', {'link_doctype': 'Supplier', 'link_name': seller, 'parenttype': 'Contact'}):
		contact_name = frappe.db.get_value('Dynamic Link', {'link_doctype': 'Supplier', 'link_name': seller, 'parenttype': 'Contact'}, 'parent')
		if contact_name:
			mobile_number_doc = frappe.get_doc('Contact', contact_name)
			print(mobile_number_doc.phone_nos[0])
			mobile_number = mobile_number_doc.phone_nos[0].phone if mobile_number_doc.phone_nos else ""
	return mobile_number		


def generate_keys(user):
	user_details = frappe.get_doc('User', user)
	api_secret = frappe.generate_hash(length=15)

	if not user_details.api_key:
		api_key = frappe.generate_hash(length=15)
		user_details.api_key = api_key

	user_details.api_secret = api_secret
	user_details.save()
	# print(api_secret)

	return api_secret



@frappe.whitelist()
def create_so():
	data=frappe.request.data
	data = json.loads(data)
	if(data):
		sync_details = data["sync_details"]
		if sync_details["docname"]:
			misc = data["misc_data"]
			doc = frappe.get_doc("Upload PO Tool",sync_details["docname"])
			doc.response = 1
			# doc.customer_name = "RC-000004"
			# doc.customer_not_found = misc["customer_name"]
			doc.customer_po_no = misc["po_number"]
			doc.po_date = misc["po_date"]
			print(doc.po_date,"*"*40)
			doc.po_delivery_date = misc["po_delivery_date"]
			doc.id = data["id"]
			cust = doc.customer_name

			so = frappe.new_doc("Sales Order")
			so.customer = cust
			so.po_no=misc["po_number"]
			so.delivery_date = misc["po_delivery_date"]
			so.po_date = misc["po_date"]
			so.set_warehouse = "Otur FCC-Finished Goods - FPVCSPL"

			doc.set("found_items", [])
			doc.set("not_found_items", [])

			table = data["table_data"]
			for item in table:
				v = item["data"]    
				# if v["quantity"] !=None and v["quantity"] != 0:
				#     v["quantity"] = v["quantity"]
				# else:
				#     v["quantity"] = 1
				sys_item = frappe.db.sql(""" select parent from `tabItem Customer Detail` where ref_code = '{0}' """.format(v["item_code"]),as_dict = True)
				if sys_item and v["quantity"] !=None and v["quantity"] != 0:
					doc.append("found_items",{
						"item_code" : v["item_code"],
						"item" : sys_item[0].get("parent"),
						"qty" : v["quantity"],
						"rate" : v["basic_cost_price"],
						"description" : v["product_description"],
					})
					so.append("items",{
						"item_code" : sys_item[0].get("parent"),
						"rate" : v["basic_cost_price"],
						"qty" : v["quantity"]
					})
				else:
					doc.append("not_found_items",{
						"item_code" : v["item_code"],
						"qty" : v["quantity"],
						"rate" : v["basic_cost_price"],
						"description" : v["product_description"],
					})
			# frappe.db.commit()
			so.save()
			so.reload()
			doc.so_no = so.name
			doc.save()
			doc.reload()

		

@frappe.whitelist(allow_guest=True)
def create_document(doc):
	try:
		if type(doc) != str:
			doc = json.dumps(doc)
		# else:
		doc = json.loads(doc)		
		if doc["doctype"] == "G4F Farm Book" or doc["doctype"] == "G4F Crop List":
			# if doc["date"] in doc.keys():
			doc["date"] = (datetime.strptime(doc["date"], '%d/%m/%Y')).strftime('%Y-%m-%d')
			# doc["planting_date"] = (datetime.strptime(doc["planting_date"], '%d/%m/%Y')).strftime('%Y-%m-%d')

			
		if doc["doctype"] == "G4F Crop Planner":
			doc["date"] = (datetime.strptime(doc["date"], '%d/%m/%Y')).strftime('%Y-%m-%d')
			if doc["crop_planner_details"]:
				for i in doc["crop_planner_details"]:
					i["planting_date"] = (datetime.strptime(i["planting_date"], '%d/%m/%Y')).strftime('%Y-%m-%d')
			
		if doc["doctype"] == "G4F Sell Your Produce":
			# if doc["posting_date"] in doc.keys():
			doc["posting_date"] = (datetime.strptime(doc["posting_date"], '%d/%m/%Y')).strftime('%Y-%m-%d')
			crop_lst = frappe.get_doc("G4F Crop List",doc["crop"])
			if crop_lst.map_items:
				for i in doc["items"]:
					for j in crop_lst.map_items:
						if i["grade_name"] == j.grade_name:
							j.uom = i["uom"]
							j.qty = i["qty"]
				doc["items"] = []
				for i in crop_lst.map_items:
					doc["items"].append(i)
			else:
				doc["items"] = []
			# doc["items"] = 
			# print(type(item_lst))
		new_doc = frappe.get_doc(doc)
		new_doc.save()
		return new_doc
	
	except HTTPError as http_err:
		print(f'HTTP error occurred: {http_err}')
	except Exception as err:
		print(f'Other error occurred: {err}')

@frappe.whitelist(allow_guest=True)
def get_seller_registered_data(mob_no):
	if frappe.db.exists("Seller Registration Form",mob_no) :
		doc = frappe.db.sql("""
			SELECT 
				sup.farm_linkage_associate as farm_linkage_associate,
				sup.center_incharge as center_incharge,
				sup.status as status,
				sup.supplier_type as supplier_type,
				sup.mobile_no as mobile_no,
				sup.farmer_sub_type as farmer_sub_type,
				sup.company_sub_type as company_sub_type,
				sup.farmer_group_sub_type as farmer_group_sub_type,
				sup.supplier_name as supplier_name,
				sup.pan as pan,
				sup.gst_no as gst_no,
				sup.contact_person_name as contact_person_name,
				sup.alternate_mobile_no as alternate_mobile_no,
				sup.email_id as email_id,
				sup.aadhar_card_no as aadhar_card_no,
				sup.attach_kyc_documents as attach_kyc_documents,
				sup.primary_address as primary_address,
				sup.latitude as latitude,
				sup.postal_code as postal_code,
				sup.taluka as taluka,
				sup.district as district,
				sup.state as state,
				sup.total_farm_area as total_farm_area,
				sup.narest_market as narest_market,
				sup.company_type as company_type,
				sup.trade_experience as trade_experience,
				sup.annual_volume as annual_volume,
				sup.annual_sales_value as annual_sales_value,
				sup.digital_platform as digital_platform,
				sup.no_of_vendors as no_of_vendors,
				sup.no_of_member_farmers as no_of_member_farmers,
				sup.team_size as team_size,
				sup.gender as gender,
				sup.education as education,
				sup.years_in_farming as years_in_farming,
				sup.farm_type as farm_type,
				sup.total_family_members as total_family_members,
				sup.no_of_farm_labour_required as no_of_farm_labour_required,
				sup.owned_vehicle_types as owned_vehicle_types,
				sup.total_owned_vehicles as total_owned_vehicles,
				sup.non_fv_crops_cultivated as non_fv_crops_cultivated,
				sup.source_of_irrigation as source_of_irrigation,
				sup.contract_staff as contract_staff,
				sup.office_type as office_type,
				sup.warehouse as warehouse,
				sup.no_of_warehouses as no_of_warehouses,
				sup.packhouse_area as packhouse_area,
				sup.processing_unit as processing_unit,
				sup.farm_infrastructure as farm_infrastructure,
				sup.rental_equipments as rental_equipments,
				sup.number_of_cattle as number_of_cattle,
				sup.transporter_name as transporter_name,
				sup.transporter_contact_number as transporter_contact_number,
				sup.current_supply_markets as current_supply_markets,
				sup.bank_name as bank_name,
				sup.bank_ac_no as bank_ac_no,
				sup.ifsc_code as ifsc_code,
				sup.type_of_loans as type_of_loans,
				sup.total_loan_amount as total_loan_amount,
				sup.other_income_sources as other_income_sources,
				sup.total_other_income as total_other_income,
				sup.remark_if_any as remark_if_any,
				sup.supplier as supplier,
				sup.user as user,
				sup.route as route,
				sup.company as company,
				sup.abbr as abbr,
				sup.pickup_van_equ as pickup_van_equ,
				sup.tractor_equ as tractor_equ,
				sup.harvestor_equ as harvestor_equ,
				sup.drone_equ as drone_equ,
				sup.rotavator_equ as rotavator_equ,
				sup.cultivator_equ as cultivator_equ,
				sup.mechanical_sprayers_equ as mechanical_sprayers_equ,
				sup.other_equipments as other_equipments,
				sup.own_car as own_car,
				sup.own_truck as own_truck,
				sup.own_pickup as own_pickup,
				sup.own_motorbike as own_motorbike,
				sup.own_tractor as own_tractor,
				sup.own_no_vehicle as own_no_vehicle
			FROM
				`tabSeller Registration Form` sup
			WHERE
				sup.name = '{0}'
		""".format(mob_no),as_dict=True)
		for i in  doc:
			for j in ['pickup_van_equ', 'tractor_equ', 'harvestor_equ', 'drone_equ', 'rotavator_equ', 'cultivator_equ', 'mechanical_sprayers_equ', 'other_equipments', 'own_car', 'own_truck', 'own_pickup', 'own_motorbike', 'own_tractor', 'own_no_vehicle']:
				if i[j]==1 or i[j]=="1":
					i[j]=True
				if i[j]==0 or i[j]=="0":
					i[j]=False
		return doc

@frappe.whitelist(allow_guest=True)
def update_seller_registered_data(mob_no,doc):
	if frappe.db.exists("Seller Registration Form",mob_no) :
		if type(doc) != str:
			doc = json.dumps(doc)
		# else:
		doc = json.loads(doc)
		# for i in  doc:
		for j in ['pickup_van_equ', 'tractor_equ', 'harvestor_equ', 'drone_equ', 'rotavator_equ', 'cultivator_equ', 'mechanical_sprayers_equ', 'other_equipments', 'own_car', 'own_truck', 'own_pickup', 'own_motorbike', 'own_tractor', 'own_no_vehicle']:
			if j in doc:
				if doc[j]==True or doc[j]=="True" or  doc[j]=="true":
					doc[j]=1
				if doc[j]==False or doc[j]=="False" or doc[j]=="false":
					doc[j]=0
		s_doc = frappe.get_doc("Seller Registration Form",mob_no)
		s_doc.update(doc)
		s_doc.save()
		return s_doc
	
@frappe.whitelist(allow_guest=True)
def get_crop_list():
	frappe.response["data"] = frappe.get_all("G4F Crop List")

@frappe.whitelist(allow_guest=True)
def get_company_list():
	frappe.response["data"] = frappe.get_all("Company")