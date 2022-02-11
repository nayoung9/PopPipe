
## PAPipe

 A comprehensive pipeline for population genetic analysis containing Read mapping, Variant calling, and Population genetic analysis

![fig1.png](figure/fig1.png)

### Install PAPipe

```
1. Download source 
	$ git clone https://github.com/jkimlab/PAPipe.git
```

### Install PAPipe using Docker

```
1. Install docker (https://docs.docker.com/install/linux/docker-ce/ubuntu)
    curl -fsSL https://get.docker.com/ | sudo sh
    sudo usermod -aG docker $USER 	# adding user to the “docker” group

2. Download source
  git clone https://github.com/jkimlab/PAPipe.git
  
3. Build image using Dockerfile 
  - Change to the directory where Dockerfile is located (PAPipe/Dockerfile)
    docker build -t [docker image name] ./ &> log_image_build

4. Run PAPipe by docker
  - Run image and create container
    docker run -v [Local directory containing data]:[Path of connecting directory on container] -it [docker image name]
```

### Run PAPipe

```
-----------------Start-----------------
usage: main.py [-h] -P PARAM -I INPUT [-A SAMPLE] [-O OUT] [-J JOB] [-S STEP]
               [-V VERBOSE] [-T THREADS] [-M MEMORY]

Pipeline of population analysis

optional arguments:
  -h, --help            show this help message and exit
  -P PARAM, --param PARAM
                        <Path> Parameter file
  -I INPUT, --input INPUT
                        <Path> Input file
  -A SAMPLE, --sample SAMPLE
                        <Path> Sample file
  -O OUT, --out OUT     <Path> Output directory (default current directory)
  -J JOB, --job JOB     <Int> The number of jobs to process at one time
                        (default 1)
  -S STEP, --step STEP  <Str> Select the steps you want up to 1-4 (default
                        1-4)
  -V VERBOSE, --verbose VERBOSE
                        <Int> If you want to see command line, set 1 (default
                        0)
  -T THREADS, --threads THREADS
                        <Int> Threads number of cores (default 5)
  -M MEMORY, --memory MEMORY
                        <Int> Memory allocation (default 10)
```

Parameters for run `main.py`
Select sub-pipes to run with -S parameter, (1: Read mapping, 2: Variant calling, 3: Filtering and format converting, 4: Population analysis)

```python
#run all steps (Default -S parameter : 1-4, Read mapping -> Variant calling -> Filtering and format converting -> Population analysis)
bin/main.py -P ./main_param.txt -I ./main_input_01.txt -A ./main_sample.txt -V 1 -J 8 &> logs

#run three sub steps from Variant calling (Variant calling -> Filtering and format converting -> Population analysis)
bin/main.py -P ./main_param.txt -I ./main_input_02.txt -A ./main_sample.txt -V 1 -J 8 -S 2-4 &> 02.logs

#run two sub steps from Filtering and format converting (Filtering and format converting -> Population analysis)
bin/main.py -P ./main_param.txt -I ./main_input_03.txt -A ./main_sample.txt -V 1 -J 8 -S 3-4 &> 03.logs

#run only Population analysis
bin/main.py -P ./main_param.txt -I ./main_input_04.txt -A ./main_sample.txt -V 1 -J 8 -S 4 &> 04.logs
```

### Prepare parameter files

Check out the directory `PAPipe/params/` containing example parameter files

