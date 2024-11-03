# Vid Sync
## A Simple YouTube Multi-Video Playback Syncing Tool

This project provides a wonky solution to a niche problem. The website [ViewSync](https://viewsync.net) allows users to watch multiple YouTube videos at the same time while setting a time offset for each video. This is great for watching different POVs of an event. 

We present a solution that (kind of) eliminates the need for manual alignment. We use audio data to obtain a set of time offsets of given YouTube URLs and generate a link to open [ViewSync](https://viewsync.net) player directly.

### Algorithm
Our algorithm compares all unique pairs of signals extracted from the audio file to maximize their correlation. First, the two signals are appended by silence to allow for all possible lag configurations. To these padded signals, we then apply the Fourier transform which allows us to access the frequency domain of the signals which naturally encodes information of the signals. 

$$X_k = \sum_{n=0}^{N-1} x_n e^{-i \frac{2 \pi}{N} k n}$$

In the frequency domain, we then compute the correlation of the two signals

$$\sum_{k=1}^{N-1} X_kY_k^*$$

and apply the inverse Fourier transform

$$x_n = \frac{1}{N} \sum_{k=0}^{N-1} X_k e^{i \frac{2 \pi}{N} k n}$$

This correlation function is then maximized to compute the temporal offset that maximizes allignment and coherence of the signals. This computation is performed and the computed optimal lags are added up. Finally we set the minimal lag needed for synchronization to 0, keeping the relative lags equal.

### Example Video Sets
Here are a couple of sets of YouTube videos that can be synchronized by our application. And this is the link to our [Demo Site](https://hacktx-demo.cyano.moe/). Simply copy the links one by one in each group into our website, and click "Kick off sync". After a while, once the loading animation disappears, you will be presented with a link and a button that takes you to the [ViewSync](https://viewsync.net) website. Just follow the instructions there to enjoy different POVs of the same event all at once. 

- Popping Battle
    - [Greentek vs Dnoi | Top Status (Top 4 Popping)](https://www.youtube.com/watch?v=0DJROtE68FA)
    - [Dnoi Vs Greentek | Popping Battles | Freestyle Session 2017](https://www.youtube.com/watch?v=h-82WLvKZgs)

- FWMC MINECRAFT JOURNEY (VTuber)
    - [【FWMC MINECRAFT JOURNEY】memories of minecraft are a bit fuzzy 🐾【MOCOCO POV】](https://www.youtube.com/watch?v=zkGA5X3tY_E)
    - [【FWMC MINECRAFT JOURNEY】memories of minecraft are always fluffy 🐾【FUWAWA POV】](https://www.youtube.com/watch?v=K7fkr0TrIvQ)
- Hololive Overwatch 2 Collaboration
    - [【Overwatch 2】gugugaga](https://www.youtube.com/watch?v=HKZ0_UQvaOw)
    - [【OVERWATCH 2】Full Team Collab !!! with Ame, IRyS, Zeta, and Bijou !](https://www.youtube.com/watch?v=ej85EfL1HYU)
    - [【OVERWATCH 2】Full Team Collab !!! with Ame, IRyS, Zeta, and Bijou !](https://www.youtube.com/watch?v=7MtuoPeC4tE)
    - [【OVERWATCH 2】Full Team Collab !!! with Ame, IRyS, Zeta, and Bijou !](https://www.youtube.com/watch?v=8B2Je1pZVpo)  

