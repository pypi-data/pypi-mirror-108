import numpy as np
import pandas as pd
from collections import deque
from astropy.convolution import Box1DKernel, Gaussian1DKernel, convolve, convolve_fft



def set_seed(star, lower=1, upper=10**7, size=1):
    """
    For Kepler targets that require a correction via CLI (--kc), a random seed is generated
    from U~[1,10^7] and stored in stars_info.csv for reproducible results in later runs.

    """

    seed = list(np.random.randint(lower,high=upper,size=size))
    df = pd.read_csv(star.info)
    stars = df.targets.values.tolist()
    idx = stars.index(star.star)
    df.loc[idx,'seed'] = int(seed[0])
    star.params[star.star]['seed'] = seed[0]
    df.to_csv(star.info,index=False)
    return star


def remove_artefact(star, lcp=1.0/(29.4244*60*1e-6), lf_lower = [240.0, 500.0], lf_upper = [380.0, 530.0], 
                    hf_lower = [4530.0, 5011.0, 5097.0, 5575.0, 7020.0, 7440.0, 7864.0],
                    hf_upper = [4534.0, 5020.0, 5099.0, 5585.0, 7030.0, 7450.0, 7867.0],):
    """
    Removes SC artefacts in Kepler power spectra by replacing them with noise (using linear interpolation)
    following a chi-squared distribution. 

    Known artefacts are:
    1) 1./LC harmonics
    2) high frequency artefacts (>5000 muHz)
    3) low frequency artefacts 250-400 muHz (mostly present in Q0 and Q3 data)

    Parameters
    ----------
    frequency : np.ndarray
        the frequency of the power spectrum
    power : np.ndarray
        the power of the power spectrum
    lcp : float
        TODO: Write description. Default value is `1/(29.4244*60*1e-6)`.

    """

    if star.params[star.name]['seed'] is None:
        star = set_seed(star)
    # LC period in Msec -> 1/LC ~muHz
    artefact = (1.0+np.arange(14))*lcp
    # Estimate white noise
    white = np.mean(star.power[(star.frequency >= star.nyquist-100.0) & (star.frequency <= star.nyquist-50.0)])

    np.random.seed(int(star.params[star.name]['seed']))
    # Routine 1: remove 1/LC artefacts by subtracting +/- 5 muHz given each artefact
    for i in range(len(artefact)):
        if artefact[i] < np.max(star.frequency):
            mask = np.ma.getmask(np.ma.masked_inside(star.frequency, artefact[i]-5.0*star.resolution, artefact[i]+5.0*star.resolution))
            if np.sum(mask) != 0:
                star.power[mask] = white*np.random.chisquare(2,np.sum(mask))/2.0

    np.random.seed(int(star.params[star.name]['seed']))
    # Routine 2: fix high frequency artefacts
    for lower, upper in zip(hf_lower, hf_upper):
        if lower < np.max(star.frequency):
            mask = np.ma.getmask(np.ma.masked_inside(star.frequency, lower, upper))
            if np.sum(mask) != 0:
                star.power[mask] = white*np.random.chisquare(2,np.sum(mask))/2.0

    np.random.seed(int(star.params[star.name]['seed']))
    # Routine 3: remove wider, low frequency artefacts 
    for lower, upper in zip(lf_lower, lf_upper):
        low = np.ma.getmask(np.ma.masked_outside(star.frequency, lower-20., lower))
        upp = np.ma.getmask(np.ma.masked_outside(star.frequency, upper, upper+20.))
        # Coeffs for linear fit
        m, b = np.polyfit(star.frequency[~(low*upp)], star.power[~(low*upp)], 1)
        mask = np.ma.getmask(np.ma.masked_inside(star.frequency, lower, upper))
        # Fill artefact frequencies with noise
        star.power[mask] = ((star.frequency[mask]*m)+b)*(np.random.chisquare(2, np.sum(mask))/2.0)

    return star


