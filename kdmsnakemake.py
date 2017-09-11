from collections import defaultdict
import re

__version__ = "0.0.1"
__all__ = ["make_regions", "make_chromosomes"]



def parsefai(fai):
    """Parses a fasta index, yielding (chomosome, length) pairs"""
    with open(fai) as fh:
        for l in fh:
            cname, clen, _, _, _ = l.split()
            clen = int(clen)
            yield cname, clen


def make_regions(rdict, window=1e6):
    """Splits a reference into `window` sized windows.

    Makes a list of regions for each reference in a dict of {refname:
        refpath: entries.

    :param rdict: dict of {refname: refpath, ...}
    :param window: Size of windows
    :returns: dict of {refname: {region: coordinates, ...}, ...}
    """
    window = int(window)
    ret = {}
    for refname, refpath in rdict.items():
        fai = refpath+".fai"
        windows = []
        curwin = []
        curwinlen = 0
        for cname, clen in parsefai(fai):
            if clen < window:
                curwinlen += clen
                reg = "{}:1-{}".format(cname, clen)
                curwin.append(reg)
                if curwinlen > window:
                    windows.append(curwin)
                    curwin = []
                    curwinlen = 0
            else:
                for start in range(0, clen, window):
                    wlen = min(clen - start, window)
                    windows.append(["{}:{}-{}".format(cname, start, start+wlen)])
        if len(curwin) > 0:
            windows.append(curwin)

        ref = dict()
        for i, w in enumerate(windows):
            wname = "W{:05d}".format(i)
            ref[wname] = w
        ret[refname] = ref
    return ret


def make_chromosomes(rdict, chrom_regex="^chr"):
    """Splits a reference into chromosome chunks

    Makes a list of regions for each reference in a dict of {refname: refpath}
    entries. Sequences matching `chrom_regex` appear as their own entires, all
    other sequences appear under a "scaffols" pseudo-chromosome.

    :param rdict: dict of {refname: refpath, ...}
    :param chrom_regex: Regular expression that (case-insensitively) matches
                        proper chromosomes.
    :returns: dict of {refname: {chromosome_set: [refseq_name, ...]}, ...}
    """
    ret = {}
    ischrom = re.compile(chrom_regex, re.IGNORECASE)
    for refname, refpath in rdict.items():
        fai = refpath + ".fai"
        ref = dict()
        scafs = []
        for cname, clen in parsefai(fai):
            if ischrom.match(cname) is not None:
                ref[cname] = [cname]
            else:
                scafs.append(cname)
        ref["scaffolds"] = scafs
        ret[refname] = ref
    return ret
