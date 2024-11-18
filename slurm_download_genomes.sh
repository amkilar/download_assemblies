#!/bin/bash
#SBATCH --job-name=down_assm  
#SBATCH -c 12                 
#SBATCH -N 1                 
#SBATCH -t 01-00:00          
#SBATCH -p eddy              
#SBATCH --mem=12G


module add Mambaforge
mamba activate /n/home10/akilar/software/env_snakemake

cd /n/eddy_lab/users/akilar/download_genomes
snakemake -s dowload_genomes.py --cores 12 --use-conda --unlock
snakemake -s dowload_genomes.py --cores 12 --use-conda 
snakemake -s dowload_genomes.py --cores 12 --use-conda --rerun-incomplete

