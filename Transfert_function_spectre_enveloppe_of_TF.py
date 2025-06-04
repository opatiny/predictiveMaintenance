from scipy.signal import hilbert
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.signal import butter, filtfilt
df = pd.read_parquet('Nom_de_la_machine.parquet')




plt.close('all')

# Afficher les colonnes pour choisir le bon signal
print(df.columns)


temps = df['timeSeconds'].values       # colonne temps
signal = df['signal_sorti'].values     #  signal analyser
consigne = df['signal_entre'].values


dt = np.mean(np.diff(temps))  # temps entre echantillons
fs = 1 / dt

# FFT entree et sortie 
N = len(signal)
fft_signal = np.fft.fft(signal)
fft_consigne = np.fft.fft(consigne)
freqs = np.fft.fftfreq(N, d=1/fs)

# Fonction de transfert 
H_f = fft_signal / fft_consigne
H_abs = np.abs(H_f) 

# Garder uniquement les frequences positives avec interet
mask = (freqs > 500) & (freqs < 800)  
H_abs = H_abs[mask]
freqs_filtered = freqs[mask]

#Enveloppe de la fonction de transfert
analytic_H = hilbert(H_abs)
envelope_H = np.abs(analytic_H)

# FFT de lenveloppe 
df = np.mean(np.diff(freqs_filtered))  # espacement entre points en Hz
freqs_env = np.fft.fftfreq(len(envelope_H), d=df)
fft_envelope = np.fft.fft(envelope_H)

# Garder seulement les frequences positives
mask_env = freqs_env > 0
freqs_env = freqs_env[mask_env]
fft_envelope = np.abs(fft_envelope[mask_env])

# grapqhique
plt.figure(figsize=(12, 5))

# Fonction de transfert (gain)
plt.subplot(1, 2, 1)
plt.plot(freqs_filtered, 20 * np.log10(H_abs))
plt.title("Gain de la fonction de transfert (dB)")
plt.xlabel("Frequence (Hz)")
plt.ylabel("Gain (dB)")
plt.grid(True)

# Spectre de lenveloppe
plt.subplot(1, 2, 2)
plt.plot(freqs_env, fft_envelope)
plt.title("Spectre de l'enveloppe de la fonction de transfert")
plt.xlabel("Frequence de modulation (Hz)")
plt.ylabel("Amplitude")
plt.grid(True)

plt.tight_layout()
plt.show()