def gaussian_bounds(x, y, guesses, best_x=None, sigma=None):
    """Get the bounds for the parameters of a Gaussian fit to the data.

    Parameters
    ----------
    x : np.ndarray
        the x values of the data
    y : np.ndarray
        the y values of the data
    best_x : Optional[float]
        TODO: Write description. Default value is `None`.
    sigma : Optional[float]
        TODO: Write description. Default value is `None`.

    Returns
    -------
    bb : List[Tuple]
        list of parameter bounds of a Gaussian fit to the data
    """
    offset, amp, center, width = guesses
    if sigma is None:
        sigma = (max(x)-min(x))/8.0/np.sqrt(8.0*np.log(2.0))
    bb = []
    b = np.zeros((2, 4)).tolist()
    
    # offset bound:
    b[1][0] = np.inf            #upper bound
    # amplitude bounds:
    if amp > 0:
        b[1][1] = 2.0*np.max(y) #upper bound
    else:
        b[0][1]=-np.inf         #lower bound
        b[1][1]=0               #upper bound
    # center bounds:
    b[0][2] = np.min(x)
    b[1][2] = np.max(x)
    # width bounds
    b[0][3] = sigma
    b[1][3] = (np.max(x)-np.min(x))*2.
    bb.append(tuple(b))
    
    return bb


def max_elements(x, y, npeaks):
    """Get the first n peaks of the given data.

    Parameters
    ----------
    x : np.ndarray
        the x values of the data
    y : np.ndarray
        the y values of the data
    npeaks : int
        the first n peaks

    Returns
    -------
    peaks_x : np.ndarray
        the x co-ordinates of the first `npeaks`
    peaks_y : np.ndarray
        the y co-ordinates of the first `npeaks`
    """

    s = np.argsort(y)
    peaks_y = y[s][-int(npeaks):][::-1]
    peaks_x = x[s][-int(npeaks):][::-1]

    return peaks_x, peaks_y


def return_max(x_array, y_array, exp_dnu=None, index=False):
    """Return the either the value of peak or the index of the peak corresponding to the most likely dnu given a prior estimate,
    otherwise just the maximum value.

    Parameters
    ----------
    x_array : np.ndarray
        the independent axis (i.e. time, frequency)
    y_array : np.ndarray
        the dependent axis
    method : str
        which method to use for determing the max elements in an array
    index : bool
        if true will return the index of the peak instead otherwise it will return the value. Default value is `False`.
    dnu : bool
        if true will choose the peak closest to the expected dnu `exp_dnu`. Default value is `False`.
    exp_dnu : Required[float]
        the expected dnu. Default value is `None`.

    Returns
    -------
    result : Union[int, float]
        if `index` is `True`, result will be the index of the peak otherwise if `index` is `False` it will instead return the
        value of the peak.
    """
    if exp_dnu is None:
        lst = list(y_array)
        idx = lst.index(max(lst))
        weights = None
    else:
        sig = 0.35*exp_dnu/2.35482 
        weights = 1./(sig*np.sqrt(2.*np.pi))*np.exp(-(x_array-exp_dnu)**2./(2.*sig**2))
        lst = list(weights*y_array)
        idx = lst.index(max(lst))
    if index:
        return idx
    else:
        return x_array[idx], y_array[idx]


def mean_smooth_ind(x, y, width):
    """Smooths the data using independent mean smoothing and binning.

    Parameters
    ----------
    x : np.ndarray
        the x values of the data
    y : np.ndarray
        the y values of the data
    width : float
        independent average smoothing width

    Returns
    -------
    sx : np.ndarray
        binned mean smoothed x data
    sy : np.ndarray
        binned mean smoothed y data
    se : np.ndarray
        standard error
    """
    step = width-1
    j=0
    
    sx = np.zeros_like(x)
    sy = np.zeros_like(x)
    se = np.zeros_like(x)

    j = 0

    while (j+step < len(x)-1):

        sx[j] = np.mean(x[j:j+step])
        sy[j] = np.mean(y[j:j+step])
        se[j] = np.std(y[j:j+step])/np.sqrt(width)
        j += step

    sx = sx[(sx != 0.0)]
    se = se[(sy != 0.0)]
    sy = sy[(sy != 0.0)]
    se[(se == 0.0)] = np.median(se)
    return sx, sy, se


