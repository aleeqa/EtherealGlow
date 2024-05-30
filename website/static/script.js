$(document).ready(function(){
    $('#search-btn').click(function(){
        var query = $('#search-input').val();
        if (query.trim() !== '') {
            searchProducts(query);
        } else {
            $('#search-results').empty().append('<p>Please enter the name of a product.</p>');
        }
    });

    $('#clear-btn').click(function(){
        $('#search-input').val('');
        $('#search-results').empty();
    });

    $(document).on('click', '#add-product-btn', function() {
        var productName = $('#search-input').val();
        showAddProductForm(productName);
        $(this).hide();
    });

    function searchProducts(query) {
        $.ajax({
            type: 'POST',
            url: '/search',
            data: { query: query },
            success: function(response){
                var resultsDiv = $('#search-results');
                resultsDiv.empty();
                if (response.length > 0) {
                    $.each(response, function(index, result){
                        resultsDiv.append('<p><strong>Product brand:</strong> ' + result.product_brand + '<br><strong>Product Name:</strong> ' + result.product_name + '<br><strong>Product Category:</strong> ' + result.product_category + '<br><strong>Product Ingredients:</strong> ' + result.ingredients +'</p>');
                    });
                } else {
                    resultsDiv.append('<br><p>The product does not exist. Please add product to obtain the result.</p>');
                    resultsDiv.append('<input type="submit" id="add-product-btn" value="Add Product">');
                }
            },
            error: function(){
                alert('Error searching for products.');
            }
        });
    }

    function showAddProductForm(productname) {
        $('#add-product-form').show();
        // Prefill product name if available
        $('#product_name').val(productname);
    }

    $('#ingredients-clear-btn').click(function(){
        $('#ingredients').val('');
        $('#analyzer-result').empty();
    });
});


//button click, retrieve values from dropdown menu, send AJAX  request to the server, display recommendation(success)
document.getElementById('get-recommendations').addEventListener('click', function() {
    //retrieve value of skintype and product_category
    var skintype = document.getElementById('skintype').value;
    var product_category = document.getElementById('product_category').value;
    
$.ajax({
        type: 'POST',
        url: '/recommendations', //where request will be sent
        //data will be sent along wirth the request
        data: {
            skintype: skintype,
            product_category: product_category
        },
        //function will execute if request is success
        success: function(response) {
            displayRecommendations(response.suggestion);
        },
        //execute if there is error during request
        error: function(error) {
            console.log(error);
        }
    });
});

function displayRecommendations(recommendations) {
    var recommendationsDiv = document.getElementById('suggestion');
    recommendationsDiv.innerHTML = '';
    

    //create unordered list elements
    var list = document.createElement('ul');
    recommendations.forEach(function(product) {
        //creates list item for each product recommendation (bullet point)
        var listItem = document.createElement('li');
        //display name of product
        listItem.textContent = product;
        //appends each list item containing a product recommendation to <ul>
        list.appendChild(listItem);
    });
    
    //display the outcome
    recommendationsDiv.appendChild(list);
}