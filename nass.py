import numpy as np
from sys import exit
from copy import copy
from common.base import partition
import re
#====== Nucleic Acid Secondary Structure =======================================
class Nass:
    pass
#Nass attributes
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def __init__(self, fn=None):
        self.remark = ''
        self.resn = []
        self.resi = []
        self.pair = []
        self.i = []
        self.i5 = []
        self.i3 = []
        self.pk = []
        if fn:
            self.read(fn)
#read function, supports multiple formats including ct, dot-bracket, bpseq, and st
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def read(self, fn, ftype=None):
        if isinstance(fn, str):
            lines = open(fn).readlines()
            if ftype is None:
                ftype = fn.split('.')[-1]
        else:
            lines = fn  # used when using class Nasses
            if ftype is None:
                ftype = 'ct'  # ct format is the most common

        lines = [x for x in lines if x.strip()!='' and x[:1]!='#']
        ##### for ct format
        if ftype == 'ct':
            self.remark = lines[0].rstrip()
            if self.remark[:1]=='>':
                self.remark = self.remark[1:]
            for line in lines[1:]:
                fds = line.split('#')[0].split()  # it may end with a comment
                self.i.append(int(fds[0]))
                self.resn.append(fds[1])
                self.i5.append(int(fds[2]))
                self.i3.append(int(fds[3]))
                self.pair.append(int(fds[4]))
                self.resi.append(int(fds[5]))
            self.n = len(self.resn)
            self.pk = [0]*self.n
        ##### for dot-bracket notation format
        elif ftype in ('dot', 'dbn'):
            if len(lines) != 3:
                print('There are more than 3 lines in dbn file!')
                exit(1)
            self.remark = lines[0][1:].strip()
            self.resn = list(lines[1].strip())
            self.n = len(self.resn)
            dbn = lines[2].strip()
            if len(dbn) != self.n:
                print('Lengths of seq and dbn do not match!')
                exit(1)
            self.i = list(range(1, self.n+1))
            self.i5 = [0] + self.i[:self.n-1]
            self.i3 = self.i[1:] + [0]
            self.resi = copy(self.i)
            self.pair = [0]*self.n
            bps,pks = unwrap_dbn(dbn)
            self.pk = pks
            for idx0,idx1 in bps:
                self.pair[idx0] = idx1+1
                self.pair[idx1] = idx0+1
        ##### for st format
        elif ftype == 'st':
            self.resn = list(lines[0].strip())
            self.n = len(self.resn)
            dbn = lines[1].strip()
            if len(dbn) != self.n:
                print('Lengths of seq and dbn do not match!')
                exit(1)
            pk = lines[3].strip()
            if len(pk) != self.n:
                print('Lengths of seq and pseudoknot-label do not match!')
                exit(1)
            self.i = list(range(1, self.n+1))
            self.i5 = [0] + self.i[:self.n-1]
            self.i3 = self.i[1:] + [0]
            self.resi = copy(self.i)
            self.pair = [0]*self.n
            bps,pks = unwrap_dbn(dbn)
            self.pk = pks
            for idx0,idx1 in bps:
                self.pair[idx0] = idx1+1
                self.pair[idx1] = idx0+1
        ##### for bpseq format
        elif ftype == 'bpseq':
            for line in lines:
                fds = line.split()
                self.i.append(int(fds[0]))
                self.resn.append(fds[1])
                self.pair.append(int(fds[2]))
            self.n = len(self.resn)
            self.i5 = [0] + self.i[:self.n-1]
            self.i3 = self.i[1:] + [0]
            self.resi = copy(self.i)
            self.pk = [0]*self.n
        else:
            print('Unsurported format: %s!'%ftype)
            exit(0)
# Remove non-classical base pairs, i.e. non-CG, AU, GU base pairs, for mcfold software
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def rm_ncbp(self):
        '''
        Remove non-canonical base pairs
        '''
        for idx,p in enumerate(self.pair):
            if p != 0:
                bp = ''.join(sorted([self.resn[idx],self.resn[p-1]]))
                if bp not in ('CG','AU','GU'):
                    self.pair[idx] = 0
                    self.pk[idx] = 0
# remove pesudo nots
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def rm_pk(self):
        '''
        Remove pseudoknots
        '''
        for idx,pk in enumerate(self.pk):
            if pk != 0:
                self.pair[idx] = 0
                self.pk[idx] = 0
# Returns a two-dimensional array representing the pairing between bases in a nucleic acid molecule.
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def ctmap(self):
        m = np.zeros((self.n,self.n), dtype='int16')
        for idx,p in enumerate(self.pair):
            if p:
                m[idx, p-1] = 1
        return m
