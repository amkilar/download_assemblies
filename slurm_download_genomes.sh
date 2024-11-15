#!/bin/bash
#SBATCH --job-name=down_assm  
#SBATCH -c 32                 
#SBATCH -N 1                 
#SBATCH -t 01-00:00          
#SBATCH -p eddy              
#SBATCH --mem=12G


module add Mambaforge
mamba activate /n/home10/akilar/software/env_snakemake

cd <path to the download_genomes repository>
snakemake -s dowload_genomes.py --cores 32 --use-conda 
