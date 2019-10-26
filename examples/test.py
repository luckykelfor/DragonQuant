# -*- coding: utf-8 -*-

from examples.python3.dragonex import DragonExV1
import time

ACCESS_KEY = '135ccedad9885ddbb2482b17770dac41'
SECRET_KEY = 'f3224b9139915e7f93535c6c161a102b'

HOST = 'https://openapi.dragonex.io'
def get_symbol_map(dragonex):
    r = dragonex.get_all_symbos()
    symbol_map = {}
    for ele in r.data:
        symbol_map[ele['symbol']]  = ele['symbol_id']
    return symbol_map

def get_volum(dragonex, check_type, code):
    r = dragonex.get_user_own_coins()
    volum_map = {}
    if check_type == 'available':
        for ele in r.data:
            volum_map[ele['code']] = ele['volume'] - ele['frozen']
    elif check_type == 'frozen':
        for ele in r.data:
            volum_map[ele['code']] = ele['frozen']
    return volum_map[code]


if __name__ == '__main__':
    dragonex = DragonExV1(access_key=ACCESS_KEY, secret_key=SECRET_KEY, host=HOST)
    print("初始化成功")
    dragonex.ensure_token_enable(False)
    print("获取token成功")
    r = dragonex.get_user_own_coins()
    # for i in r.data:
    #     for key in i:
    #         if key == 'code' and i[key] in ['dt', 'ae', 'abt']:
    #             print(i)
    symbol_map = get_symbol_map(dragonex)
    print("获取货币列表成功")

    time.sleep(5)

    
    initial_price_hold = float(dragonex.get_market_real(symbol_map["abt_usdt"]).data[0]['close_price'])
    print("获取初始价格为:", initial_price_hold)

    new_check_price = initial_price_hold
    income = 0.0
    cnt = 1
    while True:
        print("开始准备第",cnt,"次交易")
        check_cnt = 1
        # if get_volum(dragonex, "available", "abt") > 1.0:
        while (new_check_price - initial_price_hold) / initial_price_hold < 0.03 and (new_check_price - initial_price_hold) / initial_price_hold > -0.04:
            # buy_market = dragonex.get_market_buy(symbol_map["abt_usdt"])
            time.sleep(3)
            new_check_price = float(dragonex.get_market_real(symbol_map["abt_usdt"]).data[0]['close_price'])
            print("第", check_cnt,"次查询价格为:", new_check_price)
            time.sleep(5)
            check_cnt += 1

        print("准备交易")
        available_volum = get_volum(dragonex, 'available', 'abt')
        print("可用货币数量为:", available_volum)
        time.sleep(2)

        if available_volum > 1.0:
            print("挂交易卖单 价格:", new_check_price, " 数量:", available_volum)
            dragonex.add_order_sell(symbol_map['abt_usdt'], new_check_price, available_volum)
            time.sleep(2)
            print("开始检查是否交易成功")
            check_deal_cnt = 1
            while get_volum(dragonex, 'frozen', 'abt') > 0.01:
                    print("第", check_deal_cnt,"次检查交易是否成功")
                    time.sleep(2)
                    check_deal_cnt += 1
            print("第",cnt,"次交易成功, 初始价格/卖出价格 = ", initial_price_hold ,"/", new_check_price)
        


            income = new_check_price * available_volum
            print("获得ustd:", income)
            initial_price_hold = new_check_price

            cnt += 1

        elif new_check_price < initial_price_hold and available_volum < 1.0 and income > 1.0:
            buy_volume = income / new_check_price - 0.1
            print("挂交易买单，价格:", new_check_price, " 买入金额:", income, "买入数量:", buy_volume)
            dragonex.add_order_sell(symbol_map['abt_usdt'], new_check_price, buy_volume)
            check_deal_cnt = 1
            while get_volum(dragonex, "available", "abt") < 1.0:
                print("第",check_deal_cnt,"次检查交易是否成功")
                time.sleep(2)
                check_deal_cnt += 1

            print("第", cnt, "次交易成功, 初始价格/买入价格 = ", initial_price_hold, new_check_price)
            initial_price_hold = new_check_price
            cnt += 1


        else:
            initial_price_hold = new_check_price
        








    print(buy_market.data)
