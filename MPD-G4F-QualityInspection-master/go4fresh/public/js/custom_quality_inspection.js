frappe.ui.form.on("Quality Inspection",{
    before_save:function(frm){
        if(frm.doc.reference_name){
            frappe.call({
                method: "frappe.client.get",
                args: {
                    doctype: "Purchase Receipt",
                    name: frm.doc.reference_name,
                },
                callback(r) {
                    if(r.message) {
                        var pr = r.message;
                        pr.items.forEach(function(item,index){
                            if(item.item_code === frm.doc.item_code){
                                frm.set_value("received_qty",item.qty)
                                frm.refresh_field("received_qty")
                                if(item.batch_no){
                                    frm.set_value("batch_no",item.batch_no)
                                    frm.refresh_field("batch_no")
                                }
                                if(item.purchase_order){
                                    frappe.call({
                                        method:"frappe.client.get",
                                        args:{
                                            doctype:"Purchase Order",
                                            name:item.purchase_order
                                        },
                                        callback:function(r){
                                            if(r.message){
                                                var po = r.message
                                                po.items.forEach(function(i,index){
                                                    if(i.item_code === frm.doc.item_code){
                                                        frm.set_value("po_qty",i.qty)
                                                        frm.refresh_field("po_qty")
                                                    }
                                                })
                                            }
                                        }
                                    })
                                }
                            }
                        })
                    }
                }
            });
        }
    }
})