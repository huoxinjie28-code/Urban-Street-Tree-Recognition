# %%
import pandas as pd
import geopandas as gpd
import os.path as osp
import matplotlib.pyplot as plt
import contextily as ctx
import numpy as np
# import geoplot as gplt
from glob import glob
from matplotlib.patches import Patch
import rasterio
from rasterio.plot import show

plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 14
plt.rcParams['savefig.dpi'] = 1200


providers = ctx.providers.flatten()  # 调这个是调整地图的样式
# %% VIGOR
fig, ax = plt.subplots(figsize=(8, 8))

tree_categories_zhuhai = {
    "Others": 'r',
    "Palm":'g',
    "Banyan":'b',
    "Chittagong-chickrassy":'y',
    "Prunus-dulcis":'w'
}

tree_categories_seoul = {
    "Platanus": 'r',
    "Zelkova-Serrate": 'g',
    "Ginkgo-biloba": 'b',
    "Others": 'y'
}

tree_categories = tree_categories_seoul

fiLe_path = 'G://6.13//add//'
vigor_train = []
#打开文件以读取内容
with open(fiLe_path + 'result.txt', 'r') as file:
    lines = file.readlines()
    for line in lines:
        if line != '\n':
            parts = line.split(',')
            vigor_train.append([float(parts[2]), float(parts[1]), parts[4].replace('\n', '')])
vigor_train_df = pd.DataFrame(vigor_train, columns=['lon', 'lat', 'label'])

# 把数据转成geopandas
gdf = gpd.GeoDataFrame(
    vigor_train_df,
    geometry=gpd.points_from_xy(vigor_train_df['lon'], vigor_train_df['lat']))

gdf.crs = 'EPSG:4326'
gdf = gdf.to_crs(epsg=3857)

# 显示中心
center_x = (gdf.total_bounds[0] + gdf.total_bounds[2]) / 2
center_y = (gdf.total_bounds[1] + gdf.total_bounds[3]) / 2
# 显示范围
max_distance = max(
    np.max(np.abs(gdf.total_bounds[0] - center_x)),
    np.max(np.abs(gdf.total_bounds[2] - center_x)),
    np.max(np.abs(gdf.total_bounds[1] - center_y)),
    np.max(np.abs(gdf.total_bounds[3] - center_y))
)
display_margin = max_distance * 1.1
# 用geopandas的方法画图，这个好像和matplotlib差不多
legend_patches = []
for label, color in tree_categories.items():
    gdf[gdf['label'] == label].plot(
        ax=ax,
        alpha=1,
        color=color,
        marker='o',
        facecolor=color,
        edgecolor='none',
        markersize=3)
    legend_patches.append(Patch(color=color, label=label))

# 设置图像
ax.set_axis_off()
ax.set_xlim([center_x - display_margin, center_x + display_margin])
ax.set_ylim([center_y - display_margin, center_y + display_margin])
ax.legend(handles=legend_patches, title='Tree Type', loc='upper left')
# 增加底图
ctx.add_basemap(
    ax,
    source='https://d.basemaps.cartocdn.com/light_nolabels/{z}/{x}/{y}.png')


# # 读取 .tif 文件
# tif_file = fiLe_path + 'tif.tif'
# with rasterio.open(tif_file) as src:
#     tif_data = src.read(1)
#     tif_extent = (src.bounds.left, src.bounds.right, src.bounds.bottom, src.bounds.top)
#
#     gdf = gdf.to_crs(src.crs)
#     # 显示中心
#     center_x = (gdf.total_bounds[0] + gdf.total_bounds[2]) / 2
#     center_y = (gdf.total_bounds[1] + gdf.total_bounds[3]) / 2
#     # 显示范围
#     max_distance = max(
#         np.max(np.abs(gdf.total_bounds[0] - center_x)),
#         np.max(np.abs(gdf.total_bounds[2] - center_x)),
#         np.max(np.abs(gdf.total_bounds[1] - center_y)),
#         np.max(np.abs(gdf.total_bounds[3] - center_y))
#     )
#     display_margin = max_distance * 1.1
#     # 用geopandas的方法画图，这个好像和matplotlib差不多
#     legend_patches = []
#     for label, color in tree_categories.items():
#         gdf[gdf['label'] == label].plot(
#             ax=ax,
#             alpha=0.8,
#             color=color,
#             marker='o',
#             facecolor=color,
#             edgecolor='none',
#             markersize=0.7)
#         legend_patches.append(Patch(color=color, label=label))
#     # 设置图像
#     ax.set_axis_off()
#     ax.set_xlim([center_x - display_margin, center_x + display_margin])
#     ax.set_ylim([center_y - display_margin, center_y + display_margin])
#     ax.legend(handles=legend_patches, title='Tree Type', loc='upper left')
#     # 绘制 .tif 底图
#     show(src, ax=ax, extent=tif_extent, cmap='gray')

data_root = fiLe_path + 'picture'
plt.savefig(
    osp.join(data_root, 'seoul.png')
)

