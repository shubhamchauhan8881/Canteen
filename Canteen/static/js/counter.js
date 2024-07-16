
function CopyToClipBoard(id){
    let a = `
Name: ${$(`#order-details-name_${id}`).text()}
Phone: ${ $(`#order-details-phone_${id}`).text() }
Address:  ${ $(`#order-details-address_${id}`).text() }

Order id: ${ $(`#order-details-orderid_${id}`).text() }
Payment method: ${ $(`#order-details-payment-method_${id}`).text() }

Amount : ${ $(`#order-details-amount_${id}`).text() }
Items : ${ $(`#order-details-items_${id}`).text() }

`;
    navigator.clipboard.writeText(a);
}


document.querySelectorAll("#copy_address_details").forEach((btn, index)=>{
    $(btn).on("click",(e)=>{
        CopyToClipBoard(e.target.value);
        e.target.innerHTML = 'Copied'
    });
});




$(document).ready(function() {

const interval = setInterval(function() {
    $.ajax({
        url: `/counter/notification/${shop_id}/`,
        method:"GET",
        success: function(data) {
            
            if(data.status == "ok") {
                
                try{
                    noti_audio.play();
                } catch (e) {
                    console.log("failed to play audio");
                }
                try {
                    $("#home-no-orders").hide();
                } catch (error) {
                    console.log()
                }
                    data.data.forEach((value, i) => {

                        const s = `

                        <div id="row${value.id}" class="flex p-5 bg-base-100 hover:bg-base-200 rounded shadow-md relative">
                            <span class="absolute top-0 left-0 text-white text-[10px] p-0.5 px-1 rounded-ss-md rounded-ee-md bg-cyan-500">active</span>
                            <div class="grow">
                                <div>
                                    <p class="text-xs opacity-90">Order id: <span id="order-details-orderid_${value.id}">${value.order_id}</span> </p>
                                    
                                    <p class="font-bold text-lg" id="order-details-items_${value.id}">${value.itemxqtty}</p>
                                </div>
                        
                                <div class="leading-4 my-2 text-sm">
                                    <p class="text-xs opacity-90">Customer Details: </p>
                                    <h4 id="order-details-name_${value.id}">${value.name}</h4>
                                    <p id="order-details-phone_${value.id}">${value.number}</p>
                                    <p id="order-details-address_${value.id}">${value.address}</p>
                                    <div class="">
                                        <button class="btn btn-xs" id="copy_address_details" value="${value.id}">
                                            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="size-5 inline-block">
                                                <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 17.25v3.375c0 .621-.504 1.125-1.125 1.125h-9.75a1.125 1.125 0 0 1-1.125-1.125V7.875c0-.621.504-1.125 1.125-1.125H6.75a9.06 9.06 0 0 1 1.5.124m7.5 10.376h3.375c.621 0 1.125-.504 1.125-1.125V11.25c0-4.46-3.243-8.161-7.5-8.876a9.06 9.06 0 0 0-1.5-.124H9.375c-.621 0-1.125.504-1.125 1.125v3.5m7.5 10.375H9.375a1.125 1.125 0 0 1-1.125-1.125v-9.25m12 6.625v-1.875a3.375 3.375 0 0 0-3.375-3.375h-1.5a1.125 1.125 0 0 1-1.125-1.125v-1.5a3.375 3.375 0 0 0-3.375-3.375H9.75" />
                                            </svg>   
                                            Copy                       
                                        </button>
                                    </div>
                                </div>
                                <div class="">
                                    <p class="text-xs opacity-90">Payment Details: </p>
                                    <p id="order-details-payment-method_${value.id}">${value.payment_method}</p>
                                    <p class="text-xs">${value.time} | ${value.date}</p>
                                </div>
                            </div>
                            
                            <div class=" flex flex-col justify-stretch gap-4">
                                <p class="font-semibold">Rs. <span id="order-details-amount_${value.id}">${value.amount}</span></p>
                                <a href="/counter/order/setstatus/accepted/${value.id}/">
                                    <button class="grow btn btn-md btn-success">Accept</button>  
                                </a>
                                <a href="/counter/order/setstatus/rejected/${value.id}/">
                                    <button class="grow btn btn-md btn-error">Reject</button>  
                                </a>
                            </div>
                        </div>
                        `

                        $("#p-container").append(s);
                    });
                }
            }
        });
    

},20000);



});
