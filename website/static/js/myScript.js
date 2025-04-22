$('.plus-cart').click(function(){
    console.log('Button clicked')

    var id = $(this).attr('pid').toString()
    var cantidad = this.parentNode.children[2]
    $.ajax({
        type: 'GET',
        url: '/pluscart',
        data: {
            carrito_id: id
        },
        
        success: function(data){
            console.log(data)
            cantidad.innerText = data.cantidad
            document.getElementById(`cantidad${id}`).innerText = data.cantidad
            document.getElementById('amount_tt').innerText = data.amount
            document.getElementById('totalamount').innerText = data.total
        }
    })
})

$('.minus-cart').click(function(){
    console.log('Button clicked')

    var id = $(this).attr('pid').toString()
    var cantidad = this.parentNode.children[2]
    $.ajax({
        type: 'GET',
        url: '/minuscart',
        data: {
            carrito_id: id
        },
        
        success: function(data){
            console.log(data)
            cantidad.innerText = data.cantidad
            document.getElementById(`cantidad${id}`).innerText = data.cantidad
            document.getElementById('amount_tt').innerText = data.amount
            document.getElementById('totalamount').innerText = data.total
        }
    })
})


$('.remove-cart').click(function(){
   var id = $(this).attr('pid').toString()

   var to_remove = this.parentNode.parentNode.parentNode.parentNode

   $.ajax({
    type: 'GET',
    url: 'removecart',
    data: {
        carrito_id: id
    },

    success: function(data){
        document.getElementById('amount_tt').innerText = data.amount
        document.getElementById('totalamount').innerText = data.total
        to_remove.remove()

    }
   })
})


