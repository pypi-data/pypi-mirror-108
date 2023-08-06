from .crypt_utils import CryptUtil, MobioCrypt2
import datetime
from .license_mess_used import LicenseMessUsedModel
from .license_detail_mess_used import LicenseDetailMessUsedModel


def ConvertDateUTCtoStringITC(date_input_time, tz_minute, dinhdang="%H:%M %d/%m/%Y"):
    try:
        thoi_gian_itc = date_input_time + datetime.timedelta(minutes=tz_minute)
        return thoi_gian_itc.strftime(dinhdang)
    except:
        return ""


def convert_date_to_format(vNgayThang, format="%Y%m%d%H%M%S"):
    try:
        if vNgayThang is not None:
            return vNgayThang.strftime(format)
        else:
            return ""
    except:
        return ""


def convert_str_to_date(date_str, format="%Y%m%d%H%M%S"):
    try:
        return datetime.datetime.strptime(date_str, format).replace(
            tzinfo=datetime.timezone.utc
        )
    except:
        return None


def get_utc_now():
    now = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
    return now


def convert_timestamp_to_date_utc(timestamp):
    try:
        if timestamp is not None:
            return datetime.datetime.utcfromtimestamp(timestamp).replace(
                tzinfo=datetime.timezone.utc
            )
        else:
            return None
    except:
        return None


def convert_date_utc_to_date_itc(date_input_time, tz_minute):
    try:
        thoi_gian_itc = date_input_time + datetime.timedelta(minutes=tz_minute)
        return thoi_gian_itc
    except:
        return None


