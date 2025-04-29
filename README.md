# GAMBITcore
This application takes in assemblies, identifies the species, then calculates the completeness of the assemblies against the species core genome.  This is 
a good quality control step. It is acheived by looking at the GAMBIT k-mers in the assembly and comparing them to the GAMBIT k-mers in the core genome. If the assembly is poor quality, it is expected that the completeness 
of the assembly will be lower.  If GAMBIT cannot make a species or subspecies level call, GAMBITcore will be skipped.

## Installation
If you want to quickly try out the software, please use the docker container.

### Dependencies
* Python 3.10 or higher
* GAMBIT

### Conda
![ananconda-version](https://anaconda.org/bioconda/gambitcore/badges/version.svg)
![conda-platform](https://anaconda.org/bioconda/gambitcore/badges/platforms.svg)
![last-update](https://anaconda.org/bioconda/gambitcore/badges/latest_release_date.svg)
```
conda install -c conda-forge -c bioconda gambitcore
```

### Docker
To build the container, run this command from the root of the repository:
```
docker build -t gambitcore:latest .
```

To run the software from the container, run this command:
```
docker run -v /path/to/gambit/database_directory:/gambit -v /path/to/fasta/files:/fasta -it --rm gambitcore:latest gambitcore /gambit /fasta/*.fasta
```

# Usage
## gambitcore
This script takes in assemblies and a GAMBIT database and caculates the completeness of the assemblies against the core genome of a species.

```
usage: gambitcore [options]

How complete is an assembly compared to the core genome of its species?

positional arguments:
  gambit_directory      A directory containing GAMBIT files (database and signatures)
  fasta_filenames       A list of FASTA files of genomes

options:
  -h, --help            show this help message and exit
  --concise, -e         concise output (default: False)
  --cpus CPUS, -p CPUS  Number of cpus to use (default: 1)
  --kmer KMER, -k KMER  Length of the k-mer to use (default: 11)
  --kmer_prefix KMER_PREFIX, -f KMER_PREFIX
                        Kmer prefix (default: ATGAC)
  --max_species_genomes MAX_SPECIES_GENOMES, -t MAX_SPECIES_GENOMES
                        Max number of genomes in a species to consider, ignore all others above this (default: 500)
  --core_proportion CORE_PROPORTION, -c CORE_PROPORTION
                        Proportion of genomes a kmer must be in for a species to be considered core (default: 0.98)
  --num_genomes_per_species NUM_GENOMES_PER_SPECIES, -r NUM_GENOMES_PER_SPECIES
                        Number of genomes to keep for a species (0 means keep all) (default: 1)
  --verbose, -v         Turn on verbose output (default: False)
```

__gambit_directory__: The GAMBIT directory must contain a file ending in *.gdb and a file ending in *.gs. If it doesnt have these file suffixes, then the script will not work.

__fasta_filenames__: This is a list of 1 or more assemblies in FASTA format. They can be gzipped or not. 

__help__: The help text and usage information

__concise__: This gives a short version of the output. The information is provided in a tab delimited format to standard out.

__cpus__: The number of CPUs to use for GAMBIT. This is set to 1 by default, but it will have a marginal impact on the overall running time. 

__kmer__: The length of the k-mer to use. This is set to 11 by default. Dont change this because it needs to match the GAMBIT signatures file.

__kmer_prefix__: The k-mer prefix to use. This is set to ATGAC by default. Dont change this because it needs to match the GAMBIT signatures file.

__max_species_genomes__: The maximum number of genomes to use for a species. This is set to 500 by default. If there are more than 500 genomes for a species, then the script will ignore all genomes above this number. This is to speed up the script because as you add more genomes to a pangenome, you get diminishing returns, unless it has a very open pangenome.  More genomes will also probably mean more random noise in the assemblies which would be captured, leading to a smaller core.

__core_proportion__: The proportion of genomes a k-mer must be in for a species to be considered core. This is set to 0.98 by default. This means that a k-mer must be in 98% of the genomes for a species to be considered core. This is to remove k-mers that are in a small number of genomes, which are probably not core, whilst also allowing some wiggle room for assembly errors.

__num_genomes_per_species__: The number of genomes to keep for a species. This is set to 1 by default. This means that if there are multiple genomes for a species, then only the first one will be used. This parameter will probably be removed because setting it to anything other than 1 will probably lead to incorrect results.

__verbose__: Turn on verbose output. This is set to False by default. This will give you more information about what the script is doing.

### Output
gambitcore will then output a tab delimited output to standard out that looks like this:

| Filename                            | Species                       | Completeness (%) | Assembly core/Species Core | Closest accession   | Closest distance | Assembly k-mers| Species k-mers Mean | Species k-mers Std Dev | Assembly QC |
|-------------------------------------|-------------------------------|------------------|----------------------------|---------------------|------------------|----------------|---------------------|------------------------|-------------|
| test/fasta/GCF_002800775.1.fna.gz   | Mycobacteroides abscessus     | 100.00%          | (5296/5296)                | GCF_000758385.1     | 0.0360           | 10847          | 10635               | 403                    | green       |
 
To get a concise output then use the -e flag:

| Filename        | Species                   | Completeness (%) |
|-----------------|---------------------------|------------------|
| /fasta/file1.fa | Mycobacteroides abscessus | 99.75%           |

The columns are:

__Filename__: The name of the input FASTA file upon which the analysis was performed.

__Species__: The predicted species from GAMBIT.

__Completeness (%)__: This is the percentage of core k-mers from the species found in the input assembly. A fully complete assembly should contain 100% of all the core k-mers. It is normal that some k-mers may not be present due to assembly errors, although a good quality assembly should be very close to 100%. The absolute number of core k-mers found, and the number of core k-mers expected, are in brackets. 

__Closest accession__: This is the accession number of the genome from the database which is closest to the input assembly, as determined by GAMBIT. All GAMBIT k-mers are used to calcuate this.

__Closest distance__: The GAMBIT distance/diameter to the closest accession. This is a decimal number between 0 and 1, which a lower number indicating a closer match. All GAMBIT k-mers are used to calcuate this.

__Assembly k-mers__: The total number of GAMBIT k-mers in the assembly. 

__Species k-mers mean__: The mean GAMBIT k-mers for the species (all GAMBIT k-mers, not just core ones). This gives you an indication of how large the core is compared to the mean k-mers (roughly the average size). 

__Species k-mers std dev__: The standard deviation of the number of GABMIT k-mers in a sample. 

__Assembly QC__: This is a colour coded output to give you an indication of the quality of the assembly. Green means the Assembly k-mers are within 2 standard deviations (95%) of the species k-mers mean.  Amber means the Assembly k-mers are between 2 and 3 standard deviations (99.7%) of the species k-mers mean. Red means the Assembly k-mers are more than 3 standard deviations of the species k-mers mean and something might be very wrong. This is a very rough guide, but it can be useful to quickly identify assemblies that are an unusual size relative to the species.

> :warning: Warning
> 
> If GAMBIT failes to make a species- or subspecies-level assignment, GAMBITcore will be skipped with the message "Species could not be identified, skipping core genome assessment". 


## gambitcore-species
This is a script which takes in a GAMBIT database and calculates the core k-mers for every species in the database. It then outputs the details for each species to a tab delimited file.

The usage for the script is:
```
usage: gambitcore-species [options]

Kmer statistics for all species in a database. Warning it can take a long time to run.

positional arguments:
  gambit_directory      A directory containing GAMBIT files (database and signatures)

options:
  -h, --help            show this help message and exit
  --species SPECIES, -s SPECIES
                        Provide the name of a single species, default is to use everything in the database (default: None)
  --cpus CPUS, -p CPUS  Number of cpus to use (default: 1)
  --kmer KMER, -k KMER  Length of the k-mer to use (default: 11)
  --kmer_prefix KMER_PREFIX, -f KMER_PREFIX
                        Kmer prefix (default: ATGAC)
  --max_species_genomes MAX_SPECIES_GENOMES, -t MAX_SPECIES_GENOMES
                        Max number of genomes in a species to consider, ignore all others above this (default: 500)
  --core_proportion CORE_PROPORTION, -c CORE_PROPORTION
                        Proportion of genomes a kmer must be in for a species to be considered core (default: 0.98)
  --num_genomes_per_species NUM_GENOMES_PER_SPECIES, -r NUM_GENOMES_PER_SPECIES
                        Number of genomes to keep for a species (0 means keep all) (default: 1)
  --verbose, -v         Turn on verbose output (default: False)
```

The parameters are the same as above with the following exceptions:

__species__: This is a single string containing a species name which will be used to generate statistics for. It must be present in the database with the exact same string. 

### Output
gambitcore-species will then output a tab delimited output to standard out that looks like this:

| Species                      | Core k-mers | Mean k-mers | k-mers Std Dev | Min k-mers | Max k-mers | Available Genomes | Used Genomes |
|------------------------------|------------|------------|---------------|-----------|-----------|-------------------|--------------|
| Achromobacter xylosoxidans   | 4983       | 11076      | 365           | 10366     | 12167     | 133               | 133          |
| Acinetobacter baumannii      | 3014       | 8542       | 221           | 7907      | 9410      | 1276              | 500          |
| Bifidobacterium bifidum      | 3709       | 6218       | 121           | 5957      | 6539      | 23                | 23           |
| Campylobacter coli           | 164        | 1256       | 61            | 1039      | 1437      | 252               | 252          |
| Campylobacter jejuni         | 380        | 1306       | 49            | 1105      | 1454      | 556               | 500          |
| Salmonella enterica          | 5319       | 10616      | 324           | 9729      | 12333     | 4048              | 500          |

The columns are as previous with the following additions:

__min k-mers__: The lowest number of k-mers in a genome in the database for that species. If the min is far lower than the mean, accounting for the standard deviation, then it could indicate a highly variable species or assembly errors in the genomes in the database.

__max k-mers__: The highest number of k-mers in a genome in the database for that species. If the max is far higher than the mean, accounting for the standard deviation, then it could indicate a highly variable species or assembly errors in the genomes in the database.

__available genomes__: This is the number of genomes in the database for the given species. 

__used genomes__: The number of genomes used to generate the core k-mers. This can be lower than the avialable genomes if the user supplied parameter is set. This parameter is used to reduce the overall running time.

