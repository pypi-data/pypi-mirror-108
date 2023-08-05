import app.scripts.terminal_scripts as term
import app.scripts.key_mgmt_utility_scripts as kmu
import time


def genECCKeyPair(eni_ip, username, password, key_label):
    print('Configuring CloudHSM Client')
    term.configure_cloudhsm_client(eni_ip=eni_ip)
    time.sleep(1)

    print('Generating Key Pair')
    key_handles = kmu.generate_key_pair(
        username=username, password=password, key_label=key_label)
    time.sleep(1)

    print('Exporting public key file')
    pub_key_handle = key_handles['public_key']
    pub_key_pem_file_name = kmu.export_public_key(
        username=username, password=password, pub_key_handle=pub_key_handle)

    return {
        'public_key_handle': key_handles['public_key'],
        'private_key_handle': key_handles['private_key'],
        'public_key_pem_file': pub_key_pem_file_name
    }
