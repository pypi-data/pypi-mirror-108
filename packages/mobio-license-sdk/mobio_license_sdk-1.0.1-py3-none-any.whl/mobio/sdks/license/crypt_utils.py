#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" Author: AnhNT
    Company: MobioVN
    Date created: 2021/06/03
"""

import hashlib
import json
from Crypto.Cipher import AES
from .config import PathDir
import time
import os
import base64
import numpy as np


class MobioCrypt1:
    @staticmethod
    def _g(pd, s):
        n1 = 0x407
        m1 = [0x73, 0x68, 0x61]
        m2 = [0x35, 0x31, 0x32]
        m = "".join([chr(i) for i in m1]) + "".join([chr(i) for i in m2])
        dk = hashlib.pbkdf2_hmac(m, pd.encode(), s, n1).hex()
        return dk[:0x20]

    @staticmethod
    def __u(s):
        return s[: -ord(s[len(s) - 1 :])]

    @staticmethod
    def d1(enc, password, salt):
        p = MobioCrypt1._g(password, salt)
        i = enc[:0x10]
        cer = AES.new(bytes(p, "utf-8"), AES.MODE_CBC, i)
        return MobioCrypt1.__u(cer.decrypt(enc[0x10:])).decode("utf8")

    @staticmethod
    def g1(p, t, s):
        if s != 0x1341589:
            return ""
        if t == 1:
            return (
                hashlib.md5(bytes(p, "utf-8")).hexdigest()
                + hashlib.md5(bytes(p, "utf-8")).hexdigest()
            )
        if t == 2:
            ps = p.split("-")
            if len(ps) == 4:
                return ""
            return ps[1] + ps[3]


class MobioCrypt2:
    @staticmethod
    def __f1(x1):
        x = v = 1
        y = u = 0
        a = 0x100
        b = x1 % 0x100
        while b != 0:
            q = int(a / b)
            r = int(a - b * q)
            s = int(x - u * q)
            t = int(y - v * q)
            a = b
            x = u
            y = v
            b = r
            u = s
            v = t
        while y < 0:
            y += 0x100
        while y > 0x100:
            y -= 0x100
        return y

    @staticmethod
    def __f2():
        return np.random.randint(1, 0x100, 0x0A)

    @staticmethod
    def e1(raw):
        if isinstance(raw, str):
            raw = raw.encode("utf-8")

        ln = len(raw)

        r1 = bytearray()
        tmp = MobioCrypt2.__f2()

        for i in range(0, len(tmp)):
            r1.append(tmp[i])

        i = r1[0]
        k = r1[1]

        i += 1 if i % 2 == 0 else 0
        i = 0x8F if i == 1 else i

        for j in range(0, ln):
            tmp = (int(raw[j]) * i + k + r1[(2 + (j % 8))]) % 0x100
            while tmp >= 0x100:
                tmp -= 0x100
            while tmp < 0:
                tmp += 0x100
            r1.append(tmp)
        r1 = MobioCrypt3.e1(r1).rstrip("=")
        return r1 + hashlib.md5(r1.encode("utf-8")).hexdigest()

    @staticmethod
    def d1(encrypted, enc=None):
        raw = encrypted[0 : len(encrypted) - 0x20]
        c1 = encrypted[len(encrypted) - 0x20 :]
        c2 = hashlib.md5(raw.encode("utf-8")).hexdigest()
        if c2 != c1:
            return None

        raw = MobioCrypt3.d1(raw)
        ln = len(raw)

        i = raw[0]
        i += 1 if i % 2 == 0 else 0
        i = 0x8F if i == 1 else i

        lc = MobioCrypt2.__f1(i)
        m = raw[1]
        r1 = bytearray()
        for j in range(10, ln):
            tmp = ((int(raw[j]) - raw[(2 + ((j - int(0x0A)) % 8))] - m) * lc) % 0x100
            while tmp >= 0x100:
                tmp -= 0x100
            while tmp < 0:
                tmp += 0x100
            if j >= 10:
                r1.append(tmp)
        if enc:
            return r1.decode(encoding=enc)
        return r1


class MobioCrypt3:
    @staticmethod
    def e1(raw):
        try:
            bs = raw
            if isinstance(raw, str):
                bs = raw.encode("utf-8")

            ed = base64.b64encode(bs)
            return ed.decode(encoding="UTF-8")
        except:
            return ""

    @staticmethod
    def e2(raw):
        return MobioCrypt3.e1(raw).rstrip("=")

    @staticmethod
    def d1(raw, enc=None):
        try:
            if isinstance(raw, bytes):
                raw = raw.decode("UTF-8")
            dd = base64.urlsafe_b64decode(raw + "=" * (-len(raw) % 4))
            if enc:
                return dd.decode(encoding=enc)
            return dd
        except:
            return None


class CryptUtil:
    @staticmethod
    def decrypt_mobio_crypt1(key_salt, text_encrypt):
        m = MobioCrypt1.g1(key_salt, 1, 0x1341589)
        u = MobioCrypt1.g1(key_salt, 2, 0x1341589)
        return MobioCrypt1.d1(bytes.fromhex(text_encrypt), m, bytes(u, "utf-8"))

    @staticmethod
    def get_file_path_license(merchant_id):
        license_file_name = hashlib.md5(bytes(merchant_id, "utf-8")).hexdigest()
        file_path = "{}/{}.{}".format(
            PathDir.PATH_DIR_LICENSE_FILE, license_file_name, "license"
        )
        return file_path

    @staticmethod
    def get_content_from_file(file_path):
        content_file = None
        if not os.path.exists(file_path):
            return content_file
        while True:
            try:
                with open(file_path, "r") as fout:
                    content_file = fout.read()
                    fout.close()
                break
            except IOError as ex:
                print("license_sdk::get_content_from_file():message: %s" % ex)
                time.sleep(0.1)
        return content_file

    @staticmethod
    def get_license_info(license_key, merchant_id):
        license_info = None
        try:
            file_path = CryptUtil.get_file_path_license(merchant_id)
            license_encrypt = CryptUtil.get_content_from_file(file_path)
            private_key = license_key + merchant_id
            m = MobioCrypt1.g1(private_key, 1, 0x1341589)
            u = MobioCrypt1.g1(private_key, 2, 0x1341589)
            json_body = json.loads(
                MobioCrypt1.d1(bytes.fromhex(license_encrypt), m, bytes(u, "utf-8")),
                encoding="utf-8",
            )
            u1 = u
            u1 += str(json_body.get("t01")) + str(json_body.get("t06"))
            license_info = json.loads(
                MobioCrypt1.d1(
                    bytes.fromhex(json_body.get("data")), m, bytes(u1, "utf-8")
                ),
                encoding="utf-8",
            )
        except Exception as ex:
            print("license_sdk::get_license_info():message: {}".format(ex))
        return license_info

    @staticmethod
    def check_key_valid_function(key_valid, func_name):
        invalid = False
        try:
            text_decrypt = MobioCrypt2.d1(key_valid, "utf-8")
            list_param = text_decrypt.split("_")
            if len(list_param) >= 3:
                if list_param[0] == func_name:
                    if list_param[1] == "dev":
                        time_expire = int(list_param[2])
                        if time_expire > time.time():
                            invalid = True
                    elif list_param[1] == "prod":
                        invalid = True
        except Exception as ex:
            print("license_sdk::check_key_valid_function():message: {}".format(ex))
        return invalid
