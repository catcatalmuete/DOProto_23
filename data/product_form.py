import data.form_filler as ff
from data.form_filler import FLD_NM  # for tests

# Define field constants
USER_ID = 'user_id'
PRODUCT_NAME = 'product_name'
QUANTITY = 'quantity'
PRICE = 'price'
CONDITION = 'condition'
CATEGORIES = 'categories'
DESCRIPTION = 'description'
BRAND = 'brand'
DATE_POSTED = 'date_posted'
COMMENTS = 'comments'

# Define choices for condition and categories
CONDITION_CHOICES = {
    'used': 'Used',
    'new': 'New',
    'old': 'Old'
}
CATEGORY_CHOICES = {
    'clothing': 'Clothing',
    'furniture': 'Furniture',
    'school_supplies': 'School Supplies'
}

# Define the form fields
PRODUCT_FORM_FIELDS = [
    {
        FLD_NM: USER_ID,
        ff.QSTN: 'User ID:',
        ff.PARAM_TYPE: ff.QUERY_STR,
        ff.OPT: False,
    },
    {
        FLD_NM: PRODUCT_NAME,
        ff.QSTN: 'Product Name:',
        ff.PARAM_TYPE: ff.QUERY_STR,
        ff.OPT: False,
    },
    {
        FLD_NM: QUANTITY,
        ff.QSTN: 'Quantity:',
        ff.PARAM_TYPE: ff.INT,
        ff.OPT: False,
    },
    {
        FLD_NM: PRICE,
        ff.QSTN: 'Price:',
        ff.PARAM_TYPE: ff.NUMERIC,
        ff.OPT: False,
    },
    {
        FLD_NM: CONDITION,
        ff.QSTN: 'Condition:',
        ff.PARAM_TYPE: ff.QUERY_STR,
        ff.CHOICES: CONDITION_CHOICES,
        ff.OPT: False,
    },
    {
        FLD_NM: BRAND,
        ff.QSTN: 'Brand:',
        ff.PARAM_TYPE: ff.QUERY_STR,
        ff.OPT: False,
    },
    {
        FLD_NM: CATEGORIES,
        ff.QSTN: 'Category:',
        ff.PARAM_TYPE: ff.QUERY_STR,
        ff.CHOICES: CATEGORY_CHOICES,
        ff.OPT: False,
    },
    {
        FLD_NM: DATE_POSTED,
        ff.QSTN: 'Date Posted:',
        ff.PARAM_TYPE: ff.DATE,
        ff.OPT: False,
    },
    {
        FLD_NM: COMMENTS,
        ff.QSTN: 'Comments:',
        ff.PARAM_TYPE: ff.QUERY_STR,
        ff.OPT: True,
    },
    {
        FLD_NM: DESCRIPTION,
        ff.QSTN: 'Description:',
        ff.PARAM_TYPE: ff.QUERY_STR,
        ff.OPT: True,
    },
]

# Function to return form fields
def get_product_form() -> list:
    return PRODUCT_FORM_FIELDS

# Function to get a description of the form fields for documentation
def get_product_form_descr() -> dict:
    """
    For Swagger!
    """
    return ff.get_form_descr(PRODUCT_FORM_FIELDS)

# Function to get field names from the form
def get_product_form_field_names() -> list:
    return ff.get_fld_names(PRODUCT_FORM_FIELDS)

def main():
    print(f'Product Form: {get_product_form_descr()}\n')

if __name__ == '__main__':
    main()