# Write the processed data to a file, supporting multiple formats.
    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def write(self, fn):
        ftype = fn.split('.')[-1]
        ##### for ct format
        if ftype == 'ct':
            f = open(fn, 'wt')
            f.write(self.remark+'\n')
            for x in zip(self.i,self.resn,self.i5,self.i3,self.pair,self.resi):
                f.write('%5d %s %5d %5d %5d %5d\n'%tuple(x))
            f.close()
        ##### for dot bracket notation format
        elif ftype in ('dot','dbn'):
            f = open(fn, 'wt')
            f.write('>%s\n'%self.remark)
            f.write(''.join(self.resn) + '\n')
            for i,p,pk in zip(self.i,self.pair,self.pk):
                if p == 0:
                    f.write('.')
                else:
                    if pk == 0:
                        f.write('(' if i<p else ')')
                    elif pk == 1:
                        f.write('[' if i<p else ']')
                    else:
                        f.write('{' if i<p else '}')
            f.write('\n')
            f.close()
        else:
            print('Unsurported format: %s!'%ftype)
            exit(0)

#====== Nucleic Acid Multiple Secondary Structure ==============================
class Nasses():
    pass

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def __init__(self, fn=None):
        self.items = []
        self.E = []
        if fn:
            self.read(fn)

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def read(self, fn):
        ftype = fn.split('.')[-1]
        lines = open(fn).readlines()
        lines = [x for x in lines if x.strip()!='' and x[:1]!='#']


        if ftype == 'ct':
            blks = partition(lines, isborder=lambda x: x.split()[1]=='ENERGY',
                             include='header')
            for blk in blks:
                ss = Nass(blk)
                self.items.append(ss)
                self.E.append(float(ss.remark.split()[3]))


        else:
            print('Unsurported format: %s!'%ftype)
            exit(0)

    # ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    def write(self, fn):
        ftype = fn.split('.')[-1]
        ##### for ct format
        if ftype == 'ct':
            f = open(fn, 'wt')
            for ss in self.items:
                f.write(ss.remark+'\n')
                for x in zip(ss.i,ss.resn,ss.i5,ss.i3,ss.pair,ss.resi):
                    f.write('%5d %s %5d %5d %5d %5d\n'%tuple(x))
            f.close()
        elif ftype in ('dot','dbn'):
            f = open(fn, 'wt')
            for ss in self.items:
                f.write(ss.remark+'\n')
                for x in zip(ss.i,ss.resn,ss.i5,ss.i3,ss.pair,ss.resi):
                    f.write('%5d %s %5d %5d %5d %5d\n'%tuple(x))
            f.close()
        else:
            print('Unsurported format: %s!'%ftype)
            exit(0)

    # ++++ End of class definition +++++++++++++++++++++++++++++++++++++++++++++

####### Public Functions #######################################################
# ==============================================================================
# Parse the dbn file and store the base pairs and pseudoknots in the dbn file into bps and pks respectively
def unwrap_dbn(dbn):
    stack0,stack1,stack2 = [],[],[]  # stacks for (),[],{}, respectively
    bps = []  # base pairs identified from stacks
    pks = []  # store info of pseudoknot
    # parse the dot bracket string
    for idx,c in enumerate(dbn):
        if c == '(':
            stack0.append(idx)
            pks.append(0)
        elif c == ')':
            bps.append((stack0.pop(),idx))
            pks.append(0)
        elif c == '[':
            stack1.append(idx)
            pks.append(1)
        elif c == ']':
            bps.append((stack1.pop(),idx))
            pks.append(1)
        elif c == '{':
            stack2.append(idx)
            pks.append(2)
        elif c == '}':
            bps.append((stack2.pop(),idx))
            pks.append(2)
        else:
            pks.append(0)
    return bps,pks
# calculate F1 score
# ==============================================================================
def calcF1(tgt, ref):
    '''
    tgt/ref can be either Nass object or contact map
    '''
    mtgt = tgt.ctmap() if isinstance(tgt, Nass) else tgt
    mref = ref.ctmap() if isinstance(ref, Nass) else ref
    if mtgt.shape != mref.shape:
        print('Sizes of tgt and ref do not match!')
        exit(1)
    # compare contact map
    tgt_paired = (mtgt==1)
    tgt_unpair = (mtgt==0)
    ref_paired = (mref==1)
    ref_unpair = (mref==0)
    nTP = np.sum(np.logical_and(ref_paired, tgt_paired))
    nTN = np.sum(np.logical_and(ref_unpair, tgt_unpair))
    nFP = np.sum(np.logical_and(ref_unpair, tgt_paired))
    nFN = np.sum(np.logical_and(ref_paired, tgt_unpair))
    #------------------------------------
    SN = nTP/(nTP+nFN) if nTP+nFN else 0
    PR = nTP/(nTP+nFP) if nTP+nFP else 0
    if PR+SN:
        F1 = 2.0*PR*SN / (PR+SN)
    else:
        F1 = 0.
    #------------------------------------
    return F1
# ==============================================================================
# This function divides the .dbn file containing multiple RNA sequences into multiple objects and writes them into a list
def split_rna_sequences(contents):
    rna_list = []
    current_rna = []  # Initialize current_rna

    for line in contents.splitlines():
        if line.startswith('>ENERGY'):
            if current_rna:
                # When a new RNA sequence is encountered, the current RNA sequence is added to the list
                rna_list.append('\n'.join(current_rna))
                current_rna = []
        current_rna.append(line.strip())
    
    # Add the last RNA sequence
    if current_rna:
        rna_list.append('\n'.join(current_rna))

    return rna_list

