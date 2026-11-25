<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset=".github/brand/brainlife-mark-on-dark.svg">
    <img src=".github/brand/brainlife-mark-on-light.svg" alt="brainlife.io" width="140">
  </picture>
</p>

<h1 align="center">validator-neuro-wmc</h1>

<p align="center">
  Checks <code>neuro/wmc</code> datasets before brainlife.io archives them.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Status-maintained-blue.svg" alt="Status: maintained">
  <a href="https://brainlife.io"><img src="https://img.shields.io/badge/brainlife.io-site-3b9fd0.svg" alt="brainlife.io"></a>
  <a href="https://brainlife.io/docs"><img src="https://img.shields.io/badge/Docs-brainlife.io%2Fdocs-005981.svg" alt="Documentation"></a>
  <a href="https://doi.org/10.1038/s41592-024-02237-2"><img src="https://img.shields.io/badge/DOI-10.1038%2Fs41592--024--02237--2-e57536.svg" alt="Nature Methods paper"></a>
</p>

## 🧠 At a glance

| | |
|---|---|
| 🗂️ **Datatype** | `neuro/wmc` |
| 🐳 **Container** | brainlife/dipy:1.1.1 |
| 📜 **Script** | [`validate.py`](validate.py) |
| 🕰️ **Last change** | 2021-11-29 |

## ✅ What it checks

- `classification.mat` exists and holds a classification with `names` and `index`
- Names have no whitespace and are unique
- `names` is at least as long as the number of distinct index values; warns about tracts with 0 streamlines

## ⚙️ How brainlife.io runs it

Each brainlife datatype names a validator. When a dataset of that datatype is uploaded (or written by an App), brainlife.io runs this repository like an App: `main` reads `config.json` (one key per file of the datatype), runs `validate.py`, writes `product.json` with `errors` and `warnings` (and sometimes tags, datatype tags or summary plots) and links the normalized files into `output/`. Errors fail the validation; warnings are shown with the dataset.

## 💻 Run it locally

```bash
git clone https://github.com/brainlife/validator-neuro-wmc && cd validator-neuro-wmc
cp config.json.sample config.json        # point each key at your files
./main
cat product.json
```

Needs Singularity/Apptainer.

<details>
<summary><b>📝 Valid and invalid WMC examples</b></summary>

Valid (index 2 and 3 have no streamlines, which gives a warning):

```
names: ['tractA', 'tractB', 'tractC']
index: [0, 0, 1]
```

Invalid: the last index (4) exceeds the length of `names`; names contain spaces and a duplicate:

```
names: ['tract A', 'tract B', 'tract B']
index: [0, 0, 1, 0, 2, 0, 0, 3, 3, 4]
```

See the datatype definition at [brainlife.io/datatype/5cc1d64c44947d8aea6b2d8b](https://brainlife.io/datatype/5cc1d64c44947d8aea6b2d8b).

</details>

## 🔗 Related

[warehouse-next](https://github.com/brainlife/warehouse-next) (datatypes and validation) · [abcd-spec](https://github.com/brainlife/abcd-spec) (how Apps and validators run) · [all validators](https://github.com/brainlife?q=validator-&type=all)

## 📚 Citing

If you use brainlife.io in your work, please cite:

> Hayashi S, Caron BA, Heinsfeld AS, et al. brainlife.io: a decentralized and open-source cloud platform to support neuroscience research. *Nature Methods* 21:809–813 (2024). [doi:10.1038/s41592-024-02237-2](https://doi.org/10.1038/s41592-024-02237-2)

## 🤝 Contributing

Issues and pull requests are welcome in this repository. For help using brainlife.io, see the [documentation](https://brainlife.io/docs).

## ⚖️ License

This repository does not include a license file yet.

<p align="center"><sub>brainlife.io · Brain data across scales. One place to analyze, share and publish it. · The University of Texas at Austin</sub></p>
