
# Table of Contents

1.  [Overview](#orgc9cfec0)
2.  [Install](#org4bfb13b)
    1.  [Requirement](#orgb185937)
    2.  [Install from PyPI](#org56d7ddc)
    3.  [Install from Source](#org829296b)
3.  [Features](#org33d503c)
4.  [Implementation](#org1908f4b)



<a id="orgc9cfec0"></a>

# Overview

This repository is non-official third-paty re-implementation of SLIDE<sup><a id="fnr.1" class="footref" href="#fn.1">1</a></sup>.

We provide

-   Python package
-   Hash based Deep Learning
-   Parallel computing based on C++17 parallel STL

We don't provide

-   Explicit CPU optimized code like AVX (We just rely on compiler optimization)
-   Compiled binary (You need to compile by yourself)


<a id="org4bfb13b"></a>

# Install

There are two options, "Install from PyPI" and "Install from Source".
For ordinary user, "Install from PyPI" is recommended.

For both case, sufficient C++ compiler is neccessary.


<a id="orgb185937"></a>

## Requirement

-   Recent C++ compiler with parallel STL algorithm support
    -   [GCC](https://gcc.gnu.org/) 9.1 or newer together with [Intel TBB](https://github.com/oneapi-src/oneTBB)
-   [Python](https://www.python.org/) 3

Requirements can be installed on Docker image [gcc:10](https://hub.docker.com/_/gcc).

    # On local machine
    docker run -it gcc:10 bash
    
    # On gcc:10 image
    apt update && apt install -y python3-pip libtbb-dev


<a id="org56d7ddc"></a>

## Install from PyPI

    pip install HashDL


<a id="org829296b"></a>

## Install from Source

    git clone https://gitlab.com/ymd_h/hashdl.git HashDL
    cd HashDL
    pip install .


<a id="org33d503c"></a>

# Features

-   Neural Network
    -   hash-based sparse dense layer
-   Activation
    -   ReLU
    -   linear (no activation)
    -   sigmoid
-   Optimizer
    -   SGD
    -   Adam<sup><a id="fnr.2" class="footref" href="#fn.2">2</a></sup>
-   Weight Initializer
    -   constant
    -   Gauss distribution
-   Hash for similarity
    -   WTA
    -   DWTA<sup><a id="fnr.3" class="footref" href="#fn.3">3</a></sup>
-   Scheduler for hash update
    -   constant
    -   exponential decay

In the current architecture, CNN is impossible.


<a id="org1908f4b"></a>

# Implementation

The [official reference implementation](https://github.com/keroro824/HashingDeepLearning) focused on performance and
accepted some "dirtyness" like hard-coded magic number for algotihm
selection and unmanaged memory allocation.

We accept some (but hopefully small) overhead and improve
maintenability in terms of software;

-   Polymorphism with inheritance and virtual function
-   RAII and smart pointer for memory management

These archtecture allows us to construct and manage C++ class from
Python without recompile.

We also rely recent C++ standard and compiler optimization;

-   Parallel STL from C++17
-   Because of RVO (or at least move semantics), returning `std::vector`
    is not so much costful as it was.


# Footnotes

<sup><a id="fn.1" href="#fnr.1">1</a></sup> [B. Chen *et al*., "SLIDE : In Defense of Smart Algorithms over Hardware Acceleration for Large-Scale Deep Learning Systems", MLSys 2020](https://mlsys.org/Conferences/2020/Schedule?showEvent=1410) ([arXiv](https://arxiv.org/abs/1903.03129), [code](https://github.com/keroro824/HashingDeepLearning))

<sup><a id="fn.2" href="#fnr.2">2</a></sup> [D. P. Kingma and J. Ba, "Adam: A Method for Stochastic Optimization", ICLR (2015)](https://iclr.cc/archive/www/doku.php%3Fid=iclr2015:main.html) ([arXiv](https://arxiv.org/abs/1412.6980))

<sup><a id="fn.3" href="#fnr.3">3</a></sup> [B. Chen *et al*., "Densified Winner Take All (WTA) Hashing for Sparse Datasets", Uncertainty in artificial intelligence (2018)](http://auai.org/uai2018/proceedings/papers/321.pdf)
