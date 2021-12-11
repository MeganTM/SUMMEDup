# Function to fix errors and reformat the SUMup dataset
# This is designed to be used with the second release of the 2020 dataset, 'sumup_density_2020_v060121.nc'

# Import libraries
import xarray as xr
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from IPython.display import set_matplotlib_formats
import matplotlib.font_manager as font_manager
import matplotlib.ticker as mticker
import cartopy
import cartopy.crs as ccrs
from cartopy.mpl.geoaxes import GeoAxes
import cartopy.io.shapereader as shpreader
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import simplekml
from IPython.display import set_matplotlib_formats
import warnings
warnings.filterwarnings('ignore')

# Set plotting parameters
mpl.rcParams['font.size'] = 12
mpl.rcParams['mathtext.fontset'] = 'cm'
mpl.rcParams['mathtext.default'] = 'regular'
set_matplotlib_formats('svg')

# Choose pandas settings to avoid warnings
pd.options.mode.chained_assignment = None

def ReadNetcdf(file):

    sumup = xr.open_dataset(file)

    # Extract data and remove no data
    elev = sumup['Elevation'].values
    lat = sumup['Latitude'].values

    # Ignore any sea ice or erroneous data
    condition = (elev>0) & (lat>-91) & (lat<91)

    # Exctract data based on condition
    lon = sumup['Longitude'].values[condition]
    depth0 = sumup['Start_Depth'].values[condition]
    depth1 = sumup['Stop_Depth'].values[condition]
    midpoint = sumup['Midpoint'].values[condition]
    density = sumup['Density'].values[condition]
    citation = sumup['Citation'].values[condition]
    date = sumup['Date'].values[condition]
    method = sumup['Method'].values[condition]
    elev = elev[condition]
    lat = lat[condition]

    data = {'Citation':citation.astype(int),'Method':method.astype(int),'Timestamp':date,'Latitude':lat,'Longitude':lon,'Elevation':elev,
               'Midpoint':midpoint,'StartDepth':depth0,'StopDepth':depth1,'Density':density}

    df = pd.DataFrame(data=data)
    
    return df

def Reformat(df,save='no'):

    timestamp = []
    for i in range(len(df.Timestamp)):
        d = df.Timestamp[i]
        date_str = str(d)
        
        # These particular dates appear to be very incorrect
        if date_str == '19999000.0':
            date_str = '19990000.0'
        if date_str == '20089620.0':
            date_str = '20080620.0'
        
        year = date_str[0:4]
        month = date_str[4:6]
        day = date_str[6:8]
        
        # Add Jan 1 to year-only dates, and change any with 32 days to 31 days
        if month == '00':
            month = '01'
        if day == '00':
            day = '01'
        if day == '32':
            day = '31'
        
        d = float(year+month+day)
        timestamp.append(d)

    df['Timestamp'] = pd.to_datetime(timestamp,format='%Y%m%d')

    diff = df.diff()
    diff = diff[['Citation','Method','Latitude','Longitude','Midpoint','StopDepth']]

    rows = diff[(diff.Citation!=0)|(diff.Method!=0)|(diff.Latitude!=0)|(diff.Latitude!=0)|(diff.Midpoint<0)|(diff.StopDepth<0)]

    ids = rows.index[1:].values
    core_ids = np.arange(0,len(ids))

    last_check = 0
    dfs = []
    for ind in ids:
        dfs.append(df.loc[last_check:ind-1].reset_index(drop=True))
        last_check = ind

    df_list = sorted(dfs, key=lambda x:x['Latitude'].iloc[0])

    dfis = []
    for i in range(len(df_list)):

        dfi = df_list[i]
        
        dh0 = np.array(dfi.StopDepth) - np.array(dfi.StartDepth)

        midpoint = np.array(dfi.Midpoint)
        
        dh1 = midpoint[1:] - midpoint[:-1]
        dh1 = np.insert(dh1,0,midpoint[0])

        if dh0[0] == 0:
            dfi['Thickness'] = np.array(dh1)
        if dh0[0] != 0:
            dfi['Thickness'] = np.array(dh0)

        if midpoint[0] == -9999:
            mp = (np.array(dfi.StopDepth) + np.array(dfi.StartDepth)) / 2
            dfi['Midpoint'] = mp
        
        dfi = dfi[dfi.Thickness>0]
        dfi = dfi.reset_index(drop=True)
        
        dfi = dfi[['Citation','Method','Timestamp','Latitude','Longitude','Elevation',
                        'Midpoint','StartDepth','StopDepth','Thickness','Density']]
        
        if len(dfi) > 0:
            if dfi.Density[0] > 1:
                    
                density_kgm = dfi.Density/1000
                dfi['Density'] = density_kgm
            
            dfi['Density'] = dfi.Density*1000

            dfi = dfi.rename(columns={'Elevation':'Elevation (m)','Midpoint':'Midpoint (m)','StartDepth':'Start Depth (m)',
                                      'StopDepth':'Stop Depth (m)','Thickness':'Thickness (m)','Density':'Density (kg/m^-3)'})
            
            dfis.append(dfi)

    dfis2 = []
    for i in range(len(dfis)):
        dfi = dfis[i]
        a = np.zeros(len(dfi))
        id = a + i
        dfi.insert(0,'CoreID',id.astype(int))
        dfis2.append(dfi)

    df_new = pd.concat(dfis2)
    
    if save == 'yes':
        df_new.reset_index(drop=True).to_csv('output/SUMup_dataset.csv')

    return df_new.reset_index(drop=True)
    
    

