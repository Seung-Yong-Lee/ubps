#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#10주차


# In[3]:


import geopandas as gpd
from shapely.geometry import Point
import folium
from IPython.display import IFrame
import pandas as pd

# 데이터 프레임 생성
data = pd.DataFrame({
    'City': ['여의도', '여의나루', '국회의사당', '샛강'],
    'Latitude': [37.52158, 37.52715, 37.52811, 37.51706062],
    'Longitude': [126.9243, 126.9328, 126.9179, 126.9289]

})

# 데이터 프레임을 GeoDataFrame으로 변환
geometry = [Point(xy) for xy in zip(data['Longitude'], data['Latitude'])]
gdf = gpd.GeoDataFrame(data, geometry=geometry, crs='epsg:4326')

# 여의도의 중심 좌표를 사용하여 지도 초기화
center = [37.52158, 126.9243]
m = folium.Map(location=center, zoom_start=15)

# GeoDataFrame의 지점을 지도에 추가
for idx, row in gdf.iterrows():
    folium.Marker([row['Latitude'], row['Longitude']], popup=row['City']).add_to(m)

# 좌표계를 EPSG:4326(WGS84)로 변환
gdf = gdf.to_crs('epsg:4326')  

# GeoDataFrame에 버퍼 열 추가 (단위: 미터)
buffer_distance_meters = 0.003
gdf['Buffer'] = gdf['geometry'].buffer(buffer_distance_meters)

# GeoDataFrame의 버퍼를 지도에 추가
for idx, row in gdf.iterrows():
    # 색상을 빨간색으로 지정
    folium.GeoJson(row['Buffer'].__geo_interface__,
                   style_function=lambda x: {'fillColor': 'red'}).add_to(m)

# Save the map as an HTML file
html_file_path = 'map_with_red_buffer.html'
m.save(html_file_path)

# Display the HTML file in the notebook using IFrame
IFrame(html_file_path, width=800, height=500)


# In[1]:


import pandas as pd
import pydeck as pdk

data = {
    'X': [126.9139175, 126.9213333, 126.92453, 126.9187012, 126.9170227, 126.9205093, 126.9180222, 126.9319, 126.9278336, 126.9189529, 126.9208374, 126.934906, 126.9303665, 126.9258347, 126.9260483, 126.9377899, 126.9375992, 126.9333725, 126.9323654, 126.9296188, 126.9284134, 126.9242096, 126.9361191, 126.9121628, 126.9271011, 126.9216156, 126.912674, 126.914299, 126.9224548, 126.9344864, 126.9396591, 126.9140472, 126.9131699, 126.9128952, 126.9181747, 126.9174728, 126.9151077, 126.9179916, 126.9271164, 126.9230118, 126.9240799, 126.9234238, 126.9304581],
    'Y': [37.52841568, 37.53123856, 37.52881622, 37.5280571, 37.52816391, 37.52626419, 37.52466583, 37.52715683, 37.52461243, 37.52190781, 37.5230217, 37.52483749, 37.52207947, 37.52069473, 37.5193634, 37.52267456, 37.51943588, 37.51913071, 37.5200882, 37.51758575, 37.51776505, 37.53105545, 37.52434921, 37.53365707, 37.52234268, 37.51896286, 37.52863693, 37.52750778, 37.53179169, 37.51850891, 37.52070999, 37.5325737, 37.52974701, 37.53050232, 37.53054047, 37.53214645, 37.52864075, 37.53271866, 37.52347946, 37.52260971, 37.52508926, 37.52464294, 37.52539444],
    '이용합계': [162, 1763, 5103, 2862, 1368, 2226, 3362, 9469, 3534, 3159, 2018, 1426, 4156, 3192, 2035, 1828, 4318, 1426, 2591, 2510, 3019, 1217, 2614, 669, 2402, 633, 239, 776, 372, 996, 3031, 606, 663, 416, 583, 386, 225, 317, 1011, 1697, 5638, 1810, 1980],
    '대여건수': [89, 883, 2550, 1434, 687, 1112, 1805, 4947, 1691, 1825, 1046, 696, 2075, 1593, 1080, 927, 2059, 768, 1305, 1360, 1655, 609, 1269, 346, 1207, 380, 122, 488, 185, 506, 1469, 354, 331, 208, 324, 227, 132, 163, 507, 858, 2789, 903, 985],
    '반납건수': [73, 880, 2553, 1428, 681, 1114, 1557, 4522, 1843, 1334, 972, 730, 2081, 1599, 955, 901, 2259, 658, 1286, 1150, 1364, 608, 1345, 323, 1195, 253, 117, 288, 187, 490, 1562, 252, 332, 208, 259, 159, 93, 154, 504, 839, 2849, 907, 995]
}

df = pd.DataFrame(data)

# PyDeck HexagonLayer with '반납건수' as weight
layer = pdk.Layer(
    'HexagonLayer',
    data=df,
    get_position='[X, Y]',
    get_weight='반납건수',  # Using '반납건수' as weight
    elevation_scale=10,
    radius=275,
    extruded=True,
    coverage=1,
    opacity=0.9,
    color_range=[[255, 255, 178], [254, 204, 92], [253, 141, 60]], 
    
   # get_fill_color='[[255, 0, 0, 150,], [255, 255, 178], [254, 204, 92], [253, 141, 60], [240, 59, 32]]',  # Red color with alpha
)
   #  color_range=[[255, 255, 178], [254, 204, 92], [253, 141, 60], [240, 59, 32]],# Set the viewport

# Set the viewport
view_state = pdk.ViewState(
    latitude=df['Y'].mean(),
    longitude=df['X'].mean(),
    zoom=10,
    pitch=25,
    bearing=-25
)

# Create a PyDeck deck
deck = pdk.Deck(layers=[layer], initial_view_state=view_state)

# Show the deck
deck.to_html('weighted_map_return_count_pydeck.html', iframe_width=800, iframe_height=500)

