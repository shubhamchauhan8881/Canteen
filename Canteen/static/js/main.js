var cart = {};
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



function AddItemToCart(pid, action='add', e=null){
  let para = $(`#qtty${pid}`);
  let cartCounter = $("#cartCounter");
  let cartInput = $("#cartInput");
  let amc = $("#cartAmountCounter");
  let prev_qtty=0;
  switch(action){
    case "add":
      cart[pid] = 1;
      para.text(1)
      break;
    case "inc":
      prev_qtty= cart[pid];
      cart[pid]= prev_qtty+1;
      para.text(prev_qtty+1)
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
  cartCounter.text(Object.keys(cart).length);
  cartInput.val(JSON.stringify(cart));
}

const AddToCartButtons = document.querySelectorAll("#AddToCartButton");
AddToCartButtons.forEach((value, index)=>{  
  $(value).click((e)=>{
    let button = $(value);
    let pid = button.attr("value");
    AddItemToCart(pid)
    button.hide();
    button.siblings().fadeIn();
  });
});

const cart_plus_btn = document.querySelectorAll("#cart-plus-btn");
cart_plus_btn.forEach((input, index)=>{
  $(input).on("click", (e)=>{
    let pid =  e.target.value;
    AddItemToCart(pid, "inc", e);
  });
});

const cart_minus_btn = document.querySelectorAll("#cart-minus-btn");
cart_minus_btn.forEach((input, index)=>{
  $(input).on("click", (e)=>{
    let pid =  e.target.value;
    AddItemToCart(pid, "dec", e);
  });
});



var menu_toggle = 1;
$(".menu-btn").click(function(e) {
    menu_toggle += 1;
    if(menu_toggle%2==0)$('.menu-items').animate({height:'136px'},);
    else $('.menu-items').animate({height:'0px'},);
});



const OrderDetails = document.querySelectorAll("#OrderDetails");
OrderDetails.forEach((div, index)=>{
    let d = $(div);
    d.on("click", (e)=>{
      childs =d.children().siblings()[3];
      $(childs).toggleClass("h-0");
    });
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
	if(inp !== "")
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