def GetInfo(df,sort):
    
    dfs = []
    for i in range(len(np.unique(df.CoreID))):
    
        dfi = df[df.CoreID==i]
    
        id = np.array(dfi.CoreID)[0]
        cit = np.array(dfi.Citation)[0]
        method = np.array(dfi.Method)[0]
        timestamp = np.array(dfi.Timestamp)[0]
        lat = np.array(dfi.Latitude)[0]
        lon = np.array(dfi.Longitude)[0]
        elev = np.array(dfi['Elevation (m)'])[0]
        dmax = np.array(dfi['Midpoint (m)'])[-1]
    
        df_new = pd.DataFrame(data={'CoreID':id,'Citation':cit,'Method':method,'Timestamp':timestamp,'Latitude':lat,'Longitude':lon,'Elevation (m)':elev,'Core Depth (m)':dmax},
                              index=[0])
        dfs.append(df_new)
    
    df_unsorted = pd.concat(dfs).reset_index(drop=True)
    df_sorted = df_unsorted.sort_values(by=[sort]).reset_index(drop=True)
    
    return df_sorted
    


# Filter dataframe based on given conditions
def FilterPoints(df,icesheet='both',citation='all',method='all',
          startDate='1950-01-01',endDate='2020-12-31',
          minLat=-100,maxLat=100,minLon=-200,maxLon=200,
          minElev=0,maxElev=5000,minDepth=0,maxDepth=500):

    # Query by ice sheet
    if icesheet == 'Greenland':
        df = df[df.Latitude>0]
    if icesheet == 'Antarctica':
        df = df[df.Latitude<0]
    if icesheet == 'both':
        df = df

    # Query by citation
    if citation == 'all':
        df = df
    else:
        df = df[df.Citation==citation]

    # Query by method
    if method == 'all':
        df = df
    else:
        df = df[df.Method==method]
        
    # Query by date
    df = df[(df.Timestamp>=pd.to_datetime(startDate))&(df.Timestamp<=pd.to_datetime(endDate))]

    # Query by latitude
    df = df[(df.Latitude>=minLat)&(df.Latitude<=maxLat)]

    # Query by longitude
    df = df[(df.Longitude>=minLon)&(df.Longitude<=maxLon)]

    # Query by elevation
    df = df[(df['Elevation (m)']>=minElev)&(df['Elevation (m)']<=maxElev)]

    # Query by core depth
    df = df[(df['Core Depth (m)']>=minDepth)&(df['Core Depth (m)']<=maxDepth)]

    n = len(df)
    if n > 1:
        print(str(n) + ' entries match the given conditions')
    else:
        print(str(n) + ' entry matches the given conditions')
    return df
    
    
    
