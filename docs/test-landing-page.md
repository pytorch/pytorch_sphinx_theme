---
myst:
  html_meta:
    "description lang=en": "Complete PyTorch Python API reference: tensors, neural networks (torch.nn), optimizers, autograd, torch.compile, torch.export, CUDA support, and more."
sd_hide_title: true
landing_page:
  intro:
    title: PyTorch API Reference
    description: Explore the complete PyTorch Python API documentation. Find detailed references for tensor operations, neural network layers (torch.nn), optimizers (torch.optim), automatic differentiation (autograd), model compilation (torch.compile), model export (torch.export), GPU acceleration, and distributed training.
  show_search: true
  full_link: true
  categories:
    - name: Core APIs
      tag: Core
      description: Essential PyTorch operations, tensors, and fundamental functionality
      items:
        - title: torch
          description: The core PyTorch namespace with tensor operations, random sampling, serialization, and fundamental functions.
          link: https://docs.pytorch.org/docs/stable/torch.html
          type: Module
          level: Essential
          featured: true
        - title: torch.Tensor
          description: Multi-dimensional matrix containing elements of a single data type. The fundamental data structure in PyTorch.
          link: https://docs.pytorch.org/docs/stable/tensors.html
          type: Class
          level: Essential
          featured: true
        - title: Tensor Attributes
          description: Properties and metadata associated with tensors including dtype, shape, device, layout, and more.
          link: https://docs.pytorch.org/docs/stable/tensor_attributes.html
          type: Reference
          level: Common
        - title: Tensor Views
          description: Memory-efficient views of tensor data that share the same underlying storage.
          link: https://docs.pytorch.org/docs/stable/tensor_view.html
          type: Reference
          level: Common
        - title: torch.autograd
          description: Automatic differentiation engine that powers neural network training in PyTorch.
          link: https://docs.pytorch.org/docs/stable/autograd.html
          type: Module
          level: Essential
          featured: true
        - title: Type Info
          description: Numerical properties of torch data types including finfo (float) and iinfo (integer).
          link: https://docs.pytorch.org/docs/stable/type_info.html
          type: Reference
          level: Advanced

    - name: Neural Networks
      tag: NN
      description: Building blocks for constructing and training neural networks
      items:
        - title: torch.nn
          description: Core building blocks for neural networks — layers, loss functions, containers, and utilities.
          link: https://docs.pytorch.org/docs/stable/nn.html
          type: Module
          level: Essential
          featured: true
        - title: torch.nn.functional
          description: Functional interface for neural network operations — convolutions, activations, losses, and pooling.
          link: https://docs.pytorch.org/docs/stable/nn.functional.html
          type: Module
          level: Essential
        - title: torch.nn.init
          description: Weight initialization strategies for neural network parameters.
          link: https://docs.pytorch.org/docs/stable/nn.init.html
          type: Module
          level: Common
        - title: torch.nn.utils
          description: Utility functions for neural networks including gradient clipping and weight normalization.
          link: https://docs.pytorch.org/docs/stable/nn.utils.html
          type: Module
          level: Common

    - name: Optimization
      tag: Optim
      description: Optimization algorithms and learning rate scheduling
      items:
        - title: torch.optim
          description: Optimization algorithms (SGD, Adam, AdamW, etc.) for training neural networks.
          link: https://docs.pytorch.org/docs/stable/optim.html
          type: Module
          level: Essential
          featured: true
        - title: Learning Rate Schedulers
          description: Strategies for adjusting learning rates during training — StepLR, CosineAnnealing, OneCycleLR, and more.
          link: https://docs.pytorch.org/docs/stable/optim.html#how-to-adjust-learning-rate
          type: Reference
          level: Common

    - name: Data Loading
      tag: Data
      description: Tools for loading, transforming, and batching data
      items:
        - title: torch.utils.data
          description: Dataset and DataLoader abstractions for efficient data loading and batching.
          link: https://docs.pytorch.org/docs/stable/data.html
          type: Module
          level: Essential
          featured: true
        - title: torch.utils.data.DataLoader
          description: Combines dataset and sampler for iterable data loading with multiprocessing support.
          link: https://docs.pytorch.org/docs/stable/data.html#torch.utils.data.DataLoader
          type: Class
          level: Essential

    - name: Deployment & Compilation
      tag: Deploy
      description: Model compilation, export, and serving for production
      items:
        - title: torch.compile
          description: JIT-compile PyTorch models for faster execution using TorchDynamo and TorchInductor.
          link: https://docs.pytorch.org/docs/stable/torch.compiler.html
          type: Function
          level: Essential
          featured: true
        - title: torch.export
          description: Export PyTorch models to a standardized intermediate representation for deployment.
          link: https://docs.pytorch.org/docs/stable/export.html
          type: Module
          level: Common

    - name: Distributed Training
      tag: Dist
      description: Multi-GPU and multi-node training infrastructure
      items:
        - title: torch.distributed
          description: Distributed communication primitives for multi-process and multi-node training.
          link: https://docs.pytorch.org/docs/stable/distributed.html
          type: Module
          level: Advanced
          featured: true
        - title: torch.nn.parallel.DistributedDataParallel
          description: Multi-process data parallelism for efficient distributed training.
          link: https://docs.pytorch.org/docs/stable/generated/torch.nn.parallel.DistributedDataParallel.html
          type: Class
          level: Advanced
        - title: FSDP
          description: Fully Sharded Data Parallel — memory-efficient distributed training for large models.
          link: https://docs.pytorch.org/docs/stable/fsdp.html
          type: Module
          level: Specialized
  search_entries:
    - title: C++ API
      link: https://docs.pytorch.org/cppdocs/
    - title: torch
      link: https://docs.pytorch.org/docs/stable/torch.html
    - title: torch.nn
      link: https://docs.pytorch.org/docs/stable/nn.html
    - title: torch.nn.functional
      link: https://docs.pytorch.org/docs/stable/nn.functional.html
    - title: Tensors
      link: https://docs.pytorch.org/docs/stable/tensors.html
    - title: Tensor Attributes
      link: https://docs.pytorch.org/docs/stable/tensor_attributes.html
    - title: Tensor Views
      link: https://docs.pytorch.org/docs/stable/tensor_view.html
    - title: torch.amp
      link: https://docs.pytorch.org/docs/stable/amp.html
    - title: torch.autograd
      link: https://docs.pytorch.org/docs/stable/autograd.html
    - title: torch.library
      link: https://docs.pytorch.org/docs/stable/library.html
    - title: accelerator
      link: https://docs.pytorch.org/docs/stable/accelerator.html
    - title: cpu
      link: https://docs.pytorch.org/docs/stable/cpu.html
    - title: cuda
      link: https://docs.pytorch.org/docs/stable/cuda.html
    - title: torch.cuda.memory
      link: https://docs.pytorch.org/docs/stable/torch_cuda_memory.html
    - title: mps
      link: https://docs.pytorch.org/docs/stable/mps.html
    - title: xpu
      link: https://docs.pytorch.org/docs/stable/xpu.html
    - title: mtia
      link: https://docs.pytorch.org/docs/stable/mtia.html
    - title: mtia.memory
      link: https://docs.pytorch.org/docs/stable/mtia.memory.html
    - title: mtia.mtia_graph
      link: https://docs.pytorch.org/docs/stable/mtia.mtia_graph.html
    - title: meta
      link: https://docs.pytorch.org/docs/stable/meta.html
    - title: torch.backends
      link: https://docs.pytorch.org/docs/stable/backends.html
    - title: torch.export
      link: https://docs.pytorch.org/docs/stable/export.html
    - title: torch.distributed
      link: https://docs.pytorch.org/docs/stable/distributed.html
    - title: torch.distributed.tensor
      link: https://docs.pytorch.org/docs/stable/distributed.tensor.html
    - title: torch.distributed.algorithms.join
      link: https://docs.pytorch.org/docs/stable/distributed.algorithms.join.html
    - title: torch.distributed.elastic
      link: https://docs.pytorch.org/docs/stable/distributed.elastic.html
    - title: torch.distributed.fsdp
      link: https://docs.pytorch.org/docs/stable/fsdp.html
    - title: torch.distributed.fsdp.fully_shard
      link: https://docs.pytorch.org/docs/stable/distributed.fsdp.fully_shard.html
    - title: torch.distributed.tensor.parallel
      link: https://docs.pytorch.org/docs/stable/distributed.tensor.parallel.html
    - title: torch.distributed.optim
      link: https://docs.pytorch.org/docs/stable/distributed.optim.html
    - title: torch.distributed.pipelining
      link: https://docs.pytorch.org/docs/stable/distributed.pipelining.html
    - title: torch.distributed._symmetric_memory
      link: https://docs.pytorch.org/docs/stable/symmetric_memory.html
    - title: torch.distributed.checkpoint
      link: https://docs.pytorch.org/docs/stable/distributed.checkpoint.html
    - title: torch.distributions
      link: https://docs.pytorch.org/docs/stable/distributions.html
    - title: torch.compiler
      link: https://docs.pytorch.org/docs/stable/torch.compiler_api.html
    - title: torch.fft
      link: https://docs.pytorch.org/docs/stable/fft.html
    - title: torch.func
      link: https://docs.pytorch.org/docs/stable/func.html
    - title: futures
      link: https://docs.pytorch.org/docs/stable/futures.html
    - title: torch.fx
      link: https://docs.pytorch.org/docs/stable/fx.html
    - title: torch.fx.experimental
      link: https://docs.pytorch.org/docs/stable/fx.experimental.html
    - title: torch.hub
      link: https://docs.pytorch.org/docs/stable/hub.html
    - title: torch.linalg
      link: https://docs.pytorch.org/docs/stable/linalg.html
    - title: torch.monitor
      link: https://docs.pytorch.org/docs/stable/monitor.html
    - title: torch.signal
      link: https://docs.pytorch.org/docs/stable/signal.html
    - title: torch.special
      link: https://docs.pytorch.org/docs/stable/special.html
    - title: torch.overrides
      link: https://docs.pytorch.org/docs/stable/torch.overrides.html
    - title: torch.nativert
      link: https://docs.pytorch.org/docs/stable/nativert.html
    - title: torch.package
      link: https://docs.pytorch.org/docs/stable/package.html
    - title: profiler
      link: https://docs.pytorch.org/docs/stable/profiler.html
    - title: torch.nn.init
      link: https://docs.pytorch.org/docs/stable/nn.init.html
    - title: torch.nn.attention
      link: https://docs.pytorch.org/docs/stable/nn.attention.html
    - title: onnx
      link: https://docs.pytorch.org/docs/stable/onnx.html
    - title: torch.optim
      link: https://docs.pytorch.org/docs/stable/optim.html
    - title: complex_numbers
      link: https://docs.pytorch.org/docs/stable/complex_numbers.html
    - title: ddp_comm_hooks
      link: https://docs.pytorch.org/docs/stable/ddp_comm_hooks.html
    - title: quantization
      link: https://docs.pytorch.org/docs/stable/quantization.html
    - title: rpc
      link: https://docs.pytorch.org/docs/stable/rpc.html
    - title: torch.random
      link: https://docs.pytorch.org/docs/stable/random.html
    - title: masked
      link: https://docs.pytorch.org/docs/stable/masked.html
    - title: torch.nested
      link: https://docs.pytorch.org/docs/stable/nested.html
    - title: size
      link: https://docs.pytorch.org/docs/stable/size.html
    - title: sparse
      link: https://docs.pytorch.org/docs/stable/sparse.html
    - title: storage
      link: https://docs.pytorch.org/docs/stable/storage.html
    - title: torch.testing
      link: https://docs.pytorch.org/docs/stable/testing.html
    - title: torch.utils
      link: https://docs.pytorch.org/docs/stable/utils.html
    - title: torch.utils.benchmark
      link: https://docs.pytorch.org/docs/stable/benchmark_utils.html
    - title: torch.utils.checkpoint
      link: https://docs.pytorch.org/docs/stable/checkpoint.html
    - title: torch.utils.cpp_extension
      link: https://docs.pytorch.org/docs/stable/cpp_extension.html
    - title: torch.utils.data
      link: https://docs.pytorch.org/docs/stable/data.html
    - title: torch.utils.deterministic
      link: https://docs.pytorch.org/docs/stable/deterministic.html
    - title: torch.utils.jit
      link: https://docs.pytorch.org/docs/stable/jit_utils.html
    - title: torch.utils.dlpack
      link: https://docs.pytorch.org/docs/stable/dlpack.html
    - title: torch.utils.mobile_optimizer
      link: https://docs.pytorch.org/docs/stable/mobile_optimizer.html
    - title: torch.utils.model_zoo
      link: https://docs.pytorch.org/docs/stable/model_zoo.html
    - title: torch.utils.tensorboard
      link: https://docs.pytorch.org/docs/stable/tensorboard.html
    - title: torch.utils.module_tracker
      link: https://docs.pytorch.org/docs/stable/module_tracker.html
    - title: type_info
      link: https://docs.pytorch.org/docs/stable/type_info.html
    - title: named_tensor
      link: https://docs.pytorch.org/docs/stable/named_tensor.html
    - title: name_inference
      link: https://docs.pytorch.org/docs/stable/name_inference.html
    - title: "torch.__config__"
      link: https://docs.pytorch.org/docs/stable/config_mod.html
    - title: "torch.__future__"
      link: https://docs.pytorch.org/docs/stable/future_mod.html
    - title: logging
      link: https://docs.pytorch.org/docs/stable/logging.html
    - title: torch_environment_variables
      link: https://docs.pytorch.org/docs/stable/torch_environment_variables.html
