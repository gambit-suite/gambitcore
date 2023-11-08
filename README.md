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

# Usage
The script takes one or more FASTA files as input (optionally gzipped), and a directory to a GAMBIT database. The GAMBIT directory must contain a file ending in *.gdb and a file ending in *.gs. 

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

