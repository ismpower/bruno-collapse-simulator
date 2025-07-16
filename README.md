# bruno-simulator

Simulation framework for the **Bruno Unified Model** (entropy collapse threshold) prototype.

## Overview

This repository hosts a standalone Python-based simulator that explores the Bruno Unified Model of entropy collapse, which predicts when volumetric entropy must project onto a surface (2D) as systems compress and heat up. It is kept separate from the Varda (Palantír) AI backend to maintain clear project boundaries.

## Key Features

* **Bruno Constant Calculation**: Compute $\beta_B = \kappa \cdot T$ and compare against the geometric threshold.
* **R–T Phase‐Space Simulation**: Visualize the collapse boundary in radius–temperature space.
* **Time‐Evolution Tracking**: Generate entropy and $dS/dt$ traces and detect real‐time collapse echo.
* **Thermodynamic Analysis**: Perform entropy ratio and free‐energy phase‐transition analyses.
* **GRChombo‐Style Starter**: A grid‐based PDE stub for relativistic entropy collapse triggers.

## Installation

1. **Clone the repository**

   ```bash
   git clone git@github.com:ismpower/bruno-simulator.git
   cd bruno-simulator
   ```

2. **Create & activate Conda environment**

   ```bash
   conda create -n bruno-simulator-env python=3.11 -y
   conda activate bruno-simulator-env
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

   \*(Or: `pip install numpy scipy matplotlib pandas torch tensorflow`) \*

## Project Structure

```
bruno-simulator/              # Root folder of this simulator
├── data/                     # (Optional) Raw inputs or simulation outputs
│   └── raw/                  # Example CAN‑simulator CSV logs (ignored by Git)
├── notebooks/                # Interactive Jupyter notebooks for exploration
├── scripts/                  # Core simulation and analysis modules
│   ├── simulate.py           # Main simulation driver
│   ├── analysis.py           # Entropy & thermodynamic utilities
│   └── grchombo_stub.py      # GRChombo‑style PDE stub
├── environment.yml           # Conda environment specification
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## Usage

Run the main simulator with default settings:

```bash
python scripts/simulate.py --config config/default.yaml
```

Or explore the interactive notebooks under `notebooks/`.

## Contributing

1. Fork the repo and create a feature branch.
2. Submit a pull request with detailed descriptions.
3. Ensure all new code is covered by tests and follows PEP 8 style.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
# bruno-collapse-simulator
