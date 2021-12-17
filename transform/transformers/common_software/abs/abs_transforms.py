

# The following dictionaries define the transformations to perform.
# The key is the qcode, the value describes what transformation needs to be done on the value.
# A dict for the value generally describes what to do with a radio button input and a
# list indicates a function to call (at index 0) and the arguments to pass to that function.

motor_trades = {
    '11': 'period_data',
    '12': 'period_data',
    '399': 'nearest_thousand',
    '80': {'Yes': 10, 'No': 1, None: 0},
    '81': {'0-9%': 10000, '10-24%': 1000, '25-49%': 100, '50-74%': 10, '75-100%': 1, None: 0},
    '450': 'nearest_thousand',
    '403': 'nearest_thousand',
    '420': 'nearest_thousand',
    '400': 'nearest_thousand',
    '500': 'nearest_thousand',
    '599': 'nearest_thousand',
    '600': 'nearest_thousand',
    '699': 'nearest_thousand',
    '163': 'nearest_thousand',
    '164': 'nearest_thousand',
    '15': {'Yes': 10, 'No': 1, None: 0},
    '16': {'Yes': 10, 'No': 1, None: 0},
    '9': {'Yes': 10, 'No': 1, None: 0},
    '146': 'comment',
    '499': ['sum', '403', '420']
}

whole_sale = {
    '11': 'period_data',
    '12': 'period_data',
    '399': 'nearest_thousand',
    '311': 'nearest_thousand',
    '327': 'nearest_thousand',
    '80': {'Yes': 10, 'No': 1, None: 0},
    '81': {'0-9%': 10000, '10-24%': 1000, '25-49%': 100, '50-74%': 10, '75-100%': 1, None: 0},
    '450': 'nearest_thousand',
    '403': 'nearest_thousand',
    '420': 'nearest_thousand',
    '400': 'nearest_thousand',
    '415': 'nearest_thousand',
    '416': 'nearest_thousand',
    '500': 'nearest_thousand',
    '599': 'nearest_thousand',
    '600': 'nearest_thousand',
    '699': 'nearest_thousand',
    '163': 'nearest_thousand',
    '164': 'nearest_thousand',
    '15': {'Yes': 10, 'No': 1, None: 0},
    '16': {'Yes': 10, 'No': 1, None: 0},
    '9': {'Yes': 10, 'No': 1, None: 0},
    '146': 'comment',
    '499': ['sum', '403', '420']
}