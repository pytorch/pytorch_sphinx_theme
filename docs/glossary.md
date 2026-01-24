(glossary)=
# PyTorch Glossary

This glossary provides definitions for terms commonly used in PyTorch documentation.

```{glossary}
ATen
    Short for "A Tensor Library". The foundational tensor and mathematical operation library on which all else is built.

Compound Kernel
    Opposed to {term}`Device Kernel`s, Compound kernels are usually device-agnostic and belong to {term}`Compound Operation`s.

Compound Operation
    A Compound Operation is composed of other {term}`Operation`s. Its {term}`Kernel` is usually device-agnostic. Normally it doesn't have its own derivative functions defined. Instead, AutoGrad automatically computes its derivative based on operations it uses.

Composite Operation
    Same as {term}`Compound Operation`.

Custom Operation
    An {term}`Operation` defined by users, usually a {term}`Compound Operation`. For example, this [tutorial](https://pytorch.org/docs/stable/notes/extending.html) details how to create Custom Operations.

Device Kernel
    Device-specific {term}`Kernel` of a {term}`Leaf Operation`.

JIT
    Just-In-Time Compilation.

Kernel
    Implementation of a PyTorch {term}`Operation`, specifying what should be done when an operation executes.

Leaf Operation
    An {term}`Operation` that's considered a basic operation, as opposed to a {term}`Compound Operation`. Leaf Operation always has dispatch functions defined, usually has a derivative function defined as well.

Native Operation
    An {term}`Operation` that comes natively with PyTorch ATen, for example `aten::matmul`.

Non-Leaf Operation
    Same as {term}`Compound Operation`.

Operation
    A unit of work. For example, the work of matrix multiplication is an operation called `aten::matmul`.

Scripting
    Using `torch.jit.script` on a function to inspect source code and compile it as {term}`TorchScript` code.

TorchScript
    Deprecated. An interface to the TorchScript {term}`JIT` compiler and interpreter.

Tracing
    Using `torch.jit.trace` on a function to get an executable that can be optimized using just-in-time compilation.
```