def smooth(array, width, params, method='box', mode=None, fft=False, silent=False):
    """Smooths using a variety of methods. TODO: Write description.

    Parameters
    ----------
    array : np.ndarray
        the data
    TODO: Add parameters

    Returns
    -------
    TODO: Add return arguments
    """

    if method == 'box':

        if isinstance(width, int):
            kernel = Box1DKernel(width)
        else:
            width = int(np.ceil(width/params['resolution']))
            kernel = Box1DKernel(width)

        if fft:
            smoothed_array = convolve_fft(array, kernel)
        else:
            smoothed_array = convolve(array, kernel)

        if not silent:
            print('%s kernel: kernel size = %.2f muHz' % (method, width*params['resolution']))

    elif method == 'gaussian':

        n = 2*len(array)
        forward = array[:].tolist()
        reverse = array[::-1].tolist()

        if n % 4 != 0:
            start = int(np.ceil(n/4))
        else:
            start = int(n/4)
        end = len(array)

        final = np.array(reverse[start:end]+forward[:]+reverse[:start])

        if isinstance(width, int):
            kernel = Gaussian1DKernel(width)
        else:
            width = int(np.ceil(width/params['resolution']))
            kernel = Gaussian1DKernel(width, mode=mode)

        if fft:
            smoothed = convolve_fft(final, kernel)
        else:
            smoothed = convolve(final, kernel)

        smoothed_array = smoothed[int(n/4):int(3*n/4)]

        if not silent:
            print('%s kernel: sigma = %.2f muHz' % (method, width*params['resolution']))
    else:
        print('Do not understand the smoothing method chosen.')

    return smoothed_array


def smooth_gauss(array, fwhm, params, silent=False):
    """TODO: Write description.

    Parameters
    ----------
    TODO: Add parameters

    Returns
    -------
    TODO: Add return arguments
    """

    sigma = fwhm/np.sqrt(8.0*np.log(2.0))

    n = 2*len(array)
    N = np.arange(1, n+1, 1)
    mu = len(array)
    total = np.sum((1.0/(sigma*np.sqrt(2.0*np.pi)))*np.exp(-0.5*(((N-mu)/sigma)**2.0)))
    weights = ((1.0/(sigma*np.sqrt(2.0*np.pi)))*np.exp(-0.5*(((N-mu)/sigma)**2.0)))/total

    forward = array[:]
    reverse = array[::-1]

    if n % 4 != 0:
        start = int(np.ceil(n/4))
    else:
        start = int(n/4)
    end = int(n/2)

    final = np.array(reverse[start:end]+forward[:]+reverse[:start])
    fft = np.fft.irfft(np.fft.rfft(final)*np.fft.rfft(weights))
    dq = deque(fft)
    dq.rotate(int(n/2))
    smoothed = np.array(dq)
    smoothed_array = smoothed[int(n/4):int(3*n/4)]
    if not silent:
        print('gaussian kernel using ffts: sigma = %.2f muHz' % (sigma*params['resolution']))
    if params['edge'][0]:
        smoothed_array = smoothed_array[:-params['edge'][1]]

    return np.array(smoothed_array)


def bin_data(x, y, params):
    """Bins data logarithmically.

    Parameters
    ----------
    x : np.ndarray
        the x values of the data
    y : np.ndarray
        the y values of the data
    params : list
        binning parameters

    Returns
    -------
    bin_freq : np.ndarray
        binned frequencies
    bin_pow : np.ndarray
        binned power
    """

    mi = np.log10(min(x))
    ma = np.log10(max(x))
    no = np.int(np.ceil((ma-mi)/params['binning']))
    bins = np.logspace(mi, mi+(no+1)*params['binning'], no)

    digitized = np.digitize(x, bins)
    bin_freq = np.array([x[digitized == i].mean() for i in range(1, len(bins)) if len(x[digitized == i]) > 0])
    bin_pow = np.array([y[digitized == i].mean() for i in range(1, len(bins)) if len(y[digitized == i]) > 0])

    return bin_freq, bin_pow


def delta_nu(numax):
    """Estimates dnu using numax scaling relation.

    Parameters
    ----------
    numax : float
        the estimated numax

    Returns
    -------
    dnu : float
        the estimated dnu
    """

    return 0.22*(numax**0.797)
