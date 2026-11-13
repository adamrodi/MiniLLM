# MiniLLM setup

The project uses its own Python environment so its packages are separate from other projects. The environment folder is recreated locally; Git stores the instructions and package versions needed to build it.

## Tested environment

- M3 Pro MacBook running macOS 27.0.1, with a native arm64 terminal.
- Python 3.13.1, PyTorch 2.15.0, and NumPy 2.5.4.
- Apple GPU acceleration through PyTorch's MPS backend.

requirements.txt records the installed package versions, including their dependencies. It does not install Python or specify the operating system. These instructions describe the tested Mac setup.

## Get the repository

From the folder where you keep repositories, clone the project and enter it:

```sh
git clone https://github.com/adamrodi/MiniLLM.git
cd MiniLLM
```

Cloning creates a local copy of the project and its Git history. If you already have the repository, enter its folder instead.

## Create the environment

Check that python3 selects Python 3.13 before creating the environment. The following commands create a project-local .venv folder, activate it in the current shell, install the recorded packages, and check their declared dependencies:

```sh
python3 --version
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pip check
```

The final command should report `No broken requirements found.` The `-r` option tells pip to read the package list from requirements.txt. Use `python -m pip` so packages are installed for the Python interpreter you selected.

## Verify the interpreter and GPU

First check which Python is running. Its path should end in MiniLLM/.venv/bin/python:

```sh
python -c "import sys; print(sys.executable)"
```

Next, test a calculation and its derivatives on the Mac GPU. The shell passes the lines between the two PY markers to Python; the final PY must appear alone on its line.

```sh
python - <<'PY'
import numpy
import torch

print("NumPy:", numpy.__version__)
print("PyTorch:", torch.__version__)
print("MPS built:", torch.backends.mps.is_built())
print("MPS available:", torch.backends.mps.is_available())
assert torch.backends.mps.is_available(), "MPS is unavailable"
x = torch.tensor([1.0, 2.0, 3.0], device="mps", requires_grad=True)
y = (x ** 2).sum()
y.backward()
print("Sum of squares:", y.item())
print("Gradient:", x.grad)
print("Device:", x.device)
assert y.item() == 14.0
assert x.grad.tolist() == [2.0, 4.0, 6.0]
PY
```

Both MPS checks should be True. The sum should be 14, the gradient should be [2, 4, 6], and the device should be mps:0. This tests a GPU computation and automatic differentiation; it does not measure training speed or verify a complete model.

The calculation is y = x1 squared + x2 squared + x3 squared. Its derivative with respect to each input is twice that input. `requires_grad=True` asks PyTorch to track operations, and `backward()` computes these derivatives without changing x.

## Return to the project later

In a new terminal, enter your local MiniLLM folder and run:

```sh
source .venv/bin/activate
```

Activation selects the environment for that shell session. You do not need to reinstall packages each time. To stop using the environment in that shell, run:

```sh
deactivate
```

## Setup verification record

On November 13, 2026, Adam verified the original project environment: pip reported no broken requirements, both MPS checks were True, and the interactive GPU calculation produced 14 with gradient [2, 4, 6]. Adam also recreated a separate temporary environment from requirements.txt. His reported output showed NumPy 2.5.4, PyTorch 2.15.0, no broken requirements, MPS available, result 14.0, gradient [2, 4, 6], and device mps:0. This verified that the recorded packages can recreate the working environment on this Mac.
