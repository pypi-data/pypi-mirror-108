""" This funtion help developer quickly classify the provider of each number phone
Author Minh Tran"""

from vn_numberphone.normalize import normalize

# sample = {
#     'Viettel': ('097', '098', '096', '086', '032', '033',
#     '034', '035', '036', '037', '038', '039'),
#     'Mobifone': ('090', '093', '089', '070', '079', '077', '076', '078'),
#     'Vinaphone': ('091', '094', '088', '081', '082', '083', '084', '085'),
#     'Vietnammobile': ('092', '056', '058'),
#     'Gmobile': ('099', '059'),
#     'Sfone': ('095'),
#     'Landline': ('021', '022', '023', '024', '025', '026', '027', '028', '029')
# }

sample = {'097': 'Viettel', '098': 'Viettel', '096': 'Viettel', '086': 'Viettel',
          '032': 'Viettel', '033': 'Viettel', '034': 'Viettel', '035': 'Viettel',
          '036': 'Viettel', '037': 'Viettel', '038': 'Viettel', '039': 'Viettel',
          '090': 'Mobifone', '093': 'Mobifone', '089': 'Mobifone', '070': 'Mobifone',
          '079': 'Mobifone', '077': 'Mobifone', '076': 'Mobifone', '078': 'Mobifone',
          '091': 'Vinaphone', '094': 'Vinaphone', '088': 'Vinaphone', '081': 'Vinaphone',
          '082': 'Vinaphone', '083': 'Vinaphone', '084': 'Vinaphone',
          '085': 'Vinaphone', '092': 'Vietnammobile', '056': 'Vietnammobile',
          '058': 'Vietnammobile', '099': 'Gmobile', '059': 'Gmobile', '095': 'Sfone',
          '021': 'Landline', '022': 'Landline', '023': 'Landline', '024': 'Landline',
          '025': 'Landline', '026': 'Landline', '027': 'Landline',
          '028': 'Landline', '029': 'Landline'
          }


def get_provider(text_phone: str) -> str:
    """
    Classify the provider network of a number phone.
    :param text_phone: The number phone after normalized
    :return: The provider network
    """
    text_phone = normalize(text_phone)
    print(text_phone)
    head = text_phone[:3]
    provider = sample.get(head)
    if not provider:
        return "Can't find the provider of this number phone or The provider has not updated!"
    return provider


if __name__ == '__main__':
    print(get_provider("0084961557497"))
