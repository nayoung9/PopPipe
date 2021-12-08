#!/usr/bin/env python3.6

import os
import re
import sys
import argparse

import subprocess as sub
from collections import defaultdict

import Param

def tree() :
    return defaultdict(tree)


def config() :
    parser = argparse.ArgumentParser(description='Popultaion analysis')
    parser.add_argument('-P', '--param', help='<Path> parameter file', required=True)
    parser.add_argument('-O', '--out_dir', help='<Path> output directory', required=True)
    parser.add_argument('-V', '--verbose', help='<Int> if you want to se command line, set 1 (default 0)', required=True)
    args = parser.parse_args()

    return args

def ParseInput(input_, out) :
    dict_input = tree()

    sample, step, flag = "", "", 0
    for line in open(input_, 'r') :
        line = line.strip()
        if re.match(r'\s*$', line) :
            continue
        elif line.startswith('####') :
            match = (line.replace('####', '')).strip()
            if not match == "Population" :
                sys.stderr.write("Require the population input file\n")
                sys.stderr.flush()
                sys.exit()
        elif line.startswith('###') :
            step = (line.replace('###', '')).strip()
        elif line.startswith('<') :
            sample = (line.replace('<', '').replace('>', '')).strip()
        elif not line.startswith('#') :
            if step == "BAM" :
                if not os.path.isdir(out + "/01_ReadMapping/") :
                    sub.call(f'mkdir {out}/01_ReadMapping', shell=True)
                if not os.path.isdir(out + "/01_ReadMapping/04.ReadRegrouping") :
                    sub.call(f'mkdir {out}/01_ReadMapping/04.ReadRegrouping', shell=True)
 
                sub.call(f'ln -s {line} {out}/01_ReadMapping/04.ReadRegrouping/{sample}.bam', shell=True)

            elif step == "Vcf" :
                if not os.path.isdir(out + "/02_VariantCalling/") :
                    sub.call(f'mkdir {out}/02_VariantCalling', shell=True)
                if not os.path.isdir(out + "/02_VariantCalling/VariantCalling") :
                    sub.call(f'mkdir {out}/02_VariantCalling/VariantCalling', shell=True)
                if not os.path.isdir(out + "/02_VariantCalling/VariantCalling/FINAL") :
                    sub.call(f'mkdir {out}/02_VariantCalling/VariantCalling/FINAL', shell=True)

                sub.call(f'ln -s {line} {out}/02_VariantCalling/VariantCalling/FINAL/', shell=True)

            elif step == "Plink" :
                if not os.path.isdir(out + "/03_Postprocessing") :
                    sub.call(f'mkdir {out}/03_Postprocessing', shell=True)
                if not os.path.isdir(out + "/03_Postprocessing/plink") :
                    sub.call(f'mkdir {out}/03_Postprocessing/plink', shell=True)

                sub.call(f'ln -s {line}* {out}/03_Postprocessing/plink/', shell=True)

            elif step == "Hapmap" :
                if not os.path.isdir(out + "/03_Postprocessing") :
                    sub.call(f'mkdir {out}/02_Postprocessing', shell=True)
                if not os.path.isdir(out + "/03_Postprocessing/Hapmap") :
                    sub.call(f'mkdir {out}/03_Postprocessing/Hapmap', shell=True)

                sub.call(f'ln -s {line} {out}/03_Postprocessing/Hapmap/', shell=True)



def PCA(out, verbose, param, sample) :
    bindir = os.path.abspath(os.path.dirname(__file__))
    PCA = bindir + "/script/PCA.pl"

    sys.stderr.write("\nPCA\n")
    sys.stderr.flush()

    if not os.path.isdir(out + "/04_Population/PCA") :
        sub.call(f'mkdir {out}/04_Population/PCA', shell=True)
    line = PCA + " -p " + param + " -s " + sample + " -o " + out + "/04_Population/PCA"
    log = out + "/04_Population/logs/pca.log"
    
    if verbose == "1" :
        sys.stderr.write(line + " 2> " + log + "\n")
        sys.stderr.flush()
    
    with open(log, 'w') as outfile :
        value = sub.call(line, shell=True, stdout = outfile, stderr = outfile)
    if not value == 0 :
        sys.stderr.write("[ERROR] Check the log file : " + out + "/04_Population/logs/pca.log\n")
        sys.stderr.flush()


