# MyST Directives Test Page

This page tests all common MyST and sphinx-design directives to verify they render
correctly with the PyTorch Sphinx theme.

## Dropdowns

### Basic Dropdown

```{dropdown} More details on mutation and aliasing
`custom_op` asks for a precise mutation and aliasing contract because PyTorch
uses that contract in `FakeTensor`, `autograd`, `functionalization`, and
`torch.compile`.

For a functional `custom_op`, PyTorch assumes the operator does not mutate
any input and that returned tensors are fresh values. This is the easiest
kind of op to set up for `torch.compile`.

For an in-place `custom_op`, `torch.Tag.inplace` gives PyTorch a stronger
and more specific contract: the first argument and the returned object are
the same object. This lets PyTorch derive the fake-tensor behavior from
the schema instead of requiring a separate fake kernel.
```

### Dropdown with Title and Open by Default

```{dropdown} Click to expand this section
:open:

This dropdown is open by default. It contains some code:

    import torch
    x = torch.randn(3, 4)
    print(x)
```

### Dropdown with Admonition Style

```{dropdown} Important implementation note
:color: warning

This is a dropdown styled as a warning. Be careful when using this API
as it may change in future versions.

- Point one about the API
- Point two about compatibility
- Point three about deprecation timeline
```

```{dropdown} Tip: Performance optimization
:color: success

Use `torch.compile` for best performance:

    model = torch.compile(model)
```

## Admonitions

```{note}
This is a note admonition. Use it to highlight important information.
```

```{warning}
This is a warning. Proceed with caution when using experimental APIs.
```

```{tip}
Use `torch.no_grad()` context manager to disable gradient computation
during inference for better performance.
```

```{important}
Always call `model.eval()` before inference and `model.train()` before training.
```

```{caution}
Mixing CPU and CUDA tensors in operations will raise a `RuntimeError`.
```

```{danger}
Never store sensitive data in model checkpoint files without encryption.
```

```{seealso}
See the [PyTorch documentation](https://pytorch.org/docs/) for more details.
```

```{hint}
You can use `torch.cuda.is_available()` to check for GPU availability.
```

### Custom Titled Admonition

```{admonition} Custom Title Here
:class: tip

This is an admonition with a custom title styled as a tip.
```

## Tab Sets

````{tab-set}

```{tab-item} Python
Use Python for most deep learning tasks:

    import torch
    x = torch.tensor([1.0, 2.0, 3.0])
```

```{tab-item} C++
Use the C++ frontend for production:

    #include <torch/torch.h>
    auto x = torch::tensor({1.0, 2.0, 3.0});
```

```{tab-item} CLI
Use the CLI for quick experiments:

    python -m torch.utils.benchmark
```
````

## Cards

### Standalone Card

```{card} Getting Started with PyTorch
:link: https://pytorch.org/tutorials/
:link-type: url

Learn the basics of PyTorch with our beginner tutorials. Covers tensors,
autograd, neural networks, and more.
+++
Footer content
```

### Card Grid

::::{grid} 2
:::{grid-item-card} Training
:link: https://pytorch.org
:link-type: url
:class-card: card-prerequisites

Learn how to train models with PyTorch.
:::

:::{grid-item-card} Deployment
:link: https://pytorch.org
:link-type: url
:class-card: card-prerequisites

Deploy models to production with TorchServe.
:::
::::

## Badges and Buttons

{bdg}`plain badge`
{bdg-primary}`primary`
{bdg-secondary}`secondary`
{bdg-success}`success`
{bdg-warning}`warning`
{bdg-danger}`danger`
{bdg-info}`info`
{bdg-light}`light`
{bdg-dark}`dark`

### Outline Badges

{bdg-primary-line}`primary outline`
{bdg-warning-line}`warning outline`
{bdg-success-line}`success outline`

### Buttons

```{button-link} https://pytorch.org
:color: primary

Go to PyTorch
```

```{button-link} https://pytorch.org/docs/
:color: secondary
:outline:

View Documentation
```

## Definition Lists

Term 1
: Definition of the first term. This can span
  multiple lines.

Term 2
: Definition of the second term.

`torch.Tensor`
: The main data structure in PyTorch. A multi-dimensional matrix
  containing elements of a single data type.

## Field Lists

:Author: PyTorch Team
:Version: 2.0
:Status: Stable
:License: BSD-3

## Task Lists

- [x] Install PyTorch
- [x] Set up development environment
- [ ] Train first model
- [ ] Deploy to production

## Substitutions

This project is called {{project_name}} version {{version_num}}.

## Code Blocks

```{code-block} python
:linenos:
:emphasize-lines: 2, 4

import torch
import torch.nn as nn

model = nn.Linear(10, 5)
x = torch.randn(3, 10)
output = model(x)
print(output.shape)
```

```{code-block} bash
:caption: Installation command

pip install torch torchvision torchaudio
```

## Math

```{math}
\nabla_\theta J(\theta) = \mathbb{E}_{\pi_\theta} \left[ \sum_{t=0}^{T} \nabla_\theta \log \pi_\theta(a_t|s_t) \cdot G_t \right]
```

Inline math: {math}`E = mc^2`

## Tables

```{list-table} Comparison of Optimizers
:header-rows: 1
:widths: 20 40 20 20

* - Optimizer
  - Description
  - Learning Rate
  - Momentum
* - SGD
  - Stochastic Gradient Descent
  - 0.01
  - 0.9
* - Adam
  - Adaptive Moment Estimation
  - 0.001
  - N/A
* - AdamW
  - Adam with weight decay
  - 0.001
  - N/A
```

## Figures

```{figure} https://pytorch.org/assets/images/pytorch-logo.png
:alt: PyTorch Logo
:width: 200px
:align: center

The PyTorch logo.
```

## Block Attributes

The `attrs_block` extension lets you attach HTML attributes (classes, IDs) to
the next block element using `{.classname}` or `{#id}` syntax.

{.sd-text-primary}
This paragraph is styled with the `sd-text-primary` class via attrs_block.

{.sd-bg-light .sd-p-3 .sd-rounded-3}
This paragraph has a light background, padding, and rounded corners.

## Toggles (Nested Dropdowns)

::::{dropdown} Outer dropdown
This is the outer content.

:::{dropdown} Inner dropdown
This is nested inside the outer dropdown.
:::
::::

## Sphinx-Design Containers

::::{grid} 3
:gutter: 2

:::{grid-item}
:columns: 12 6 6 4

### Column 1
Content in the first column of a responsive grid.
:::

:::{grid-item}
:columns: 12 6 6 4

### Column 2
Content in the second column.
:::

:::{grid-item}
:columns: 12 12 12 4

### Column 3
Content in the third column. On mobile, all columns stack vertically.
:::
::::
