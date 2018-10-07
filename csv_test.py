import csv

headers_zh = ['地址', '纬度', '经度', '本月均价', '物业类型', '物业费', '总建筑面积', '总户数', '建造年代', '停车位',
              '容  积  率', '绿化率', '开  发  商', '物业公司', '出售房源', '出租房源', '地区价格', '小区价格']
headers_en = ['address', 'lat', 'lng', 'average', 'style', 'property_costs', 'total_area', 'households', 'age', 'park',
              'volume_ratio', 'green_ratio', 'developer', 'property', 'for_sales', 'for_rent', 'area_price', 'community_price']
receive_data = {
    'address' : '',
    'lat' : '',
    'lng' : '',
    'average' : '',
    'style' : '',
    'property_costs' : '',
    'total_area' : '',
    'households' : '',
    'age' : '',
    'park' : '',
    'volume_ratio' : '',
    'green_ratio' : '',
    'developer' : '',
    'property' : '',
    'for_sales' : '',
    'for_rent' : '',
    'area_price' : '',
    'community_price' : ''
}

with open("anjuk_data.csv", "a+", newline='') as aj_data:
    norm_writer = csv.writer(aj_data)
    dic_writer = csv.DictWriter(aj_data, headers_en)
    receive_data['address'] = '渝北-金州-湖红路365号'
    receive_data['average'] = '18842'
    receive_data['for_sales'] = '1733'
    dic_writer.writeheader()
    dic_writer.writerow(receive_data)
    dic_writer.writerow(receive_data)
