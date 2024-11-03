import librosa
import numpy as np
import soundfile as sf
from scipy.fft import fft, ifft, fftshift
from scipy.signal import correlate, correlation_lags
from audio_separator.separator import Separator
    
def save_merged_signal(signal_list, lags, fs, filename):
    shifted_signals = []
    for i in range(len(signal_list)):
        shifted_signals.append(np.array([0 for _ in range(int(fs*lags[i]))] + signal_list[i].tolist()))
    max_len = max([len(x) for x in shifted_signals])
    signals = []
    for i in range(len(shifted_signals)):
        signals.append(np.array(shifted_signals[i].tolist() + [0 for _ in range(max_len - shifted_signals[i].shape[0])]))
    
    signals = np.array(signals)
    combined_signal = np.mean(signals, axis = 0)
    
    sf.write(filename, combined_signal, fs)

def compute_lag_pair(signal1, signal2, fs):
    min_length = min(signal1.shape[0], signal2.shape[0])
    F1 = fft(signal1)[:min_length]
    F2 = fft(signal2)[:min_length]

    cross_spectrum = F1 * np.conj(F2)
    cross_spectrum /= np.abs(cross_spectrum)
    inverse_fft = ifft(cross_spectrum)
    shifted = np.abs(fftshift(inverse_fft))

    delay_idx = np.argmax(shifted)
    lag = delay_idx - min(len(signal1), min_length) // 2
    if lag > 0:
        return (lag/fs, 0)
    else:
        return (0, -1*lag/fs)
    
def compute_lag_pair_cor(signal1, signal2, fs):
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

def compute_lags_cor(signal_list, fs):
    N = len(signal_list)
    lags = [0 for _ in range(N)]
    for a, signal1 in enumerate(signal_list):
        for b in range(a):
            if a!= b:
                lag_pair = compute_lag_pair_cor(signal1, signal_list[b], fs)
                lags[a] += lag_pair[0]
                lags[b] += lag_pair[1]
    m = min(lags)
    lags = [lag - m for lag in lags]
    return lags

def resolve_lags(filelist, fs):
    signal_list = []
    for filename in filelist:
        signal, _ = librosa.load(filename, sr=fs, mono=True)
        signal_list.append(signal)
    lags = compute_lags(signal_list, fs)
    for i in range(len(lags)):
        signal_list[i] = np.array([0.0 for _ in range(int(fs*lags[i]))] + signal_list[i].tolist())
    lags2 = compute_lags_cor(signal_list, fs)
    lags = [lag1 + lag2 for lag1, lag2 in zip(lags, lags2)]
    m = min(lags)
    lags = [lag - m for lag in lags]
    return lags

def resolve_lags_cor(filelist, fs):
    signal_list = []
    for filename in filelist:
        signal, _ = librosa.load(filename, sr=fs, mono=True)
        signal_list.append(signal)
    lags = compute_lag_pair(signal_list, fs)
    return lags
    
if __name__ == "__main__":
    signal_name = ["7MtuoPeC4tE.mp3", "8B2Je1pZVpo.mp3", "ej85EfL1HYU.mp3", "HKZ0_UQvaOw.mp3"]
    # signal_name = ["MOCOCO.mp3", "FUWAWA.mp3"]
    fs = 4000
    
    separator = Separator()
    separator.load_model(model_filename='model_bs_roformer_ep_317_sdr_12.9755.ckpt')
    voc_inst = separator.separate(signal_name[0])
    
    output_files = separator.separate(signal_name)
    print(f"Separation complete! Output file(s): {' '.join(output_files)}")
    
    # signal_list = []
    # for filename in signal_name:
    #     signal, _ = librosa.load(filename, sr=fs, mono=True)
    #     signal_list.append(signal)

    # lags = resolve_lags(signal_name, fs)
    
    # for name, lag in zip(signal_name, lags):
    #     print(name, lag)
    # save_merged_signal(signal_list, lags, fs, "merged_signal.wav")
    
    