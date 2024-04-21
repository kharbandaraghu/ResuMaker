# Run 
## Before you start
Setup Prompts folder based on configuration.md inside the folder
## Running the Script `run.sh` to Generate Resume

The `run.sh` script provided is designed to automate the process of generating a resume using two Python scripts: `GetAIResume.py` and `ResumeGenerator.py`. The script accepts all arguments and forwards them to the respective Python scripts for resume generation.

### Usage

To run the `run.sh` script, follow these steps:

1. Run `run.sh` script in the same directory as `GetAIResume.py` and `ResumeGenerator.py`.

2. Open a terminal window and navigate to the directory containing the scripts.

3. Run the following command to execute the `run.sh` script and generate the resume:

```bash 
./run.sh [ARGUMENTS]
```

# Run Individually + Available Arguements

## Getting JSON Data For Resume Based on a Prompt

GetAIResume.py is a Python script that generates a resume using an AI language model. The script takes user input and prompts the AI model to generate a resume based on the provided information.

### Usage

```
python GetAIResume.py [-h] [-m MODEL] [-t TEMPERATURE]
```
Max tokens is always 4000
### Arguments

- `-h`, `--help`: Show the help message and exit.
- `-m MODEL`, `--model MODEL`: Specify the AI model to use for generating the resume. The default model is `GPT4`. Available models are GPT4 and GPT3.
- `-t TEMPERATURE`, `--temperature TEMPERATURE`: Set the temperature value for the AI model's response. The temperature controls the randomness of the generated text. A higher temperature value (e.g., 1.0) will make the output more random, while a lower temperature value (e.g., 0.2) will make the output more deterministic and focused. The default temperature is `0.6`.

### Example

To generate a resume using the default settings (GPT3 model and temperature of 0.6), run:

```shell
python GetAIResume.py
```

To generate a resume using a different model (e.g., GPT4) and temperature (e.g., 0.8), run:

```shell
python GetAIResume.py -m GPT4 -t 0.8
```

The generated resume will be saved in a file named `resumeData.json` in the `tmp` directory.

Note: Make sure you have the required Python packages installed before running the script.

## Generating Resume PDF

ResumeGenerator.py is a Python script generates a resume in PDF format based on the provided data in a JSON file. It uses the `Packages.ResuMaker` module to create a Word document and then converts it to PDF using the `docx2pdf` library.

### Usage

1. Ensure that you have a `resumeData.json` file in the `tmp` directory with the necessary resume data.

2. Run the script with the desired options:

```
python ResumeGenerator.py [-h] [-bfs BASE_FONT_SIZE] [-ff FONT_FAMILY] [-bls BULLET_LINE_SPACING] [-o OUTPUT_FILE]
```

The available options are:

- `-bfs` or `--base-font-size`: Base font size (default: 10.5)
- `-ff` or `--font-family`: Font family (default: 'GoogleSans')
- `-bls` or `--bullet-line-spacing`: Bullet line spacing (default: 1.0)
- `-o` or `--output-file`: Output file name (default: 'resume.pdf')

3. The script will generate a Word document named `Resume.docx` in the `tmp` directory and then convert it to a PDF file with the specified output file name in the current directory.