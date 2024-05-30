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

    $('#search-input').autocomplete({
        source: function(request, response) {
            $.ajax({
                url: '/autocomplete',
                method: 'POST',
                data: { query: request.term },
                success: function(data) {
                    response(data.map(item => item.name));
                },
                error: function() {
                    response([]);
                }
            });
        }
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
                        var imageUrl = '/static/uploads/' + result.image;
                        var resultHTML = '<div class="search-results">';
                        resultHTML += '<img src="' + imageUrl + '">';
                        resultHTML += '<div class="product-details">';
                        resultHTML += '<p><strong>Product Brand:</strong> ' + result.product_brand + '</p>';
                        resultHTML += '<p><strong>Product Name:</strong> ' + result.product_name + '</p>';
                        resultHTML += '<p><strong>Product Category:</strong> ' + result.product_category + '</p>';
                        resultHTML += '<p><strong>Product Ingredients:</strong> ' + result.ingredients +'</p>';
                        resultHTML += '</div>';
                        resultHTML += '</div>';
                        resultsDiv.append(resultHTML);
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
        // Prefill product name
        $('#product_name').val(productname);
    }

    $('#ingredients-clear-btn').click(function(){
        $('#ingredients').val('');
        $('#analyzer-result').empty();
    });
});
