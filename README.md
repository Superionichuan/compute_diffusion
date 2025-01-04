# Compute Diffusion Coefficients from MSD Data

This Python tool calculates diffusion coefficients (\(D\)) from Mean Squared Displacement (MSD) data using user-provided parameters.

---

## Formula Derivation

### Step 1: Mean Squared Displacement (MSD)
The Mean Squared Displacement (MSD) is defined as:

$$
MSD(t) = \langle |r(t) - r(0)|^2 \rangle
$$

For normal diffusion in an n-dimensional space:

$$
MSD(t) = 2 \cdot n \cdot D \cdot t
$$

Where:
- **n**: Dimension of the system (e.g., 1 for `1D`, 2 for `2D`, and 3 for `3D`)
- **D**: Diffusion coefficient [10⁻⁴ cm²/s]
- **t**: Time (s)

---

### Step 2: Using MSD to Calculate \(D\)

#### 1. **Rearranging MSD Formula**

From the MSD equation:

$$
D = \frac{MSD(t)}{2 \cdot n \cdot t}
$$

#### 2. **Slope Method**

In practical experiments, MSD values are obtained at various time intervals. To compute \(D\), we calculate the slope of the MSD vs. \(t\) curve:

$$
	\text{slope} = \frac{MSD}{t}
$$

Substituting this into the formula for \(D\):

$$
D = \frac{\text{slope}}{2 \cdot n}
$$

#### 3. **Segmented Fitting**

To enhance reliability, the dataset is often divided into segments. For each segment, the slope is calculated, and the final \(D\) is obtained by averaging the results across all segments.

The `slope` of the linear fit for the Mean Squared Displacement `(MSD)` vs. time (`t`) is calculated using the formula:

$$
\text{slope} = \frac{N \sum (t_i \cdot MSD_i) - \sum t_i \sum MSD_i}{N \sum t_i^2 - (\sum t_i)^2}
$$

Where:
- $N$: The number of data points in the segment.
- $t_i$: The $i$-th time value.
- $MSD_i$: The $i$-th MSD value.
- $sum$: Summation over all data points in the segment.

This formula is derived from the least squares regression method, which minimizes the sum of squared errors between the observed and predicted \(MSD\) values.

---

### Step 3: Unit Conversion

#### 1. **Ångström to Centimeters**

- $1 \\ Å = 10^{-8} \\ cm²$
- $1 \\ Å^{2} = (10^{-8})^2  =  10^{-16} 	\\ cm^{2} $

#### 2. **Femtoseconds to Seconds**

- $1 \\ ps = 10^{-12} \\ s $
  
If the slope is in  $Å^{2}$  ps, convert to $cm^{2}$ s:

$$
\frac{{Å}^2}{ps} = \frac{10^{-16} \\ cm^{2} }{ 10^{-12} \\ s }= 10^{-4} \\ cm^{2} \\ s^{-1}
$$

#### 3. **Express in $10^{-4} \\ cm^{2} \\ s$**

To standardize results:

$$
D = \frac{	slope}{2 \cdot n \cdot 	time\\_unit} \cdot 10^{-4} \\ cm^{2} \\ s^{-1}
$$

Where \(	ext{time\_unit}\) is the scaling factor for time (e.g., 1 for ps, 0.001 for ps).

---


### Key Insights

1. **Dimensional Influence**: Higher dimensions (\(n\)) result in faster diffusion due to increased MSD. The factor \(2 \cdot n\) adjusts \(D\) to account for this.
2. **Noise Mitigation**: Fitting MSD curves reduces noise in experimental data, leading to more accurate \(D\) values.
3. **Unit Consistency**: Converting experimental data (\(	ext{Å}^2/	ext{fs}\)) to standard physical units (\(	ext{cm}^2/	ext{s}\)) ensures proper interpretation.

---

## Installation

### Install from GitHub
```bash
pip install git+https://github.com/Superionichuan/compute_diffusion.git
```

---

## Usage

### Command Line
```bash
compute-diffusion --filename MSD__                   --skip_row 1                   --time_index 0                   --msd_col 1                   --time_unit 1                   --group_size 4                   --dimension 3
```

### Parameters
| Parameter      | Description                                           |
|----------------|-------------------------------------------------------|
| `--filename`   | Input data file (e.g., `MSD.dat`).                      |
| `--skip_row`   | Number of rows to skip in the input file.             |
| `--time_index` | Column index for time data (0-based).                 |
| `--msd_col`    | Column index for MSD data (0-based).                  |
| `--time_unit`  | Time unit conversion factor (e.g., 1 for ps, 0.001 for fs). |
| `--group_size` | Number of cumulative segments to compute slopes.      |
| `--dimension`  | Number of spatial dimensions (e.g., 3 for 3D diffusion). |

---

## Example Output

```text
[INFO] Final Configuration:
{
    "filename": "filename",
    "skip_row": 1,
    "time_index": 0,
    "msd_col": 1,
    "time_unit": 1,
    "group_size": 4,
    "dimension": 3
}

[INFO] Data points: 10000, Segment size: 2500
Segment 1 :  1 ~ 2500  slope= 3.612335
Segment 2 :  1 ~ 5000  slope= 3.329569
Segment 3 :  1 ~ 7500  slope= 3.381865
Segment 4 :  1 ~ 10000 slope= 3.497184

[RESULT] Avg= 3.455239
[RESULT] Max= 3.612335
[RESULT] Min= 3.329569
[RESULT] D= 0.000058 (10^-4 cm^2/s)
[RESULT] Error= 0.000010 (10^-4 cm^2/s)
```

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Contributions

Contributions are welcome! Please open an issue or submit a pull request on GitHub to contribute to the project.

---

## Contact

For any questions or issues, feel free to contact [shichuan.sun@ntu.edu.sg].
