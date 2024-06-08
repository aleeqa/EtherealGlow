$(document).ready(function(){
    //search functionality
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
                        resultHTML += '<p><strong>Product Ingredients:</strong> ' + result.product_ingredients +'</p>';
                        resultHTML += '<p><strong>Comedogenic Status:</strong> ' + result.comedogenic + '</p>'; 
                        resultHTML += '</div>';
                        resultHTML += '</div>';
                        resultsDiv.append(resultHTML);
                    });
                } else {
                    resultsDiv.append('<br><p class="not-exist-result">The product does not exist. Please add product to obtain the result.</p>');
                    resultsDiv.append('<p class="not-exist-result"><input type="submit" id="add-product-btn" value="Add Product"></p>');
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

    //analyzer tool 
    $('#analyze-form').submit(function(event){
        event.preventDefault();
        
        var ingredients = $('#ingredients').val().trim();
        
        if (ingredients === '') {
            $('#analyzer-result').html('Please enter a list of skincare ingredients.');
            return;
        }
        
        $.ajax({
            type: 'POST',
            url: '/analyze',
            data: { ingredients: ingredients },
            success: function(response){
                $('#analyzer-result').html(response.result);
            },
            error: function(){
                console.error('Error analyzing ingredients.');
            }
        });
    });

    $('#ingredients-clear-btn').click(function(){
        $('#ingredients').val('');
        $('#analyzer-result').empty();
    });

     //feedback functionality
     $('#search-feedback-btn').click(function(){
        var query = $('#product_input').val();
        if (query.trim() !== '') {
            searchProductFeedbacks(query);
        } else {
            $('#feedback-results').empty().append('<p>Please enter the name of a product.</p>');
        }
    });

    $('#search-feedback-btn').click(function(){
        var query = $('#product_input').val();
        searchProductFeedbacks(query);
    });

    $('#clear-feedback-btn').click(function(){
        $('#product_input').val('');
        $('#feedback-results').empty();
    });

    $('#product_input').autocomplete({
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

    function searchProductFeedbacks(query) {
        $.ajax({
            type: 'POST',
            url: '/searchfeedback',
            data: { query: query },
            success: function(response){
                var resultsDiv = $('#feedback-results');
                resultsDiv.empty();
                if (response.length > 0) {
                    $.each(response, function(index, result){
                        var resultHTML = '<div class="product-feedback">';
                        resultHTML += '<p>This product is already exist in the database and feel free to share your journey and feedbacks about ' + result.product_name + '.</p>';
                        resultHTML += '</div>';
                        resultHTML += '</div>';
                        resultsDiv.append(resultHTML);
                    });
                } else {
                    resultsDiv.append('<br><p>This product does not exist our database. You can still proceed to leave a feedback and share your journey about this product.</p>');
                }
            },
            error: function(){
                alert('Error searching for products.');
            }
        });
    }
    

});
