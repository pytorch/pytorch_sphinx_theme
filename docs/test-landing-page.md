---
meta:
  template: landing
  landing-show-search: "true"
  description: PyTorch Documentation - A comprehensive guide to PyTorch libraries and tools
---

# PyTorch Documentation

```{landingsearchbar}
:placeholder: Ask PyTorch Assistant...
:style: prominent
```

## Core Libraries

````{landingcardgrid}
:columns: 3

```{landingcard}
:title: PyTorch
:link: https://pytorch.org/docs/stable/

Open source machine learning framework for tensors and neural networks
```

```{landingcard}
:title: TorchVision
:link: https://pytorch.org/vision/stable/

Datasets, transforms and models for computer vision
```

```{landingcard}
:title: TorchAudio
:link: https://pytorch.org/audio/stable/

Audio processing tools and pretrained models
```

```{landingcard}
:title: TorchText
:link: https://pytorch.org/text/stable/

Text processing utilities and datasets for NLP
```

```{landingcard}
:title: TorchRec
:link: https://pytorch.org/torchrec/

Domain library for recommendation systems
```

```{landingcard}
:title: TorchServe
:link: https://pytorch.org/serve/

Model serving framework for PyTorch models
```
````

## Deployment & Inference

````{landingcardgrid}
:columns: 3

```{landingcard}
:title: TorchScript
:link: https://pytorch.org/docs/stable/jit.html

Serialize and optimize PyTorch models for production
```

```{landingcard}
:title: ExecuTorch
:link: https://pytorch.org/executorch/

Deploy PyTorch models to edge devices
```

```{landingcard}
:title: ONNX Export
:link: https://pytorch.org/docs/stable/onnx.html

Export models to ONNX format for interoperability
```
````

## Distributed Training

````{landingcardgrid}
:columns: 2

```{landingcard}
:title: Distributed Data Parallel
:link: https://pytorch.org/docs/stable/distributed.html

Train models across multiple GPUs and nodes
```

```{landingcard}
:title: FSDP
:link: https://pytorch.org/docs/stable/fsdp.html

Fully Sharded Data Parallel for large model training
```
````

## Using the Landing Page Template

To use this landing page template on your own pages, add the following frontmatter at the top of your `.md` file:

```yaml
---
meta:
  template: landing
  landing-show-search: "true"
  description: Your page description here
---
```

The available options are:

- `template: landing` - Activates the landing page layout (left sidebar only, no right TOC)
- `landing-show-search: "true"` - Shows a prominent search bar at the top (optional)
- `description:` - Sets the page description for SEO and LLM metadata

If no `template` is specified, the page uses the default layout with both sidebars.

## Card Usage

Use the `landingcardgrid` and `landingcard` directives:

````markdown
```{landingcardgrid}
:columns: 3

```{landingcard}
:title: Card Title
:link: /path/to/page.html

Card description text
```

```{landingcard}
:title: Another Card
:link: /another/page.html

Another description
```
````

Available column options: `2`, `3`, or `4`.
