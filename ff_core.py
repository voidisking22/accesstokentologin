#!/usr/bin/env python3
import binascii
import base64
import time
import warnings
from datetime import datetime
import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from google.protobuf import descriptor_pool, message_factory
import blackboxprotobuf

warnings.filterwarnings("ignore")
requests.packages.urllib3.disable_warnings()

mYdEsCrIpToR = b'\n\x08my.proto"\xae\t\n\x08GameData\x12\x11\n\ttimestamp\x18\x03 \x01(\t\x12\x11\n\tgame_name\x18\x04 \x01(\t\x12\x14\n\x0cgame_version\x18\x05 \x01(\x05\x12\x14\n\x0cversion_code\x18\x07 \x01(\t\x12\x0f\n\x07os_info\x18\x08 \x01(\t\x12\x13\n\x0bdevice_type\x18\t \x01(\t\x12\x18\n\x10network_provider\x18\n \x01(\t\x12\x17\n\x0fconnection_type\x18\x0b \x01(\t\x12\x14\n\x0cscreen_width\x18\x0c \x01(\x05\x12\x15\n\rscreen_height\x18\r \x01(\x05\x12\x0b\n\x03dpi\x18\x0e \x01(\t\x12\x10\n\x08cpu_info\x18\x0f \x01(\t\x12\x11\n\ttotal_ram\x18\x10 \x01(\x05\x12\x10\n\x08gpu_name\x18\x11 \x01(\t\x12\x13\n\x0bgpu_version\x18\x12 \x01(\t\x12\x0f\n\x07user_id\x18\x13 \x01(\t\x12\x12\n\nip_address\x18\x14 \x01(\t\x12\x10\n\x08language\x18\x15 \x01(\t\x12\x0f\n\x07open_id\x18\x16 \x01(\t\x12\x15\n\rplatform_type\x18\x17 \x01(\x05\x12\x1a\n\x12device_form_factor\x18\x18 \x01(\t\x12\x14\n\x0cdevice_model\x18\x19 \x01(\t\x12\x14\n\x0caccess_token\x18\x1d \x01(\t\x12\x18\n\x10unknown_field_30\x18\x1e \x01(\x05\x12"\n\x1asecondary_network_provider\x18) \x01(\t\x12!\n\x19secondary_connection_type\x18* \x01(\t\x12\x11\n\tunique_id\x18\x39 \x01(\t\x12\x10\n\x08field_60\x18< \x01(\x05\x12\x10\n\x08field_61\x18= \x01(\x05\x12\x10\n\x08field_62\x18> \x01(\x05\x12\x10\n\x08field_63\x18? \x01(\x05\x12\x10\n\x08field_64\x18@ \x01(\x05\x12\x10\n\x08field_65\x18A \x01(\x05\x12\x10\n\x08field_66\x18B \x01(\x05\x12\x10\n\x08field_67\x18C \x01(\x05\x12\x10\n\x08field_70\x18F \x01(\x05\x12\x10\n\x08field_73\x18I \x01(\x05\x12\x14\n\x0clibrary_path\x18J \x01(\t\x12\x10\n\x08field_76\x18L \x01(\x05\x12\x10\n\x08apk_info\x18M \x01(\t\x12\x10\n\x08field_78\x18N \x01(\x05\x12\x10\n\x08field_79\x18O \x01(\x05\x12\x17\n\x0fos_architecture\x18Q \x01(\t\x12\x14\n\x0cbuild_number\x18S \x01(\t\x12\x10\n\x08field_85\x18U \x01(\x05\x12\x18\n\x10graphics_backend\x18V \x01(\t\x12\x19\n\x11max_texture_units\x18W \x01(\x05\x12\x15\n\rrendering_api\x18X \x01(\x05\x12\x18\n\x10encoded_field_89\x18Y \x01(\t\x12\x10\n\x08field_92\x18\\ \x01(\x05\x12\x13\n\x0bmarketplace\x18] \x01(\t\x12\x16\n\x0eencryption_key\x18^ \x01(\t\x12\x15\n\rtotal_storage\x18_ \x01(\x05\x12\x10\n\x08field_97\x18a \x01(\x05\x12\x10\n\x08field_98\x18b \x01(\x05\x12\x10\n\x08field_99\x18c \x01(\t\x12\x11\n\tfield_100\x18d \x01(\tb\x06proto3'

