## Datasets

The datasets used in this paper are released in three versions (e.g. containing 200, 500, and 1000 training tasks) for evaluating data efficiency. We use the `logo_unlimited_200` and `re2_1000` datasets in the paper.
All datasets have the following directory structure.

```
|_ logo                           # Domain name.
  |__ language                    # Contains language datasets.
      |__logo_unlimited_200       # Dataset version (e.g. 200 tasks.)
          |_ synthetic            # Synthetic language data.
              |_train
                |_ language.json  # Language annotations.
                |_ vocab.json     # Vocabulary.
              |_test ...
          |_ human   ...          # Where available, human language data.
      |...
  |
  |__ tasks                       # Contains task example specification.
      |__logo_unlimited_200       # Dataset version.
          |_ train                # Contains domain-specific tasks.
          |_ test
```

Domain-specific loaders are provided for each dataset. See Training, below.

###### String Editing Domain

The string editing (regex) dataset is available on Zenodo [here](https://zenodo.org/record/3889088#.XuGEWp5KhTY).
The unzipped dataset should be stored in `data/re2`. Our paper uses the `re2_1000` dataset (consisting of 1000 training tasks and 500 testing tasks).
The dataset tasks and human language comes from the regex domain in *Learning with Latent Language* (Andreas et. al, 2017) [[paper](https://arxiv.org/abs/1711.00482)] [[code](https://github.com/jacobandreas/l3)]

This dataset contains synthetic language and human language for all three training task versions. Tasks are stored in JSON containing the example inputs and outputs, but can be loaded with the domain-specific dataset loader.

###### Compositional Graphics Domain

The graphics programs (LOGO) dataset is available on Zenodo [here](https://doi.org/10.5281/zenodo.3889096).
The unzipped dataset should be stored in `data/logo`. Our paper uses the `logo_unlimited_200` dataset (consisting of 200 training tasks and 111 testing tasks).

This dataset contains synthetic language for the 200, 500, and 1000 training task versions (and the 111 testing tasks); and human data for the 200 task version. We also provide rendered images for each task. Tasks are stored in the codebase-specific task format (which includes ground truth programs), and must be loaded through this repository (see Training).

The repository also contains code to generate the compositional graphics datasets from scratch (and synthetic language).

```
python bin/logo.py \
--generateTaskDataset [logo_unlimited_200 | logo_unlimited_500 | logo_unlimited_500] \
--generateLanguageDataset [logo_unlimited_200 | logo_unlimited_500 | logo_unlimited_500] \
```

###### Scene Reasoning Domain

The scene reasoning dataset is available on Zenodo [here](https://doi.org/10.5281/zenodo.4533370).
The unzipped dataset should be stored in `data/clevr`.

Code to generate the scene reasoning datasets and their synthetic annotations, as well as to render the images, is provided at this repository [here](https://github.com/CatherineWong/too_clevr) [Warning: this is a link to a live GitHub repository. Do not click during the review period].
This code builds on the CLEVR generation code from *CLEVR: A Diagnostic Dataset for Compositional Language and Elementary Visual Reasoning*(Johson et. al, 2017)[[paper](http://cs.stanford.edu/people/jcjohns/clevr/)] [[code](https://github.com/facebookresearch/clevr-dataset-gen)]
