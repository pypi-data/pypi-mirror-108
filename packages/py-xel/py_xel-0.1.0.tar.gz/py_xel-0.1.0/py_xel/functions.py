import pandas as pd

def xlookup(lookup_value, lookup_array, return_array, if_not_found: str = ''):
    '''
    Searches column for lookup value and returns value from second column at the same index

    Parameters:
    lookup_value: value to search for in pandas dataframe
    lookup_array: this is a column inside the source pandas dataframe, we are looking for the “lookup_value” inside this array/column
    return_array: this is a column inside the source pandas dataframe, we want to return values from this column
    if_not_found: will be returned if the “lookup_value” is not found

    Returns:
        match_value.tolist()[0]: returns a pandas Series with the value(s) based on the lookup value, returns if_not_found str if no match.
    '''


    match_value = return_array.loc[lookup_array == lookup_value]
    if match_value.empty:
        return f'"{lookup_value}" not found!' if if_not_found == '' else if_not_found

    else:
        return match_value.tolist()[0]
