import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt, hilbert

#  Parametres
fs = 10000  # frequence dechantillonnage en Hz (a ajuster au besoin de ce qu'on veut voir)
lowcut = 5   # frequence basse du filtre passe-bande (Hz)
highcut = 500 # frequence haute 


df = pd.read_parquet('Nom_de_la_machine.parquet')


plt.close('all')

# Afficher les colonnes pour choisir le bon signal
print(df.columns)


temps = df['timeSeconds'].values       # colonne temps
signal = df['signal'].values     # le signal 

#filtre passe bande

def bandpass_filter(signal, fs, lowcut, highcut, order=4):
    b, a = butter(order, [lowcut, highcut], btype='band', fs=fs)
    return filtfilt(b, a, signal)

signal_filtre = bandpass_filter(signal, fs, lowcut, highcut)

signal_clipped = np.clip(signal_filtre, -800, 800)

# Calcul de enveloppe
enveloppe = np.abs(hilbert(signal_clipped))


# Spectre de enveloppe
N = len(enveloppe)
frequencies = np.fft.fftfreq(N, d=1/fs)
enveloppe_fft = np.fft.fft(enveloppe)
spectre = np.abs(enveloppe_fft) / N

# Ne garder que les frequences positives
mask = (frequencies > 50) & (frequencies < 2000)  
frequencies = frequencies[mask]
spectre = spectre[mask]

#Affichage
plt.figure(figsize=(14, 6))



plt.plot(signal_clipped, label='signal', linewidth=2)
plt.title("Signal Nom_de_la_machine")
plt.xlabel("Temps S")
plt.ylabel("Amplitude mA")
plt.legend()

plt.figure()
plt.plot(enveloppe[:1500], label='Enveloppe', linewidth=2)
plt.title("Enveloppe du Signal Nom_de_la_machine")
plt.xlabel("Temps S")
plt.ylabel("Amplitude mA")
plt.legend()

plt.figure()
plt.plot(frequencies, spectre)
plt.title("Spectre de l’enveloppe (FFT)")
plt.xlabel("Frequence (Hz)")
plt.ylabel("Amplitude mA/Hz")
plt.grid(True)

plt.tight_layout()
plt.show()