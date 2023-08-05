"""This module help developer can quickly convert, normalize vietnam phonenumber
Author: Minh Tran"""

from vn_numberphone.utils import (check_type_single,
                                  check_type_inter,
                                  convert_11_2_10,
                                  convert_inter_code,
                                  convert_inter_2_localize
                                  )


def normalize(text: str, international: bool = False, head='+84') -> str:
    """
    This funtion can be normalize phone number,
    convert from old version to new version for Vietnam number phone
    :param text: The input contain only number phone need to be normalize
    :param international: The output follow internaltional type or not
    :param head: The international coding would be display, it maybe is '+84' or '0084'
    :return: Phone number normalized
    """
    _, __ = check_type_single(text), check_type_inter(international)
    text = convert_11_2_10(text)
    text = convert_inter_2_localize(text)
    if international:
        text = convert_inter_code(text, head)
    return text


if __name__ == '__main__':
    print(normalize("01665441455", True))