oUtPuTdEsCrIpToR = b'\n\x13jwt_generator.proto"\xd2\x02\n\nGarena_420\x12\x12\n\naccount_id\x18\x01 \x01(\x03\x12\x0e\n\x06region\x18\x02 \x01(\t\x12\r\n\x05place\x18\x03 \x01(\t\x12\x10\n\x08location\x18\x04 \x01(\t\x12\x0e\n\x06status\x18\x05 \x01(\t\x12\r\n\x05token\x18\x08 \x01(\t\x12\n\n\x02id\x18\t \x01(\x05\x12\x0b\n\x03api\x18\n \x01(\t\x12\x0e\n\x06number\x18\x0c \x01(\x05\x12\x1e\n\tGarena420\x18\x0f \x01(\x0b\x32\x0b.Garena_420\x12\x0c\n\x04area\x18\x10 \x01(\t\x12\x11\n\tmain_area\x18\x12 \x01(\t\x12\x0c\n\x04city\x18\x13 \x01(\t\x12\x0c\n\x04name\x18\x14 \x01(\t\x12\x11\n\ttimestamp\x18\x15 \x01(\x03\x12\x0e\n\x06binary\x18\x16 \x01(\x0c\x12\x13\n\x0bbinary_data\x18\x17 \x01(\x0c\x1a"\n\x12Decrypted_Payloads\x12\x0c\n\x04type\x18\x01 \x01(\x05b\x06proto3'

pOoL = descriptor_pool.Default()
pOoL.AddSerializedFile(mYdEsCrIpToR)
pOoL.AddSerializedFile(oUtPuTdEsCrIpToR)
factory = message_factory.MessageFactory()
gAmEdAtA = factory.GetPrototype(pOoL.FindMessageTypeByName('GameData'))
gArEnA420 = factory.GetPrototype(pOoL.FindMessageTypeByName('Garena_420'))

aEsKeY = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
aEsIv = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])

mAjOrLoGiNuRl = "https://loginbp.ggblueshark.com/MajorLogin"
iNsPeCtUrL = "https://100067.connect.garena.com/oauth/token/inspect"
xOrKeY = b"1e5898ccb8dfdd921f9bdea848768b64a201"


def eNcRyPtDaTa(dAtA):
    cIpHeR = AES.new(aEsKeY, AES.MODE_CBC, aEsIv)
    return cIpHeR.encrypt(pad(dAtA, AES.block_size))


def dEcRyPtDaTa(dAtA):
    if len(dAtA) % 16 != 0:
        return dAtA
    try:
        cIpHeR = AES.new(aEsKeY, AES.MODE_CBC, aEsIv)
        return unpad(cIpHeR.decrypt(dAtA), AES.block_size)
    except Exception:
        return dAtA


def pRoToBuFdEcOdE(dAtA: bytes):
    dEcOdEd, _ = blackboxprotobuf.decode_message(dAtA)
    return dEcOdEd


def iNsPeCtToKeN(aCcEsStOkEn):
    uRl = f"{iNsPeCtUrL}?token={aCcEsStOkEn}"
    hEaDeRs = {'User-Agent': "GarenaMSDK/4.0.19P9"}
    rEsP = requests.get(uRl, headers=hEaDeRs, timeout=10, verify=False)
    if rEsP.status_code != 200:
        raise Exception(f"Inspect failed: {rEsP.status_code}")
    dAtA = rEsP.json()
    return dAtA.get('open_id')


def dEcOdEfFnAmE(b64_str: str) -> str:
    try:
        if not b64_str:
            return ""
        b64_str = b64_str.strip()
        b64_str += "=" * ((4 - len(b64_str) % 4) % 4)
        encrypted_bytes = base64.b64decode(b64_str)
        decrypted_bytes = bytearray()
        for i, byte in enumerate(encrypted_bytes):
            key_byte = xOrKeY[i % len(xOrKeY)]
            decrypted_bytes.append(byte ^ key_byte)
        return decrypted_bytes.decode('utf-8', errors='ignore')
    except Exception:
        return b64_str


