## usage: loomwords.py [-h] --input_template [INPUT_TEMPLATE] --output_file [OUTPUT_FILE]
##                     [--replacement_file [REPLACEMENT_FILE]] [--theme [THEME]] [--debug]
## 
## Loomwords - a dynamic text generation platform
## 
## optional arguments:
##   -h, --help            show this help message and exit
##   --input_template [INPUT_TEMPLATE]
##                         input template filename
##   --output_file [OUTPUT_FILE]
##                         output filename
##   --replacement_file [REPLACEMENT_FILE]
##                         replacements filename
##   --theme [THEME]       theme directory, must match data_[THEME]
##   --debug               print debugging output


# DON'T EDIT ANYTHING BELOW THIS POINT UNLESS YOU KNOW WHAT YOU'RE DOING!

# TODO:
# 1. Output directly to HTML.
# 2. Handle capitalizing variables that begin sentences after HTML tags.
# 3. Remove recursion.
# 4. Handle a/an automatically.
# 8. Any line beginning with // should be removed and ignored.
# 10. Allow dynamic subtemplate behavior within stickies.
# 14. Add --debug mode which shows info like all vocabs used, all stickies, etc.
# 16. Put in GitHub repo with examples and proper .gitignore.
# 19. Support random integer generation with _1-99, _2-6, etc.
# 21. Create default data pack for distribution.
# 22. Allow shorthands like ! for sticky, ++ for incrementer.

# Import any libraries you need here.
import os,sys,random,glob,re,codecs,argparse

# The main data structure holding all taxonomies.
# Top level keys are taxonomies. Each taxonomy has a dictionary of vocabularies.
database = {}

# Thesaurus to handle <_word> syntax.
thesaurus = {}

# Storage for sticky values.
# Each key has its own dictionary of vocabulary:value.
stickies = {}
incrementers = {}

# Storage for templates that don't have values.
# Show these at the end for information's sake.
missing = {}
missing_thesaurus = {}

# Properly case all sentences.
def sentenceCase(text):
    return re.sub(r"(\A\w)|"+             # start of string
             "(?<!\.\w)([\.?!] )\w|"+     # after a ?/!/. and a space, 
                                          # but not after an acronym
             "\w(?:\.\w)|"+               # start/middle of acronym
             "(?<=\w\.)\w",               # end of acronym
             lambda x: x.group().upper(), 
             text)

# Load the thesaurus.
def loadThesaurus(thesaurus_file,thesaurus):
    try:
        thesaurus_lines = open(thesaurus_file,'r').readlines()
        count = 0
        for d in thesaurus_lines:
            entries = d.strip().split(',')
            for e in entries:
                if e in thesaurus.keys():
                    thesaurus[e].append(count)
                else:
                    thesaurus[e] = [count]
            count += 1
    except:
        print("No thesaurus loaded.")
    return thesaurus_lines

# Identify our taxonomies from our data directories.
def getTaxonomies(dirs):
    # We'll either have one or two dirs.
    taxonomies = []
    for d in dirs:
        files = glob.glob(d + "/*.txt")
        for f in files:
            path = os.path.join(".",f)
            filename = os.path.basename(path)
            if filename.find("_") != -1:
                taxonomy = filename.split("_")[0]
                if taxonomy not in taxonomies:
                    taxonomies.append(taxonomy)
    return taxonomies
    

# Load all the taxonomies.
def loadTaxonomies(dirs,taxonomies,database):
    for d in dirs:
        for t in taxonomies:
            if t == "sticky":
                print("Sorry, but you can't have a 'sticky' taxonomy!")
                print("That's reserved for persistent values!")
                print("Please remove it from TAXONOMIES and try again.")
                sys.exit()
            files = glob.glob(d + "/" + t + '*.txt')
            for f in files:
                # Ensure we have [taxonomy]_[vocab] pattern.
                path = os.path.join(".",f)
                filename = os.path.basename(path)
                if filename.startswith(t + "_") != -1:
                    taxname = filename.split(".txt")[0]
                    if t not in database.keys():
                        database[t] = {}
                    data = []
                    for l in codecs.decode(open(path,'rb').read()).splitlines():
                        if l != '':
                            data.append(l)
                    # Since we process a chosen theme last, this will supersede defaults when a theme is used.
                    database[t][taxname] = data

