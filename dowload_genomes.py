DATABASE = '"Enoplea"[Organism] AND (latest[filter] AND "reference genome"[filter] AND all[filter] NOT anomalous[filter])'

rule all:
    input:  "downloaded_genomes_and_tax.csv"


rule create_genome_list:
    output: touch("list_of_genomes.txt")
    conda:  "env/entrez_env.yaml"
    
    shell:
        r"""
        mkdir -p temp/

        esearch -db assembly -query '{DATABASE}' \
        | esummary \
        | xtract -pattern DocumentSummary -element FtpPath_GenBank \
        | while read -r line ; 
        do
            fname=$(echo $line | grep -o 'GCA_.*' | sed 's/$/_genomic.fna.gz/');
            wildcard=$(echo $fname | sed -e 's!.fna.gz!!');

            echo "$line/$fname" > temp/$wildcard;
            echo $wildcard >> {output}

        done
        """

checkpoint check_genome_list:
    output: touch(".create_genome_list.touch")

    input: "list_of_genomes.txt"

# checkpoint code to read the genome list and specify all wildcards for genomes
class Checkpoint_MakePattern:
    def __init__(self, pattern):
        self.pattern = pattern

    def get_names(self):
        with open('list_of_genomes.txt', 'rt') as fp:
            names = [ x.rstrip() for x in fp ]
        return names

    def __call__(self, w):
        global checkpoints

        # wait for the results of 'list_of_genomes.txt'; this will trigger an
        # exception until that rule has been run.
        checkpoints.check_genome_list.get(**w)

        # information used to expand the pattern, using arbitrary Python code
        names = self.get_names()

        pattern = expand(self.pattern, name=names, **w)

        return pattern


rule download_genome:
    output: "database/{genome}.fna.gz"
    
    input:  "temp/{genome}"

    shell:
        r"""
        GENOME_LINK=$(cat {input})

        ADAPTED_LINK=$(echo $GENOME_LINK | sed 's/ftp:\/\/ftp.ncbi.nlm.nih.gov\/genomes\//rsync:\/\/ftp.ncbi.nlm.nih.gov\/genomes\//' )

        rsync -q -av \
        $ADAPTED_LINK \
        ./database/{wildcards.genome}
        
        sleep 5

        """

rule unzip_genome:
   output: "database/{genome}.fna"

   input:  "database/{genome}.fna.gz"
   
   shell:
       r"""
       gunzip -q {input}
       """

rule search_taxonomy:
    output: "taxonomy/{genome}.taxonomy.row.csv"

    input:  script = "scripts/search_taxonomy.r",
            genome = "database/{genome}.fna"

    conda:  "env/search_taxonomy.yaml"        

    shell:  "Rscript {input.script} {input.genome} {output}"


rule wrap_up:
    output: "download_genomes.txt"
    input:  Checkpoint_MakePattern("database/{name}.fna")

    shell:
        r"""
        echo "{input}" >> {output}
        """

rule add_taxonomy:
    output: "downloaded_genomes_and_tax.csv"

    input:  Checkpoint_MakePattern("taxonomy/{name}.taxonomy.row.csv")

    shell:
        r"""
        cat {input} >> {output}
        """
