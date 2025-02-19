from pyedflib import highlevel
import pyedflib as plib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statistics as stats
import seaborn as sns
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from scipy.signal import windows
import xml.etree.ElementTree as ET
from intervaltree import Interval, IntervalTree

"""Main module"""

class EDA:

    def read_file_signal(file_path, index):
        f = plib.EdfReader(file_path)
        signal = f.readSignal(index)
        f.close()
        return signal

    def signal_labels(file_path):
        f = plib.EdfReader(file_path)
        labels = f.getSignalLabels()
        f.close()
        return labels

    def combined_signal_from_files(file_list, index):
        combined_signals = []
        for file in file_list:
            temp = EDA.read_file_signal(file, index)
            combined_signals.append(temp)
        return np.concatenate(combined_signals)

    def combined_signal_from_signals(signal_list, index):
        combined_signals = []
        for signal in signal_list:
            combined_signals.append(signal)
        return np.concatenate(combined_signals)

    def plot_signal(label, signal):
        plt.figure(figsize=(20, 10))
        plt.plot(signal)
        plt.title(f"{label} signal")
        plt.xlabel("time")
        plt.ylabel("amplitude")
        # plt.ylim(-300, 300)
        plt.show()

    def thresholding(signal, threshold, replace_with):
        mean = signal.mean()
        std = stats.stdev(signal)
        lower_limit = mean - threshold * std
        upper_limit = mean + threshold * std
        filtered_signal = np.where((signal >= lower_limit) & (signal <= upper_limit), signal, replace_with)
        return filtered_signal

    def resample_signal(signal, num_samples):
        original_indices = np.linspace(0, len(signal) - 1, num=len(signal))
        resampled_indices = np.linspace(0, len(signal) - 1, num=num_samples)
        resampled_signal = np.interp(resampled_indices, original_indices, signal)
        return resampled_signal

    def channel_coeff_of_var(signal_list):
        means = []
        for signal in signal_list:
            means.append(signal.mean())
        mean = stats.mean(means)
        std = stats.stdev(means)
        if mean == 0:
            return 0
        return std / mean
    
    def coeff_of_var_line_plot(cv_dict):
        df_cv = pd.DataFrame(list(cv_dict.items()), columns=['Channel', 'Coefficient of Variation'])
        df_cv = df_cv.sort_values(by='Coefficient of Variation', ascending=False)
        plt.figure(figsize=(20, 10))
        plt.plot(df_cv['Channel'], df_cv['Coefficient of Variation'])
        plt.title("Coefficient of Variation of Channels")
        plt.xlabel("Channel")
        plt.ylabel("Coefficient of Variation")
        plt.grid(True)
        plt.show()

    def coeff_of_var_heatmap(cv_dict):
        df = pd.DataFrame.from_dict(cv_dict, orient='index', columns=['Priority'])
        plt.figure(figsize=(20, 10))
        sns.heatmap(df, annot=True, cmap='Blues', linewidths=0.5)
        plt.title("Coefficient of Variation of Channels")
        plt.xlabel("Priority")
        plt.ylabel("Channel")
        plt.show()

    def plot_cv_dendrogram(cv_dict):
        df = df.replace([np.inf, -np.inf], np.nan).dropna(axis=0)
        Z = linkage(df, method='ward')
        plt.figure(figsize=(20, 10))
        dendrogram(Z, labels=df.index)
        plt.title("Dendrogram of Coefficient of Variation")
        plt.xlabel("Channel")
        plt.ylabel("Distance")    
        plt.show()
    
    def plot_log_cv_dendrogram(cv_dict):
        df_log = np.log(cv_dict)
        df_log = df_log.replace([np.inf, -np.inf], np.nan).dropna(axis=0)
        Z = linkage(df_log, method='ward')  
        plt.figure(figsize=(10, 7))
        dendrogram(Z, labels=df_log.index)
        plt.title("Dendrogram of Channels")
        plt.xlabel("Channel")
        plt.ylabel("Distance")
        plt.show()

    # divide signal into parts of equal length
    # calculate mean of each part
    # calculate var of these means and mean of these means
    def time_division_of_signals(signal, num_divisions):
        time_division = []
        length = len(signal)//num_divisions
        for i in range(num_divisions):
            time_division.append(signal[i*length:(i+1)*length])
        return time_division
    
    def hourly_coeff_of_var(normal, mild, moderate, severe, num_divisions):
        normal_time_div = EDA.time_division_of_signals(normal, num_divisions)
        mild_time_div = EDA.time_division_of_signals(mild, num_divisions)
        moderate_time_div = EDA.time_division_of_signals(moderate, num_divisions)
        severe_time_div = EDA.time_division_of_signals(severe, num_divisions)
        cv_list = []
        for i in range(num_divisions):
            means = []
            means.append(np.mean(normal_time_div[i]))
            means.append(np.mean(mild_time_div[i]))
            means.append(np.mean(moderate_time_div[i]))
            means.append(np.mean(severe_time_div[i]))
            mean = stats.mean(means)
            var = stats.variance(means)
            if mean == 0:
                cv_list.append(0)
            else:
                cv_list.append(abs(var / mean))
        return cv_list

    def principle_comp_analysis_of_channels(df, n): #channels must be rows and time must be columns
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(df)

        pca = PCA(n_components=n)
        X_pca = pca.fit_transform(X_scaled)

        explained_variance = pca.explained_variance_ratio_
        print("Explained variance by each component:", explained_variance)
        num_channels = X_pca.shape[0]
        colors = plt.cm.get_cmap('tab20', num_channels)  # Use a colormap with enough colors
        channel_names = df.index.tolist()
        plt.figure(figsize=(10, 7))
        scatter = plt.scatter(X_pca[:, 0], X_pca[:, 1], c=np.arange(num_channels), cmap='tab20')
        plt.colorbar(scatter, ticks=np.arange(num_channels), label='Channel Index')
        for i, channel in enumerate(channel_names):
            plt.text(X_pca[i, 0], X_pca[i, 1], channel, fontsize=9, color=colors(i))

        plt.xlabel('Principal Component 1')
        plt.ylabel('Principal Component 2')
        plt.title('PCA of Channels')
        plt.grid(True)
        plt.tight_layout()
        plt.show()

    def rolling_mean(signal, window_size):
        return np.convolve(signal, np.ones(window_size)/window_size, mode='valid')

    def signal_fft(signal, sampling_rate):
        window = windows.hann(len(signal))
        windowed_signal = signal * window
        fft_result = np.fft.fft(windowed_signal)
        freqs = np.fft.fftfreq(len(fft_result), 1/sampling_rate)
        magnitude_spectrum = np.abs(fft_result)
        return fft_result, freqs, magnitude_spectrum

    def reconstruct_signal(fft_result, threshold=20):
        fft_filtered = np.copy(fft_result)
        fft_filtered[threshold:] = 0
        reconstructed_signal = np.fft.ifft(fft_filtered).real
        return reconstructed_signal

    def plot_fft(signal, reconstructed_signal):
        plt.figure(figsize=(12, 6))
        plt.plot(signal, label='Original Signal')
        plt.plot(reconstructed_signal, label='Reconstructed Signal')
        plt.xlabel('Time')
        plt.ylabel('Amplitude')
        plt.title('Original and Reconstructed Signal')
        plt.legend()
        plt.show()


