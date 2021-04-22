#!/usr/bin/env python
# coding: utf-8

# In[2]:


import numpy as np
import pandas as pd
import cartopy
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from cartopy.mpl.geoaxes import GeoAxes
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from mpl_toolkits.axes_grid1 import AxesGrid
import seaborn as sns 
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


# In[3]:


data=pd.read_csv('../../US/data/data_whole_add_ndvipeak.csv')
real=data[data['wf_end_builit_year0.95']<2018][data['wf_end_builit_year0.95']>0]

ndvi_peak=real['ndvi_peak_trend_8_10']
ndvi_peak
ndvi_peak_str='mean='+str(round(ndvi_peak.mean(),4)*10000*10)


# In[17]:



sns.set_palette("hls") #设置所有图的颜色，使用hls色彩空间
lons=real['xlong']
lats=real['ylat']
# make plot
projection = ccrs.PlateCarree()
axes_class = (GeoAxes,
              dict(map_projection=projection))

fig = plt.figure(figsize=(18, 12))

grid = AxesGrid(fig, 111, axes_class=axes_class,
                 nrows_ncols=(1, 1),
                 axes_pad=0.6,  # pad between axes in inch.

                 cbar_location='right',
                 cbar_mode='single',
                 cbar_pad=0.2,
                 cbar_size='2%',
                 share_all=True,
                 label_mode=" ")


def add_map_lines(ax):
    ax.coastlines(resolution='50m', lw=0.6)
    ax.add_feature(cartopy.feature.LAKES, edgecolor='k', facecolor='w', lw=0.6)
    ax.add_feature(cfeature.BORDERS.with_scale('50m'))
    ax.add_feature(cfeature.STATES.with_scale('50m'),lw=0.3,zorder=2)
    ax.set_extent([-130, -60, 24, 45], ccrs.Geodetic())
    ax.set_xticks(np.linspace(-130,-60, 3), crs=projection)
    ax.set_yticks(np.linspace(25, 45, 3), crs=projection)
    lon_formatter = LongitudeFormatter(zero_direction_label=True)
    lat_formatter = LatitudeFormatter()
    ax.xaxis.set_major_formatter(lon_formatter)
    ax.yaxis.set_major_formatter(lat_formatter)

    

p = grid[0].scatter(lons, lats, 
               c=ndvi_peak*10000*10,
#               s=background_info['p_cap'],
               vmin=-600,
               vmax=600,
                transform=projection,
                cmap='bwr',
                zorder=10)
add_map_lines(grid[0])
#grid[0].text(-0.07, 1.03, 'a', fontsize=20, transform=grid[0].transAxes, fontweight='bold')
#grid[0].set_title(r"JJA NDVI",fontsize=20)

#add kde plot
ax1 = grid[0].inset_axes([0.78,0.15,0.2,0.3],transform=grid[0].transAxes)
sns.distplot(ndvi_peak*10000*10,color="g",bins=50,ax=ax1)
ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
ax1.spines['left'].set_visible(False)
ax1.yaxis.set_visible(False)
ax1.set_xlim(-2000,2000)
ax1.set_xlabel('Distribution')
ax1.text(0.65,0.7,ndvi_peak_str,fontsize=10,transform=ax1.transAxes)


cb = grid.cbar_axes[0].colorbar(p,ticks=np.arange(-800, 1000 ,150))
cb.ax.tick_params(axis='y',direction='in')
cb.set_label_text(r'$\theta$NDVI',fontsize=24)

#plt.savefig('/mnt/e/US/figure/fig4.effects_on_peak_ndvi.jpg',dpi=300)
plt.show()

