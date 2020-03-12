# juicer

*juicer* is a module for preprocessing of text which can perform actions such as lemmatization, stopword removal and entity extraction.

## Installation
**Optional: Create a virtual environment**
```bash
$ virtualenv .env
$ source .env/bin/activate    # *nix
$ .\.env\Scripts\activate     # win
```
**Install**
```bash
$ git clone git@github.com:mortea15/juicer.git
$ cd juicer && pip3 install .
```
```bash
$ pip3 install git+ssh://git@github.com/mortea15/juicer.git
```
## Usage
**Set env vars**
```bash
$ cp env.vars.example env.vars
$ vim env.vars
$ source env.vars
```
### CLI
#### Basic usage
```bash
# Specify file to read
$ juicer -f <path_to_file> [options] [action]
# Read input from stdin
$ cat <path_to_file> | juicer -s [options] [action]
```

#### Examples
```bash
# Remove stopwords
$ juicer -f some_textfile -r
# Lemmatize (stem)
$ juicer -f some_other_file -l
# Extract entities
$ juicer -f some_other_file -e
# Named Entity Extraction using Stanford NER, save result to OUTFILE
$ juicer -f some_other_file -n -o results.out
# Process the text (removes stopwords, lemmatizes)
$ cat some_file | juicer -s -p
# Process the text (removes stopwords, lemmatizes and performs Named Entity Extraction)
$ cat some_file | juicer -s -p --ner
```
#### Help
```bash
$ juicer --help
usage: juicer (-f INPUT_FILE | -s) [-a] [--ner] [-w] [-p] [-r] [-l] [-t] [-e] [-n] [-d FORMAT] [-o OUTPUT_FILE] [-c] [-v] [-g]

      -f, --infile            Extract entities from file
      -s, --stdin             Extract entities from STDIN

      -a, --all               Extract all entities (default is named entities only)
      --ner                   Enable Named Entity Recognition for `--process`. (disabled by default)
      -w, --whitelist         Extract whitelisted tags only (verbs and nouns)

      -p, --process           Process the input and output entities
      -r, --remove-stops      Remove stopwords
      -l, --lemmatize         Lemmatize the text (stemming)
      -t, --speech-tag        POS tag the text
      -e, --extract           Extract entities from the text
      -n, --stanford          Entity extraction using the Stanford NER. (Use with -a to extract all entities).

      -o, --outfile           Output results to this file
      -d, --format            Output results as this format.
                              Available formats: [plain (default), json]

      -c, --check             Check if all required NLTK packages are present. Downloads missing packages.

      -v, --verbose           Increase verbosity (can be used several times, e.g. -vvv)
      -g, --log-file          Write log events to the file `juicer.log`
      --help                  Print this message
```

## Resources