class CrudeScoring:

    def get_timestamps_for_scoring(signal, freq):
        timestamps = np.linspace(0, 3600*freq, len(signal))
        return timestamps

    def count_obstructive_apnea(fp2_signal, freq, timestamps):
        mean_fp2 = np.mean(fp2_signal)
        count = 0
        apnea_start = None
        time_drops = []
        for i in range(1, len(fp2_signal)):
            if (mean_fp2 - fp2_signal[i])/mean_fp2 >= 0.9:
                if apnea_start is None:
                    apnea_start = timestamps[i]
            else:
                if apnea_start is not None and (timestamps[i - 1] - apnea_start) >= 10*freq:
                    count += 1  # Count the drop
                    time_drops.append((apnea_start, timestamps[i - 1]))
                apnea_start = None  # Reset the drop

        if apnea_start is not None and (timestamps[-1] - apnea_start) >= 10*freq:
            count += 1
            time_drops.append((apnea_start, timestamps[-1]))

        return count, time_drops

    def plot_signal_with_apnea_drops(fp2_signal, timestamps):
        count, time_drops = CrudeScoring.count_obstructive_apnea(fp2_signal, timestamps)
        plt.figure(figsize=(12, 6))
        plt.plot(timestamps, fp2_signal, label='FP2 Signal')
        
        for start, end in time_drops:
            plt.axvspan(start, end, color='red', alpha=0.5, label='Apnea Drop' if start == time_drops[0][0] else "")
        
        plt.xlabel('Time')
        plt.ylabel('FP2 Signal')
        plt.title('FP2 Signal with Apnea Drops Highlighted')
        plt.legend()
        plt.show()

    def count_obstructive_hypopnea(fp1_data, spo2_data, freq, timestamps):
        mean_fp1 = np.mean(fp1_data)  
        mean_spo2 = np.mean(fp1_data)
        drop_start = None
        count = 0
        time_drops = []

        for i in range(1, min(len(fp1_data), len(spo2_data))):
            if (mean_fp1 - fp1_data[i])/mean_fp1 >= 0.3 and (mean_spo2 - spo2_data[i])/mean_spo2 >= 0.03:
                if drop_start is None:
                    drop_start = timestamps[i]  # Start timing the drop
            else:
                if drop_start is not None and (timestamps[i - 1] - drop_start) >= 10*freq:
                    count += 1  # Count the drop
                    time_drops.append((drop_start, timestamps[i - 1]))
                drop_start = None  # Reset the drop

        if drop_start is not None and (timestamps[-1] - drop_start) >= 10*freq:
            count += 1
            time_drops.append((drop_start, timestamps[-1]))

        return count, time_drops        

    def plot_signals_with_hypopnea_drops(fp1_data, spo2_data, timestamps):
        count, time_drops = CrudeScoring.count_obstructive_hypopnea(fp1_data, spo2_data, timestamps)
        
        plt.figure(figsize=(12, 6))
        
        # Plot fp1 signal
        plt.plot(timestamps, fp1_data, label='FP1 Signal')
        
        # Plot spo2 signal
        plt.plot(timestamps, spo2_data, label='SpO2 Signal')
        
        # Highlight the drops
        for start, end in time_drops:
            plt.axvspan(start, end, color='red', alpha=0.5, label='Hypopnea Drop' if start == time_drops[0][0] else "")
        
        plt.xlabel('Time')
        plt.ylabel('Signal Value')
        plt.title('FP1 and SpO2 Signals with Hypopnea Drops Highlighted')
        plt.legend()
        plt.show()

    def apnea_hypopnea_index(apnea_counts, hypopnea_counts):
        return (apnea_counts+hypopnea_counts)/2

    def zoomed_plot_oa(start_time, end_time, signal, hour):
        if start_time>10:
            start_index = int(start_time)-10
        else:
            start_index = 0
        if end_time<3590:
            end_index = int(end_time)+10
        else:
            end_index = 3600
        plt.figure(figsize=(12, 6))
        plt.plot(signal[start_index:end_index])
        plt.axvspan(10, end_time-start_time+10, color='red', alpha=0.5, label='Apnea Drop')
        plt.title(f'Zoomed Plot for OA at hour {hour+1}, {int(start_time)} to {int(end_time)}')
        plt.xlabel('Time')
        plt.ylabel('Signal')
        plt.show()    

    def zoomed_plot_oh(start_time, end_time, fp1_data, spo2_data, hour):
        if start_time>10:
            start_index = int(start_time)-10
        else:
            start_index = 0
        if end_time<3590:
            end_index = int(end_time)+10
        else:
            end_index = 3600
        plt.figure(figsize=(12, 6))
        plt.plot(fp1_data[start_index:end_index], label='FP1 Signal')
        plt.plot(spo2_data[start_index:end_index], label='SpO2 Signal')
        plt.axvspan(10, end_time-start_time+10, color='red', alpha=0.5, label='Apnea Drop')
        plt.xlabel('Time')
        plt.ylabel('Signal Value')
        plt.title(f'Zoomed Plot for OA for at hour {hour+1}, {int(start_time)} to {int(end_time)}')
        plt.legend()
        plt.show()

