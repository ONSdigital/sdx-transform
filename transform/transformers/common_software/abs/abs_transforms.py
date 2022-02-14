

# The following dictionaries define the transformations to perform.
# The key is the qcode, the value describes what transformation needs to be done on the value.
# A dict for the value generally describes what to do with a radio button input and a
# list indicates a function to call (at index 0) and the arguments to pass to that function.

# 1802
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

# 1804
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

# 1808
catering = {
    '11': 'period_data',
    '12': 'period_data',
    '346': 'nearest_thousand',
    '80': {'Yes': 10, 'No': 1, None: 0},
    '81': {'0-9%': 10000, '10-24%': 1000, '25-49%': 100, '50-74%': 10, '75-100%': 1, None: 0},
    '450': 'nearest_thousand',
    '499': 'nearest_thousand',
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
}

# 1810 - Property
property_survey = {
    '11': 'period_data',
    '12': 'period_data',
    '399': 'nearest_thousand',
    '80': {'Yes': 10, 'No': 1, None: 0},
    '81': {'0-9%': 10000, '10-24%': 1000, '25-49%': 100, '50-74%': 10, '75-100%': 1, None: 0},
    '450': 'nearest_thousand',
    '499': 'nearest_thousand',
    '400': 'nearest_thousand',
    '501': 'nearest_thousand',
    '502': 'nearest_thousand',
    '600': 'nearest_thousand',
    '699': 'nearest_thousand',
    '163': 'nearest_thousand',
    '164': 'nearest_thousand',
    '15': {'Yes': 10, 'No': 1, None: 0},
    '16': {'Yes': 10, 'No': 1, None: 0},
    '9': {'Yes': 10, 'No': 1, None: 0},
    '146': 'comment',
}

# 1812 - Transport
transport_services = {
    '11': 'period_data',
    '12': 'period_data',
    '399': 'nearest_thousand',
    '80': {'Yes': 10, 'No': 1, None: 0},
    '81': {'0-9%': 10000, '10-24%': 1000, '25-49%': 100, '50-74%': 10, '75-100%': 1, None: 0},
    '450': 'nearest_thousand',
    '499': 'nearest_thousand',
    '400': 'nearest_thousand',
    '600': 'nearest_thousand',
    '699': 'nearest_thousand',
    '163': 'nearest_thousand',
    '164': 'nearest_thousand',
    '15': {'Yes': 10, 'No': 1, None: 0},
    '16': {'Yes': 10, 'No': 1, None: 0},
    '9': {'Yes': 10, 'No': 1, None: 0},
    '146': 'comment',
}

# 1814 - Service Commission industry
service_commission = {
    '11': 'period_data',
    '12': 'period_data',
    '399': 'nearest_thousand',
    '337': 'nearest_thousand',
    '339': 'nearest_thousand',
    '80': {'Yes': 10, 'No': 1, None: 0},
    '81': {'0-9%': 10000, '10-24%': 1000, '25-49%': 100, '50-74%': 10, '75-100%': 1, None: 0},
    '450': 'nearest_thousand',
    '499': 'nearest_thousand',
    '400': 'nearest_thousand',
    '600': 'nearest_thousand',
    '699': 'nearest_thousand',
    '163': 'nearest_thousand',
    '164': 'nearest_thousand',
    '15': {'Yes': 10, 'No': 1, None: 0},
    '16': {'Yes': 10, 'No': 1, None: 0},
    '9': {'Yes': 10, 'No': 1, None: 0},
    '146': 'comment',
}

# 1818 - Computer
computer_industry = {
    '11': 'period_data',
    '12': 'period_data',
    '399': 'nearest_thousand',
    '80': {'Yes': 10, 'No': 1, None: 0},
    '81': {'0-9%': 10000, '10-24%': 1000, '25-49%': 100, '50-74%': 10, '75-100%': 1, None: 0},
    '450': 'nearest_thousand',
    '499': 'nearest_thousand',
    '400': 'nearest_thousand',
    '501': 'nearest_thousand',
    '502': 'nearest_thousand',
    '600': 'nearest_thousand',
    '699': 'nearest_thousand',
    '163': 'nearest_thousand',
    '164': 'nearest_thousand',
    '15': {'Yes': 10, 'No': 1, None: 0},
    '16': {'Yes': 10, 'No': 1, None: 0},
    '9': {'Yes': 10, 'No': 1, None: 0},
    '146': 'comment',
}

