def normalize_results(dict):
    """Change the way the results are displayed in order to conform a beter way for the font-end to consume
    
    Args:
        dict (str:any): Dictionary with the devices
    
    Returns:
        dict ([str:any]): Dictionary with a list fo devices
    """
    result = []
    for (key, values) in dict.items():
        values['mac'] = key
        result.append(values)
    return result
