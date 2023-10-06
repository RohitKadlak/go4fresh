import frappe
import ast

@frappe.whitelist()
def hide_fields(s_user):
    user_doc = frappe.get_doc("User",{"name":s_user})
    b = 0
    for i in user_doc.roles:
        if i.role == "Warehouse User":
            b=1
    return b

@frappe.whitelist()
def select_items(sel,doc):
    sel_list = [n.strip() for n in ast.literal_eval(sel)]
    doc = frappe.get_doc("Purchase Receipt",doc)
    sel = doc.items
    doc.items = []
    doc.items = [element for element in sel if element.get("name") in sel_list]
    for index, row in enumerate(doc.items):
        row.idx = index+1
    doc.save()