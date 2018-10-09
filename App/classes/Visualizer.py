import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib

def makeLineMap(line):
  line_plot = gpd.GeoSeries(line)
  line_plot = line_plot.plot(figsize=(24, 24), color="white")
  line_plot.set_facecolor("#111111")
  line_plot.spines['bottom'].set_color("white")
  line_plot.spines['left'].set_color("white")
  line_plot.xaxis.label.set_color('white')
  line_plot.tick_params(axis='x', colors='white')
  line_plot.yaxis.label.set_color('white')
  line_plot.tick_params(axis='y', colors='white')
  line_plot.set_xlabel('Longitude')
  line_plot.set_ylabel('Latitude')
  return line_plot

def assignColorsToTrains(train_ids):
  vals = np.linspace(0,1,len(train_ids))
  np.random.shuffle(vals)
  colors = plt.cm.colors.ListedColormap(plt.cm.jet(vals))
  return {train_ids[index]: colors(index) for index in range(len(train_ids))}

def makeMarey(stations, vehicles, colors, time_min, time_max):
  plt.style.use('dark_background')
  fig = plt.figure(figsize=[60,48])
  ax1 = fig.add_subplot(121)
  format_time_axis(ax1, time_min, time_max)
  format_location_axis(ax1)
  
  for index, vehicle in vehicles:
    times = vehicle['datetime']
    distances = vehicle['relative_position'].values
    nans = np.where(np.abs(np.diff(distances)) >= 0.2)[0]
    distances[nans] = np.nan
    ax1.plot(distances, times, lw=2, color=colors[index])

  for index, row in stations.iterrows():
    ax1.axvline(row['relative_position'], color='#555555', lw=1, linestyle='-.')
    ax1.text(row['relative_position'], time_min, row['display_name'] + '  ', fontSize='18', color='#999999', rotation='vertical', horizontalalignment='center', verticalalignment='top')
  

def format_time_axis(axis, time_min, time_max):
  time_interval = matplotlib.dates.MinuteLocator(byminute=None, interval=5, tz=None)
  interval_format = matplotlib.dates.DateFormatter('%H:%M')
  axis.set_ylim(time_min, time_max)
  axis.yaxis.set_major_locator(time_interval)
  axis.yaxis.set_major_formatter(interval_format)
  axis.set_xlim(0, 1)

def format_location_axis(axis):
  axis.set_xticks([])