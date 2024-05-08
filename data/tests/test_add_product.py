import data.add_product as prods

def test_add_product():

	user_id = "user_0001"
	product_name = "Test Product"
	product_price = 10.0
	product_condition = "New"
	product_brand = "TestBrand"
	product_categories = "Electronics" 
	product_date_posted = "2023-11-30"
	product_comments = "A great product!"

	# check that product is not already in the database
	find_product = prods.dbc.fetch_one({prods.USER_ID: user_id,prods.PRODUCT_NAME: product_name, 
									 prods.PRODUCT_PRICE: product_price})
	assert find_product is None

	# add the product
	new_product = prods.add_product(
		user_id, product_name, product_price, 
		product_condition, product_brand, product_categories,
		product_date_posted, product_comments
		)

	# check if product was added successfully
	assert new_product is True

	# retrieve the product from the database
	added_product = prods.dbc.fetch_one({prods.USER_ID: user_id, prods.PRODUCT_NAME: product_name, 
									 prods.PRODUCT_PRICE: product_price})
	
	# check if product retrieved from database matches product added
	assert added_product is not None
	assert added_product[prods.USER_ID] == user_id
	assert added_product[prods.PRODUCT_NAME] == product_name
	assert added_product[prods.PRODUCT_PRICE] == product_price
	assert added_product[prods.PRODUCT_CONDITION] == product_condition
	assert added_product[prods.PRODUCT_BRAND] == product_brand
	assert added_product[prods.PRODUCT_CATEGORIES] == product_categories
	assert added_product[prods.PRODUCT_DATE_POSTED] == product_date_posted
	assert added_product[prods.PRODUCT_COMMENTS] == product_comments