1. main_input_00.txt (01~04 for running PAPipe from different steps)
    
    Except for the case of running from the Read mapping step, using [main_input_01.txt], PAPipe automatically generates link of the files given through the rest of the input files to connect the user-data into PAPipe [main_input_02,03,04.txt] 
    
    1. **`main_input_01.txt`:**  Input for PAPipe running from Read mapping step (WGS sequence FASTQ)
        
        ```
        #===================================================================#
        #                  Input file for ReadMapping step                  #
        #===================================================================#
        
        #### ReadMapping ####
        ### DNA-seq data path(input file of ReadMapping) ###
        ## Paired-end read pairs
        ## <Hanwoo_Hanwoo1> => RGSM name, format:(BreedName)_(BreedName)(Number)
        ## [lib1]
        ## Path of forward read
        ## path of reverse read
        <Abreed_Abreed1>
        [lib1]
        [path to sequencing read]/[sequencing read]-1.fq.gz
        [path to sequencing read]/[sequencing read]-2.fq.gz
        [lib2]
        [path to sequencing read]/[sequencing read]-1.fq.gz
        [path to sequencing read]/[sequencing read]-2.fq.gz
        <Abreed_Abreed2>
        [lib1]
        [path to sequencing read]/[sequencing read]-1.fq.gz
        [path to sequencing read]/[sequencing read]-2.fq.gz
        [lib2]
        [path to sequencing read]/[sequencing read]-1.fq.gz
        [path to sequencing read]/[sequencing read]-2.fq.gz
        ```
        
    2. **`main_input_02.txt`:**  Input for PAPipe running from Variant calling step (Alignment BAM)
        
        ```
        #==================================================================#
        #                Input file for VariantCalling step                #
        #==================================================================#
        
        #### VariantCalling ####
        ### Bam file path(input file of ReadMapping or Varaint Calling) ###
        ## <Hanwoo_Hanwoo1> => RGSM name (Before read grouping in ReadMapping step, format:(BreedName)_(BreedName)(Number), example : Hanwoo_Hanwoo1)
        # Path of bam file
        <Abreed_Abreed1>
        [path to bam file]/[Abreed_Abreed1].recal.addRG.marked.sort.bam
        <Abreed_Abreed2>
        [path to bam file]/[Abreed_Abreed2].recal.addRG.marked.sort.bam
        <Bbreed_Breed1>
        [path to bam file]/[Bbreed_Breed1].recal.addRG.marked.sort.bam
        <Bbreed_Breed2>
        [path to bam file]/[Bbreed_Breed2].recal.addRG.marked.sort.bam
        ```
        
    3. **`main_input_03.txt`:**  Input for PAPipe running from Format converting or data filtering step (Variant call VCF, Alignment BAM for PSMC analysis)
        
        ```
        #==================================================================#
        #                Input file for Postprocessing step                #
        #==================================================================#
        
        #### Postprocessing ####
        ### Vcf file path(input file of Postprocessing) ###
        ## Path of vcf file
        [path to variant call VCF]/[variant call].vcf.gz
        
        #### If you take the Effective size step in Population analysis, write the BAM files path ####
        #### Population ####
        ### Bam files path ###
        ## <Hanwoo_Hanwoo1> => RGSM name (Before read grouping in ReadMapping step, format:(BreedName)_(BreedName)(Number), example : Hanwoo_Hanwoo1)
        ## Path of BAM file
        <Abreed_Abreed1>
        [path to bam file]/[Abreed_Abreed1].recal.addRG.marked.sort.bam
        <Abreed_Abreed2>
        [path to bam file]/[Abreed_Abreed2].recal.addRG.marked.sort.bam
        <Bbreed_Breed1>
        [path to bam file]/[Bbreed_Breed1].recal.addRG.marked.sort.bam
        <Bbreed_Breed2>
        [path to bam file]/[Bbreed_Breed2].recal.addRG.marked.sort.bam
        ```
        
    4. **`main_input_04.txt`:**  Input for PAPipe running Population analysis (Variant VCF, directory containing converted files (HAPMAP, PLINK),Alignment BAM for PSMC analysis )
        
        ```
        #==================================================================#
        #                  Input file for Population step                  #
        #==================================================================#
        
        #### Population ####
        ### BAM ###
        ## <Hanwoo_Hanwoo1> => RGSM name (Before read grouping in ReadMapping step, format:(BreedName)_(BreedName)(Number), example : Hanwoo_Hanwoo1)
        ## Path of bam file
        <Abreed_Abreed1>
        [path to bam file]/[Abreed_Abreed1].recal.addRG.marked.sort.bam
        <Abreed_Abreed2>
        [path to bam file]/[Abreed_Abreed2].recal.addRG.marked.sort.bam
        <Bbreed_Breed1>
        [path to bam file]/[Bbreed_Breed1].recal.addRG.marked.sort.bam
        <Bbreed_Breed2>
        [path to bam file]/[Bbreed_Breed2].recal.addRG.marked.sort.bam
        
        ### Vcf ###
        ## Path of vcf file
        
        ### Plink ###
        ## Input file of Population analysis ##
        
        ### Hapmap ###
        ## Input file of Population analysis ##
        
        ```
        
2. main_param.txt (containing parameters for all steps)\
    1. **`main_param.txt`** 
        
        ```
        #=======================================================================#
        #                   parameter file for Population pipeline              #
        #=======================================================================#
        
        #==================================================#
        ####                 ReadMapping                ####
        #==================================================#
        ### Program path ###
        ## Write 'OPTION = 1' if you want to use the BWA tool in Mapping step
        ## Write 'OPTION = 2' if you want to use the Bowtie2 tool in Mapping step
        
        OPTION = 1
        BWA = [program path]/bwa
        BOWTIE2 = [program path]/bowtie2
        SAMTOOLS = [program path]/samtools
        PICARD = [program path]/picard.jar
	#==================================================#
	####               VariantCalling               ####
	#==================================================#
	### Program path ###
	## Write 'OPTION = 1' if you want to use the GATK3 in Variant calling step
	## Write 'OPTION = 2' if you want to use the GATK4 in Variant calling step
	## Write 'OPTION = 3' if you want to use the SAMTOOLS-BCFTOOLS in Variant calling step
        ```
	
	
        
    2. **`main_param_docker.txt`** 
        
        There is a fixed parameter file for the Docker environment. User needs to modify 
        
        ```
        #=======================================================================#
        #                   parameter file for Population pipeline              #
        #=======================================================================#
        
        #==================================================#
        ####                 ReadMapping                ####
        #==================================================#
        ### Program path ###
        ## Write 'OPTION = 1' if you want to use the BWA tool in Mapping step
        ## Write 'OPTION = 2' if you want to use the Bowtie2 tool in Mapping step
        
        OPTION = 1
        BWA = [program path]/bwa
        BOWTIE2 = [program path]/bowtie2
        SAMTOOLS = [program path]/samtools
        PICARD = [program path]/picard.jar
        ...
        ```
        
