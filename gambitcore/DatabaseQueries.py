import sqlite3
import logging

class DatabaseQueries:

    def __init__(self, database_filename):
        self.database_filename = database_filename
        self.cursor = self.connect_to_db(database_filename)

    def find_species_from_accession(self, closest_accession):
    
        sql = '''
        SELECT taxa.name
        FROM genomes
        JOIN genome_annotations ON genomes.id = genome_annotations.genome_id
        JOIN taxa ON genome_annotations.taxon_id = taxa.id
        WHERE genomes.refseq_acc = ?
        '''
    
        self.cursor.execute(sql, (closest_accession,))
        species_name = self.cursor.fetchone()
    
        species_name_for_accession = 'Unknown'
        if species_name:
            species_name_for_accession = species_name[0]
    
        return species_name_for_accession
    
    # only get species not subspecies
    def get_all_species_from_db(self):
        taxa = [row[0] for row in self.cursor.execute("SELECT name FROM taxa WHERE rank LIKE 'species'  ORDER BY name ASC")]
        return taxa

    def get_species_from_genomes_accession_from_db(self, genome_accession):
      try:
        query = """
          SELECT t.name AS species_name, GROUP_CONCAT(g.refseq_acc) AS genbank_accessions
          FROM genomes g
          JOIN genome_annotations ga ON g.id = ga.genome_id
          JOIN taxa t ON ga.taxon_id = t.id AND t.rank = 'species' 
          WHERE g.refseq_acc = ? 
          GROUP BY t.name
        """
        self.cursor.execute(query, (genome_accession,))
        results = self.cursor.fetchall()
        # make sure the results array is not empty
        if len(results) == 0:
            return None
        species = results[0][0]
    
        return species
      except sqlite3.Error as e:
        logging.error(f"get_species_from_genomes_accession_from_db - Database query error: {e}")
        exit(1)
    
    def connect_to_db(self, db_name):
        try:
            return sqlite3.connect(db_name).cursor()
        except sqlite3.Error as e:
            logging.error(f"Error connecting to the database: {e}")
            exit(1)
    
    # get species and subspecies
    def get_all_genomes_for_a_species_from_db(self, species):
        try:
            query = """
                SELECT t.name AS species_name, GROUP_CONCAT(g.refseq_acc) AS genbank_accessions
                FROM genomes g
                JOIN genome_annotations ga ON g.id = ga.genome_id
                JOIN taxa t ON ga.taxon_id = t.id AND t.rank IS NOT 'genus'
                WHERE t.name LIKE ?
                GROUP BY t.name
            """
            like_pattern = species + '%'
            self.cursor.execute(query, (like_pattern,))
            results = self.cursor.fetchall()
            
            results_taxon_to_accessions = {row[0]: row[1].split(",") for row in results}
            species_to_accessions = {}
            species_to_accessions[species] = [item for sublist in results_taxon_to_accessions.values() for item in sublist]
            return species_to_accessions
        except sqlite3.Error as e:
            logging.error(f"get_all_genomes_for_a_species_from_db - Database query error: {e}")
            exit(1)
