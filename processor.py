import librosa
import numpy as np
from scipy.signal import correlate, correlation_lags

def compute_lag_pair(signal1, signal2, fs):
    corr = correlate(signal1, signal2, mode='full')
    lags = correlation_lags(signal1.shape[0], signal2.shape[0], mode="full")
    lag = lags[np.argmax(corr)]
    if lag > 0:
        return (0, lag/fs)
    else:
        return (-1*lag/fs, 0)
    
def compute_lags(signal_list, fs):
    N = len(signal_list)
    lags = [0 for _ in range(N)]
    for a, signal1 in enumerate(signal_list):
        for b in range(a):
            if a!= b:
                lag_pair = compute_lag_pair(signal1, signal_list[b], fs)
                lags[a] += lag_pair[0]
                lags[b] += lag_pair[1]
    m = min(lags)
    lags = [lag - m for lag in lags]
    return lags

def resolve_lags(filelist):
    fs = 8000
    signal_list = []
    for filename in filelist:
        signal, _ = librosa.load(filename, sr=fs, mono=True)
        signal_list.append(signal)

    lags = compute_lags(signal_list, fs)
    return lags

if __name__ == "__main__":
    lags = resolve_lags(["MOCOCO.mp3", "FUWAWA.mp3"])
    print(lags)