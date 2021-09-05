# Loomwords

Loomwords is a dynamic text-generation platform that does not make use of any machine learning or neural network artificial intelligence. It works completely offline to your specifications.

It only requires a Python 3.x installation with default modules.

## How it works

1. Drawing on data files in the `data` directory along with custom themes, dynamic text replacements are done on your template.
2. Supposing you have a data file named `person_firstname.txt` containing a line-delimited list of names, using the tag `<person_firstname>` in a template will draw one of those names at random.
3. A replacement can be used repeatedly via the `sticky` mechanism. For example, `<sticky_mc_person_firstname>` will produce the same output every time it is used in a particular run.
4. Incrementers, such as for chapter numbers, are also available using syntax like: `<sticky_chapter_incrementer>`
5. There is a built-in thesaurus which will do quasi-intelligent replacements. Just use the syntax: `<_[word]>` such as `<_hot>` or `<_cold>`
6. Overriding particular vocabulary files is available using a theme system. Create a directory named `data_[theme]` where `[theme]` is the name of your theme, then invoke that theme when running Loomwords. Any vocabularies defined in a theme will override the default vocabularies in the `data` directory.
7. A replacement file may also be used to do static replacements on the output before it is written to a file, like so: `source text|replacement text`

## Usage

```
usage: loomwords.py [-h] --input_template [INPUT_TEMPLATE] --output_file [OUTPUT_FILE]
                    [--replacement_file [REPLACEMENT_FILE]] [--theme [THEME]] [--thesaurus_file [THESAURUS_FILE]]
                    [--debug]

Loomwords - a dynamic text generation platform

optional arguments:
  -h, --help            show this help message and exit
  --input_template [INPUT_TEMPLATE]
                        input template filename
  --output_file [OUTPUT_FILE]
                        output filename
  --replacement_file [REPLACEMENT_FILE]
                        replacements filename
  --theme [THEME]       theme directory, must match data_[THEME]
  --thesaurus_file [THESAURUS_FILE]
                        custom thesaurus file
  --debug               print debugging output
```

## Example

Create a file in the `data` directory named `person_firstname.txt` with the contents:

```
Bob
Alice
Caroline
```

Create a file in the `data` directory named `person_lastname.txt` with the contents:

```
Clark
Denson
Edwards
```

Now, create a file in the `data` directory or elsewhere and call it whatever you wish, but `template.txt` in the will work. Contents:

```
This is the <_story> of <person_firstname> <person_lastname>, a <_truly> <_clever> <_person>.
```

Now, run Loomwords:

`python --input_template template.txt --output_file output.txt`

You should see output like this:

```
Loading thesaurus...
Loaded 103306 thesaurus lines with 2550525 synonym cross-references.
Identifying taxonomies...
Loading taxonomies...
Loaded 2 taxonomies with 3 vocabularies and 7 values.
Determining seed text...
Processing templates...
Writing output to file...
Output saved to: output.txt
```

Open `output.txt` and you should see something like:

`This is the lie of Alice Edwards, a word by word stand-up comic prefabricate.`

It's not Shakespeare, but this should give you an idea of what you can do with this system.
