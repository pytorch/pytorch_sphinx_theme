(torch.compiler_ir)=

# IRs

PyTorch 2.0 offers two set of IRs for backends to interface with: Core {term}`ATen` IR and Prims IR.

## Core ATen IR

Core {term}`aten<ATen>` ops is the core subset of {term}`aten<ATen>` operators that can be used to compose other operators.
Core {term}`aten<ATen>` IR is fully functional, and there is no `inplace` or `_out` variants in this opset.
In contrast to Prims IR, core {term}`aten<ATen>` ops reuses the existing {term}`aten<ATen>` ops in "native_functions.yaml",
and it doesn't further decompose ops into explicit type promotion and broadcasting ops.
This opset is designed to serve as the functional IR to interface with backends.

```{warning}
  This opset is still under active development, more ops will be added in the future.
```

## Prims IR

Prims IR is a set of primitive operators that can be used to compose other operators.
Prims IR is a lower level opset than core aten IR, and it further decomposes ops into explicit
type promotion and broadcasting ops: prims.convert_element_type and prims.broadcast_in_dim.
This opset is designed to interface with compiler backends.

```{warning}
  This opset is still under active development, more ops will be added in the future.
```

## Glossary Terms Demo

This section demonstrates tooltips for various glossary terms. Hover over the highlighted terms to see their definitions.

### Operations

An {term}`Operation` is a unit of work in PyTorch. There are different types of operations:

- **{term}`Native Operation`**: Operations that come natively with PyTorch ATen
- **{term}`Custom Operation`**: Operations defined by users, usually a {term}`Compound Operation`
- **{term}`Leaf Operation`**: Basic operations that always have dispatch functions defined
- **{term}`Compound Operation`**: Operations composed of other operations (also known as {term}`Composite Operation` or {term}`Non-Leaf Operation`)

### Kernels

A {term}`Kernel` is the implementation of a PyTorch operation. There are two main types:

- **{term}`Device Kernel`**: Device-specific kernel of a {term}`Leaf Operation`
- **{term}`Compound Kernel`**: Device-agnostic kernels that belong to {term}`Compound Operations<Compound Operation>`

### JIT Compilation

PyTorch supports {term}`JIT` (Just-In-Time) compilation through {term}`TorchScript`. There are two main approaches:

1. **{term}`Tracing`**: Using `torch.jit.trace` on a function to get an executable that can be optimized
2. **{term}`Scripting`**: Using `torch.jit.script` to inspect source code and compile it as {term}`TorchScript` code

### Summary Table

| Term | Type | Description |
|------|------|-------------|
| {term}`ATen` | Library | Foundational tensor library |
| {term}`Operation` | Concept | Unit of work |
| {term}`Kernel` | Implementation | What happens when an operation executes |
| {term}`JIT` | Technique | Just-In-Time Compilation |
| {term}`TorchScript` | Interface | JIT compiler and interpreter |

## Intersphinx References

Note: Intersphinx tooltips only work with documentation hosted on Read the Docs that has the embed API enabled.
Most external documentation sites (docs.python.org, docs.pytorch.org, numpy.org) do not support this feature.

The following are standard intersphinx links (clickable but without tooltips):

- {py:class}`torch:torch.Tensor` - The main tensor class
- {py:func}`torch:torch.zeros` - Create a tensor of zeros
- {py:class}`python:list` - Python's built-in list type