class SleepStages:

    def parse_stages_user(file_path):
        tree = ET.parse(file_path)
        root = tree.getroot()
        output = {}
        for stage in root.findall('.//User/Stage'):
            stage_type = stage.get('Type')
            start_time = stage.get('Start')
            output[start_time] = stage_type
        return output

    def parse_stages_machine(file_path):
        tree = ET.parse(file_path)
        root = tree.getroot()
        output = {}
        for stage in root.findall('.//Machine/Stage'):
            stage_type = stage.get('Type')
            start_time = stage.get('Start')
            output[start_time] = stage_type
        return output
    
    def get_root(file_path):
        tree = ET.parse(file_path)
        root = tree.getroot()
        return root
    
    def find_intervals_user(type, root):
        time_intervals = []
        time_pair = []
        for stage in root.findall('.//User/Stage'):
            stage_type = stage.get('Type')
            start_time = int(stage.get('Start'))

            if stage_type == type:
                if len(time_pair) == 0:
                    time_pair.append(start_time)
            else:
                if len(time_pair) == 1:
                    time_pair.append(start_time)
                    time_intervals.append(time_pair)
                    time_pair = []

        return time_intervals     

    def find_intervals_machine(type, root):
        time_intervals = []
        time_pair = []
        for stage in root.findall('.//Machine/Stage'):
            stage_type = stage.get('Type')
            start_time = int(stage.get('Start'))

            if stage_type == type:
                if len(time_pair) == 0:
                    time_pair.append(start_time)
            else:
                if len(time_pair) == 1:
                    time_pair.append(start_time)
                    time_intervals.append(time_pair)
                    time_pair = []

        return time_intervals     

    def calculate_overlapping_rangetimes_for_stages(user_stage_times, machine_stage_times):
        t1_tree = IntervalTree(Interval(start, end) for start, end in user_stage_times)
        exact_overlaps = []
        for start, end in machine_stage_times:
            overlapping_intervals = t1_tree.overlap(start, end)
            for interval in overlapping_intervals:
                # Calculate exact overlap
                overlap_start = max(interval.begin, start)
                overlap_end = min(interval.end, end)
                exact_overlaps.append((overlap_start, overlap_end))
        return exact_overlaps

    def plot_sleep_stages(user_stage_times, machine_stage_times, overlaps):
        max_time = max(max(end for start, end in user_stage_times), max(end for start, end in machine_stage_times), max(end for start, end in overlaps))

        x = np.arange(0, max_time + 1, 0.01)
        y1 = np.zeros_like(x)
        y2 = np.zeros_like(x)
        y3 = np.zeros_like(x)

        def mark_intervals(y, intervals):
            for start, end in intervals:
                y[(x >= start) & (x <= end)] = 1

        mark_intervals(y1, user_stage_times)
        mark_intervals(y2, machine_stage_times)
        mark_intervals(y3, overlaps)

        plt.figure(figsize=(10, 6))
        plt.plot(x, y1, label='user wake times', color='blue')
        plt.plot(x, y2, label='machine wake times', color='purple')
        plt.plot(x, y3, label='wake overlaps', color='red')
        plt.xlabel('Time')
        plt.ylabel('Active (1) / Inactive (0)')
        plt.title('Time Interval Sets')
        plt.legend()
        plt.grid(True)
        plt.show()



        



        



    
    
    