3. main_sample.txt (Sample information for population analysis)
    
    ```python
    #sample sex[F, M, U, FemaleMale/U for none] population
    ABreed1 U        Abreed
    ABreed2 U        Abreed
    BBreed1 U        Bbreed
    BBreed2 U        Bbreed
    ```

### PAPipe Results

Results from all steps

1. Read mapping (BAM) 
    
    ```python
    #Read mapping files for all samples
    - 01_readMapping/04ReadRegrouping/[population]_[sample].addRG.marked.sort.bam
    ```
    
2. Variant Calling (VCF)
    
    ```python
    #Variant call generated using all population sequencing data 
    - 02_VariantCalling/VariantCalling/All.variant.combined.g.vcf.gz
    ```
    
3. Postprocessing
    
    ```
    #Various formatted variant call data 
    - 03_Postprocessing/Hapmap/variant.combined.GT.SNP.flt.hapmap
    - 03_Postprocessing/plink/[prefix].bed
    - 03_Postprocessing/plink/[prefix].bim
    - 03_Postprocessing/plink/[prefix].fam
    - 03_Postprocessing/plink/[prefix].map
    - 03_Postprocessing/plink/[prefix].nosex
    - 03_Postprocessing/plink/[prefix].ped
    ```
    
4. Population analysis
    1. Population structure analysis
        
        ```
        #STRUCTURE results per K in PNG files and all STRUCTURE results in a single PDF file
        - 04_Population/STRUCTURE/CLUMPAK/K=[n].MajorCluster.png        
        - 04_Population/STRUCTURE/CLUMPAK/pipeline_summary.pdf
        ```
        
    2. Fixation index analysis
        
        ```
        #Fixation index results figure, different rounds uses different target and comparing population
        - 04_Population/Fst/round[n]/Fst_result.pdf
        ```
        
    3. LD decay analysis
        
        ```
        #Estimated LD values
        - 04_Population/LD/[maximum distance parameter]/Plot/out.[population name]
        
        #LD decay plot
        - 04_Population/LD/[maximum distance parameter]/Plot/Rplots.pdf
        ```
        
    4. Population admixture analysis
        
        ```
        #Admixture analysis results from all available combinations generated to estimate each statistics
        - 04_Population/ADMIXTOOLS/admixtools_3pop/result.out
        - 04_Population/ADMIXTOOLS/admixtools_4diff/result.out
        - 04_Population/ADMIXTOOLS/admixtools_f4stat/result.out        
        - 04_Population/ADMIXTOOLS/admixtools_Dstat/result.out
        ```
        
    5. PCA
        
        ```
        #PCA results
        - 04_Population/PCA/PCs.info
        
        #PCA plot of all available combination of two PCs
        - 04_Population/PCA/all.PCA.pdf
        ```
        
    6. Phylogenetic analysis
        
        ```
        #NEWICK formatted phylogenetic tree
        - 04_Population/SNPhylo/snphylo.ml.txt
        
        #Two figures of different visualization type of phylogenetic tree
        - 04_Population/SNPhylo/snphylo_tree.pdf #rooted tree
        - 04_Population/SNPhylo/Rplots.pdf #unrooted tree
        ```
        
    7. Effective Size estimation
        
        ```
        #psmc_plot
        - 04_Population/EffectiveSize/psmc_plot.pdf
        ```
        
### NOTES
- Running PAPipe-Variant calling with GATK3 (Variant calling OPTION = 1), parameter-given dbSNP file should be sorted vcf format.
	```
	gzip -d ./dbSNP.vcf.gz
	bcftools sort ./dbSNP.vcf > ./dbSNP.sorted.vcf
	```


### Run PAPipe for making the results

- DATA
    - Four cattle population (Jersey, Simmental, Angus, Holstein from NCBI SRA, PRJNA238491, DOI: [10.1038/ng.3034](https://doi.org/10.1038/ng.3034))
    - Additional single cattle breed data (Hanwoo from NCBI SRA, PRJNA210523, DOI: [10.1093/gbe/evu102](https://dx.doi.org/10.1093%2Fgbe%2Fevu102))
- Quality Control
    - IlluQC ([https://doi.org/10.1371/journal.pone.0030619](https://doi.org/10.1371/journal.pone.0030619))
    - TrimGalore ([https://www.bioinformatics.babraham.ac.uk/projects/trim_galore/](https://www.bioinformatics.babraham.ac.uk/projects/trim_galore/))
- Run PAPipe
    - Command
    
    ```python
    bin/main.py -P ./main_param.txt -I ./main_input_pre.txt -A ./main_sample.txt -V 1 -J 8 &> logs
    ```
    
    - see `example/main_input_01.txt`
    - see `example/main_sample.txt`
    - see `example/main_param.txt`

### **Included third-party tools**

See `Requirements/ThirdPartyTools.txt`

### Contact

[bioinfolabkr@gmail.com](mailto:bioinfolabkr@gmail.com)
