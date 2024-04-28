from Crypto.Cipher import AES
from Crypto.Hash import MD5
from Crypto.Util.Padding import pad, unpad
import base64
IS_ENCRYPT_KEY_TYPE_HEX = True


def aes_encryption(data, key: str):
    cipher = AES.new(key.encode(), AES.MODE_ECB)
    encrypted_data = cipher.encrypt(pad(data.encode(), AES.block_size))

    return base64.b64encode(encrypted_data).decode("utf-8")


def aes_decryption(data, key):
    parsed_key = key.encode("utf-8")
    if IS_ENCRYPT_KEY_TYPE_HEX:
        parsed_key = bytes.fromhex(key)
    cipher = AES.new(parsed_key, AES.MODE_ECB)
    decrypted_bytes = cipher.decrypt(base64.b64decode(data))
    padded_plain_text = unpad(decrypted_bytes, AES.block_size)
    return padded_plain_text.decode()


def _generate_md5_key(input_string, model_name, device_mac):
    model_name = model_name.split('.')[-1]
    formatted_mac = device_mac.lower().replace(':', '')
    
    if len(model_name) == 2:
        model_name = '00' + model_name
    elif len(model_name) == 3:
        model_name = '0' + model_name

    model_name_mapping = {
        'b106tr': '06tr',
        'b106eu': '06eu',
        'b106bk': '06bk'
    }
    if len(model_name) == 6:
        if model_name not in model_name_mapping:
            print("Warning unknown model.")
        model_name = model_name[2:]

    temp_key = formatted_mac + model_name
    aeskey = aes_encryption(input_string, temp_key)
    md5_hash = MD5.new(aeskey.encode('utf-8')).hexdigest()

    if IS_ENCRYPT_KEY_TYPE_HEX:
        return md5_hash
    else:
        return md5_hash[8:-8].upper()


def generate_md5_key(wifi_info_sn: str, owner_id: str, device_id: str, model: str, device_mac: str):
    try:
        arr = [str(wifi_info_sn), str(owner_id), str(device_id)]
        temp_string = '+'.join(arr)
        return _generate_md5_key(temp_string, model, device_mac)
    except Exception as e:
        print("DEBUG ERROR Function : genMD5key : %s " % e)
        return None


def unGzipCommon(data: bytes, wifi_info_sn: str, owner_id: str, device_id: str, model: str, device_mac: str):
    try:
        temp_key = generate_md5_key(wifi_info_sn, owner_id, device_id, model, device_mac)
        temp_string = aes_decryption(data, temp_key)
        return temp_string
    except Exception as e:
        print("DEBUG ERROR Function : unGzipCommon : %s" % e)
        return None
