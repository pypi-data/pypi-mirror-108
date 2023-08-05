import math
import argparse
import matplotlib.pyplot as plt
import sys
from Bio import SeqIO
from collections import namedtuple
import os
import gzip
import shutil


class Object:
    def __init__(self, sequence, nuc_1, nuc_2, stepsize=None, windowsize=None):
        self.stepsize = stepsize if stepsize is not None else None
        self.windowsize = windowsize if windowsize is not None else None
        self.sequence = sequence
        self.nuc_1 = nuc_1
        self.nuc_2 = nuc_2
    def gen_stepsize(self):
        return int(len(self.sequence) / 1000)

    def gen_windowsize(self):
        return int(len(self.sequence) / 1000)

    def gen_results(self):
            if not self.stepsize:
                self.stepsize = self.gen_stepsize()
            if not self.windowsize:
                self.windowsize = self.gen_windowsize()
            x = []
            y1 = []
            y2 = []
            y2_scaled = []
            cumulative_unscaled = 0
            cm_list = []
            i = int(self.windowsize / 2)
            for each in range(math.ceil(len(self.sequence) / self.stepsize)):
                a = self.sequence[i - int(self.windowsize / 2):i + int(self.windowsize / 2)].count(self.nuc_1)
                b = self.sequence[i - int(self.windowsize / 2):i + int(self.windowsize / 2)].count(self.nuc_2)
                skew = (a - b) / (a + b)
                y1.append(skew)
                cumulative_unscaled = cumulative_unscaled + skew
                y2.append(cumulative_unscaled)
                x.append(i + 1)
                cm_list.append(cumulative_unscaled)
                i = i + self.stepsize
            cm = max(cm_list)
            m = max(y1)
            scale = m / cm
            max_position = y2.index(max(y2)) * self.stepsize
            min_position = y2.index(min(y2)) * self.stepsize
            for j in cm_list:
                y2_scaled.append(j * scale)
            results = namedtuple("results",
                                 ['x', 'skew', 'cumulative', 'cumulative_unscaled', 'max_cumulative', 'min_cumulative',
                                  'max_cm_position', 'min_cm_position', 'stepsize', 'windowsize', 'nuc_1', 'nuc_2'])
            return results(x, y1, y2_scaled, cm_list, max(y2), min(y2), max_position, min_position, self.stepsize, self.windowsize,
                           self.nuc_1, self.nuc_2)


def input_files(file_location_list, file_type):
    is_gzip = False
    is_directory = False
    c = 0
    file_location_processed = []
    to_delete = []
    for file_location in file_location_list:
        try:
            with gzip.open(file_location, 'r') as fh:
                try:
                    fh.read(1)
                    is_gzip = True
                    with gzip.open(file_location, 'rt') as f_in:
                        with open(file_location.replace('.gz', ''), 'wt') as f_out:
                            shutil.copyfileobj(f_in, f_out)
                            file_location_processed.append(file_location.replace('.gz', ''))
                            to_delete.append(file_location.replace('.gz', ''))
                except gzip.BadGzipFile:
                    pass
        except IsADirectoryError:
            # os.scandir anstatt listdir
            for entry in os.listdir(file_location):
                if os.path.isfile(os.path.join(file_location, entry)):
                    is_directory = True
                    if os.path.join(file_location, entry).split('.')[-1] == file_type:
                        file_location_processed.append(file_location + "/" + entry)
                    if os.path.join(file_location, entry).split('.')[-1] == 'gz':
                        is_gzip = True
                        with gzip.open(os.path.join(file_location, entry), 'rt') as f_in:
                            with open(os.path.join(file_location, entry).replace('.gz', ''), 'wt') as f_out:
                                shutil.copyfileobj(f_in, f_out)
                                file_location_processed.append(
                                    os.path.join(file_location, entry).replace('.gz', ''))
                                to_delete.append(os.path.join(file_location, entry).replace('.gz', ''))
        if not is_directory:
            # if not is_directory geht auch -> besser lesbar
            if not is_gzip:
                file_location_processed.append(file_location)
        is_gzip = False
        is_directory = False
        c = c + 1
    return file_location_processed


def gen_sequence(file_location, file_type):
    with open(file_location) as handle:
        for seq_record in SeqIO.parse(handle, file_type):
            pass
    sequence = ''.join(
        [str(elem) for elem in [seq_record.seq for seq_record in SeqIO.parse(file_location, file_type)]])
    if len(sequence) == sequence.count("N"):
        sys.exit("There seems to be no sequence in your file!")
    return sequence

# brauch ich das wirklich als methode?
def plot_sequence(results, filelocation, outputfolder=None, out_file_type=None, dpi=None):
    #if not_spec == 'vuusjv7i93':
    #    outputfolder = filelocation.replace(filelocation.split('/')[-1], "")
    if not outputfolder:
        outputfolder = filelocation.replace(filelocation.split('/')[-1], "")
        not_spec = 'vuusjv7i93'
    if not out_file_type:
        out_file_type = 'png'
    fig, ax = plt.subplots()
    # plotting the graph
    ax.plot(results.x, results.skew, color="blue", linewidth=0.3)
    ax.plot(results.x, results.cumulative, color="red", linewidth=0.3)
    ax.axvline(x=int(results.max_cm_position), color="green", linewidth=0.3,
               label="maximum, at " + str(results.max_cm_position))
    ax.axvline(x=int(results.min_cm_position), color="green", linewidth=0.3,
               label="minimum, at " + str(results.min_cm_position))
    ax.set_title("Gen-skew plot for sequence: " + ", with stepsize: " + str(  # + q_variables[b].description
        results.stepsize) + " and windowsize: " + str(results.windowsize))
    ax.set_xlabel("position in sequence")
    ax.set_ylabel(results.nuc_1 + " " + results.nuc_2 + " skew")
    ax.grid(b=None, which='major', axis='both')
    ax.ticklabel_format(axis='x', style='plain')
    ax.legend()
    fig.savefig(
        outputfolder + '/' + filelocation.replace(".fasta", "").split('/')[
            -1] + results.nuc_1 + results.nuc_2 + "skew." + out_file_type,
        bbox_inches='tight', dpi=dpi)





# '/home/julius/Downloads/sequence.fasta'
