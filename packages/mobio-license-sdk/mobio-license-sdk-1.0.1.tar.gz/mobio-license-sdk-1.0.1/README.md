##  Thư viện license Mobio 


### Cài đặt:
```bash
 $ pip3 install mobio-license-sdk
 ```


### Sử dụng:

##### 1. Khởi tạo sdk:
   ```python
    from mobio.sdks.license import MobioLicenseSDK

    MobioLicenseSDK().config(
        admin_host="",	# admin host
        redis_uri="",	# redis uri
        module_use="",	# liên hệ admin để khai báo tên của module
        module_encrypt="",	# liên hệ admin để lấy mã
        license_key="", # key salt
    )
    
   ```

##### 2. Lấy thông tin license:
   ```python
    from mobio.sdks.license import MobioLicenseSDK
    result = MobioLicenseSDK().get_json_license(
        merchant_id,
    )
    """
    {
      ...   # license info
      
    }
    """
   ```


#### Log - 1.0.1
    - tạo sdk 
