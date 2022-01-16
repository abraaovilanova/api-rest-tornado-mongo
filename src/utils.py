def mandatory_keys_check(list_mandatory, list_dict_keys):
  """
    Check if the payload json file have the mandatory keys
    :param list_mandatory: list
    :param list_dict_keys: list
    :return True or False
  """
  check = all(item in list_dict_keys for item in list_mandatory)
  return check