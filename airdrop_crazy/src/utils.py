def normalize_results(dict, key_name):
    """Change the way the results are displayed in order to conform a beter way for the font-end to consume
    
    Args:
        dict (str:any): Dictionary with the devices
        key_name (str): name of the key
    
    Returns:
        dict ([str:any]): Dictionary with a list fo devices
    """
    result = []
    for (key, values) in dict.items():
        values[key_name] = key
        result.append(values)
    return result

if __name__ == "__main__":
    test = {}
    print(normalize_results(test, "hash"))