# Plot locations
def PlotLocs(df,color_by='r',color_map='none',save='no',**kwargs):
    
    vmin = kwargs.get('vmin', None)
    vmax = kwargs.get('vmax', None)
    
    # Create figure with white background
    fig = plt.figure(figsize=(10,5))
    fig.patch.set_facecolor('#FFFFFF')
    
    ### Antarctica ###
    
    # Create subplot
    ax1 = plt.subplot(1,2,1,projection=ccrs.SouthPolarStereo())
    ax1.set_extent([-180, 180, -90, -65], ccrs.PlateCarree())
    ax1.coastlines(resolution='50m',color='dimgray',zorder=0)
    ax1.set_title('Antarctica')
    
    # Plot grid lines
    grid1 = ax1.gridlines(crs=ccrs.PlateCarree(),draw_labels=True,
                          linewidth=0.5, color='lightgray',zorder=1)
    grid1.ylocator = mticker.FixedLocator([-80,-70,-60])
    grid1.top_labels = False
    grid1.xlabel_style = {'size':10}
    grid1.ylabel_style = {'size':10}
    
    # Plot locations
    AIS = ax1.scatter(df.Longitude,df.Latitude,
                      transform=ccrs.PlateCarree(),zorder=2,
                      c=color_by,
                      cmap=color_map,
                      vmin=vmin,vmax=vmax,
                      s=40,edgecolor='k',linewidth=0.5)
    
    ### Greenland ###
    
    # Create subplot
    ax2 = plt.subplot(1,2,2,projection=ccrs.NorthPolarStereo(central_longitude=-45))
    ax2.set_extent([-60, -28, 58, 85], ccrs.PlateCarree())
    ax2.coastlines(resolution='50m',color='dimgray',zorder=0)
    ax2.set_title('Greenland')
    
    # Plot grid lines
    grid2 = ax2.gridlines(crs=ccrs.PlateCarree(),draw_labels=True,
                          linewidth=0.5, color='lightgray',zorder=1,
                          y_inline=False)
    grid2.xlocator = mticker.FixedLocator([-30,-45,-60])
    grid2.ylocator = mticker.FixedLocator([60,70,80])
    grid2.top_labels = False
    grid2.right_labels = False
    grid2.xlabel_style = {'size':10}
    grid2.ylabel_style = {'size':10}
    
    # Plot locations
    GrIS = ax2.scatter(df.Longitude,df.Latitude,
                       transform=ccrs.PlateCarree(),zorder=2,
                       c=color_by,
                       cmap=color_map,
                       vmin=vmin,vmax=vmax,
                       s=40,edgecolor='k',linewidth=0.5)
    
    if color_map != 'none':
        # Create colorbar next to Greenland
        cbar = plt.colorbar(GrIS,shrink=0.75)
        cbar.set_label(color_by.name,fontsize=12)
    
    # Show figure with tight layout
    plt.tight_layout()
    
    if save == 'yes':
        plt.savefig('figures/SUMup_locations.png',dpi=500,bbox_inches='tight')
    
    
# Save locations as csv or kmz
def SavePoints(df,ftype,by_icesheet):

    img = pd.read_table('imgurURLs.txt',header=None)
    img = np.array(img)

    df = df.sort_values(by=['CoreID']).reset_index(drop=True)

    if by_icesheet == 'yes':
        df_AIS = df[df.Latitude<0]
        df_AIS = df_AIS.reset_index(drop=True)
        df_GrIS = df[df.Latitude>0]
        df_GrIS = df_GrIS.reset_index(drop=True)
        img_AIS = img[:887]
        img_GrIS = img[887:]

        if ftype == 'csv':
            df_AIS.to_csv('output/SUMupLocs_AIS.csv')
            df_GrIS.to_csv('output/SUMupLocs_GrIS.csv')

        if ftype == 'kmz':
            kml_AIS = simplekml.Kml()
            kml_AIS.parsetext(parse=False)
            for i in range(len(df_AIS)-1):
                pnt_AIS = kml_AIS.newpoint()
                pnt_AIS.name = 'Core {}'.format(df_AIS['CoreID'][i])
                pnt_AIS.coords = [(df_AIS['Longitude'][i],df_AIS['Latitude'][i])]
                pnt_AIS.description = '<img src='+str(img_AIS[i])[1:-1]+' width="250"/>'
                pnt_AIS.style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/shapes/snowflake_simple.png'
            kml_AIS.savekmz('output/SUMupLocs_AIS.kmz',format=False)
            

            kml_GrIS = simplekml.Kml()
            kml_GrIS.parsetext(parse=False)
            for i in range(len(df_GrIS)-1):
                pnt_GrIS = kml_GrIS.newpoint()
                pnt_GrIS.name = 'Core {}'.format(df_GrIS['CoreID'][i])
                pnt_GrIS.coords = [(df_GrIS['Longitude'][i],df_GrIS['Latitude'][i])]
                pnt_GrIS.description = '<img src='+str(img_GrIS[i])[1:-1]+' width="250"/>'
                pnt_GrIS.style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/shapes/snowflake_simple.png'
            kml_GrIS.savekmz('output/SUMupLocs_GrIS.kmz',format=False)

    if by_icesheet == 'no':
        
        if ftype == 'csv':
            df.to_csv('output/SUMupLocs.csv')

        if ftype == 'kmz':
            kml = simplekml.Kml()
            kml.parsetext(parse=False)
            for i in range(len(df)):
                pnt = kml.newpoint()
                pnt.name = 'Core {}'.format(df['CoreID'][i])
                pnt.coords = [(df['Longitude'][i],df['Latitude'][i])]
                pnt.description = '<img src='+str(img[i])[1:-1]+' width="250"/>'
                pnt.style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/shapes/snowflake_simple.png'
            kml.savekmz(path='output/SUMupLocs.kmz')       


