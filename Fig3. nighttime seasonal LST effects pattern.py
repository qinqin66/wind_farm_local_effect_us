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

night_jja=real.iloc[:,173:176].mean(1)*10
night_djf=pd.concat([real.iloc[:,179:180],real.iloc[:,168:170]],axis=1).mean(1)*10
night_mam=real.iloc[:,170:173].mean(1)*10
night_son=real.iloc[:,176:179].mean(1)*10

night_mam_str='mean='+str(round(night_mam.mean(),2))
night_jja_str='mean='+str(round(night_jja.mean(),2))
night_son_str='mean='+str(round(night_son.mean(),2))
night_djf_str='mean='+str(round(night_djf.mean(),2))


# In[4]:





sns.set_palette("hls") #设置所有图的颜色，使用hls色彩空间
lons=real['xlong']
lats=real['ylat']
# make plot
projection = ccrs.PlateCarree()
axes_class = (GeoAxes,
              dict(map_projection=projection))

fig = plt.figure(figsize=(18, 12))

grid = AxesGrid(fig, 111, axes_class=axes_class,
                 nrows_ncols=(2, 2),
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
    ax.add_feature(cfeature.STATES.with_scale('50m'),zorder=2)
    ax.set_extent([-130, -60, 24, 45], ccrs.Geodetic())
    ax.set_xticks(np.linspace(-130,-60, 3), crs=projection)
    ax.set_yticks(np.linspace(25, 45, 3), crs=projection)
    lon_formatter = LongitudeFormatter(zero_direction_label=True)
    lat_formatter = LatitudeFormatter()
    ax.xaxis.set_major_formatter(lon_formatter)
    ax.yaxis.set_major_formatter(lat_formatter)

    
    
#day mam
p = grid[0].scatter(lons, lats, 
               c=night_mam,
               s=18,
               vmin=-2,
               vmax=2,
                transform=projection,
                cmap='bwr',
                zorder=10)
#                cbar_kwargs=cbar_kwargs)  
add_map_lines(grid[0])
grid[0].text(-0.07, 1.03, 'a', fontsize=20, transform=grid[0].transAxes, fontweight='bold')
grid[0].set_title(r"MAM",fontsize=20)

#add kde plot
ax1 = grid[0].inset_axes([0.78,0.15,0.2,0.3],transform=grid[0].transAxes)
sns.distplot(night_mam,color="g",bins=30,ax=ax1)
#ax1.set_xlabel('')
ax1.set_xlabel('Distribution')

ax1.spines['top'].set_visible(False)
ax1.spines['right'].set_visible(False)
#ax1.spines['bottom'].set_visible(False)
ax1.spines['left'].set_visible(False)
ax1.set_xlim(-5,5)
ax1.text(0.6,0.7,night_mam_str,fontsize=8,transform=ax1.transAxes)
#ax1.text(-3,1.2,'>0: 50.2%')
#ax1.set_title('day')






#night
p2 = grid[1].scatter(lons, lats, 
               c=night_jja,
               s=18,
               vmin=-2,
               vmax=2,
                transform=projection,
                cmap='bwr',
                zorder=10)
#                cbar_kwargs=cbar_kwargs)  
add_map_lines(grid[1])
grid[1].text(-0.07, 1.03, 'b', fontsize=20, transform=grid[1].transAxes, fontweight='bold')
grid[1].set_title(r"JJA",fontsize=20)

ax2 = grid[1].inset_axes([0.78,0.15,0.2,0.3],transform=grid[1].transAxes)
sns.distplot(night_jja,color="g",bins=30,ax=ax2)
#ax1.set_xlabel('')
ax2.set_xlabel('Distribution')
ax2.yaxis.set_visible(False)
ax2.spines['top'].set_visible(False)
ax2.spines['right'].set_visible(False)
#ax2.spines['bottom'].set_visible(False)
ax2.spines['left'].set_visible(False)
ax2.set_xlim(-5,5)
ax2.text(0.6,0.7,night_jja_str,fontsize=8,transform=ax2.transAxes)
#ax2 = fig.add_axes([left, bottom, width, height])
#sns.distplot(night_annual,color="r",bins=30,kde=True)
#ax2.set_xlabel('LST changed')
#ax2.set_ylabel('Counts')
#ax2.set_title('night')
#ax2.text(-1,2.5,'mean=0.02')
#ax2.text(-1,2.0,'>0: 63.3%')
#plt.tight_layout()
plt.subplots_adjust(left=0.05, right=0.9)
#plt.savefig('1.annual_lst_changed.jpg',dpi=300)

#day son
p2 = grid[2].scatter(lons, lats, 
               c=night_son,
               s=18,
               vmin=-2,
               vmax=2,
                transform=projection,
                cmap='bwr',
                zorder=10)
#                cbar_kwargs=cbar_kwargs)  
add_map_lines(grid[2])
grid[2].text(-0.07, 1.03, 'c', fontsize=20, transform=grid[2].transAxes, fontweight='bold')
grid[2].set_title(r"SON",fontsize=20)

ax3 = grid[2].inset_axes([0.78,0.15,0.2,0.3],transform=grid[2].transAxes)
sns.distplot(night_son,color="g",bins=30,ax=ax3)
#ax1.set_xlabel('')
ax3.set_xlabel('Distribution')
ax3.yaxis.set_visible(False)
ax3.spines['top'].set_visible(False)
ax3.spines['right'].set_visible(False)
#ax3.spines['bottom'].set_visible(False)
ax3.spines['left'].set_visible(False)
ax3.set_xlim(-5,5)
ax3.text(0.6,0.7,night_son_str,fontsize=8,transform=ax3.transAxes)
#ax2 = fig.add_axes([left, bottom, width, height])
#sns.distplot(night_annual,color="r",bins=30,kde=True)
#ax2.set_xlabel('LST changed')
#ax2.set_ylabel('Counts')
#ax2.set_title('night')
#ax2.text(-1,2.5,'mean=0.02')
#ax2.text(-1,2.0,'>0: 63.3%')
#plt.tight_layout()
plt.subplots_adjust(left=0.05, right=0.9)
#plt.savefig('1.annual_lst_changed.jpg',dpi=300)

#day djf
p3 = grid[3].scatter(lons, lats, 
               c=night_djf,
               s=18,
               vmin=-2,
               vmax=2,
                transform=projection,
                cmap='bwr',
                zorder=10)
#                cbar_kwargs=cbar_kwargs)  
add_map_lines(grid[3])
grid[3].text(-0.07, 1.03, 'd', fontsize=20, transform=grid[3].transAxes, fontweight='bold')
grid[3].set_title(r"DJF",fontsize=20)

ax4 = grid[3].inset_axes([0.78,0.15,0.2,0.3],transform=grid[3].transAxes)
sns.distplot(night_djf,color="g",bins=30,ax=ax4)
#ax1.set_xlabel('')
ax4.set_xlabel('Distribution')
ax4.yaxis.set_visible(False)
ax4.spines['top'].set_visible(False)
ax4.spines['right'].set_visible(False)
#ax4.spines['bottom'].set_visible(False)
ax4.spines['left'].set_visible(False)
ax4.set_xlim(-5,5)
ax4.text(0.60,0.7,night_djf_str,fontsize=8,transform=ax4.transAxes)
#ax2 = fig.add_axes([left, bottom, width, height])
#sns.distplot(night_annual,color="r",bins=30,kde=True)
#ax2.set_xlabel('LST changed')
#ax2.set_ylabel('Counts')
#ax2.set_title('night')
#ax2.text(-1,2.5,'mean=0.02')
#ax2.text(-1,2.0,'>0: 63.3%')
#plt.tight_layout()
plt.subplots_adjust(left=0.05, right=0.9)
#plt.savefig('1.annual_lst_changed.jpg',dpi=300)


#lgend = ax1.legend()
cb = grid.cbar_axes[0].colorbar(p,ticks=np.arange(-3, 3, 0.5))
cb.ax.tick_params(axis='y', direction='in')
cb.set_label_text(r'Nighttime $\theta$LST(℃)',fontsize=24)


#plt.savefig('/mnt/e/US/figure/fig3.nighttime lst trend.jpg',dpi=300)
plt.show()

