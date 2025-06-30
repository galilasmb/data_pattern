# DATA\_PATTERN

This repository follows a standard structure for ad hoc data projects, focusing on organization, reproducibility, and clarity throughout the entire analysis lifecycle.

## Project Structure

```plaintext
DATA_PATTERN/
├── docs/
│   └── README.md
├── output/
│   ├── excel/
│   ├── imagens/
│   ├── power point/
│   └── word/
├── scripts/
│   ├── analysis/
│   ├── data/
│   └── dynavis/
├── todo/
│   ├── tasks.md
│   └── README.md
```

### `data/`

Responsible for storing local datasets and raw data files used in the project.

### `docs/`

Contains supporting documents such as ordinances, technical notes, specifications, and anything that contributes to understanding the project and the analyses conducted.

### `output/`

Folder where generated results are saved:

* **excel/**: spreadsheets with results or processed data.
* **imagens/**: saved plots, figures, and visualizations.
* **power point/**: presentations derived from the analysis.
* **word/**: textual reports exported in Word format.

### `scripts/`

Contains the scripts used in the project, organized by purpose:

* **analysis/**: main analysis scripts or notebooks.
* **dags/**: folder containing Airflow DAG files (workflow definitions).

### `todo/`

Section intended for planning and task tracking:

* **tasks.md**: list of tasks, pending items, or backlog.
* **README.md**: additional explanations or execution guidelines.

---

## Recommendations

* Use the `tasks.md` file to track the progress of activities or other tools (Jira, Teams, Google)
* Add execution instructions to the scripts when necessary.
* Keep the directories organized to facilitate collaboration and reproducibility.
