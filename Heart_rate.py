import numpy as np
import imageio
import matplotlib.pyplot as plt

fps = 30
file_path = input('Enter the file path:')

#POST PROCESSING

video = imageio.get_reader(file_path, 'ffmpeg')
colors = {'red':[],'green':[],'blue':[]}
for frame in video:
    lumped_pixel = np.mean(frame,axis=(0,1))
    colors['red'].append(lumped_pixel[0])
    colors['green'].append(lumped_pixel[1])
    colors['blue'].append(lumped_pixel[2])
for key in colors:
    colors[key] = np.divide(colors[key],255)
x = np.arange(len(colors['red'])) / fps

#FILTTERING DATA

colors['red_filt'] = list() 
colors['red_filt'] = np.append(colors['red_filt'], colors['red'][0])
tau = 0.25
fsample = fps
alpha = tau / (tau + 2/fsample)
for index, frame in enumerate(colors['red']): 
    if index > 0:
        y_prev= colors['red_filt'][index - 1]
        x_curr= colors['red'][index]
        x_prev= colors['red'][index - 1]
        colors['red_filt'] = np.append(colors['red_filt'], alpha*(y_prev + x_curr - x_prev))
x_filt = x[50:-1]
colors['red_filt'] = colors['red_filt'][50:-1]

#PERFORMING FFT ON DATA

red_fft = np.absolute(np.fft.fft(colors['red_filt']))
N = len(colors['red_filt'])
freqs = np.arange(0,fsample/2,fsample/N)
red_fft = red_fft[0:len(freqs)]

#MEASURING HEARTRATE FROM FFT

max_val = 0
max_index = 0
for index, fft_val in enumerate(red_fft):
    if fft_val > max_val:
        max_val = fft_val
        max_index = index
heartrate = freqs[max_index]*60
print('Estimated Heartrate: {} bpm'.format(heartrate))
