import os
import glob
import matplotlib.pyplot as plt  # 🔧 Ajouté
import matplotlib
matplotlib.use("QtAgg")  # ou "QtAgg" si Tk ne marche pas


# === Custom modules ===
from src.preprocessing import detect_sampling_rate, adjust_signal_scale, ensure_time_column, remove_time_gaps
from src.segmentation import detect_stable_segments
from src.fft_analysis import extract_fft_peaks
from src.io import load_parquet_file, FrequencyClusterer
from src.plot import create_plot_folder, plot_signal_with_segments


def main(interactive=False):
    data_folder = "C:/Users/gaelv/OneDrive - HESSO/S2/PI_MaintPred/Little MAGIC/data"
    files = glob.glob(os.path.join(data_folder, "*.parquet"))

    all_peaks = []
    freq_table = FrequencyClusterer(tolerance=0.5)

    for file_path in files:
        print(f"▶ Processing file: {os.path.basename(file_path)}")
        try:
            data = load_parquet_file(file_path).to_pandas()
            data = ensure_time_column(data)
            data = adjust_signal_scale(data, file_path)
            sampling_rate = detect_sampling_rate(file_path)
            print(f"Detected sampling rate: {sampling_rate} Hz")
            data = remove_time_gaps(data, time_column='timeSeconds')

            segments = detect_stable_segments(
                data,
                signal_column='stSigSpindleIndicator',
                window=200,
                std_threshold=0.1,
                min_length=sampling_rate,
                max_segments=6,
                min_stable_duration=50,
                min_segment_duration=30.0
            )

            plot_folder = create_plot_folder(file_path)
            plot_signal_with_segments(data, segments, signal_column='stSigSpindleIndicator', folder_path=plot_folder, show=interactive)

            segment_peaks = extract_fft_peaks(
                data,
                segments,
                signal_column='stSigSpindleIndicator',
                file_path=file_path,
                folder_path=plot_folder,
                all_peaks=all_peaks,
                show=interactive
            )
            
            for segment_idx, freqs, amps in segment_peaks:
                freq_table.add_peaks(file_path, segment_idx, freqs, amps)


                if interactive:
                    print("📊 Affichage du graphique (ferme la fenêtre pour continuer)...")
                    plt.show()
                    print("📊 Fenêtre fermée, poursuite du traitement...")
                    input("🕵️‍♂️ Appuie sur Entrée pour traiter le fichier suivant...")
                else:
                    # Affiche brièvement la figure et ferme toutes les fenêtres proprement
                    plt.draw()           # Force le dessin
                    plt.pause(0.1)       # Laisse la boucle d'événements tourner (assez court)
                    plt.close('all')     # Ferme toutes les figures
                

        except Exception as e:
            print(f"❌ Error processing {os.path.basename(file_path)}: {e}")

    if all_peaks:
        print("💾 Sauvegarde des résultats dans Excel...")
        # Exemple : si tu veux enregistrer les résultats dans deux fichiers
        freq_table.save_excels("outputs/frequencies.xlsx", "outputs/amplitudes.xlsx")
        print("✅ Traitement terminé avec succès, résultats sauvegardés.")
    else:
        print("⚠ Aucun pic détecté dans les fichiers.")


if __name__ == "__main__":
    main()