# Grab a random item from the chosen taxonomy.
# Don't process it yet.
def getRandomFromTaxonomy(taxonomy,database):
    # We actually do *two* choices here!
    # First is to choose the file we'll pull from.
    # Second is to choose an actual entry from that file.
    key = random.choice(list(database[taxonomy].keys()))
    return random.choice(database[taxonomy][key])

# Recursively process templates.
def process(text,database,missing,laststicky,thesaurus,thesaurus_lines):
    #print(text)
    matches = re.findall("(\<\w+\>)",text)
    # This gives us an array of matches.
    # We'll then need to reconstruct the sentence with each template replaced.
    # Take the result and process it again.
    # If the next result exactly matches the current result, we're done.
    # Return it!
    # We'll gradually transform this into our result text.
    result = text
    for m in matches:
        parts = result.split(m)
        preceding = parts[0]
        template = m.split("<")[1].split(">")[0]
        sticky = 0
        builtin = 0
        if template.startswith("sticky_"):
            # We have a sticky value.
            # Second part is the asset name.
            # The rest is the real taxonomy.
            sticky = 1
        if sticky:
            taxonomy = template.split("_")[2]
            stickytemplate = "_".join(template.split("_")[2:])
        else:
            taxonomy = template.split("_")[0]
        if taxonomy == "":
            builtin = 1
            word = template.split("_")[1]
            # Use the thesaurus.
            if word in thesaurus.keys():
                index = random.choice(thesaurus[word])
                entries = thesaurus_lines[index].split(",")
                replacement = random.choice(entries)
            else:
                # Track missing thesaurus words.
                missing_thesaurus[word] = ""
                replacement = word
        try:
            if not builtin:
                if sticky:
                    # Get the sticky reference.
                    stickyref = template.split("_")[1]
                    if stickyref == "this" and laststicky != "" and laststicky != "this" and laststicky != "TOPLEVEL":
                        # Special behavior.
                        # Need to refer to whatever the last sticky was.
                        try:
                            stickyref = laststicky
                        except:
                            print("Use of 'sticky_this' without proper context:",template)
                    if stickytemplate == "incrementer":
                        # Special handling for incrementers.
                        if stickyref not in incrementers.keys():
                            incrementers[stickyref] = 1
                        else:
                            incrementers[stickyref] += 1
                        replacement = str(incrementers[stickyref])
                    else:
                        if stickyref == "this":
                            print("Use of 'sticky_this' without proper context:",template)
                            replacement = random.choice(database[taxonomy][template])
                        else:
                            # Normal handling.
                            if stickyref not in stickies.keys():
                                # This one is new so create it from scratch.
                                stickies[stickyref] = {}
                            if stickytemplate not in stickies[stickyref].keys():
                                # Never encountered before so let's pick one.
                                replacement = random.choice(database[taxonomy][stickytemplate])
                                tmpresult = process(replacement,database,missing,stickyref,thesaurus,thesaurus_lines)
                                if replacement != tmpresult:
                                    replacement = process(tmpresult,database,missing,stickyref,thesaurus,thesaurus_lines)
                                stickies[stickyref][stickytemplate] = replacement
                            else:
                                replacement = stickies[stickyref][stickytemplate]
                else:
                    replacement = random.choice(database[taxonomy][template])
                    #stickies[stickyref][stickytemplate] = replacement
        except:
            if template.find("_") != -1:
                missing[template] = ""
            else:
                # Probably an HTML tag or something.
                pass
            continue
        if preceding != "":
            result = preceding + replacement + m.join(parts[1:])
        else:
            result = replacement + m.join(parts[1:])
    if result != text:
        result = process(result,database,missing,laststicky,thesaurus,thesaurus_lines)
    return result