class Utils:
    DATE_YYYYmmdd = "%Y%m%d"
    DATE_YYYYmm = "%Y%m"
    TIME_ZONE = 420

    @staticmethod
    def license_get_value_by_key(license_key, merchant_id, key_get):
        json_license = CryptUtil.get_license_info(license_key, merchant_id)
        if json_license:
            return json_license.get(key_get)
        else:
            return None

    @staticmethod
    def get_data_mess_license(license_key, merchant_id):
        data_mess = {}
        json_license = CryptUtil.get_license_info(license_key, merchant_id)
        if json_license:
            data_mess["base_messages"] = json_license.get("base_messages", 0)
            data_mess["increase_messages"] = json_license.get("increase_messages", [])
            data_mess["gift_messages"] = json_license.get("gift_messages", [])
        return data_mess

    # lay so luong mess cho phep su dung trong license
    @staticmethod
    def get_mess_allow_in_license(data_mess, month_get_mess):
        list_block_mess_id, list_gift_code, data_number_mess = [], [], {}
        if data_mess.get("increase_messages"):
            for item in data_mess.get("increase_messages", []):
                try:
                    from_time = ConvertDateUTCtoStringITC(
                        convert_timestamp_to_date_utc(item.get("from_time")),
                        Utils.TIME_ZONE,
                        Utils.DATE_YYYYmm,
                    )
                    to_time = ConvertDateUTCtoStringITC(
                        convert_timestamp_to_date_utc(item.get("to_time")),
                        Utils.TIME_ZONE,
                        Utils.DATE_YYYYmm,
                    )
                    if month_get_mess >= from_time and month_get_mess <= to_time:
                        data_number_mess[item.get("block_mess_id")] = item.get(
                            "total_messages", 0
                        )
                        list_block_mess_id.append(item.get("block_mess_id"))
                except Exception as ex:
                    print(
                        "license_sdk::get_mess_allow_in_license():message: {}".format(
                            ex
                        )
                    )
                    continue
        if data_mess.get("gift_messages"):
            for item in data_mess.get("gift_messages", []):
                if item.get("type_use") == "one_times":
                    data_number_mess[item.get("gift_code")] = item.get("number", 0)
                    list_gift_code.append(item.get("gift_code"))
        return list_block_mess_id, list_gift_code, data_number_mess

    @staticmethod
    def get_time_using_mess(day_of_month):
        if day_of_month:
            last_month = convert_date_to_format(
                convert_str_to_date(day_of_month, Utils.DATE_YYYYmmdd).replace(day=1)
                - datetime.timedelta(days=1),
                Utils.DATE_YYYYmm,
            )
            month_get_mess = day_of_month[:6]
        else:
            dnow_itc = convert_date_utc_to_date_itc(get_utc_now(), Utils.TIME_ZONE)
            last_month = convert_date_to_format(
                dnow_itc.replace(day=1) - datetime.timedelta(days=1),
                Utils.DATE_YYYYmm,
            )
            month_get_mess = convert_date_to_format(dnow_itc, Utils.DATE_YYYYmm)
        return month_get_mess, last_month

    @staticmethod
    def calculator_number_mess_allow_used(license_key, merchant_id, day_of_month=None):
        number_mess, messages = 0, ""
        try:
            data_mess_license = Utils.get_data_mess_license(license_key, merchant_id)
            if data_mess_license:
                if data_mess_license.get("base_messages") < 0:
                    print(
                        "license_sdk::check_number_mess_allow_used(): mess unlimit on package enterprise_package"
                    )
                    return -1, "enterprise package unlimited messages"
                number_mess += data_mess_license.get("base_messages")
                month_get_mess, last_month = Utils.get_time_using_mess(day_of_month)
                (
                    list_block_mess_id,
                    list_gift_code,
                    data_number_mess_license,
                ) = Utils.get_mess_allow_in_license(data_mess_license, month_get_mess)
                print(
                    "license_sdk::check_number_mess_allow_used(): list_block_mess_id: {}, list_gift_code: {}, data_number_mess_license: {}".format(
                        list_block_mess_id, list_gift_code, data_number_mess_license
                    )
                )
                (
                    data_remaining_messages,
                    number_remaining_mess,
                ) = Utils.get_number_remaining_messages(
                    merchant_id,
                    list_block_mess_id,
                    list_gift_code,
                    data_number_mess_license,
                )
                print(
                    "license_sdk::check_number_mess_allow_used(): data_remaining_messages: {}, number_remaining_mess: {}".format(
                        data_remaining_messages, number_remaining_mess
                    )
                )
                number_mess += number_remaining_mess
                # kiem tra so mess can khau tru
                data_mess_month_now = LicenseMessUsedModel().find_one_license_mess_used(
                    merchant_id, month_get_mess
                )
                data_mess_last_month = (
                    LicenseMessUsedModel().find_one_license_mess_used(
                        merchant_id, last_month
                    )
                )
                if not Utils.check_data_mess_used(
                    data_mess_month_now
                ) or not Utils.check_data_mess_used(data_mess_last_month):
                    print(
                        "license_sdk::check_number_mess_allow_used(): data invalid checksum"
                    )
                    return 0, "data invalid checksum"

                mess_base_used = 0
                mess_surplus = 0
                if data_mess_month_now:
                    if (
                        data_mess_month_now.get(LicenseMessUsedModel.mess_surplus, 0)
                        > 0
                    ):
                        mess_surplus = data_mess_month_now.get(
                            LicenseMessUsedModel.mess_surplus, 0
                        )
                    if (
                        data_mess_month_now.get(LicenseMessUsedModel.mess_base_used, 0)
                        > 0
                    ):
                        mess_base_used = data_mess_month_now.get(
                            LicenseMessUsedModel.mess_base_used, 0
                        )
                elif data_mess_last_month:
                    if (
                        data_mess_last_month.get(LicenseMessUsedModel.mess_surplus, 0)
                        > 0
                    ):
                        mess_surplus = data_mess_last_month.get(
                            LicenseMessUsedModel.mess_surplus, 0
                        )
                if mess_surplus > 0:
                    number_mess = number_mess - mess_surplus
                if mess_base_used > 0:
                    number_mess = number_mess - mess_base_used
                if number_mess < 0:
                    print(
                        "license_sdk::check_number_mess_allow_used(): hien da su dung qua so luong tin nhan"
                    )
                    number_mess = 0
            else:
                print("license_sdk::check_number_mess_allow_used(): license none")
        except Exception as ex:
            print("license_sdk::check_number_mess_allow_used():message: {}".format(ex))
        return number_mess, messages

    # kiem tra checksum du lieu co bi sua ko
    @staticmethod
    def check_data_mess_used(data_mess):
        data_invalid = False
        if not data_mess:
            return True
        try:
            check_sum = data_mess.get(LicenseMessUsedModel.check_sum)
            data_text = LicenseMessUsedModel().data_mess_to_string(data_mess)
            if MobioCrypt2.e1(data_text) == check_sum:
                data_invalid = True
        except Exception as ex:
            print("license_sdk::check_data_mess_used():message: {}".format(ex))
        return data_invalid

    # kiem tra so luong mess trong license va so luong mess da su dung
    @staticmethod
    def get_number_remaining_messages(
        merchant_id, list_block_mess_id, list_gift_code, data_number_mess_license
    ):
        data_remaining_messages, total_mess = {}, 0
        list_mess_id = []
        if list_block_mess_id:
            list_mess_id.extend(list_block_mess_id)
        if list_gift_code:
            list_mess_id.extend(list_gift_code)
        data_used = LicenseDetailMessUsedModel().get_number_mess_used_from_mess_id(
            merchant_id, list_mess_id
        )
        if data_number_mess_license:
            for key, value in data_number_mess_license.items():
                mess_used = value
                if data_used:
                    mess_used = value - data_used.get(key, 0)
                if mess_used > 0:
                    data_remaining_messages[key] = mess_used
                    total_mess += mess_used
        return data_remaining_messages, total_mess

    # tinh toan su dung mess can gui
    @staticmethod
    def create_number_mess_need_used(
        license_key, merchant_id, number_mess_need_used, day_of_month=None
    ):
        try:
            pass
        except Exception as ex:
            print("license_sdk::create_number_mess_need_used():message: {}".format(ex))
