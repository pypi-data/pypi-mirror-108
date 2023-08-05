import numpy as np
from scipy import integrate
from .narrowband import Narrowband
from ..tools import pdf_rayleigh_sum

class FuCebon(Narrowband):
    """Class for fatigue life estimation using frequency domain 
    method by Fu and Cebon [1].
    
    References
    ----------
    [1] Tsengti Fu, David Cebon. Predicting fatigue lives for bi-modal stress spectral densities.
        International Journal of Fatigue, 22(1):11-21, 2000
    [2] Janko Slavič, Matjaž Mršnik, Martin Česnik, Jaka Javh, Miha Boltežar. 
        Vibration Fatigue by Spectral Methods, From Structural Dynamics to Fatigue Damage
        – Theory and Experiments, ISBN: 9780128221907, Elsevier, 1st September 2020
    
    Example
    -------
    Import modules, define time- and frequency-domain data

    >>> import FLife
    >>> import pyExSi as es
    >>> import numpy as np
    >>> from matplotlib import pyplot as plt
    >>> # time-domain data
    >>> N = 2 ** 16  # number of data points of time signal
    >>> fs = 2048  # sampling frequency [Hz]
    >>> t = np.arange(0, N) / fs  # time vector
    >>> # frequency-domain data
    >>> M = N // 2 + 1  # number of data points of frequency vector
    >>> freq = np.arange(0, M, 1) * fs / N  # frequency vector
    >>> PSD_lower = es.get_psd(freq, 20, 60, variance = 5)  # lower mode of random process
    >>> PSD_higher = es.get_psd(freq, 100, 120, variance = 2)  # higher mode of random process
    >>> PSD = PSD_lower + PSD_higher # bimodal one-sided flat-shaped PSD

    Get Gaussian stationary signal, instantiate SpectralData object and plot PSD

    >>> rg = np.random.default_rng(123) # random generator seed
    >>> x = es.random_gaussian(N, PSD, fs, rg) # Gaussian stationary signal
    >>> sd = FLife.SpectralData(input=x, dt=1/fs) # SpectralData instance
    >>> plt.plot(sd.psd[:,0], sd.psd[:,1]) 
    >>> plt.xlabel('Frequency [Hz]')
    >>> plt.ylabel('PSD')

    Define S-N curve parameters and get fatigue-life estimatate

    >>> C = 1.8e+22  # S-N curve intercept [MPa**k]
    >>> k = 7.3 # S-N curve inverse slope [/]
    >>> fc = FLife.FuCebon(sd, PSD_splitting=('userDefinedBands', [80,150]))
    >>> print(f'Fatigue life: {fc.get_life(C,k):.3e} s.')

    Plot segmentated PSD, used in Fu-Cebon method

    >>> lower_band_index, upper_band_index= fc.band_stop_indexes
    >>> plt.plot(sd.psd[:,0], sd.psd[:,1])
    >>> plt.vlines(sd.psd[:,0][lower_band_index], 0, np.max(sd.psd[:,1]), 'k', linestyles='dashed', alpha=.5)
    >>> plt.fill_between(sd.psd[:lower_band_index,0], sd.psd[:lower_band_index,1], 'o', label='lower band', alpha=.2, color='blue')
    >>> plt.vlines(sd.psd[:,0][upper_band_index], 0, np.max(sd.psd[:,1]), 'k', linestyles='dashed', alpha=.5)
    >>> plt.fill_between(sd.psd[lower_band_index:upper_band_index,0], sd.psd[lower_band_index:upper_band_index,1], 'o', label='upper band', alpha=.5, color ='orange')
    >>> plt.xlabel('Frequency [Hz]')
    >>> plt.ylabel('PSD')
    >>> plt.xlim(0,300)
    >>> plt.legend()
    """
    def __init__(self, spectral_data, PSD_splitting = ('equalAreaBands', 2)):
        """Get needed values from reference object.
        
        :param spectral_data: Instance of class SpectralData
        :param PSD_splitting: tuple
                PSD_splitting[0] is PSD spliting method, PSD_splitting[1] is method argument. 
                Splitting methods:

                - 'userDefinedBands', PSD_splitting[1] must be of type list or tupple, with N 
                  elements specifying upper band frequencies of N random processes.
                - 'equalAreaBands', PSD_splitting[1] must be of type int, specifying N random processes.

                Defaults to ('equalAreaBands', 2).
        """       
        Narrowband.__init__(self, spectral_data)
        self.PSD_splitting = PSD_splitting
        self.band_stop_indexes = self.spectral_data._get_band_stop_frequency(self.PSD_splitting)

    def get_life(self, C, k):
        """Calculate fatigue life with parameters C, k, as defined in [1, 2].

        :param C: [int,float]
            S-N curve intercept [MPa**k].
        :param k: [int,float]
            S-N curve inverse slope [/].
        :return:
            Estimated fatigue life in seconds.
        :rtype: float
        """
        # -- spectral moments for each narrowband
        moments = self.spectral_data.get_spectral_moments(self.PSD_splitting, moments=[0])
        m0L, = moments[0] #spectral moments for lower band
        m0H, = moments[1] #spectral moments for upper band

        # -- positive slope zero crossing frequency
        v0L, v0H = self.spectral_data.get_nup(self.PSD_splitting)
        v0Small = v0H - v0L  #freqeuncy of small cycless
        
        #dNB small
        #small cycles consist of high frequency component
        dNB_small = self.damage_intesity_NB(m0H, v0Small, C, k) 

        #dNB large
        #large cycles consist of low and high frequency component
        pdf_large = pdf_rayleigh_sum(m0L,m0H)
        S_large = integrate.quad(lambda x:  x**k * pdf_large(x), 0, np.inf)[0]
        dNB_large = v0L * S_large / C
        d = dNB_small + dNB_large
        T = 1 / d
        return T

    def get_PDF(self, s):
        raise Exception(f'Function <get_PDF> is not available for class {self.__class__.__name__:s}.')