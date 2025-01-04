# Compute Diffusion Coefficients from MSD Data

This Python tool calculates diffusion coefficients (\(D\)) from Mean Squared Displacement (MSD) data based on user-provided parameters.

```text
## Formula Derivation

### Step 1: Mean Squared Displacement (MSD)
MSD(t) = < |r(t) - r(0)|^2 >

For normal diffusion in n-dimensional space:
MSD(t) = 2 * n * D * t

where:
- n: Dimension of the system (e.g., 1 for 1D, 2 for 2D, and 3 for 3D);
- D: Diffusion coefficient (cm^2/s);
- t: Time (s).

### Step 2: Using Slope to Calculate D
Rearranging the MSD formula:
D = MSD(t) / (2 * n * t)

The slope (slope) of the MSD vs. t curve is calculated using least squares regression:
slope = MSD / t

Substituting slope into the formula for D:
D = slope / (2 * n)

### Step 3: Unit Conversion
The raw slope is calculated in units of Å^2/time_unit. To convert this into cm^2/s:
1. 1 Å = 10^-8 cm;
2. 1 Å^2 = 10^-16 cm^2;
3. If time is measured in fs (1 fs = 10^-15 s):
   1 Å^2/fs = 10^-1 cm^2/s

Finally, expressing D in 10^-4 cm^2/s:
D = slope / (2 * n * time_unit) * 10^-4

## Installation

### Clone the Repository
git clone https://github.com/yourusername/compute_diffusion.git
cd compute_diffusion

### Install the Package
pip install .

### Install from GitHub
pip install git+https://github.com/yourusername/compute_diffusion.git

## Usage

### Command Line

compute-diffusion --filename MSD__ --skip_row 1 --time_index 0 --msd_col 1 --time_unit 1 --group_size 4 --dimension 3

### Parameters

--filename : Input data file (e.g., MSD__).
--skip_row : Number of rows to skip (e.g., 1).
--time_index : Column index for time data (0-based).
--msd_col : Column index for MSD data (0-based).
--time_unit : Time unit conversion factor (1 for fs, 1000 for ps).
--group_size : Number of cumulative segments.
--dimension : Number of spatial dimensions (e.g., 3 for 3D diffusion).

## Example Output

[INFO] Final Configuration:
{
    "filename": "MSD__",
    "skip_row": 1,
    "time_index": 0,
    "msd_col": 1,
    "time_unit": 1,
    "group_size": 4,
    "dimension": 3
}

[INFO] Data points: 9999, Segment size: 2499
Segment 1 slope= 3.612335
Segment 2 slope= 3.329569
Segment 3 slope= 3.381865
Segment 4 slope= 3.497184

[RESULT] Avg= 3.455239
[RESULT] Max= 3.612335
[RESULT] Min= 3.329569
[RESULT] D= 0.000058 (10^-4 cm^2/s)
[RESULT] Error= 0.000010 (10^-4 cm^2/s)

## License

This project is licensed under the MIT License.

