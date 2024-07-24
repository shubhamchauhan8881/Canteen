var cart =  JSON.parse(localStorage.getItem("cart")) || {};
const AddToCartButtons = document.querySelectorAll("#AddToCartButton");
const cart_plus_btn = document.querySelectorAll("#cart-plus-btn");
const cart_minus_btn = document.querySelectorAll("#cart-minus-btn");
const OrderDetails = document.querySelectorAll("#OrderDetails");

var sum_amount = 0;

const swiper = new Swiper('.swiper', {
	autoplay: {
		delay: 2000,
		disableOnInteraction: false,
	},
	loop: true,

	pagination: {
		el: '.swiper-pagination',
		clickable: true
	},

});


$("#cart-btn-form").on("submit", e=>{
  e.preventDefault();
  $("#cartInput").val(localStorage.getItem("cart"));
  e.target.submit();
});



function AddItemToCart(pid, action='add', e=null){
  let para = $(`#qtty${pid}`);
  let cartCounter = $("#cartCounter");
  // 
  let amc = $("#cartAmountCounter");
  let prev_qtty=0;
  switch(action){
    case "add":
      cart[pid] = 1;
      para.text(1)
      break;
    case "inc":
      cart[pid] += 1;
      para.text(cart[pid]);
      break;
    case "dec":
      prev_qtty = cart[pid];
      prev_qtty -= 1;
      if(prev_qtty <= 0){
        delete cart[pid];
        para.text(0)
        $(e.target).parent().parent().hide();
        $(e.target).parent().parent().siblings().fadeIn();
      }else{
        cart[pid]= prev_qtty;
        para.text(prev_qtty)
      }
      break;
  }
  localStorage.setItem("cart", JSON.stringify(cart));
  cartCounter.text(Object.keys(cart).length);
  // cartInput.val(JSON.stringify(cart));
}


$(document).ready(function(){
  let cartCounter = $("#cartCounter");
  cartCounter.text(Object.keys(cart).length);
  
  AddToCartButtons.forEach((value, index)=>{  
    let button = $(value);
    let pid = button.attr("value")
    if(cart[pid]){
      button.hide();
      button.siblings().fadeIn();
      $(`#qtty${pid}`).text(cart[pid])
    }
  
    $(value).on("click", (e)=>{
      AddItemToCart(button.attr("value"));
      button.hide();
      button.siblings().fadeIn();
    });
  });



  cart_plus_btn.forEach((input, index)=>{
    $(input).on("click", (e)=>{
      AddItemToCart( e.target.value, "inc", e);
    });
  });

  
  cart_minus_btn.forEach((input, index)=>{
    $(input).on("click", (e)=>{
      AddItemToCart( e.target.value, "dec", e);
    });
  });


  

  OrderDetails.forEach((div, index)=>{
    let d = $(div);
    d.on("click", (e)=>{
      childs =d.children().siblings()[3];
      $(childs).toggleClass("h-0");
    });
  });


});



var menu_toggle = 1;
$(".menu-btn").on("click", function(e) {
    menu_toggle += 1;
    if(menu_toggle%2==0)$('.menu-items').animate({height:'136px'},);
    else $('.menu-items').animate({height:'0px'},);
});





const debounce = (callback, wait) => {
  let timeoutId = null;
  return (...args) => {
    window.clearTimeout(timeoutId);
    timeoutId = window.setTimeout(() => {
      callback(...args);
    }, wait);
  };
}


function GetSearchResults(e){
	let inp =  e.target.value;
	const search_no_results = $("#search-no-results");
	const search_results_container = $("#search-results-container");
  const search_results_wrapper = $(".search-results-wrapper")
	if(inp !== "" && inp.length > 3)
		{			
			$.ajax({
				url:"/search/",
				data:{ input: inp},
				method:"post",
				success: (data, textStatus,jqXHR)=>{
					search_no_results.hide();
					search_results_container.empty();
          search_results_wrapper.show();
					data.data.forEach((p, i)=>{	
						let s = `<a href="/refreshment/${p.id}/" class="p-1 px-2 block w-full rounded-md hover:bg-Yellow">${p.name}</a>`
						search_results_container.append(s);
					})
				},  
				error: (jqXHR, textStatus, errorThrown)=>{
					search_no_results.show();
          search_results_wrapper.show();
					search_no_results.text("No results found")
				}
			});
			
		}
	else{
		search_results_container.empty();
		search_no_results.text("Search Results...");
		search_no_results.show();
    search_results_wrapper.hide();
	}
}

document.querySelector("#search-input").addEventListener("input", debounce((e)=>GetSearchResults(e), 300));

document.querySelector("#search-input").addEventListener("focus", (e)=>{
	window.scrollTo({top:e.target.offsetHeight+120})
})