# 1820 - Other
other_services = {
    '11': 'period_data',
    '12': 'period_data',
    '399': 'nearest_thousand',
    '80': {'Yes': 10, 'No': 1, None: 0},
    '81': {'0-9%': 10000, '10-24%': 1000, '25-49%': 100, '50-74%': 10, '75-100%': 1, None: 0},
    '450': 'nearest_thousand',
    '499': 'nearest_thousand',
    '400': 'nearest_thousand',
    '600': 'nearest_thousand',
    '699': 'nearest_thousand',
    '163': 'nearest_thousand',
    '164': 'nearest_thousand',
    '15': {'Yes': 10, 'No': 1, None: 0},
    '16': {'Yes': 10, 'No': 1, None: 0},
    '9': {'Yes': 10, 'No': 1, None: 0},
}

# 1824 - Postal
postal = {
    '11': 'period_data',
    '12': 'period_data',
    '399': 'nearest_thousand',
    '300': 'nearest_thousand',
    '80': {'Yes': 10, 'No': 1, None: 0},
    '81': {'0-9%': 10000, '10-24%': 1000, '25-49%': 100, '50-74%': 10, '75-100%': 1, None: 0},
    '450': 'nearest_thousand',
    '499': 'nearest_thousand',
    '400': 'nearest_thousand',
    '600': 'nearest_thousand',
    '699': 'nearest_thousand',
    '163': 'nearest_thousand',
    '164': 'nearest_thousand',
    '15': {'Yes': 10, 'No': 1, None: 0},
    '16': {'Yes': 10, 'No': 1, None: 0},
    '9': {'Yes': 10, 'No': 1, None: 0},
    '146': 'comment',
}

# 1826 - Marketing
non_marketing = {
    '11': 'period_data',
    '12': 'period_data',
    '399': 'nearest_thousand',
    '318': 'nearest_thousand',
    '80': {'Yes': 10, 'No': 1, None: 0},
    '81': {'0-9%': 10000, '10-24%': 1000, '25-49%': 100, '50-74%': 10, '75-100%': 1, None: 0},
    '450': 'nearest_thousand',
    '499': 'nearest_thousand',
    '475': 'nearest_thousand',
    '476': 'nearest_thousand',
    '400': 'nearest_thousand',
    '600': 'nearest_thousand',
    '699': 'nearest_thousand',
    '163': 'nearest_thousand',
    '164': 'nearest_thousand',
    '15': {'Yes': 10, 'No': 1, None: 0},
    '16': {'Yes': 10, 'No': 1, None: 0},
    '9': {'Yes': 10, 'No': 1, None: 0},
    '146': 'comment',
}

# 1862 - Duty's
duty = {
    '11': 'period_data',
    '12': 'period_data',
    '399': 'nearest_thousand',
    '80': {'Yes': 10, 'No': 1, None: 0},
    '81': {'0-9%': 10000, '10-24%': 1000, '25-49%': 100, '50-74%': 10, '75-100%': 1, None: 0},
    '450': 'nearest_thousand',
    '499': 'nearest_thousand',
    '412': 'nearest_thousand',
    '431': 'nearest_thousand',
    '455': 'nearest_thousand',
    '415': 'nearest_thousand',
    '419': 'nearest_thousand',
    '414': 'nearest_thousand',
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
}

# 1864 - Standard
standard = {
    '11': 'period_data',
    '12': 'period_data',
    '399': 'nearest_thousand',
    '80': {'Yes': 10, 'No': 1, None: 0},
    '81': {'0-9%': 10000, '10-24%': 1000, '25-49%': 100, '50-74%': 10, '75-100%': 1, None: 0},
    '450': 'nearest_thousand',
    '499': 'nearest_thousand',
    '400': 'nearest_thousand',
    '414': 'nearest_thousand',
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
}

# 1874 - Construction
construction = {
    '11': 'period_data',
    '12': 'period_data',
    '399': 'nearest_thousand',
    '80': {'Yes': 10, 'No': 1, None: 0},
    '81': {'0-9%': 10000, '10-24%': 1000, '25-49%': 100, '50-74%': 10, '75-100%': 1, None: 0},
    '450': 'nearest_thousand',
    '499': 'nearest_thousand',
    '400': 'nearest_thousand',
    '414': 'nearest_thousand',
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
}