---

# PyTorch API Reference

<!-- Page body is rendered from YAML frontmatter by the landing template -->

```{toctree}
:glob:
:maxdepth: 1
:caption: Python API

installing
torch
nn
nn.functional
tensors
tensor_attributes
tensor_view
torch.amp <amp>
torch.autograd <autograd>
torch.library <library>
accelerator
cpu
cuda
torch.cuda.memory <torch_cuda_memory>
mps
xpu
mtia
mtia.memory
mtia.mtia_graph
meta
torch.backends <backends>
torch.export <user_guide/torch_compiler/export>
torch.distributed <distributed>
torch.distributed.tensor <distributed.tensor>
torch.distributed.algorithms.join <distributed.algorithms.join>
torch.distributed.elastic <distributed.elastic>
torch.distributed.fsdp <fsdp>
torch.distributed.fsdp.fully_shard <distributed.fsdp.fully_shard>
torch.distributed.tensor.parallel <distributed.tensor.parallel>
torch.distributed.optim <distributed.optim>
torch.distributed.pipelining <distributed.pipelining>
torch.distributed._symmetric_memory <symmetric_memory>
torch.distributed.checkpoint <distributed.checkpoint>
torch.distributions <distributions>
torch.compiler <torch.compiler_api>
torch.fft <fft>
torch.func <func>
futures
fx
fx.experimental
torch.hub <hub>
torch.linalg <linalg>
torch.monitor <monitor>
torch.signal <signal>
torch.special <special>
torch.overrides
torch.nativert <nativert>
torch.package <package>
profiler
nn.init
nn.attention
onnx
optim
complex_numbers
ddp_comm_hooks
quantization
rpc
torch.random <random>
masked
torch.nested <nested>
size
sparse
storage
torch.testing <testing>
torch.utils <utils>
torch.utils.benchmark <benchmark_utils>
torch.utils.checkpoint <checkpoint>
torch.utils.cpp_extension <cpp_extension>
torch.utils.data <data>
torch.utils.deterministic <deterministic>
torch.utils.jit <jit_utils>
torch.utils.dlpack <dlpack>
torch.utils.mobile_optimizer <mobile_optimizer>
torch.utils.model_zoo <model_zoo>
torch.utils.tensorboard <tensorboard>
torch.utils.module_tracker <module_tracker>
type_info
named_tensor
name_inference
torch.__config__ <config_mod>
torch.__future__ <future_mod>
logging
torch_environment_variables
```
