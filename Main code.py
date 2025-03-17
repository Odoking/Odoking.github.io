import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

def logged_graph():
    plt.yscale("log")
    plt.xscale("log")
    plt.plot(x,T)
    plt.scatter(bin_centers, T_bins, color='red', label="Observed Data")
    plt.fill_between(x,y_err,T_err2, color='orange', alpha=0.3, label="Error Bounds")
    plt.legend()
    plt.title('Fitted Fréchet Distribution')
    plt.xlabel('Speed Jump (km/s)')
    plt.ylabel('Return Period (yrs)')
    plt.show()

def histogram():
    plt.yscale("log")
    plt.hist(data, density = True, bins=64, alpha=0.6, color='gray', label='Data Histogram')
    plt.plot(x, pdf, 'r-', label='Fitted Fréchet Distribution')
    plt.show() 
    
file_path = 'shocks_20250128_180854.dat'  
data = np.genfromtxt(file_path, delimiter=',', skip_header=1)
data = data[:,8]
shape, loc, scale = stats.genextreme.fit(data)
print(scale)
x = np.linspace(20, 1000, 1000)
pdf = stats.genextreme.pdf(x, shape, loc=loc, scale=scale)
error = stats.genextreme.std(int(shape), loc, scale)
print(error)
pdf_err = stats.genextreme.pdf(x,shape, loc=loc, scale = scale+error)
binN = 64
freq, bins = np.histogram(data, bins=binN, density = True)
bin_centers = (bins[:-1] + bins[1:]) / 2
time_gap = 49.1671
nonzero_indices = freq > 0
freq = freq[nonzero_indices]
bin_centers = bin_centers[nonzero_indices]
n = binN/ (9*56.3)
T = (time_gap/(pdf * len(data)))*n
T_err2 = (time_gap/(pdf_err * len(data)))*n
T_bins = (time_gap/(freq * len(data)))*n

y_err = T + (T - T_err2)
for i in range( 0, len(y_err)):
    if T[i] < 1:
        y_err[i] = T[i]
        T_err2[i] = T[i]
logged_graph()
histogram()



