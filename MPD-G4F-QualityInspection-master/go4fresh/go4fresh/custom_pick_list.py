import json
from collections import OrderedDict, defaultdict
from itertools import groupby
from typing import Dict, List, Set

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.model.mapper import map_child_doc
from frappe.utils import cint, floor, flt, today
from frappe.utils.nestedset import get_descendants_of

from erpnext.selling.doctype.sales_order.sales_order import (
	make_delivery_note as create_delivery_note_from_sales_order,
)
from erpnext.stock.get_item_details import get_conversion_factor

from erpnext.stock.doctype.pick_list.pick_list import get_available_item_locations,get_items_with_location_and_quantity
from erpnext.stock.doctype.pick_list.pick_list import PickList

class MPickList(PickList):    
    @frappe.whitelist()
    def set_item_locations(self, save=False):
        self.validate_for_qty()
        items = self.aggregate_item_qty()
        self.item_location_map = frappe._dict()

        from_warehouses = None    
        if self.parent_warehouse:
            if frappe.db.get_value("Warehouse",self.parent_warehouse,'is_group') == 1:
                from_warehouses = get_descendants_of("Warehouse", self.parent_warehouse)
            else :
                from_warehouses = []
                from_warehouses.append(self.parent_warehouse)
                
        # Create replica before resetting, to handle empty table on update after submit.
        locations_replica = self.get("locations")

        # reset
        self.delete_key("locations")
        for item_doc in items:
            item_code = item_doc.item_code

            self.item_location_map.setdefault(
                item_code,
                get_available_item_locations(
                    item_code, from_warehouses, self.item_count_map.get(item_code), self.company
                ),
            )

            locations = get_items_with_location_and_quantity(
                item_doc, self.item_location_map, self.docstatus
            )

            item_doc.idx = None
            item_doc.name = None

            for row in locations:
                location = item_doc.as_dict()
                location.update(row)
                self.append("locations", location)

        # If table is empty on update after submit, set stock_qty, picked_qty to 0 so that indicator is red
        # and give feedback to the user. This is to avoid empty Pick Lists.
        if not self.get("locations") and self.docstatus == 1:
            for location in locations_replica:
                location.stock_qty = 0
                location.picked_qty = 0
                self.append("locations", location)
            frappe.msgprint(
                _(
                    "Please Restock Items and Update the Pick List to continue. To discontinue, cancel the Pick List."
                ),
                title=_("Out of Stock"),
                indicator="red",
            )

        if save:
            self.save()