# Plot density profiles
def PlotDensity(df,CoreID,color=['m','c','k','y','r','b'],save='no',compare='no'):

    n = len(CoreID)

    if compare == 'no':

        fig, ax = plt.subplots(1,n,figsize=(n*3.25,6))
        fig.patch.set_facecolor('#FFFFFF')

        for i in range(n):

            core = df[df['CoreID']==CoreID[i]]
            core = core.reset_index(drop=True)

            depth = np.array(core['Midpoint (m)'])
            startdepth = np.array(core['Start Depth (m)'])
            stopdepth = np.array(core['Stop Depth (m)'])
            density = np.array(core['Density (kg/m^-3)'])
            label = 'Core: {}\nCitation: {:.0f}\nLat: {:.2f}\nLon: {:.2f}\nElev: {:.0f} m\nDate: {}'.format(
                core['CoreID'][0],core['Citation'][0],core['Latitude'][0],core['Longitude'][0],
                core['Elevation (m)'][0],str(core['Timestamp'][0])[:10])
            
            if n > 1:
                ax[i].invert_yaxis()
                ax[i].set_ylabel('Depth (m)')
                ax[i].set_xlabel(r'Density (kg m$^{-3}$)')
                
                if startdepth[-1] == -9999:
                    ax[i].plot(density,depth,
                            color=color[0],marker='o',markersize=2,linewidth=1,
                            label=label)
                else:
                    ax[i].step(np.append(density,density[-1]),
                               np.append(startdepth,stopdepth[-1]),
                               color=color[0],linewidth=1,
                               label=label)

                legend = ax[i].legend(prop={'size':8}, bbox_to_anchor=(-0.0075,1.015), loc='lower left',borderpad=0.1,labelspacing=1.0)
                legend.get_frame().set_edgecolor('k')
                legend.get_frame().set_boxstyle('Square')

                if core['Latitude'][0] < 0:
                    ax_map = inset_axes(ax[i], width=0.85, height=0.85, bbox_to_anchor=(1,1.02),bbox_transform=ax[i].transAxes, 
                                        loc='lower right', borderpad=0,
                                        axes_class=cartopy.mpl.geoaxes.GeoAxes, 
                                        axes_kwargs=dict(map_projection=ccrs.SouthPolarStereo()))
                    ax_map.set_extent([-180, 180, -90, -65], ccrs.PlateCarree())
                else:
                    ax_map = inset_axes(ax[i], width=1, height=0.975, bbox_to_anchor=(1.065,1.02),bbox_transform=ax[i].transAxes, 
                                        loc='lower right', borderpad=0,
                                        axes_class=cartopy.mpl.geoaxes.GeoAxes, 
                                        axes_kwargs=dict(map_projection=ccrs.NorthPolarStereo(central_longitude=-45)))
                    ax_map.set_extent([-60, -28, 58, 85], ccrs.PlateCarree())

                ax_map.axes.xaxis.set_ticks([])
                ax_map.axes.yaxis.set_ticks([])
                ax_map.coastlines(resolution='110m',color='gray',zorder=0)

                ax_map.scatter(core['Longitude'][0],core['Latitude'][0],
                            transform=ccrs.PlateCarree(),
                            color=color[0],s=60,edgecolors='none',marker='*')

            if n == 1:
                ax.invert_yaxis()
                ax.set_ylabel('Depth (m)')
                ax.set_xlabel(r'Density (kg m$^{-3}$)')

                if startdepth[-1] == -9999:
                    ax.plot(density,depth,
                            color=color[0],marker='o',markersize=2,linewidth=1,
                            label=label)
                else:
                    ax.step(np.append(density,density[-1]),
                            np.append(startdepth,stopdepth[-1]),
                            color=color[0],linewidth=1,
                            label=label)
                
                legend = ax.legend(prop={'size':8}, bbox_to_anchor=(-0.0075,1.015), loc='lower left',borderpad=0.1,labelspacing=1.0)
                legend.get_frame().set_edgecolor('k')
                legend.get_frame().set_boxstyle('Square')

                if core['Latitude'][0] < 0:
                    ax_map = inset_axes(ax, width=0.8, height=0.8, bbox_to_anchor=(1,1.02),bbox_transform=ax.transAxes, 
                                        loc='lower right', borderpad=0,
                                        axes_class=cartopy.mpl.geoaxes.GeoAxes, 
                                        axes_kwargs=dict(map_projection=ccrs.SouthPolarStereo()))
                    ax_map.set_extent([-180, 180, -90, -65], ccrs.PlateCarree())
                else:
                    ax_map = inset_axes(ax, width=1, height=0.975, bbox_to_anchor=(1.065,1.02),bbox_transform=ax.transAxes, 
                                        loc='lower right', borderpad=0,
                                        axes_class=cartopy.mpl.geoaxes.GeoAxes, 
                                        axes_kwargs=dict(map_projection=ccrs.NorthPolarStereo(central_longitude=-45)))
                    ax_map.set_extent([-60, -28, 58, 85], ccrs.PlateCarree())

                ax_map.axes.xaxis.set_ticks([])
                ax_map.axes.yaxis.set_ticks([])
                ax_map.coastlines(resolution='110m',color='gray',zorder=0)

                ax_map.scatter(core['Longitude'][0],core['Latitude'][0],
                            transform=ccrs.PlateCarree(),
                            color=color[0],s=60,edgecolors='none',marker='*')
    if compare == 'yes':

        fig, ax = plt.subplots(1,1,figsize=(3.25,6))
        fig.patch.set_facecolor('#FFFFFF')
        ax.invert_yaxis()
        ax.set_ylabel('Depth (m)')
        ax.set_xlabel(r'Density (kg m$^{-3}$)')

        if np.array(df['Latitude'][df['CoreID']==CoreID[0]])[0] < 0:
            ax_map = inset_axes(ax, width=0.8, height=0.8, bbox_to_anchor=(1,1.02),bbox_transform=ax.transAxes, 
                                loc='lower right', borderpad=0,
                                axes_class=cartopy.mpl.geoaxes.GeoAxes, 
                                axes_kwargs=dict(map_projection=ccrs.SouthPolarStereo()))
            ax_map.set_extent([-180, 180, -90, -65], ccrs.PlateCarree())
        else:
            ax_map = inset_axes(ax, width=1, height=0.975, bbox_to_anchor=(1.065,1.02),bbox_transform=ax.transAxes, 
                                loc='lower right', borderpad=0,
                                axes_class=cartopy.mpl.geoaxes.GeoAxes,
                                axes_kwargs=dict(map_projection=ccrs.NorthPolarStereo(central_longitude=-45)))
            ax_map.set_extent([-60, -28, 58, 85], ccrs.PlateCarree())

        ax_map.axes.xaxis.set_ticks([])
        ax_map.axes.yaxis.set_ticks([])
        ax_map.coastlines(resolution='110m',color='gray',zorder=0)

        for i in range(n):
            
            core = df[df['CoreID']==CoreID[i]]
            core = core.reset_index(drop=True)

            depth = np.array(core['Midpoint (m)'])
            startdepth = np.array(core['Start Depth (m)'])
            stopdepth = np.array(core['Stop Depth (m)'])
            density = np.array(core['Density (kg/m^-3)'])

            if startdepth[-1] == -9999:
                ax.plot(density,depth,
                        color=color[i],marker='o',markersize=2,linewidth=1,
                        label='Core {}'.format(core['CoreID'][0]))
            else:
                ax.step(np.append(density,density[-1]),
                        np.append(startdepth,stopdepth[-1]),
                        color=color[i],linewidth=1,
                        label='Core {}'.format(core['CoreID'][0]))

            legend = ax.legend(prop={'size':8}, bbox_to_anchor=(-0.0075,1.015), loc='lower left',borderpad=0.1,labelspacing=1.0)
            legend.get_frame().set_edgecolor('k')
            legend.get_frame().set_boxstyle('Square')

            ax_map.scatter(core['Longitude'][0],core['Latitude'][0],
                           transform=ccrs.PlateCarree(),
                           color=color[i],s=60,edgecolors='none',marker='*')

    plt.tight_layout()

    if save == 'yes':
        core_str = str(CoreID)[1:-1]
        core_strs = core_str.replace(', ','_')
        plt.savefig('figures/DensityProfile{}.png'.format(core_strs),dpi=300,bbox_inches='tight')