def gEnErAtEmAjOrLoGiNrEsP(aCcEsStOkEn, oPeNiD, bAsEfIeLdS, pReFeRrEdPlAtFoRm=None):
    aLlPlAtFoRmS = list(range(1, 10))
    if pReFeRrEdPlAtFoRm is not None and pReFeRrEdPlAtFoRm in aLlPlAtFoRmS:
        pLaTfOrMs = [pReFeRrEdPlAtFoRm] + [p for p in aLlPlAtFoRmS if p != pReFeRrEdPlAtFoRm]
    else:
        pLaTfOrMs = aLlPlAtFoRmS

    for pLaTfOrM in pLaTfOrMs:
        try:
            gAmE = gAmEdAtA()
            for fIeLdNuMsTr, vAlUe in bAsEfIeLdS.items():
                fIeLdNuM = int(fIeLdNuMsTr)
                fIeLd = gAmEdAtA.DESCRIPTOR.fields_by_number.get(fIeLdNuM)
                if fIeLd is None:
                    continue
                if fIeLd.type == fIeLd.TYPE_STRING:
                    if isinstance(vAlUe, bytes):
                        try:
                            vAlUe = vAlUe.decode('utf-8')
                        except UnicodeDecodeError:
                            vAlUe = vAlUe.hex()
                    setattr(gAmE, fIeLd.name, str(vAlUe))
                elif fIeLd.type in (fIeLd.TYPE_INT32, fIeLd.TYPE_INT64,
                                    fIeLd.TYPE_UINT32, fIeLd.TYPE_UINT64,
                                    fIeLd.TYPE_SINT32, fIeLd.TYPE_SINT64):
                    setattr(gAmE, fIeLd.name, int(vAlUe))
                elif fIeLd.type == fIeLd.TYPE_BOOL:
                    setattr(gAmE, fIeLd.name, bool(vAlUe))
                elif fIeLd.type == fIeLd.TYPE_BYTES:
                    if isinstance(vAlUe, str):
                        try:
                            vAlUe = binascii.unhexlify(vAlUe)
                        except Exception:
                            vAlUe = vAlUe.encode()
                    setattr(gAmE, fIeLd.name, vAlUe)
                else:
                    setattr(gAmE, fIeLd.name, vAlUe)
            gAmE.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            gAmE.open_id = oPeNiD
            gAmE.access_token = aCcEsStOkEn
            gAmE.platform_type = pLaTfOrM
            gAmE.field_99 = str(pLaTfOrM)
            gAmE.field_100 = str(pLaTfOrM)
            sEr = gAmE.SerializeToString()
            eNc = eNcRyPtDaTa(sEr)
            hEaDeRs = {
                "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; ASUS_Z01QD Build/PI)",
                "Content-Type": "application/octet-stream",
                "X-Unity-Version": "2018.4.11f1",
                "X-GA": "v1 1",
                "ReleaseVersion": "OB54"
            }
            rEsP = requests.post(mAjOrLoGiNuRl, data=eNc, headers=hEaDeRs, verify=False, timeout=10)
            if rEsP.status_code == 200:
                return rEsP.content
        except Exception:
            pass
        time.sleep(0.1)
    raise Exception("No valid response after trying all platforms 1-9")


def fEtChAcCoUnTiNfO(aCcEsStOkEn):
    uRl = f"https://ff-jwt-gen-api.lovable.app/api/public/token?access_token={aCcEsStOkEn}"
    rEsP = requests.get(uRl, timeout=10, verify=False)
    if rEsP.status_code != 200:
        raise Exception(f"API returned {rEsP.status_code}")
    dAtA = rEsP.json()
    if not dAtA.get('success', False):
        raise Exception("API indicated failure")
    aCcOuNtUiD = dAtA.get('account_uid', 'N/A')
    rEgIoN = dAtA.get('region', 'N/A')
    pLaTfOrMuSeD = dAtA.get('platform_type_used')
    pAyLoAd = dAtA.get('jwt_decoded', {}).get('payload', {})
    nIcKnAmEeNc = pAyLoAd.get('nickname', '')
    nIcKnAmE = dEcOdEfFnAmE(nIcKnAmEeNc) if nIcKnAmEeNc else 'Unknown'
    return aCcOuNtUiD, rEgIoN, nIcKnAmE, pLaTfOrMuSeD