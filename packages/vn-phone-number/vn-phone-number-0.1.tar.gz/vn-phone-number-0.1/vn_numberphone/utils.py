"""Author Minh Tran"""
import re


def check_type_single(number: str) -> None:
    """
    Check the type of input must be string.
    :param number: input contains number phone
    :return: None
    """
    if not isinstance(number, str):
        raise ValueError("The `number` value ('{}') must be string type, "
                         "but {} founded".format(number, type(number)))


def check_type_inter(flag: bool) -> None:
    """
    Check the value of international code.
    :param flag: Using international code or not
    :return: None
    """
    if not isinstance(flag, bool):
        raise ValueError("The `international` value ('{}') must be Bool type, "
                         "but {} founded.".format(flag, type(flag)))


def check_length(number: str) -> bool:
    """
    Check the length after extract only digits.
    :param number: Phone number
    :return: 10 <= len(number) <= 11
    """
    return 10 <= len(number) <= 14


def convert_inter_code(number: str, head: str) -> str:
    """
    :param number: The number phone - input.
    :param head:  The code of Vietnam number phone, is +84 or 0084 for international coding
    :return: International type
    """
    return number.replace('0', head, 1)


def pre_process_single(text_number: str) -> str:
    """
    Should be extract only digits number in input, change 84 for localize.
    :param text_number: the number phone input
    :return: number phone after pre-process
    """
    # Extract only digits from input
    text_number = re.findall(r'\d+', text_number)
    text_number = ''.join(text_number)

    # if text_number.startswith('84'):
    #     text_number = text_number.replace('84', '0', 1)

    return text_number


def convert_inter_2_localize(number_phone: str) -> str:
    """
    Process international part
    :param number_phone: The number phone need to be convert to localize version
    :return: The number phone after localize
    """
    number_phone = pre_process_single(number_phone)
    s = ['0084', '084', '84']
    for head in s:
        if number_phone.startswith(head):
            number_phone = number_phone.replace(head, '0', 1)
            break
    return number_phone


heading = {
    # Viettel
    '0169': '039',
    '0168': '038',
    '0167': '037',
    '0166': '036',
    '0165': '035',
    '0164': '034',
    '0163': '033',
    '0162': '032',
    # mobifone
    '0120': '070',
    '0121': '079',
    '0122': '077',
    '0126': '076',
    '0128': '078',
    # vinaphone
    '0123': '083',
    '0124': '084',
    '0125': '085',
    '0127': '081',
    '0129': '082',
    # gmobile
    '0199': '059',
    # vietnamemobile
    '0186': '056',
    '0188': '058'

}


def convert_11_2_10(number: str) -> str:
    """
    Convert the older version to new version of Vietnam numberphone.
    :param number: the number phone input
    :return: number phone new version
    """
    number = pre_process_single(number)
    if not check_length(number):
        raise ValueError("Should be review this input, "
                         "contains many numbers in input: {}".format(number))

    head_ = number[:4]
    val = heading.get(head_)
    if not val:
        return number

    number = number.replace(head_, val, 1)
    return number
