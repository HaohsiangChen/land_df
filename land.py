import pandas as pd

df_a = pd.read_csv('data/a_lvr_land_a.csv')
df_b = pd.read_csv('data/b_lvr_land_a.csv')
df_e = pd.read_csv('data/e_lvr_land_a.csv')
df_f = pd.read_csv('data/f_lvr_land_a.csv')
df_h = pd.read_csv('data/h_lvr_land_a.csv')

df_all = pd.concat([df_a[1:], df_b[1:], df_e[1:], df_f[1:], df_h[1:]])


def chinese_to_arabic(cn):
    cn_num = {
        '〇': 0, '一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9, '零': 0,
        '壹': 1, '贰': 2, '叁': 3, '肆': 4, '伍': 5, '陆': 6, '柒': 7, '捌': 8, '玖': 9, '貮': 2, '两': 2,
    }

    cn_unit = {
        '十': 10,
        '拾': 10,
        '百': 100,
        '佰': 100,
        '千': 1000,
        '仟': 1000,
        '万': 10000,
        '萬': 10000,
        '亿': 100000000,
        '億': 100000000,
        '兆': 1000000000000,
    }
    unit = 0   # current
    ldig = []  # digest
    for cndig in reversed(cn):
        if cndig in cn_unit:
            unit = cn_unit.get(cndig)
            if unit == 10000 or unit == 100000000:
                ldig.append(unit)
                unit = 1
        else:
            dig = cn_num.get(cndig)
            if unit:
                dig *= unit
                unit = 0
            ldig.append(dig)
    if unit == 10:
        ldig.append(10)
    val, tmp = 0, 0
    for x in reversed(ldig):
        if x == 10000 or x == 100000000:
            val += tmp * x
            tmp = 0
        else:
            tmp += x
    val += tmp
    return val

# Q1 filter_a.csv
df_all['總樓層數'].fillna('零層', inplace=True)
floor = df_all['總樓層數'].str.slice(stop=-1).map(chinese_to_arabic)
res = df_all[(df_all['主要用途'].str.contains('住家用')) & (df_all['建物型態'].str.contains("住宅大樓")) & (floor > 12)]

res.to_csv('filter_a.csv', index=False)

# Q1 filter_b.csv
total_number = len(df_all.index)
parking_number = df_all['交易筆棟數'].str.slice(start=-1).astype(int).sum()
total_price_mean = df_all['總價元'].astype(int).mean()
parking_price_mean = df_all['車位總價元'].astype(int).sum()/parking_number

res_2 = [(total_number, parking_number, total_price_mean, parking_price_mean)]
res_df_2 = pd.DataFrame(res_2, columns=['總件數', '總車位數', '平均總價元', '平均車位總價元'])

res_df_2.to_csv('filter_b.csv', index=False)