# GAMBITcore
This application takes in assemblies, identifies the species, then calculates the completeness of the assemblies against the species core genome.  This is 
a good quality control step. It is acheived by looking at the GAMBIT k-mers in the assembly and comparing them to the GAMBIT k-mers in the core genome. If the assembly is poor quality, it is expected that the completeness 
of the assembly will be lower.  

## Installation
If you want to quickly try out the software, please use the docker container.

### Dependencies
* Python 3.9 or higher
* GAMBIT

### Docker
To build the container, run this command from the root of the repository:
```
docker build -t gambitcore:latest .
```

To run the software from the container, run this command:
```
docker run -v /path/to/gambit/database_directory:/gambit -v /path/to/fasta/files:/fasta -it --rm gambitcore:latest gambitcore /gambit /fasta/*.fasta
```

You will then get a tab delimited output to standard out that looks like this:

| Filename        | Species                   | Completeness (%) |
|-----------------|---------------------------|------------------|
| /fasta/file1.fa | Mycobacteroides abscessus | 99.75%           |


To get an extended output then use the -e flag:
```

```


# Usage
This scripts takes in assemblies and a GAMBIT database and caculates the completeness of the assemblies against the core genome of a species.

```
usage: gambitcore [options]
How complete is an assembly compared to the core genome of its species?

positional arguments:
  gambit_directory      A directory containing GAMBIT files (database and signatures)
  fasta_filenames       A list of FASTA files of genomes

options:
  -h, --help            show this help message and exit
  --extended, -e        Extended output (default: False)
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
__extended__: This will give you more information about the completeness of the assembly. It will give you the number of GAMBIT k-mers in the core genome, the number of GAMBIT k-mers in the assembly that are in the core genome, and the proportion of k-mers in the assembly that are in the core genome. The information is provided in a tab delimited format to standard out.
__cpus__: The number of CPUs to use for GAMBIT. This is set to 1 by default, but it will have a marginal impact on the overall running time. 
__kmer__: The length of the k-mer to use. This is set to 11 by default. Dont change this because it needs to match the GAMBIT signatures file.
__kmer_prefix__: The k-mer prefix to use. This is set to ATGAC by default. Dont change this because it needs to match the GAMBIT signatures file.
__max_species_genomes__: The maximum number of genomes to use for a species. This is set to 500 by default. If there are more than 500 genomes for a species, then the script will ignore all genomes above this number. This is to speed up the script because as you add more genomes to a pangenome, you get diminishing returns, unless it has a very open pangenome.  More genomes will also probably mean more random noise in the assemblies which would be captured, leading to a smaller core.
__core_proportion__: The proportion of genomes a k-mer must be in for a species to be considered core. This is set to 0.98 by default. This means that a k-mer must be in 98% of the genomes for a species to be considered core. This is to remove k-mers that are in a small number of genomes, which are probably not core, whilst also allowing some wiggle room for assembly errors.
__num_genomes_per_species__: The number of genomes to keep for a species. This is set to 1 by default. This means that if there are multiple genomes for a species, then only the first one will be used. This parameter will probably be removed because setting it to anything other than 1 will probably lead to incorrect results.
__verbose__: Turn on verbose output. This is set to False by default. This will give you more information about what the script is doing.