def SNPhylo(out, verbose, param) :
    bindir = os.path.abspath(os.path.dirname(__file__))
    SNPhylo = bindir + "/script/SNPHYLO.pl"

    sys.stderr.write("\nSNPhylo\n")
    sys.stderr.flush()

    if not os.path.abspath(out + "/04_Population/SNPhylo") :
        sub.call(f'mkdir {out}/04_Population/SNPhylo', shell=True)
    line = SNPhylo + " -p " + param + " -o " + out + "/04_Population/SNPhylo"
    log = out + "/04_Population/logs/snphylo.log"

    if verbose == "1" :
        sys.stderr.write(line + " 2> " + log + "\n")
        sys.stderr.flush()

    with open(log, 'w') as outfile :
        value = sub.call(line, shell=True, stdout = outfile, stderr = outfile)
    if not value == 0 :
        sys.stderr.write("[ERROR] Check the log file : " + out + "/04_Population/logs/snphylo.log\n")
        sys.stderr.flush()


def STRUCTURE(out, verbose, param, sample) :
    
    bindir = os.path.abspath(os.path.dirname(__file__))
    STRUCTURE = bindir + "/script/STRUCTURE.pl"

    sys.stderr.write("\nSTRUCTURE\n")
    sys.stderr.flush()

    if not os.path.abspath(out + "/04_Population/STRUCTURE") :
        sub.call(f'mkdir {out}/04_Population/STRUCTURE', shell=True)
    
    line = STRUCTURE + " -p " + param + " -s " + os.path.abspath(sample) + " -o " + out + "/04_Population/STRUCTURE"
    log = out + "/04_Population/logs/structure.log"
    
    if verbose == "1" :
        sys.stderr.write(line + " 2> " + log + "\n")
        sys.stderr.flush()

    with open(log, 'w') as outfile :
        value = sub.call(line, shell=True, stdout = outfile, stderr = outfile)
    
    if not value == 0 :
        sys.stderr.write("[ERROR] Check the log file : " + out + "/04_Population/logs/structure.log\n")
        sys.stderr.flush()


def Fst(out, verbose, param, sample) :
    bindir = os.path.abspath(os.path.dirname(__file__))
    Fst = bindir + "/script/FST.pl"

    sys.stderr.write("\nFst\n")
    sys.stderr.flush()

    if not os.path.abspath(out + "/04_Population/Fst") :
        sub.call(f'mkdir {out}/04_Population/Fst', shell=True)
    
    line = Fst + " -p " + param + " -o " + out + "/04_Population/Fst -s " + sample
    log = out + "/04_Population/logs/fst.log"

    if verbose == "1" :
        sys.stderr.write(line + " 2> " + log + "\n")
        sys.stderr.flush()

    with open(log, 'w') as outfile :
        value = sub.call(line, shell=True, stdout = outfile, stderr = outfile)
    
    if not value == 0 :
        sys.stderr.write("[ERROR] Check the log file : " + out + "/04_Population/logs/fst.log\n")
        sys.stderr.flush()


