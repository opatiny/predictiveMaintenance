import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import uniform_filter1d
from scipy.signal import coherence
from scipy.signal import welch

df = pd.read_parquet('Nom_de_la_machine.parquet')


plt.close('all')

# Afficher les colonnes pour choisir le bon signal
print(df.columns)


temps = df['timeSeconds'].values       # colonne temps, en secondes
signal = df['signal_sorti'].values     # le signal à analyser
consigne = df['signal_entre'].values



t_start = 0  # seuil de temps
mask_t = temps > t_start

temps = temps[mask_t]
signal = signal[mask_t]
consigne = consigne[mask_t]

# Calcul de intervalle echantillonnage (si regulier)
signal = signal - np.mean(signal)
consigne = consigne - np.mean(consigne)




dt = np.mean(np.diff(temps))     # duree entre deux points
fs = 1/(dt)     
print("Frequence echantillonnage :", fs, "Hz") 

f_psd, Pxx = welch(signal, fs=fs, window='hann', nperseg=1024, noverlap=512)

plt.figure(figsize=(10, 5))
plt.semilogy(f_psd, Pxx)
plt.title("Power Spectral Density of the signal (Welch method)")
plt.xlabel("Frequency (Hz)")
plt.ylabel("PSD (A²/Hz)")
plt.grid(True)
plt.xlim(0, fs/2)
plt.show()          

# Appliquer la FFT
N = len(signal)

fft_vals = np.fft.fft(signal)
fft_consigne = np.fft.fft(consigne)
freqs = np.fft.fftfreq(N, 1/fs)


H_f = fft_vals / fft_consigne

# Ne garder que les frequences positives
mask = (freqs > 1) & (freqs < 2000)
freqs = freqs[mask]
fft_amplitude = np.abs(fft_vals[mask]) / N  # normalisation
H_f = H_f[mask]


# Affichage du spectre de frequence
plt.figure(figsize=(10, 6))
plt.plot(freqs, fft_amplitude)
plt.title("Frequency spectrum of the signal")
plt.xlabel("Frequency Hz")
plt.ylabel("Amplitude A")
plt.grid(True)
plt.show()


amplitude = np.abs(H_f)
phase = np.angle(H_f, deg=True)



plt.figure(figsize=(10, 5))
plt.semilogx(freqs, 20 * np.log10(amplitude))
plt.title("Transfer function module (dB)")
plt.xlabel("Frequency (Hz)")
plt.ylabel("Gain (dB)")
plt.grid(True)

plt.show()