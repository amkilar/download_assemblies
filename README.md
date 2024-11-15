# Snakemake Pipeline for Downloading Genomes and Taxonomy Information

This pipeline automates the process of downloading genome sequences for a specific organism from the NCBI Assembly database and extracting taxonomy information. The example provided focuses on the `Nematoda` organism group, using filters to ensure representative genomes are downloaded.

---

## **Pipeline Overview**

The pipeline consists of the following steps:
1. Query the NCBI Assembly database for the specified organism (`Nematoda`) and create a list of genome links.
2. Download the genome sequences in `.fna.gz` format.
3. Decompress the genome files.
4. Extract taxonomy information for each genome.
5. Combine downloaded genomes and taxonomy data into a final summary file.

---

## **Setup Instructions**

### **1. Prerequisites**
- Ensure that you have access to a cluster or a machine with `Mambaforge` or `Conda` installed.
- Install Snakemake:
  ```bash
  mamba install -c bioconda snakemake
  ```

### **2. Create Required Environments**
The pipeline uses two Conda environments for:
1. **NCBI Entrez tools** (for querying the Assembly database): `env/entrez_env.yaml`.
2. **R Environment** (for taxonomy extraction): `env/search_taxonomy.yaml`.

Create the environments:
```bash
conda env create -f env/entrez_env.yaml
conda env create -f env/search_taxonomy.yaml
```

### **3. Activate Your Snakemake Environment**
Activate the Snakemake environment before running the pipeline:
```bash
mamba activate /n/home10/akilar/software/env_snakemake
```

---

## **Running the Pipeline**

### **Command**
Run the pipeline with the following command:
```bash
snakemake -s dowload_genomes.py --cores 32 --use-conda
```

### **Inputs**
- The pipeline uses the following query for genome downloads:
  ```bash
  DATABASE = '"Nematoda"[Organism] AND (latest[filter] AND "representative genome"[filter] AND all[filter] NOT anomalous[filter])'
  ```
- To adjust the search criteria, modify the `DATABASE` variable in the `dowload_genomes.py` file.

### **Outputs**
- `downloaded_genomes_and_tax.csv`: The final summary file containing genome and taxonomy data.

---

## **Pipeline Rules**

### **1. Create Genome List**
Generates a list of genome download links from the NCBI Assembly database:
- **Input**: Organism query (`DATABASE`).
- **Output**: `list_of_genomes.txt`.

### **2. Download Genome**
Downloads genome files using `rsync`:
- **Input**: `list_of_genomes.txt`.
- **Output**: `database/{genome}/{genome}.fna.gz`.

### **3. Unzip Genome**
Decompresses `.fna.gz` genome files:
- **Input**: Compressed genome files.
- **Output**: `database/{genome}/{genome}.fna`.

### **4. Search Taxonomy**
Extracts taxonomy information for each genome:
- **Input**: Genome file (`.fna`).
- **Output**: `taxonomy/{genome}.taxonomy.row.csv`.

### **5. Wrap Up**
Aggregates the list of downloaded genomes:
- **Output**: `download_genomes.txt`.

### **6. Add Taxonomy**
Combines taxonomy information into the final CSV file:
- **Output**: `downloaded_genomes_and_tax.csv`.

---

## **Customization**

### **Modify Search Query**
To customize the organism or filters, update the `DATABASE` variable:
```python
DATABASE = '"OrganismName"[Organism]'
```

### **Adjust Threads**
To optimize performance, adjust the `--cores` parameter when running Snakemake:
```bash
snakemake -s dowload_genomes.py --cores <number_of_cores> --use-conda
```

---

## **Notes**
- Ensure sufficient disk space for genome files.
- Verify network access to NCBI servers for `rsync` commands.
- Errors in individual rules are logged in `.snakemake/log/`.

For additional details, refer to the `dowload_genomes.py` file or the [Snakemake documentation](https://snakemake.readthedocs.io/).