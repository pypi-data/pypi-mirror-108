# VisPathways Documentation

**VisPathways** is a python library that allows for user-friendly pathway ontology summarization and visualization. The library supports usage from the python environment. Some of functionalities can also be achieved by calling certain files from the command-line.

## Content

1. [Table of Content](#Content)
2. [Installation](#Installation)
3. [Dependencies](#Dependencies)
4. [Functions](#Functions)
5. [Tutorials](#Tutorials)
6. [Acknowledgement](#Acknowledgement)

## Installation

You can install the package with [pip](https://pypi.org/project/pip/) using the command below:

```
https://pypi.org/project/VisPathways/0.1.1.8/
```

If you would like the development version of this package, check out our [Github page](https://github.com/tommyfuu/FancyTaxonomies).

## Dependencies

The dependencies should be automatically installed along with VisPathways when you install VisPathway using pip. If you would like to use the development version and install dependencies manually, in addition to the default libraries that come with python, you need:

- the ete3 module. (Install by [pip](https://pypi.org/project/ete3/) or [conda](http://etetoolkit.org/download/))
- [scipy](https://scipy.org/install.html) version 1.6.3
- [pandas](https://pandas.pydata.org/pandas-docs/stable/getting_started/install.html)
- [PyQt5](https://pypi.org/project/PyQt5/)

## Functions

Since **VisPathways** is a python library, the users will get the most out of this library by calling the classes and methods from the python environment. The functions of the VisPathways package can easily called within the VisPathways Master Class, which has several subclasses:

- VisPathways
  - [MergeDatabase](#MergeDatabase) (streamlined summarization for GeneOntology, Reactome, and Kegg).
    - [InferGoSlimToGO](#InferGoSlimToGO) (Finding all available pathway hierarchies for GeneOntology database)
    - [InferGoKeggToGO](#InferGoKeggToGO) (Finding all available pathway hierarchies for Kegg database)
    - [InferGoReactomeToGO](#InferGoReactomeToGo) (Finding all available pathway hierarchies for Reactome database)
    - [SummarizePathwayHierarchy](#SummarizePathwayHierarchy) (Generate summary table for a given set of enrichment data)
  - [EnrichmentPreprocess](#EnrichmentPreprocess) (Format and clean enrichment data; conduct scaled summary stats generation)
  - [GOTrees](#GOTrees) (Pathway ontology and enrichment visualization for GeneOntology)

Here we present some of our core methods of each of these classes.

_**IMPORTANT NOTE:** Make sure that `outputRoot` is consistent throughout running the whole workflow from summarization to visualization._

## Inputs for the whole Summarization + Visualization workflow

- You will need a `.obo` file from the GeneOntology database including the pathway hierarchy information. For example, you can use [`go-basic.obo`](http://geneontology.org/docs/download-ontology/), which is the file we use for writing our algorithm if you prefer to use that. There are also other options on that page for downloads. Similar file is required for Kegg (e.g. [`hsa00001.keg`](https://www.kegg.jp/kegg-bin/download_htext?htext=hsa00001.keg&format=htext&filedir=)) and Reactome (e.g.[ `ReactomePathwaysRelation.txt`](https://reactome.org/download/current/ReactomePathwaysRelation.txt)).
- You will need a `.xml` file including all the pathway signatures. We have one ([`msigdb_v7.2.xml`](https://www.gsea-msigdb.org/gsea/downloads_archive.jsp)) by default in this directory if you prefer to use that.
- You will need at least one pathway enrichment file in `.csv` format. For examples of this file, see `H_24hUV_over_30minUV_Enrichment.csv` or `gsea.FCG_GObp_8.27.20.csv` in the `test` directory. We are working on supporting more file formats. Additionally, you can have more relevant enrichment files in the same format for visualization. Note that this csv file should only contain one single column, with a column name that is NOT pathway name, and the file should NOT contain indices. There is also an option for inputting multiple enrichments at once to generate multiple summary statistics. For that, check out the `multipleEnrichmentFileProcess` method under the `EnrichmentPreprocess` class for more information.

### MergeDatabase

#### The initialization of an MergeDatabase object

```
MergeDatabase(goSlims, goXml, outputRoot)
```

_Arguments:_

- **goDatabase** (string): path to the ontology file such as `hsa00001.keg`.
- **goXml** (string): path to the gsea xml file, such as `msigdb_v7.2.xml`.
- **pathwayFileName** (string): enrichment file (a single enrichment, for multiple enrichment please check out the splitFilesRunSummary function)
- **outputRoot** (string): remains consistent with the previous parts

**_Example Usage (python)_**

```
#  After specifying ontologyFile (path), xmlFile (path), enrichmentFile (path), outputRoot (string)
from VisPathways import MergeDatabase
md = MergeDatabase(ontologyFile, xmlFile, enrichmentFile, outputRoot)
```

**_Example Usage (command line)_**

The command line usage of the mergeDatabases script will automatically execute the work function as outlined in the next part. Command line input of the mergeDatabases python script requires/can take in the following arguments:

```
  -g GODATABASE, --goDatabase GODATABASE
                        name of the database specific source file. (.obo file for Geneontology; .txt file for Kegg and Reactome)
  -x GOXML, --goXml GOXML
                        XML version of the MSigDB Gene Ontology BP
  -p PATHWAYFILENAME, --pathwayFileName PATHWAYFILENAME
                        name of the pathway file, recommend csv format
  -o OUTPUTROOT, --outputRoot OUTPUTROOT
                        root/prefix of the output files
```

Here is an example:

```
python3 mergeDatabases.py  -g go-basic.obo -x msigdb_v7.2.xml -p H_24hUV_over_30minUV_Enrichment.csv -o test
```

#### _Function_ MergeDatabase.generateSummaries

```
MergeDatabase.generateSummaries()
```

Asks user to input and confirm database used (G for GeneOntology; R for Reactome; K for Kegg).

Generate three files:

- _OutputRoot_.term_classes_to_pathways.xls (summarizing each standard pathway and its descendants)
- _OutputRoot_.pathway_to_go_id_ancestors.xls (summarizing each standard pathway and its ancestors)
- _OutputRoot_.pathway_count.xls (summarizing each enriched pathway's summary data)

**_Example Usage (Python)_**

```
#  After specifying ontologyFile (path), xmlFile (path), enrichmentFile (path), outputRoot (string)
from VisPathways import MergeDatabase
md = MergeDatabase(ontologyFile, xmlFile, enrichmentFile, outputRoot)
md.generateSummaries()
```

### InferGoSlimToGO

#### The initialization of an InferGoSlimToGO object

```
InferGoSlimToGO(goSlims, goXml, outputRoot)
```

_Arguments:_

- **goSlims** (string): path to the ontology file such as `hsa00001.keg`.
- **goXml** (string): path to the gsea xml file, such as `msigdb_v7.2.xml`.
- **outputRoot** (string): remains consistent with the previous parts

**_Example Usage (python)_**

```
# After specifying ontologyFile (path), xmlFile (path),outputRoot (string)

from VisPathways import InferGoSlimToGO
in = InferGoSlimToGO(ontologyFile, xmlFile, outputRoot)
```

**_Example Usage (command line)_**

The command line usage of the InferGoSlimToGOBP script will automatically execute the work function as outlined in the next part. Command line input of the InferGoSlimToGOBP python script requires/can take in the following arguments:

```
  -g GOSLIMS, --goSlims GOSLIMS
                        gene ontology basic go slims
  -x GOXML, --goXml GOXML
                        XML version of the MSigDB GOBP
  -o OUTPUTROOT, --outputRoot OUTPUTROOT
                        root of the output files
```

Here is an example:

```
python3 InferGoSlimToGOBP.py -o test -x msigdb_v7.2.xml -g go-basic.obo
```

#### _Function_ InferGoSlimToGO.work

```
InferGoSlimToGO.work()
```

Generate two files:

- _OutputRoot_.term_classes_to_pathways.xls (summarizing each standard pathway and its descendants)
- _OutputRoot_.pathway_to_go_id_ancestors.xls (summarizing each standard pathway and its ancestors)

(Along with some artifact files necessary for tree visualization, don't delete!)

**_Example Usage_**

```
#  After specifying ontologyFile (path), xmlFile (path),outputRoot (string)
from VisPathways import InferGoSlimToGO
in = InferGoSlimToGO(ontologyFile, xmlFile, outputRoot)
in.work()
```

### InferGoKeggToGO

#### The initialization of an InferGoKeggToGO object

```
InferGoKeggToGO(goKegg, goXml, outputRoot)
```

_Arguments:_

- **goKegg** (string): path to the ontology file such as `hsa00001.keg`.
- **goXml** (string): path to the gsea xml file, such as `msigdb_v7.2.xml`.
- **outputRoot** (string): remains consistent with the previous parts

**_Example Usage (python)_**

```
# After specifying ontologyFile (path), xmlFile (path),outputRoot (string)

from VisPathways import InferGoKeggToGO
in = InferGoKeggToGO(ontologyFile, xmlFile, outputRoot)
```

**_Example Usage (command line)_**

The command line usage of the InferGoKeggToGOBP script will automatically execute the work function as outlined in the next part. Command line input of the InferGoKeggToGOBP python script requires/can take in the following arguments:

```
  -g GOKEGG, --goKegg GOKEGG
                        kegg hsa gene ontology input file
  -x GOXML, --goXml GOXML
                        XML version of the MSigDB GOBP
  -o OUTPUTROOT, --outputRoot OUTPUTROOT
                        root of the output files
```

Here is an example:

```
python3 InferGoKeggToGOBP.py -o test -x msigdb_v7.2.xml -g hsa00001.keg
```

#### _Function_ InferGoKeggToGO.work

```

InferGoKeggToGO.work()

```

Generate two files:

- _OutputRoot_.term_classes_to_pathways.xls (summarizing each standard pathway and its descendants)
- _OutputRoot_.pathway_to_go_id_ancestors.xls (summarizing each standard pathway and its ancestors)

**_Example Usage (Python)_**

```

# After specifying ontologyFile (path), xmlFile (path),outputRoot (string)

from VisPathways import InferGoKeggToGO
in = InferGoKeggToGO(ontologyFile, xmlFile, outputRoot)
in.work()

```

### InferGoReactomeToGO

#### The initialization of an InferGoReactomeToGO object

```
InferGoReactomeToGO(goReactome, goXml, outputRoot)
```

_Arguments:_

- **goReactome** (string): path to the ontology file such as `ReactomePathwaysRelation.txt`.
- **goXml** (string): path to the gsea xml file, such as `msigdb_v7.2.xml`.
- **outputRoot** (string): remains consistent with the previous parts.

**_Example Usage (python)_**

```
# After specifying ontologyFile (path), xmlFile (path),outputRoot (string)

from VisPathways import InferGoReactomeToGO
in = InferGoReactomeToGO(ontologyFile, xmlFile, outputRoot)
```

**_Example Usage (command line)_**

The command line usage of the InferGoReactomeToGOBP script will automatically execute the work function as outlined in the next part. Command line input of the InferGoReactomeToGOBP python script requires/can take in the following arguments:

```
  -g GOREACTOMES, --goReactomes GOREACTOMES
                        Reactome gene ontology hiearchy input file
  -x GOXML, --goXml GOXML
                        XML version of the MSigDB GOBP
  -o OUTPUTROOT, --outputRoot OUTPUTROOT
                        root of the output files
```

Here is an example:

```
python3 InferGoReactomeToGOBP.py -o test -x msigdb_v7.2.xml -g ReactomePathwaysRelation.txt
```

#### _Function_ InferGoReactomeToGO.work

```

InferGoReactomeToGO.work()

```

Generate two files:

- _OutputRoot_.term_classes_to_pathways.xls (summarizing each standard pathway and its descendants)
- _OutputRoot_.pathway_to_go_id_ancestors.xls (summarizing each standard pathway and its ancestors)

**_Example Usage (Python)_**

```

# After specifying ontologyFile (path), xmlFile (path),outputRoot (string)

from VisPathways import InferGoReactomeToGO
in = InferGoReactomeToGO(ontologyFile, xmlFile, outputRoot)
in.work()

```

### SummarizePathwayHierarchy

#### The initialization of an SummarizePathwayHierarchy object

```
SummarizePathwayHierarchy(goReactome, goXml, outputRoot)
```

_Arguments:_

- **pathToAncestor** (string): path to the pathToAncestor file generated from previous functions, such as `test.pathway_to_go_id_ancestors.xls`.
- **ancestorToDescendant** (string): path to the ancestorToDescendant file generated from previous functions, such as `test.term_classes_to_pathways.xls`.
- **pathwayList** (string): path to a single enrichment file.
- **minPathwayCount** (integer, entered as string): minimum number of descendants a pathway has to have to be considered as an ancestor.
- **outputRoot** (string): remains consistent with the previous parts.

**_Example Usage (python)_**

```
# After specifying term_classes_to_pathways_path (path), pathway_to_go_id_ancestors (path), outputRoot (string)

from VisPathways import SummarizePathwayHierarchy
md = SummarizePathwayHierarchy(term_classes_to_pathways_path, pathway_to_go_id_ancestors, outputRoot)
```

**_Example Usage (command line)_**

The command line usage of the summarizePathwayHierarchy script will automatically execute the work function as outlined in the next part. Command line input of the summarizePathwayHierarchy python script requires/can take in the following arguments:

```
  -a PATHTOANCESTOR, --pathToAncestor PATHTOANCESTOR
                        path to ancestors
  -d ANCESTORTODESCENDANT, --ancestorToDescendant ANCESTORTODESCENDANT
                        node to descendant
  -p PATHWAYLIST, --pathwayList PATHWAYLIST
                        pathway list file
  -m MINPATHWAYCOUNT, --minPathwayCount MINPATHWAYCOUNT
                        minimum pathway count to consider an ancestor
  -o OUTPUTROOT, --outputRoot OUTPUTROOT
                        root of the output files
```

Here is an example:

```
python3 summarizePathwayHierarchy.py -a test.pathway_to_go_id_ancestors.xls -d test.term_classes_to_pathways.xls -p H_24hUV_over_30minUV_Enrichment.csv -m 10 -o test
```

#### _Function_ SummarizePathwayHierarchy.work

```

SummarizePathwayHierarchy.work()

```

Given outputs of any of the three functions above, generate:

- _OutputRoot_.pathway_count.xls (summarizing each enriched pathway's summary data)

_Note that because of the limited ontology information in Kegg and Reactome databases, it is generally recommended to use this method for GeneOntology rather than the other two databases._

**_Example Usage_**

```

# After specifying term_classes_to_pathways_path (path), pathway_to_go_id_ancestors (path), outputRoot (string)

from VisPathways import SummarizePathwayHierarchy
md = SummarizePathwayHierarchy(term_classes_to_pathways_path, pathway_to_go_id_ancestors, outputRoot)
md.generateSummaries()

```

### GOTrees

#### The initialization of an GOTrees object

```

GOTrees(outputRoot, canonicalEnrichment='', displayedEnrichmentColors=['Red', 'Green', 'Blue'], select='legit', enrichment=1, firstEnrichmentName='enrichment 1', enrichVis='pie', outputFormat='png', numOfBackgroundEnrichments=0, allEnrichmentColor='Purple'):

```

_Arguments:_

- **outputRoot** (string): remains consistent with the previous parts
- **canonicalEnrichment** (string): a canonical enrichment is the enrichment that you find the subroots of the plotted trees with. If you used the MergeDatabase class to generate summary stats, you may ignore this argument. However, if you used the **splitFilesAndRunSummary** to generate summary stats for your canonical enrichment, you might have additional characters in your summary xls files' names between _outputRoot_ and _.xls_, which is usually a column name. This argument is where you fill that part. By default it's an empty string.
- **displayedEnrichmentColors**. This is a list of up to 3 colors which by default would be ['Red', 'Green', 'Blue'], the colors used to color the up to 3 enrichments displayed in the pie charts or bubbles. Make sure you have the right number of colors here that match the number of displayed enrichments, otherwise you might catch errors. Color options can be seen [here](http://etetoolkit.org/docs/latest/reference/reference_treeview.html?highlight=color#color-names).
- **select** (string): **'all'** (visualize tree for all descendants of a selected node in the GeneOntology database) or **'legit'** (visualize tree for standard descendants of a selected node specified in the xml file in the GeneOntology database). By default, select has the value of 'legit'.
- **enrichment** (int): **1**, **2**, or **3**. Number of enrichment files displayed in one single tree graph. The current package supports up to 3 enrichments (1 default enrichment from summarization + 0-2 additional enrichment files). Note that the function will ask users to specify the path to additional enrichment files if applicable.
- **firstEnrichmentName** (string): default value **'enrichment 1'**. The name of the default enrichment from summarization displayed on the trees. Note that the function will ask users to specify the names of the other enrichment files if applicable.
- **enrichVis** (string): **'pie'** or **'sphere'**, default value **'pie'**, the two different ways to visualize enrichment annotations on ontology trees.
- **outputFormat** (string): **'png'**, **'pdf'**, or **'svg'**, default value **'png'**, three supported output formats of ontology visualizations.
- **numOfBackgroundEnrichments** (int): default value **0**. Background enrichments are those enrichments who will show up at the tips but not as part of the pie chart or sphere representation.
- **allEnrichmentColor** (str): color of all nodes that are ever enriched - i.e. either contained in one of the visualized enrichments in pie/bubble chart or contained by background enrichments. Color options can be seen [here](http://etetoolkit.org/docs/latest/reference/reference_treeview.html?highlight=color#color-names).

**_Example Usage (python)_**

```

# default usage

# After defining outputRoot (string)

from VisPathways import GOTrees
tr = GOTrees(outputRoot)

# more advanced usage

tr = GOTrees(outputRoot, canonicalEnrichment='aNewEnrichment', displayedEnrichmentColors = ['Yellow', 'Green', 'Brown'], enrichment = 3, outputFormat = 'pdf', allEnrichmentColor = 'Yellow')

```

**_Example Usage (command line)_**

The command line usage of the treeGO script will automatically execute the graphTreeWrapper function as outlined in the next part. Command line input of the treeGO python script requires/can take in the following arguments:

```

-o OUTPUTROOT, --outputRoot OUTPUTROOT
root of the output files
-c CANONICALENRICHMENT, --canonicalEnrichment CANONICALENRICHMENT
the prefix after the outputRoot for the canonical enrichment, if empty just do not enter this argument
-d DISPLAYEDENRICHMENTCOLORS [DISPLAYEDENRICHMENTCOLORS ...], --displayedEnrichmentColors DISPLAYEDENRICHMENTCOLORS [DISPLAYEDENRICHMENTCOLORS ...]
a list of up to 3 colors displayed in the pie chart/bubble chart, input format e.g.: Red Blue Green
-s SELECT, --select SELECT
two options for graphing - either legit and all, see documentation for more info
-e ENRICHMENT, --enrichment ENRICHMENT
number of enrichmets displayed in pie charts/bubble charts (up to 3)
-f FIRSTENRICHMENTNAME, --firstEnrichmentName FIRSTENRICHMENTNAME
displayed name of the first enrichment, default called 'enrichment 1'
-v ENRICHVIS, --enrichVis ENRICHVIS
type of enrichment visualization, either 'pie' or 'sphere', default 'pie'
-m OUTPUTFORMAT, --outputFormat OUTPUTFORMAT
output format, currently supporting 'png', 'pdf', 'svg', default 'png'
-n NUMOFBACKGROUNDENRICHMENTS, --numOfBackgroundEnrichments NUMOFBACKGROUNDENRICHMENTS
number of background enrichments, displayed as purple tips but not in pie chart or bubble chart
-a ALLENRICHMENTCOLOR, --allEnrichmentColor ALLENRICHMENTCOLOR
tip color for all nodes that are enriched, default purple

```

Here is an example:

```

python3 treeGO.py -o test -d Red Yellow Green -s legit -e 3 -a Green

```

#### _Function_ GOTrees.graphTreeWrapper

```

GOTrees.graphTreeWrapper()

```

Generate:

- _OutputRoot_.treeGraph*index*._outputFormat_ (tree visualizations of pathway ontology and enrichments, e.g. _test.treeGraph.1.svg_. The function can generate multiple tree graphs at a time.)

_Note that the function can also request users to input the following_

- The paths to additional enrichments (if applicable).
- The names of additional enrichments (if applicable).
- Segment Coloring (if _select = **'all**_, you can choose to color certain parts of the tree).

**_Example Usage (Python)_**

```

# After defining outputRoot (string)

from VisPathways import GOTrees
tr = GOTrees(outputRoot, displayedEnrichmentColors = ['Yellow', 'Green', 'Brown'], enrichment = 3, outputFormat = 'pdf', allEnrichmentColor = 'Yellow')
tree.graphTreeWrapper()

```

### EnrichmentPreprocess

#### The initialization of an GOTrees object

```

EnrichmentPreprocess(outputRoot, multiEn='', goSlims='', goXml='')

```

_Arguments:_

- **multiEn** (string): path to the enrichment file that contains multiple columns. The first column contains all the pathway names while the rest of the columns each contains the enrichment data. The method assumes a non-zero value in a cell as the pathway being enriched in that corresponding column. An example of such file would be the `namsed-pathwaysuper-sig-bp.txt` file in the `test` directory.
- **goSlims** (string): path to the ontology file such as `go-basic.obo`.
- **goXml** (string): path to the gsea xml file, such as `msigdb_v7.2.xml`.

**_Example Usage (python)_**

```

# After defining outputRoot (string)

from VisPathways import GOTrees
en = EnrichmentPreprocess(outputRoot, multiEn = 'namsed-pathwaysuper-sig-bp.txt', goSlims = 'go-basic.obo', goXml = 'msigdb_v7.2.xml')

```

**_Example Usage (command line)_**

The command line usage of the enrichment script will automatically execute the splitFilesAndRunSummary function as outlined in the next part. Command line input of the enrichment python script requires/can take in the following arguments:

```

-o OUTPUTROOT, --outputRoot OUTPUTROOT
root of the output files
-m MULTIEN, --multiEn MULTIEN
csv/txt format multiple enrichment file path
-g GOSLIMS, --goSlims GOSLIMS
gene ontology basic go slims path
-x GOXML, --goXml GOXML
XML version of the MSigDB GOBP path

```

Here is an example:

```

python3 enrichment.py -m /Users/chenlianfu/Documents/Github/FancyTaxonomies/stableUsage/test/testSourceData/namsed-pathwaysuper-sig-bp.txt -o hoa -g /Users/chenlianfu/Documents/Github/FancyTaxonomies/stableUsage/test/testSourceData/go-basic.obo -x /Users/chenlianfu/Documents/Github/FancyTaxonomies/stableUsage/test/testSourceData/msigdb_v7.2.xml

```

#### _Function_ EnrichmentPreprocess.splitFilesAndRunSummary

```

EnrichmentPreprocess.splitFilesAndRunSummary(runAncAndDes=False, deleteTempCSV=True)

```

_Arguments:_

- **runAncAndDes** (boolean): whether or not to run the part of the workflow that generates the `pathway_to_ancestor` and `pathway_to_descendant` files. If _False_ (by default), then the function assumes that you have the `pathway_to_ancestor` and `pathway_to_descendant` files in the current directory.
- **deleteTempCSV** (boolean): the function generates artifact csv files that are essentially the csv files needed to run one single enrichment summary with the **SummarizePathwayHierarchy** class. If you wish to keep these files, set this argument to False, otherwise, set it to True.

Generate:

A series of _OutputRoot_**columnName**.pathway_count.xls (the number of files in this series will be the number of columns in the input file)

If **runAncAndDes** is set to True, the method also generates:

- _OutputRoot_.term_classes_to_pathways.xls (summarizing each standard pathway and its descendants)
- _OutputRoot_.pathway_to_go_id_ancestors.xls (summarizing each standard pathway and its ancestors)

If **deleteTempCSV** is set to False, the method also generates a series of files that look like _outputRoot_**colNames**.temp.csv, each of which is a single enrichment file.

_Note that because of the limited ontology information in Kegg and Reactome databases, it is generally recommended to use this method for GeneOntology rather than the other two databases._

**_Example Usage (Python)_**

```

# After defining outputRoot (string), ontologyFile (string), xmlFile (string)

from VisPathways import EnrichmentPreprocess
en = EnrichmentPreprocess(outputRoot)
en.splitFilesAndRunSummary(source, ontologyFile, xmlFile, runAncAndDes=True)

```

## Tutorials

Here are two tutorials for using the whole summarization + visualization workflow. Note that you will need to do everything here in the Python environment! (You can do it by simply typing `python` or `python3` in your terminal and then return)

### 1. Single enrichment summarization + canonical tree visualization

```

from VisPathways import *
ontologyFile = 'go-basic.obo'
xmlFile = 'msigdb_v7.2.xml'
enrichmentFile = 'H_24hUV_over_30minUV_Enrichment.csv'
outputRoot = 'test'

# summarization

md = MergeDatabase(ontologyFile, xmlFile, enrichmentFile, outputRoot)
md.generateSummaries()

# visualization

gr = GOTrees(outputRoot, displayedEnrichmentColors = ['Yellow', 'Green', 'Brown'], enrichment = 3, outputFormat = 'pdf', allEnrichmentColor = 'Yellow')
gr.graphTreeWrapper()

## upon function request, select the third tree to plot (select top 3 enrichments, and select N to the first two tree and Y for the third tree), then input two additional enrichment files and their names (here we assign as 'enrichment 1' and 'yeehaw'), and we are done!

```

### 2. Multiple enrichment summarization + canonical tree visualization

```

from VisPathways import *
ontologyFile = 'go-basic.obo'
xmlFile = 'msigdb_v7.2.xml'
multiEnrichmentFile = 'namsed-pathwaysuper-sig-bp.txt'
outputRoot = 'hoa'

# summarization

<!-- md = MergeDatabase(ontologyFile, xmlFile, 'enrichmentPlaceholder', outputRoot)
md.generateAncAndDecOnly() -->
en = EnrichmentPreprocess(outputRoot, multiEn = multiEnrichmentFile, goSlims = ontologyFile, goXml = xmlFile)
en.splitFilesAndRunSummary(runAncAndDes=True)

# visualization

gr = GOTrees(outputRoot, displayedEnrichmentColors = ['Yellow', 'Green', 'Brown'], enrichment = 3, outputFormat = 'pdf', allEnrichmentColor = 'Yellow')
gr.graphTreeWrapper()

## upon function request, select the third tree to plot (select top 3 enrichments, and select N to the first two tree and Y for the third tree), then input two additional enrichment files and their names (here we assign as 'enrichment 1' and 'yeehaw'), and we are done!

```

## Acknowledgement

**author**: Chenlian (Tom) Fu, Dr. Cristian Coarfa\
**affiliation**: Coarfa Lab, Baylor College of Medicine\
**support**: Dr. Cristian Coarfa, Dr. Sandy Grimm, Dr. Tajhal Patel, Dr. Hoa Nguyen-Phuc

Cheers,\
TF\
6/1/2021
