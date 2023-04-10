# Leveraging Language for Abstraction and Program Search

This repository is adapted from [the official LAPS branch of the dreamcoder repo](https://github.com/ellisk42/ec/tree/icml_2021_supplement) used in Leveraging Language for Abstraction and Program Search (ICML 2021, Wong et. al 2021). That branch was a static branch designed to reproduce the results in the paper, whereas this provides a template for future work using the DreamCoder/LAPS software.

## Installation

The following setup has been tested on a macOS Ventura 13.2 machine. The codebase is implemented in both Python and OCaml. 

##### Install Python 3.9.16 and the Python requirements.

1. On macOS, one can create a fresh install (including pip) with Homebrew as follows:

```
brew install python@3.9
pip install --upgrade setuptools
```

This (and subsequent instructions) assume that `pip` and `python3` have been correctly symlinked to the appropriate version of python (in this case, `python3.9`). If version errors occur, replacing `pip` with `pip3.9` and `python3` with `python3.9` should suffice in all following instructions.

2. Install the requirements.
   
   ```
   pip install -r requirements.txt
   ```

3. Download the NLTK Tokenizer. At an interactive Python prompt, run:
   
   ```
   > import nltk; nltk.download('punkt')
   ```

##### Build the OCaml binaries.

To build the OCaml binaries from scratch, you can run the following from the root of the repo. Tested on Ubuntu 18.04 and OS X 12.3 (M1).

1. Install Opam. (e.g. https://opam.ocaml.org/doc/Install.html)
   
   ```
   brew install opam
   ```

2. Install the OCaml dependencies.
   
   ```
   make setup-ocaml
   ```

3. Run the following from the directory root to build the binaries.
   
   ```
   make
   ```

The enumeration can be tested with

```
python3 bin/list.py --primitives McCarthy --dataset bootstrap --structurePenalty 1. --pseudoCounts 30 --arity 4 -t 10 --taskReranker unsolved --topK 5 --maximumFrontier 5 --CPUs 10
```

which will crash :) but not before successfully doing some enumeration

##### Download Moses.

The codebase uses the [Moses](http://www.statmt.org/moses/?n=Moses.Releases) statistical machine translation system to implement the joint generative model for translating between program and natural language tokens. This is only required if you are attempting to use LAPS, and is not required for DreamCoder installations.
On an Ubuntu 16.04 machine, you can download and use the prebuilt Moses binaries directly. (Binaries for [Ubuntu 17.04](http://www.statmt.org/moses/RELEASE-4.0/binaries/) are also available, as well as instructions for compiling from scratch on other architectures. As a caveat, we found this particularly hard to get working on a Mac machine, although instructions are available [here](http://www.statmt.org/moses/?n=Moses.Releases).)

From the root of the directory, run:

```
wget http://www.statmt.org/moses/RELEASE-4.0/binaries/ubuntu-16.04.tgz;
tar -xvf ubuntu-16.04.tgz; mv ubuntu-16.04/ moses_compiled;
rm -rf  ubuntu-16.04.tgz;
```

## Training and Evaluation

Scripts to run the algorithm on each of the domains are located in the `bin/` directory.
By default, as the algorithm is iterative, the training scripts will both run the algorithm for a specified number of iterations, and evaluate on a held-out test task every n iterations (where n is an adjustable argument.)

Running the commands below will produce fairly verbose log outputs that include evaluation metrics, and the location of the model checkpoint. In particular, running

```
grep 'checkpoint' [LOG_FILE]
```

will print out the path of the checkpoints at each iteration, and running

```
grep 'testing tasks' [LOG_FILE]
```

will print out the held-out task evaluation metrics.

It is also possible to resume and evaluate a model checkpoint from any iteration in training. By default, the scripts write timestamped checkpoints to a directory titled `experimentOutputs` (the exact directory appears with other informaiton in the output.)

The ```--resume [CHECKPOINT_PATH]``` commandline argument will resume training from a checkpoint, including to re-run evaluation tasks.

For additional information on the command line output (and default scripts to graph the outputs from the checkpoints), see docs/EC_README.md.

For additional information on adding new domains beyond those listed here, see docs/creating-new-domains.md.

For downloading the datasets and executing the tasks to reproduce results from the LAPS paper, please see docs/old-laps-readme.md.

##### Mathematical Equation Solving

The script to train and evaluate on the scene resaoning domain is located at `bin/mathDomain.py`.

```
python3 bin/mathDomain.py -RE 100
```

where the `-RE` argument quantifies the number of epochs the recognition model is allowed to run for. 

## Contributing

MIT License
Copyright (c) 2021 Catherine Wong

Copyright (c) 2023 Sagnik Anupam

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
