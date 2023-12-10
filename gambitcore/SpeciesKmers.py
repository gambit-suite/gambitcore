import numpy as np
import logging

class SpeciesKmers:
    def __init__(self, genome_kmers, species):
        self.genome_kmers = genome_kmers
        self.species = species
        self.calculate_species_core_kmers_stats(self.genome_kmers, self.species)
        self.available_genomes = 0 
        self.used_genomes = 0

    def calculate_species_core_kmers_stats(self, genome_kmers, species):
        self.genome_kmers = np.array(genome_kmers)
        self.genome_kmers_mean = np.mean(genome_kmers)
        self.genome_kmers_std = np.std(genome_kmers)
        self.genome_kmers_min = np.min(genome_kmers)
        self.genome_kmers_max = np.max(genome_kmers)

        logging.info(f"Mean kmers for {species} in a genome: {self.genome_kmers_mean}")
        logging.info(f"Std dev kmers for {species} in a genome: {self.genome_kmers_std}")
        logging.info(f"Min kmers for {species} in a genome: {self.genome_kmers_min}")
        logging.info(f"Max kmers for {species} in a genome: {self.genome_kmers_max}")
