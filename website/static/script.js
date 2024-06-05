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

