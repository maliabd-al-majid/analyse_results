# analyse_results
## Analyse
### Configuration
Update the path (output_path, parse2csv_name, csv2dpdbtw_name) in **Constant.py**
### Usage
```python
python3 parse_json.py
python3 parse2csv.py
python3 csv2dpdbtw.py
```

## Plots
### Configuration
Update the path (CSV_NAME_all_in) with your output csv from csv2dpdbbtw.py  in **constants.py**
### Filter
Uncomment the filters in each plot script you want to apply filter on it.
### Usage
[1e_plot_solved_wrt_projections_all_solvers.py](https://github.com/maliabd-al-majid/analyse_results/blob/main/plots_output_tool/plots/1e_plot_solved_wrt_projections_all_solvers.py)
```python
python3 1e_plot_solved_wrt_projections_all_solvers.py
```
[1e_plot_solved_wrt_treewidth_all_solvers.py](https://github.com/maliabd-al-majid/analyse_results/blob/main/plots_output_tool/plots/1e_plot_solved_wrt_treewidth_all_solvers.py)
```python
python3 1e_plot_solved_wrt_treewidth_all_solvers.py
```
[1e_plot_solved_wrt_models_all_solvers.py](https://github.com/maliabd-al-majid/analyse_results/blob/main/plots_output_tool/plots/1e_plot_solved_wrt_models_all_solvers.py)
```python
python3 1e_plot_solved_wrt_models_all_solvers.py
```
[2a_cactus_plot.py](https://github.com/maliabd-al-majid/analyse_results/blob/main/plots_output_tool/plots/2a_cactus_plot.py)
```python
python3 2a_cactus_plot.py
```
[2b_cactus_plot_reversed.py](https://github.com/maliabd-al-majid/analyse_results/blob/main/plots_output_tool/plots/2b_cactus_plot_reversed.py)
```python
python3 2b_cactus_plot_reversed.py
```
