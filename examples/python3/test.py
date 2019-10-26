# -*- coding: utf-8 -*-

from examples.python3.dragonex import DragonExV1

ACCESS_KEY = '135ccedad9885ddbb2482b17770dac41'
SECRET_KEY = 'f3224b9139915e7f93535c6c161a102b'

HOST = 'https://openapi.dragonex.io'

if __name__ == '__main__':
    dragonex = DragonExV1(access_key=ACCESS_KEY, secret_key=SECRET_KEY, host=HOST)
    dragonex.ensure_token_enable(False)
    r = dragonex.get_user_own_coins()
    print(r.data, "")