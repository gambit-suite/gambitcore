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
        if len(genome_kmers) == 0:
            logging.info(f"No genomes for {species} in the database")
            return
        self.genome_kmers = np.array(genome_kmers)
        self.genome_kmers_mean = np.mean(genome_kmers)
        self.genome_kmers_std = np.std(genome_kmers)
        self.genome_kmers_min = np.min(genome_kmers)
        self.genome_kmers_max = np.max(genome_kmers)

        logging.info(f"Mean kmers for {species} in a genome: {self.genome_kmers_mean}")
        logging.info(f"Std dev kmers for {species} in a genome: {self.genome_kmers_std}")
        logging.info(f"Min kmers for {species} in a genome: {self.genome_kmers_min}")
        logging.info(f"Max kmers for {species} in a genome: {self.genome_kmers_max}")

    def __str__(self):
        return f"Species: {self.species}\nMean kmers for {self.species} in a genome: {self.genome_kmers_mean}\nStd dev kmers for {self.species} in a genome: {self.genome_kmers_std}\nMin kmers for {self.species} in a genome: {self.genome_kmers_min}\nMax kmers for {self.species} in a genome: {self.genome_kmers_max}\nAvailable genomes: {self.available_genomes}\nUsed genomes: {self.used_genomes}"

    def quality_control_rag_for_assembly(self, num_assembly_kmers):
        quality_string = 'red'
        if num_assembly_kmers == 0 or self.genome_kmers_mean == 0:
            quality_string = "red"
        elif num_assembly_kmers >= self.genome_kmers_mean - self.genome_kmers_std and num_assembly_kmers <= self.genome_kmers_mean + self.genome_kmers_std:
            quality_string =  "green"
        elif num_assembly_kmers >= self.genome_kmers_mean - (2*self.genome_kmers_std) and num_assembly_kmers <= self.genome_kmers_mean + (2*self.genome_kmers_std):
            quality_string =  "amber"
        return quality_string