# Replace target values with replacement values.
def replacements(replacementfile,text):
    lines = open(replacementfile,'r').readlines()
    for l in lines:
        rep = l.strip().split("|")
        target = rep[0]
        replacement = rep[1]
        parts = text.split(target)
        text = replacement.join(parts)
    return text

# Output our processed data to a file.
def outputToFile(outfile,text):
    outtext = sentenceCase(text)
    # Prepare text for file output.
    outtext = codecs.encode(outtext,'utf-8','ignore')
    outtext = codecs.decode(outtext,'utf-8','ignore')
    # Now fix the first-word capitalization of each line.
    lines = outtext.split("\n")
    outtext = ""
    for l in lines:
        if outtext != "":
            if len(l) > 0:
                outtext += "\n" + l[0].upper() + l[1:]
            else:
                outtext += "\n"
        else:
            outtext += l[0].upper() + l[1:]
    output = open(outfile,"wb")
    output.write(bytes(outtext,'utf-8'))
    output.close()
    return

parser = argparse.ArgumentParser(description='Loomwords - a dynamic text generation platform')
# --input_template=inputfile.txt
# --output_file=outputfile.txt
# --replacement_file=replacements.txt
# --theme=mytheme
# --debug
parser.add_argument('--input_template', nargs='?',help='input template filename',required=True)
parser.add_argument('--output_file',nargs='?',help='output filename',required=True)
parser.add_argument('--replacement_file',nargs='?',default='',help='replacements filename',required=False)
parser.add_argument('--theme',nargs='?',default='',help='theme directory, must match data_[THEME]',required=False)
parser.add_argument('--thesaurus_file',nargs='?',default='thesaurus.txt',help='custom thesaurus file',required=False)
parser.add_argument('--debug',action='store_true',help='print debugging output',required=False)
args = parser.parse_args()
input_template = args.input_template
output_file = args.output_file
replacement_file = args.replacement_file
theme = args.theme
debug = args.debug
thesaurus_file = args.thesaurus_file

# Load our taxonomies.
dirs = ['data']
if theme != '':
    # Make sure the directory exists.
    testdir = 'data_' + theme
    if os.path.isdir(os.path.join(".",testdir)):
        dirs = ['data',testdir]
print("Loading thesaurus...")
thesaurus_lines = loadThesaurus(thesaurus_file,thesaurus)
numsynonyms = 0
for k in thesaurus.keys():
    numsynonyms += len(thesaurus[k])
print("Loaded",len(thesaurus.keys()),"thesaurus lines with",numsynonyms,"synonym cross-references.")
print("Identifying taxonomies...")
taxonomies = getTaxonomies(dirs)
print("Loading taxonomies...")
loadTaxonomies(dirs,taxonomies,database)
numvocabs = 0
numvalues = 0
for k in database.keys():
    numvocabs += len(database[k])
    for v in database[k].keys():
        numvalues += len(database[k][v])
numtaxonomies = len(database.keys())
print("Loaded",len(database.keys()),"taxonomies with",numvocabs,"vocabularies and",numvalues,"values.")
# Grab our starting point.
print("Determining seed text...")
# File encoding is the bane of existence.
try:
    # Attempt utf-8 first.
    start = codecs.open(input_template,'r','utf-8').read()
except:
    # Might be latin-1 instead. Try that.
    try:
        start = codecs.open(input_template,'r','latin-1').read()
    except:
        # To hell with this.
        print("Unknown encoding in file: " + input_template)
        print("Quitting...")
        sys.exit()
# Process templates recursively.
print("Processing templates...")
output = process(start,database,missing,"TOPLEVEL",thesaurus,thesaurus_lines)
if replacement_file != "":
    print("Processing replacements...")
    output = replacements(replacement_file,output)
# Display our final output.
print("Writing output to file...")
#print(output)
outputToFile(output_file,output)
print("Output saved to:",output_file)
if len(missing.keys()) > 0:
    print("Missing templates:")
    for k in missing.keys():
        print(k)
if len(missing_thesaurus.keys()) > 0:
    print("Missing thesaurus terms:")
    for k in missing_thesaurus.keys():
        print(k)
