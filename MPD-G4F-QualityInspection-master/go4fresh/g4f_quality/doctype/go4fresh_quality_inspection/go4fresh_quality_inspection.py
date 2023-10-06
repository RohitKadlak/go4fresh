# Copyright (c) 2022, Mannlowe Information Services Pvt. Ltd. and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class Go4FreshQualityInspection(Document):
	def before_save(self):
		if(self.product_name=="Onion"):
			if len(self.qi_sample)!=0:
				gross_weight = 0.00
				total_defect = 0.00
				for i in self.qi_sample:
					gross_weight = gross_weight + i.gross_weight
					total_defect = total_defect + i.total_defects

				self.total_samples = len(self.qi_sample)
				self.total_gross_weight = gross_weight
				self.total_defect = total_defect
				self.average_defect = (total_defect/gross_weight)*100