def Effective_size(out, verbose, param, th) :
    bindir = os.path.abspath(os.path.dirname(__file__))
    Eff = bindir + "/script/psmc.pl"

    sys.stderr.write("\nEffective Size\n")
    sys.stderr.flush()

    if not os.path.abspath(out + "/04_Population/EffectiveSize") :
        sub.call(f'mkdir {out}/04_Population/EffectiveSize', shell=True)
    
    line = Eff + " -t " + str(th) + " -p " + param + " -o " + out + "/04_Population/EffectiveSize"
    log = out + "/04_Population/logs/effectivesize.log"

    if verbose == "1" :
        sys.stderr.write(line + " 2> " + log + "\n")
        sys.stderr.flush()
    with open(log, 'w') as outfile :
        value = sub.call(line, shell=True, stdout = outfile, stderr= outfile)
    
    if not value == 0 :
        sys.stderr.write("[ERROR] Check the log file : " + out + "/04_Population/logs/effectivesize.log\n")
        sys.stderr.flush()


def ADMIXTOOLS(out, verbose, param, sample) :
    bindir = os.path.abspath(os.path.dirname(__file__))
    ADMIXTOOLS = bindir + "/script/ADMIXTOOLS.pl"

    sys.stderr.write("\nADMIXTOOLS\n")
    sys.stderr.flush()

    if not os.path.isdir(out + "/04_Population/ADMIXTOOLS") :
        sub.call(f'mkdir {out}/04_Population/ADMIXTOOLS', shell=True)
    
    line = ADMIXTOOLS + " -p " + param + " -s " + sample + " -o " + out + "/04_Population/ADMIXTOOLS"
    log = out + "/04_Population/logs/admixtools.log"
    
    if verbose == "1" :
        sys.stderr.write(line + " 2> " + log + "\n")
        sys.stderr.flush()
   
    with open(log, 'w') as outfile :
        value = sub.call(line, shell=True, stdout = outfile, stderr = outfile)
    
    if not value == 0 :
        sys.stderr.write("[ERROR] Check the log file : " + out + "/04_Population/logs/admixtools.log\n")
        sys.stderr.flush()


def LD(out, verbose, param, sample) :
    bindir = os.path.abspath(os.path.dirname(__file__))
    LD_script = bindir + "/script/LD_analysis.py"

    sys.stderr.write("\nLD\n")
    sys.stderr.flush()

    if not os.path.isdir(out + "/04_Population/LD") :
        sub.call(f'mkdir {out}/04_Population/LD', shell=True)
    
    line = "python3 " + LD_script + " -p " + param + " -s " + sample + " -o " + out + "/04_Population/LD"
    log = out + "/04_Population/logs/LD.log"

    if verbose == "1" :
        sys.stderr.write(line + " 2> " + log + "\n")
        sys.stderr.flush()
    
    with open(log, 'w') as outfile :
        value = sub.call(line, shell=True, stdout = outfile, stderr = outfile)
    
    if not value == 0 :
        sys.stderr.write("[ERROR] Check the log file : " + out + "/04_Population/logs/LD.log\n")
        sys.stderr.flush()


def main_pipe(args, dict_param, index) :
    sys.stderr.write("---------------Population--------------\n")
    sys.stderr.flush()
    
    if not os.path.isdir(args.out + "/04_Population") :
        sub.call(f'mkdir {args.out}/04_Population', shell=True)
    if not os.path.isdir(args.out + "/04_Population/logs") :
        sub.call(f'mkdir {args.out}/04_Population/logs', shell=True)

    if index == 0 :
        ParseInput(args.input, args.out)
    
    pop_param = Param.Population(args.out, dict_param)
    PCA(os.path.abspath(args.out), args.verbose, pop_param['PCA'], args.sample)
    SNPhylo(os.path.abspath(args.out), args.verbose, pop_param['SNPhylo'])
    STRUCTURE(os.path.abspath(args.out), args.verbose, pop_param['STRUCTURE'], args.sample)
    Fst(os.path.abspath(args.out), args.verbose, pop_param['Fst'], args.sample)
    Effective_size(os.path.abspath(args.out), args.verbose, pop_param['EffectiveSize'], args.threads)
    ADMIXTOOLS(os.path.abspath(args.out), args.verbose, pop_param['ADMIXTOOLS'], args.sample)
    LD(os.path.abspath(args.out), args.verbose, pop_param['LD'], args.sample)
