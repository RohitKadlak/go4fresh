// Copyright (c) 2022, Mannlowe Information Services Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Planner', {
	// refresh: function(frm) {
	// 	var arr=[
	// 		{
	// 		  "crop_name":"Potato",
	// 		  "harvest_tracker_crop_yield_in_kg": 2000,
	// 		  "harvest_uom":"KG",
	// 		  "for_sale_yield_in_kg":1500,
	// 		  "for_sale_uom":"KG",
	// 		  "sku_item":[
	// 				{
	// 				  "item_code":"VEG-00176",
	// 				  "sku_item_name":"Organic Potato-1KG",
	// 				  "po_orders":100,
	// 				  "e_orders":200
	// 				},
	// 				{
	// 				  "item_code":"VEG-00036",
	// 				  "sku_item_name":"BH-Potato Organic, 1 kg",
	// 				  "po_orders":150,
	// 				  "e_orders":100
	// 				},
					
	// 				{
	// 				  "item_code":"VEG-00154",
	// 				  "sku_item_name":"BH-Fresh Potato, 1 Kg",
	// 				  "po_orders":300,
	// 				  "e_orders":50
	// 				}
	// 		    ],
	// 			"yield_avg":600,
	// 			"yield_avg_uom":"KG"
	// 		},
	// 		{
	// 		  "crop_name":"Papaya",
	// 		  "harvest_tracker_crop_yield_in_kg":10000,
	// 		  "harvest_uom":"KG",
	// 		  "for_sale_yield_in_kg":8000,
	// 		  "for_sale_uom":"KG",
	// 		  "sku_item":[
	// 				{
	// 				  "item_code":"FRT-00061",
	// 				  "sku_item_name":"Organic Raw Papaya-600-800g",
	// 				  "po_orders":500,
	// 				  "e_orders":1500
	// 				},
	// 				{
	// 				  "item_code":"VEG-00036",
	// 				  "sku_item_name":"BH-Raw Papaya, (400 gm - 600 gm)",
	// 				  "po_orders":1000,
	// 				  "e_orders":400
	// 				},
					
	// 				{
	// 				  "item_code":"VEG-00154",
	// 				  "sku_item_name":"BH-Papaya Organically Grown, 1 unit (1.2-1.5 kg)",
	// 				  "po_orders":200,
	// 				  "e_orders":900
	// 				}
	// 		    ],
	// 		    "yield_avg":3500,
	// 			"yield_avg_uom":"KG"
	// 		},
	// 		{
	// 			"crop_name":"Potato",
	// 			"harvest_tracker_crop_yield_in_kg": 2000,
	// 			"harvest_uom":"KG",
	// 			"for_sale_yield_in_kg":1500,
	// 			"for_sale_uom":"KG",
	// 			"sku_item":[
	// 				  {
	// 					"item_code":"VEG-00176",
	// 					"sku_item_name":"Organic Potato-1KG",
	// 					"po_orders":100,
	// 					"e_orders":200
	// 				  },
	// 				  {
	// 					"item_code":"VEG-00036",
	// 					"sku_item_name":"BH-Potato Organic, 1 kg",
	// 					"po_orders":150,
	// 					"e_orders":100
	// 				  },
					  
	// 				  {
	// 					"item_code":"VEG-00154",
	// 					"sku_item_name":"BH-Fresh Potato, 1 Kg",
	// 					"po_orders":300,
	// 					"e_orders":50
	// 				  }
	// 			  ],
	// 			  "yield_avg":600,
	// 			  "yield_avg_uom":"KG"
	// 		  },
	// 		  {
	// 			"crop_name":"Papaya",
	// 			"harvest_tracker_crop_yield_in_kg":10000,
	// 			"harvest_uom":"KG",
	// 			"for_sale_yield_in_kg":8000,
	// 			"for_sale_uom":"KG",
	// 			"sku_item":[
	// 				  {
	// 					"item_code":"FRT-00061",
	// 					"sku_item_name":"Organic Raw Papaya-600-800g",
	// 					"po_orders":500,
	// 					"e_orders":1500
	// 				  },
	// 				  {
	// 					"item_code":"VEG-00036",
	// 					"sku_item_name":"BH-Raw Papaya, (400 gm - 600 gm)",
	// 					"po_orders":1000,
	// 					"e_orders":400
	// 				  },
					  
	// 				  {
	// 					"item_code":"VEG-00154",
	// 					"sku_item_name":"BH-Papaya Organically Grown, 1 unit (1.2-1.5 kg)",
	// 					"po_orders":200,
	// 					"e_orders":900
	// 				  }
	// 			  ],
	// 			  "yield_avg":3500,
	// 			  "yield_avg_uom":"KG"
	// 		  }
	//     ]
	// 	// var final = '<div id="accordion">'+table+'</div>';
	// 	// $(".planner").append(final)
		
	// 	var code = ``
	// 	arr.forEach(function(item,index){
	// 		var table_row = ``;
	// 		item.sku_item.forEach(function(it,idx){
	// 			table_row = table_row + `
	// 				<tr>
	// 			        <th scope="row">${idx+1}</th>
	// 			        <td>${it.item_code}</td>
	// 			        <td contenteditable='true' style="text-align:right;"> 
	// 						<input id="td${index+1}" type="number" class="form-control" placeholder="Example input" value="${it.po_orders}">
	// 			        </td>
	// 			        <td id="td${index+1}" contenteditable='true' style="text-align:right;">
	// 						<input id="td${index+1}" type="number" class="form-control" placeholder="Example input" value="${it.e_orders}">
	// 					</td>
	// 			    </tr>
	// 			`;
	// 		})
	// 		var row = `
	// 				<div class="card">
	// 					<div class="p-3 mb-2 bg-success card-header" id="heading${index+1}">
	// 					  <h5 class="mb-0">
	// 					    <div class="row collapsed" data-toggle="collapse" data-target="#collapse${index+1}" aria-expanded="false" aria-controls="collapse${index+1}">
	// 					        <div class="col-xs-10">
	// 								<button class="btn btn-link p-3 mb-2 bg-success text-white collapsed" data-toggle="collapse" data-target="#collapse${index+1}" aria-expanded="false" aria-controls="collapse${index+1}" style="width:100%">
	// 									<b>${item.crop_name}</b>
	// 							    </button>    
	// 					        </div>
	// 					        <div class="col-xs-2"><br>
	// 								<i class="fa fa-plus text-white text-center"></i></div>
	// 						    </div>
	// 					  </h5>
	// 					</div>
	// 					<div id="collapse${index+1}" class="collapse" aria-labelledby="heading${index+1} bg-light" data-parent="#accordion">
	// 					    <div class="card-body">
	// 							<form>
	// 								<div class="form-group">
	// 								    <label for="formGroupExampleInput">Harvest Tracker Crop yield</label>
	// 								    <div class="input-group mb-3">
	// 									    <input type="text" class="form-control" id="harvestTracker${index+1}" placeholder="Example input" value="${item.harvest_tracker_crop_yield_in_kg}">
	// 									    <div class="input-group-append">
	// 									        <span class="input-group-text"><b>${item.harvest_uom}</b></span>
	// 									    </div>
	// 								    </div>
	// 								</div>
	// 								<div class="form-group">
	// 								    <label for="formGroupExampleInput">For Sale Yield</label>
	// 								    <div class="input-group mb-3">
	// 									    <input type="text" class="form-control" id="saleYield${index+1}" placeholder="Example input" value="${item.for_sale_yield_in_kg}">
	// 									    <div class="input-group-append">
	// 									        <span class="input-group-text"><b>${item.for_sale_uom}</b></span>
	// 									    </div>
	// 								    </div>
	// 								</div>
	// 								<table id="table${index+1}" class="table table-bordered table-hover">
	// 								    <thead class="thead-light">
	// 									    <tr>
	// 									      <th scope="col">#</th>
	// 									      <th scope="col" style="text-align:center;">Item</th>
	// 									      <th scope="col" style="text-align:center;">PO</th>
	// 									      <th scope="col" style="text-align:center;">E-Comm</th>
	// 									    </tr>
	// 								    </thead>
	// 								    <tbody>
	// 										${table_row}    
	// 								    </tbody>
	// 								</table>
	// 								<div class="form-group">
	// 								    <label for="formGroupExampleInput">Yield Average</label>
	// 								    <div class="input-group mb-3">
	// 									    <input type="text" class="form-control" id="yieldAvg${index+1}" placeholder="Example input" value="${item.yield_avg}">
	// 									    <div class="input-group-append">
	// 									        <span class="input-group-text"><b>${item.yield_avg_uom}</b></span>
	// 									    </div>
	// 								    </div>
	// 								</div>
	// 								<button id="${index+1}" type="button" class="btn btn-primary btn-lg btn-block">RFQ</button>
	// 							</form>
	// 					    </div>
	// 					</div>
	// 				</div>
	// 			`;	
	// 			code = code + row;
	// 	})
	// 	var final = '<div id="accordion">'+code+'</div>';
	// 	$(".planner").append(final)
		
	// 	$(".collapse.show").each(function () {
	// 		$(this)
	// 		  .prev(".card-header")
	// 		  .find(".fa")
	// 		  .addClass("fa-minus")
	// 		  .removeClass("fa-plus");
	// 	  });
	// 	  $(".collapse")
	// 	  .on("show.bs.collapse", function () {
	// 		$(this)
	// 		  .prev(".card-header")
	// 		  .find(".fa")
	// 		  .removeClass("fa-plus")
	// 		  .addClass("fa-minus");
	// 	  })
	// 	  .on("hide.bs.collapse", function () {
	// 		$(this)
	// 		  .prev(".card-header")
	// 		  .find(".fa")
	// 		  .removeClass("fa-minus")
	// 		  .addClass("fa-plus");
	// 	  });
	// }
});