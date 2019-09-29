import json
import os
import time

def check_integrity(data=None):
    if data == None:
        # check current config file
        x = config
    else:
        # check new config data
        x = data
    # check type
    if type(x) != dict:
        return False
    # check accounts and api keys
    if len(x['accounts']) < 1:
        return False
    for acc in x['accounts']:
        if 'api' not in acc:
            return False
        if 'key' not in acc['api']:
            return False
        if 'secret' not in acc['api']:
            return False
        if 'sl' not in acc or 'tp' not in acc:
            return False
        if 'dist' not in acc['sl'] or 'trail' not in acc['sl']:
            return False
        if 'dist' not in acc['tp']:
            return False
    # if all checks pass return True
    return True

def new_config():
    # create new config
    conf = {}
    accounts = []
    tmp_acc = {
        'api': {'key': '', 'secret': ''},
        'sl': {'dist': 0.02, 'trail': 0.005},
        'tp': {'dist': 0.05}
    }
    accounts.append(tmp_acc)
    # populate config file and save
    conf['accounts'] = accounts
    f = open('config.json', 'w')
    f.write(json.dumps(conf))
    f.close()
    print('New config file created.')
    time.sleep(5)
    load_config()

def load_config():
    global config
    f = open('config.json', 'r').read()
    config = json.loads(f)
    if check_integrity() == False:
        print('Config file is corrupted... creating new file.')
        new_config()

def get_settings():
    load_config()
    return config

def save_settings(new_config):
    valid = check_integrity(new_config)
    if valid:
        # save settings
        f = open('config.json', 'w')
        f.write(json.dumps(conf))
        f.close()
        print('Saved successfully.')
        
def _init():
    # check for config file
    config_exists = os.path.exists('config.json')
    if config_exists:
        load_config()
    else:
        new_config()