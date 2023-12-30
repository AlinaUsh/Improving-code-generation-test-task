## Test task for improving code generation with code analysis and project information

### Dataset generation

The django repository was used to generate the dataset. Python methods were extracted from it.
To start the generation:

`python3 data_collection.py`

The result is the dataset of 28178 samples with the following fields:

- Name -- the name of the function
- Args -- arguments passed to the function
- Body -- function code
- Context -- the context in which the function is located (class name)
- File name -- the file in which the function is located

It can be found in `django.csv`.

Example of a row from a dataset:

- Name: "state_forwards"
- Args: "self, app_label, state"
- Body: "pass\n"
- Context: "RunPython"
- File name: "django/db/migrations/operations/special.py"

### Fine-tuning and evaluation

I used the CodeT5+ model.
Fine-tune was made according to the example from the repository.
The codebleu metric was chosen to evaluate the quality of the model.

Code for data analysis, model fine-tuning and evaluation can be found in `task1.ipynb`

Weights for fine-tuned model can be found [here](https://drive.google.com/file/d/1HtAL1pPVzWpQMnR3_g6ukN7cneBrJJj-/view?usp=sharing).

| **metric**                 | **original model** | **after fine-tune** |
|----------------------------|--------------------|---------------------|
| codebleu                   | 0.271 +- 0.070     | 0.259 +- 0.013      |
| ngram_match_score          | 0.004 +- 0.029     | 0.022 +- 0.031      |
| weighted_ngram_match_score | 0.004 +- 0.030     | 0.014 +- 0.020      |
| syntax_match_score         | 0.077 +- 0.254     | 0.000 +- 0.000      |

### What else can be tried:

- See what other metrics may be suitable for this task for a more complete description of the results
- Try to use more context about the function (for example, the name of the file or the class where it lies)
- Try CodeT5+ in other sizes, as well as other models