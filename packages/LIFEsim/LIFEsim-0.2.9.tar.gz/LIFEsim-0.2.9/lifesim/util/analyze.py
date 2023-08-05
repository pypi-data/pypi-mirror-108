import lifesim as ls
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
import numpy as np


def log_hist(x, y, x_lim, y_lim, bins):
    xmin = np.log10(x_lim[0])
    xmax = np.log10(x_lim[1])
    ymin = np.log10(y_lim[0])
    ymax = np.log10(y_lim[1])

    xbins = np.logspace(xmin, xmax, bins)  # <- make a range from 10**xmin to 10**xmax
    ybins = np.logspace(ymin, ymax, bins)  # <- make a range from 10**ymin to 10**ymax

    counts, _, _ = np.histogram2d(x, y, bins=(xbins, ybins))

    return xbins, ybins, counts


def norm_hist(x, y, x_lim, y_lim, bins):
    xmin = x_lim[0]
    xmax = x_lim[1]
    ymin = y_lim[0]
    ymax = y_lim[1]

    xbins = np.linspace(xmin, xmax, bins)  # <- make a range from 10**xmin to 10**xmax
    ybins = np.linspace(ymin, ymax, bins)  # <- make a range from 10**ymin to 10**ymax

    counts, _, _ = np.histogram2d(x, y, bins=(xbins, ybins))

    return xbins, ybins, counts

matplotlib.use('Qt5Agg')

bus = ls.Bus()

bus.data.import_catalog(input_path='/home/felix/Documents/MA/Outputs/LIFEsim_development/'
                                    'Clean_AHGS_hab.hdf5')

bus.data.catalog['l_sun'] = bus.data.catalog.radius_s ** 2 * (bus.data.catalog.temp_s / 5780) ** 4
bus.data.catalog['insolation'] = bus.data.catalog.l_sun / (bus.data.catalog.semimajor_p ** 2)
#
all = bus.data.catalog
det = bus.data.catalog.loc[bus.data.catalog.detected]

# sns.histplot(data=det, x='insolation', y='radius_p', log_scale=(True, True), bins=20)

# sns.histplot(data=all, x='insolation', y='radius_p', hue='detected', log_scale=(True, True), bins=20)
# plt.show()

# ---------- Radius Vs Insolation ---------------

y_lim = [np.min(np.concatenate((det.radius_p.to_numpy(), all.radius_p.to_numpy()))),
         np.max(np.concatenate((det.radius_p.to_numpy(), all.radius_p.to_numpy())))]
x_lim = [np.min(np.concatenate((det.insolation.to_numpy(), all.insolation.to_numpy()))),
         np.max(np.concatenate((det.insolation.to_numpy(), all.insolation.to_numpy())))]

bins = 30

xb_all, yb_all, c_all = log_hist(all.insolation, all.radius_p, x_lim, y_lim, bins)
xb_det, yb_det, c_det = log_hist(det.insolation, det.radius_p, x_lim, y_lim, bins)

if not (np.array_equal(xb_all, xb_det) and np.array_equal(yb_all, yb_det)):
    raise ValueError('blah')

fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2)

pcm = ax1.pcolormesh(xb_all, yb_all, np.nan_to_num(c_det/c_all).T)
plt.colorbar(pcm, ax=ax1)
#fig.colorbar(pcm, ax=ax2)  # this works too

## The following line doesn't actually work...
## See http://stackoverflow.com/questions/29175093/creating-a-log-linear-plot-in-matplotlib-using-hist2d
#H = ax2.hist2d(x, y, bins=[xbins, ybins])
#fig.colorbar(H[3], ax=ax2)

ax1.set_xscale('log')               # <- Activate log scale on X axis
ax1.set_yscale('log')               # <- Activate log scale on Y axis

ax1.set_xlim(xmin=xb_all[0])
ax1.set_xlim(xmax=xb_all[-1])
ax1.set_ylim(ymin=yb_all[0])
ax1.set_ylim(ymax=yb_all[-1])

# ---------- Distance Vs Stellar Temp ---------------

# bus2 = ls.Bus()
# bus2.data.options.set_scenario('baseline')
# bus2.data.catalog_from_ppop(input_path='/home/felix/Documents/MA/lifeOS/Data/baselineSample.fits')
# bus2.data.catalog_remove_distance(stype=4, mode='larger', dist=10.)

# _, ind = np.unique(bus2.data.catalog.nstar, return_index=True)
#
# all = bus2.data.catalog.iloc[ind]

y_lim = [np.min(np.concatenate((det.distance_s.to_numpy(), all.distance_s.to_numpy()))),
         np.max(np.concatenate((det.distance_s.to_numpy(), all.distance_s.to_numpy())))]
x_lim = [np.min(np.concatenate((det.temp_s.to_numpy(), all.temp_s.to_numpy()))),
         np.max(np.concatenate((det.temp_s.to_numpy(), all.temp_s.to_numpy())))]

bins = 50

xb_all, yb_all, c_all = norm_hist(all.temp_s, all.distance_s, x_lim, y_lim, bins)
xb_det, yb_det, c_det = norm_hist(det.temp_s, det.distance_s, x_lim, y_lim, bins)

if not (np.array_equal(xb_all, xb_det) and np.array_equal(yb_all, yb_det)):
    raise ValueError('blah')

xb_all = np.unique(all.temp_s)

c_all, _, _ = np.histogram2d(all.temp_s, all.distance_s, bins=(xb_all, yb_all))
c_det, _, _ = np.histogram2d(det.temp_s, det.distance_s, bins=(xb_all, yb_all))

pcm = ax2.pcolormesh(xb_all, yb_all, np.nan_to_num(c_det/c_all).T)
plt.colorbar(pcm, ax=ax2)

# ax2.set_xlim(xmin=xb_all[0])
# ax2.set_xlim(xmax=xb_all[-1])
# ax2.set_ylim(ymin=yb_all[0])
# ax2.set_ylim(ymax=yb_all[-1])


plt.show()
