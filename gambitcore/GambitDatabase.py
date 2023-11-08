import os
import tempfile
import numpy as np
import logging
from gambit.sigs import load_signatures, dump_signatures, AnnotatedSignatures, SignatureArray

class GambitDatabase:
    def __init__(self, gambit_directory):
        self.gambit_directory = gambit_directory
        pass

    # given a GAMBIT directory, find the file ending in .gdb (the database) and the file ending in .gs (the signatures).
    def find_gambit_files(self):
        gambit_files = os.listdir(self.gambit_directory)
        database_filename = None
        signatures_filename = None

        for filename in gambit_files:
            if filename.endswith('.gdb'):
                database_filename = os.path.join(self.gambit_directory,filename)
            elif filename.endswith('.gs'):
                signatures_filename = os.path.join(self.gambit_directory,filename)

        return database_filename, signatures_filename

    def get_kmers_from_fasta(self, fasta_filename, kmer, kmer_prefix,  cpus):
     with tempfile.TemporaryDirectory() as temp_dir:
        tmp_sigs_file = os.path.join(temp_dir, 'tmp_sigs_file.gs')
        os.system(f"gambit signatures create -c {cpus} -k {kmer} -p {kmer_prefix} -o {tmp_sigs_file} --no-progress {fasta_filename}")

        with load_signatures(tmp_sigs_file) as src:
            return src[0]

    # Given an accession number get the kmers in the signature (the integer corresponding to kmers rather than the actual sequences)
    def get_closest_kmers(self, closest_accession, signatures_filename):
        with load_signatures(signatures_filename) as src:
            in_gidxs = np.flatnonzero(np.in1d(src.ids, [closest_accession]))
            filtered_src = src[in_gidxs][0]
            return filtered_src
    
    def write_updated_signatures(self, core_src, core_src_ids, signatures_output_filename, src):
        core_src_sa = SignatureArray(core_src, kmerspec=src.kmerspec, dtype=src.dtype)
        out_sigs = AnnotatedSignatures(core_src_sa, np.array(core_src_ids), src.meta)
        dump_signatures(signatures_output_filename, out_sigs)
