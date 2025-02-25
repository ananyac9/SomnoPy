# Polysomnography Analyser

![PyPI Version](https://img.shields.io/pypi/v/SomnoPy.svg)
[![Build Status](https://img.shields.io/travis/ananyac9/SomnoPy.svg)](https://travis-ci.com/ananyac9/SomnoPy)
[![Documentation Status](https://readthedocs.org/projects/psg-analyser/badge/?version=latest)](https://psg-analyser.readthedocs.io/en/latest/?version=latest)

Exploratory data analysis and crude sleep scoring for OSA reports.

-   **Free software:** MIT license
-   **Documentation:** [psg-analyser.readthedocs.io](https://psg-analyser.readthedocs.io)

## Import:

```python
from somnopy import EDA, CrudeScoring, SleepStages
```

## EDA:

### Reading signal from EDF file

```python
read_file_signal(file_path, index)
```

where `index` is the index of the channel.

### Obtaining channel labels

```python
signal_labels(file_path)
```

### Combining signals from multiple files

```python
combined_signal_from_files(file_list, index)
```

where `file_list` is a list of EDF file paths and `index` is the index of the channel.

### Combining signals from a list of signals

```python
combined_signal_from_signals(signal_list, index)
```

where `signal_list` is a list of signals.

### Plotting a signal

```python
plot_signal(label, signal)
```

where `label` is the signal label and `signal` is the signal data.

### Thresholding a signal

```python
thresholding(signal, threshold, replace_with)
```

where `threshold` is the standard deviation multiplier and `replace_with` is the replacement value.

### Resampling a signal

```python
resample_signal(signal, num_samples)
```

where `num_samples` is the desired number of samples.

### Calculating coefficient of variation for a list of signals

```python
channel_coeff_of_var(signal_list)
```

where `signal_list` is a list of signals
it returns the coefficient of variation of that channel

### Plotting coefficient of variation as a line plot

```python
coeff_of_var_line_plot(cv_dict)
```

where `cv_dict` is a dictionary of channel names and coefficient of variation values.

### Plotting coefficient of variation as a heatmap

```python
coeff_of_var_heatmap(cv_dict)
```

### Plotting a dendrogram for coefficient of variation

```python
plot_cv_dendrogram(cv_dict)
```

### Plotting a log-transformed dendrogram for coefficient of variation

```python
plot_log_cv_dendrogram(cv_dict)
```

### Dividing a signal into equal time segments

```python
time_division_of_signals(signal, num_divisions)
```

### Calculating hourly coefficient of variation

```python
hourly_coeff_of_var(normal, mild, moderate, severe, num_divisions)
```

gives coefficient of varitation across all channels for the different time segments

### Principal Component Analysis (PCA) of channels

```python
principle_comp_analysis_of_channels(df, n)
```

where `df` has channels as rows and time as columns, and `n` is the number of principal components.

### Calculating rolling mean of a signal

```python
rolling_mean(signal, window_size)
```

where `window_size` is the size of the moving window.

### Performing FFT on a signal

```python
signal_fft(signal, sampling_rate)
```

where `sampling_rate` is the frequency at which the signal is recorded.
output is [fft_result, frequencies, magnitude_spectrum]

### Reconstructing a signal from FFT components

```python
reconstruct_signal(fft_result, threshold=20)
```

where `threshold` is the number of frequency components retained.

### Plotting original and reconstructed signals

```python
plot_fft(signal, reconstructed_signal)
```

## CrudeScoring:

### Generating timestamps for scoring

```python
get_timestamps_for_scoring(signal, freq)
```

where `freq` is the sampling frequency.

### Counting obstructive apnea events

```python
count_obstructive_apnea(fp2_signal, freq, timestamps)
```

where `fp2_signal` is the FP2 signal and `timestamps` are the corresponding time points.

### Plotting FP2 signal with apnea drops

```python
plot_signal_with_apnea_drops(fp2_signal, timestamps)
```

### Counting obstructive hypopnea events

```python
count_obstructive_hypopnea(fp1_data, spo2_data, freq, timestamps)
```

where `fp1_data` is the FP1 signal and `spo2_data` is the SpO2 signal.

### Plotting FP1 and SpO2 signals with hypopnea drops

```python
plot_signals_with_hypopnea_drops(fp1_data, spo2_data, timestamps)
```

### Calculating Apnea-Hypopnea Index (AHI)

```python
apnea_hypopnea_index(apnea_counts, hypopnea_counts)
```

### Zoomed-in plot for obstructive apnea event

```python
zoomed_plot_oa(start_time, end_time, signal, hour)
```

where `start_time` and `end_time` are the event boundaries, and `hour` represents the hour of recording.

## Sleep Stages:

### Parsing user-defined sleep stages from XML

```python
parse_stages_user(file_path)
```

where file_path is the path to the XML file.

### Parsing machine-defined sleep stages from XML

```python
parse_stages_machine(file_path)
```

where file_path is the path to the XML file.

### Retrieving the root of an XML file

```python
get_root(file_path)
```

where file_path is the path to the XML file.

### Finding time intervals for user-defined sleep stages

```python
find_intervals_user(type, root)
```

where type is the sleep stage type and root is the XML root.

### Finding time intervals for machine-defined sleep stages

```python
find_intervals_machine(type, root)
```

where type is the sleep stage type and root is the XML root.

### Calculating overlapping time ranges for sleep stages

```python
calculate_overlapping_rangetimes_for_stages(user_stage_times, machine_stage_times)
```

where user_stage_times and machine_stage_times are lists of time intervals.

### Plotting sleep stages and overlaps

```python
plot_sleep_stages(user_stage_times, machine_stage_times, overlaps)
```

where user_stage_times, machine_stage_times, and overlaps are lists of time intervals.

## Credits

This package was created with Cookiecutter* and the `audreyr/cookiecutter-pypackage`* project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
