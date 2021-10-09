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
8. Template replacements are *recursive*, meaning data files can themselves contain template references. Just be careful not to make them circular!
9. You can use syntax like `<_1-99>` to insert random integers. `<_word_5-10>` will create a random word 5-10 letters long. `<_name_5-10>` will do the same, but capitalized like a name.
10. The `--runs` parameter, when followed by an integer, will perform that number of runs and output them to the same file separated by a new line.
11. You may denote comment lines by starting them with `//`. They will be removed from final output and no blank lines they create will be kept.
12. You may even use one template's value to call another. This would be useful for a pronoun system, for instance: `<sticky_mc_pronoun_<sticky_mc_person_gender>>`. So, if the value pulled from `person_gender.txt` is `male` then the template is interpreted as `<sticky_mc_pronoun_male>`.
13. Shorthands for some templates are available! Use `!` to replace `sticky_`, `!!` to replace `sticky_this_` and `++` to replace `_incrementer`.

## Usage

```
usage: loomwords.py [-h] --input_template [INPUT_TEMPLATE] --output_file [OUTPUT_FILE]
                    [--replacement_file [REPLACEMENT_FILE]] [--theme [THEME]] [--thesaurus_file [THESAURUS_FILE]]
                    [--runs [RUNS]] [--debug]

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
  --runs [RUNS]         number of runs to output
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

## Future Work

There are a number of features and improvements planned for the future, including:

* A migration script for when you realize you've littered a template with 60 instances of `<my_junk>` and want to change it to `<good_stuff>`.
* Different output formatting options, such as markdown-to-HTML.
* More intelligent capitalization for sentences.
* Intelligent handling of articles like a/an.
* A standard for putting comment lines in templates that will be ignored and stripped out when rendering.
* Enabling dynamic subtemplate behavior for stickies.
* Making the `--debug` switch do something useful.
* Creation of shorthands for various syntax for the power users among you.
* More intelligent path handling for the replacement file option.
* A standard data pack and themes to help you get started using Loomwords with community-sourced data.
