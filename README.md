# Archon 
![Archon Flow](https://user-images.githubusercontent.com/29315147/169671284-69a5be7d-8212-43d4-bfd0-f12ef9069e3a.png)

## 1. Overview
Archon is an open-source interface designed for Demiurge, a generative performance ecosystem powered by machine learning (developed in collaboration with [Marek Poliks](https://robertoalonsotrillo.com/projects/)). It can be used with any database of lossless audio stored on Google Drive.

Demiurge and Archon were built with the belief that the music of the future will take post-work as a point of departure, supplanting instruments with style transfer, sample library generation, and pattern proliferation, replacing the studio itself with readymade conformity-driven operations. Musical activities will consist of higher-level curatorial actions at the level of genre or mood or intensity. In liberating music from musicians, one both liberates its future from anthropocentric bias and accelerates its death-drive. [Demiurge](www.marekpoliks.com/demiurge), [Hydra](www.marekpoliks.com/hydra), and [Archon](www.marekpoliks.com/archon) go nowhere near accomplishing this vision, but are nevertheless committed to its realization.

Archon is written in Python and Supercollider, and will be developed over the course of 2022. Its function is to mediate between human and database, a neglected instrumentality. Unlike existing work in concatenative synthesis, Archon is both realtime (GPU accelerated) and behaviorally adaptive to audio signal. 

At present, Archon is ready for v0 testing - play around with database consolidation, descriptor extraction, and live feature matching. Archon will adapt database playback machine morphology over time based on probabilistic responses to live input and is highly reactive to performance.

![1C72CCFA-BA42-4AA9-8B52-004A18D58180](https://user-images.githubusercontent.com/29315147/169711042-dc4a23f0-89e6-4b52-8819-f86086409b9f.JPG)

## 2. Extraction
The '/utilities' folder has many scripts that can be useful to prepare your audio database, from any accessible directory within GDrive. 

a. `archon_split.ipynb` is a Colab notebook that grabs audio from walking through a directory and splices it into homogenous chunks. Since many collaborative directories, especially those used in machine learning, often have lots of duplicates, the `archon_dedupe.ipynb` script uses file hash to trim out any redundant material from your target directory.
b. `archon_analyze.ipynb` has two components. First, a script that extracts median descriptors across the length of each sample (this will ultimately be developed for greater granularity, but for short splices like 500ms it works great). Second, there's an optional script that reorganizes the target directory by descriptor. This is definitely optional, but dealing with GDrive downloading can be a headache without this. (I don't recommend using Google Takeout, which can compromise filenames and do weird things to you data, and instead break up your directories and download them independently with a separate script). There's an unsort argument here you can use to collapse everything back into the original flat directory structure.
c. `archon_post_processing.ipynb` gives you some insights into your data - histograms collected against each major descriptor type (showing pitched data only, unpitched data only, or both for maximum visibility into the contents of your workspace).

The recommended flow is to use the split and analyze scripts to diffract an existing database into many grains, analyze them, sort them, download them, and also download the analysis file (a JSON file) and place it in the directory you cloned this one into.

## 3. Supercollider Interface 
Once you've downloaded your audio, your analysis file, and this repo, move the library directory to your Supercollider Extensions directory (`/Library/Application Support/Supercollider/Extensions`). Then open up Supercollider, which will auto-compile the class library. 

Then poke around `archon_query.py` to get a sense of the arguments available to you, including specifying the location of the analysis file and your audio sample directory. The ports here are auto-specified to work with Supercollider, but if you see a mismatch when you boot `archon_brain.scd` you can easily make an adjustment by passing the `--output_port` argument with the relevant port that SC prints out for you.

To boot the SC script, just click anywhere within the SC editor and hit CMD+Enter (Mac). It will take a few seconds to load. You'll see `OK: Ready!` in the post window when it's time to proceed.

After it's ready, open up your command line editor, navigate to the directory where you cloned this repo, and run `python archon_query.py`. You may need to install torch/numpy/pandas/python_osc depending on your build (I'll have a script grab these in the future). This query can take a few seconds to minutes to load, depending on the size of your analysis file. It'll let you know it's serving on the localhost once you're good to go.

Make sure your headphones are plugged in and make some sound! Play around with the PKill function in the `archon_classes.sc` extension file for maximum fun. Stay tuned, this will grow quite a bit and I'll keep the readme up to date.
