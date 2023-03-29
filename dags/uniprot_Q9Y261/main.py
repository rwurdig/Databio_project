# Import the required libraries
import os
from datetime import timedelta
from itertools import chain
import xmltodict
import urllib.request
from airflow import DAG
from airflow.decorators import dag, task
from neo4j import GraphDatabase, basic_auth
from pendulum import today
from airflow.utils.dates import days_ago

# Set the start date for the DAG
start_date = today('UTC') - timedelta(days=1)

# Get the current working directory
dag_path = os.getcwd()

# Set default arguments for the DAG
default_args = {'owner': 'airflow'}

# Define the ETL DAG
@dag(description='ETL of a XML file from UniProt that contain info about the protein Q9Y261', 
    schedule=timedelta(days=1), 
    catchup=True, 
    start_date=start_date, 
    default_args=default_args)

def etl_uniprot_Q9Y261():
    
    # Initialize the connection to the Neo4j database
    driver = GraphDatabase.driver("bolt://neo4j:7687", auth=basic_auth("neo4j", "12345678"))
    
    # Define a helper function for running write transactions in Neo4j
    def write_transaction(query: str, params: dict):
        with driver.session() as session:
            session.execute_write(lambda tx: tx.run(query, **params))
        driver.close()
        
    # Task to fetch the XML file from the provided URL
    @task(task_id='fetch_xml_file')
    def fetch_xml_file():
        url = "https://raw.githubusercontent.com/weavebio/data-engineering-coding-challenge/main/data/Q9Y261.xml"

        # Download the XML file
        response = urllib.request.urlopen(url)
        xml_data = response.read()
        return xmltodict.parse(xml_data)
    
    # Task to write the accession data into the Neo4j database
    @task(task_id='write_accession')
    def write_accession(dict_data):
        accession = dict_data.get("uniprot").get("entry").get("accession")[0]

        query = "CREATE (:Protein {id: $id})"
        params = {
            "id": accession
        }
        write_transaction(query, params)
        
        return accession

    # Task to extract the full name of the protein and write it to the Neo4j database
    @task(task_id='write_full_name')
    def write_full_name(dict_data, accession):
        full_name = dict_data.get("uniprot").get("entry").get("protein").get("recommendedName").get("fullName")

        query = "MATCH (p:Protein {id: $id}) CREATE (p)-[:HAS_FULL_NAME]->(:FullName {name: $name})"
        params = {
            "id": accession,
            "name": full_name
        }

        write_transaction(query, params)
        
    # Task to extract the alternate names of the protein and write them to the Neo4j database
    @task(task_id='write_alternate_names')
    def write_alternate_names(dict_data, accession):
        alternate_names = dict_data.get("uniprot").get("entry").get("protein").get("alternativeName")

        if alternate_names:
            if not isinstance(alternate_names, list):
                alternate_names = [alternate_names]

            alternate_full_names = []
            for alternate_name in alternate_names:
                alt_full_name = alternate_name.get("fullName")
                alternate_full_names.append(alt_full_name)

            query = """
                UNWIND $alternate_full_names AS alt_full_name
                MATCH (p:Protein {id: $id})
                CREATE (p)-[:HAS_ALTERNATE_NAME]->(:AlternateName {name: alt_full_name})
                """
            params = {
                "id": accession,
                "alternate_full_names": alternate_full_names
            }

            write_transaction(query, params)

    # Task to extract gene data and write it to the Neo4j database
    @task(task_id='write_genes')
    def write_genes(dict_data, accession):
        def get_genes(gene):
            return {
                "id": accession,
                "name": gene.get("#text"),
                "status": gene.get('@type')
            }

        genes = dict_data.get("uniprot").get("entry").get("gene").get("name")

        if not isinstance(dict_data.get("uniprot").get("entry").get("gene").get("name"), list):
            genes.append(dict_data.get("uniprot").get("entry").get("gene").get("name"))
        else:
            genes = dict_data.get("uniprot").get("entry").get("gene").get("name")

        genes = list(map(get_genes, genes))

        query = """
            UNWIND $genes AS gene
            MATCH (p:Protein {id: gene.id})
            CREATE (p)-[:FROM_GENE {status: gene.status}]->(:Gene {name: gene.name})
        """
        write_transaction(query, { "genes": genes })

    # Task to extract organism data and return it for further processing
    @task(task_id='get_organisms')
    def get_organisms(dict_data, accession):
        organisms = []

        def get_organism(organism):
            organism_name = next(filter(lambda name: name.get("@type") == "scientific", organism.get("name"))).get("#text")
            organism_common = next(filter(lambda name: name.get("@type") == "common", organism.get("name"))).get("#text")
            taxonomy_id = organism.get("dbReference").get("@id")
            lineages = organism.get("lineage").get("taxon")
            
            return {
                "id": accession,
                "organism_name": organism_name, 
                "organism_common": organism_common, 
                "taxonomy_id": taxonomy_id, 
                "lineages": lineages
            }

        if(isinstance(dict_data.get("uniprot").get("entry").get("organism"), list)):
            organisms = dict_data.get("uniprot").get("entry").get("organism")
        else:
            organisms.append(dict_data.get("uniprot").get("entry").get("organism"))

        organisms = list(map(get_organism, organisms))

        return organisms
    
    # Task to write the author information of references into the graph database
    @task(task_id='write_authors_of_references')
    def write_authors_of_references(references):
        def get_author_from_reference(reference):
            if not reference.get("citation"):
                return []
            
            if(isinstance(reference.get("citation").get("authorList").get("person"), list)):
                return list(map(lambda author: {
                    "name": author.get("@name"), 
                    "reference": reference.get("citation").get("@name")
                }, reference.get("citation").get("authorList").get("person")))
            else:
                if "person" in reference.get("citation").get("authorList"):
                    return [{"name": reference.get("citation").get("authorList").get("person")}]

                if "consortium" in reference.get("citation").get("authorList"):
                    return [{"name": reference.get("citation").get("authorList").get("consortium")}]

        authors = list(map(get_author_from_reference, references))
        authors = [item for sublist in authors for item in sublist]
                
        query = """
            UNWIND $authors AS author
            MATCH (r:Reference {name: author.reference}) CREATE (r)-[:HAS_AUTHOR]->(:Author {name: author.name})
        """
        write_transaction(query, { "authors": authors })


    # Task to write the organism information into the graph database
    @task(task_id='write_organisms')
    def write_organisms(organisms):
        
        # Define the Cypher query to create a relationship between a Protein node and an Organism node
        query = """
            UNWIND $organisms AS organism
            MATCH (p:Protein {id: organism.id})
            CREATE 
                (p)-[:IN_ORGANISM]->
                (:Organism {taxonomy_id: organism.taxonomy_id, name: organism.organism_name, common_name: organism.organism_common})
        """
        # Execute the write transaction with the organisms data
        write_transaction(query, { "organisms": organisms })
        
    # Task to write the lineage information of organisms into the graph database
    @task(task_id='write_lineages_of_organisms')
    def write_lineages_of_organisms(organisms):
        
        # Function to map the lineage of an organism
        def get_lineage(organism, lineage):
            return {
                "taxonomy_id": organism.get("taxonomy_id"),
                "taxon": lineage
            }

        # Map the lineages of organisms and flatten the list
        lineages = list(map(lambda organism: list(map(lambda lineage: get_lineage(organism, lineage), organism.get("lineages"))), organisms))
        lineages = [item for sublist in lineages for item in sublist]

        # Define the Cypher query to create a relationship between an Organism node and a Lineage node
        query = """
            UNWIND $lineages AS lineage
            MATCH (o:Organism {taxonomy_id: lineage.taxonomy_id})
            CREATE (o)-[:FROM_LINEAGE]->(:Lineage {taxon: lineage.taxon})
        """
        
        # Execute the write transaction with the lineages data
        write_transaction(query, { "lineages": lineages })

    # Task to write the features of a protein into the graph database
    @task(task_id='write_features')
    def write_features(dict_data, accession):
        
        # Cypher query to create the relationship between Protein and Feature nodes with their properties
        query = """
            UNWIND $features AS feature
            MATCH (p:Protein {id: feature.id})
            CREATE
                (p)-[:HAS_FEATURE {position_begin: feature.position_begin, position_end: feature.position_end}]->
                (:Feature {description: feature.description, type: feature.type, evidence: feature.evidence})
        """

        # Helper function to extract feature information and return it as a dictionary
        def get_feature(feature):
            
            # If the feature location does not contain begin and end positions, they are created based on the position attribute
            if "begin" not in feature.get("location"):
                feature["location"] = {
                    "begin": {
                        "@position": feature.get("location").get("position").get("@position")
                    },
                    "end": {
                        "@position": feature.get("location").get("position").get("@position")
                    }
                }

            return {
                "id": accession,
                "position_begin": feature.get("location").get("begin").get("@position"),
                "position_end": feature.get("location").get("end").get("@position"),
                "description": feature.get("@description"),
                "type": feature.get("@type"),
                "evidence": feature.get("@evidence"),
            }

        # Get the raw feature data from the dictionary and process them
        raw_features = dict_data.get("uniprot").get("entry").get("feature", [])
        if not isinstance(raw_features, list):
            raw_features = [raw_features]

        # Map the features data using the get_feature function
        features = list(map(get_feature, raw_features))
        
        # Task to write the evidence information into the graph database
        write_transaction(query, {"features": features})
    
    # Task to write the evidence information into the graph database
    @task(task_id='write_evidences')
    def write_evidences(dict_data, accession):  
        
        # Cypher query to create the relationship between Protein and Evidence nodes with their properties
        query = """
            UNWIND $evidences AS evidence
            MATCH (p:Protein {id: evidence.id}) 
            CREATE 
                (p)-[:HAS_EVIDENCE]->
                (:Evidence {type: evidence.type, key: evidence.key})
        """
        
        # Function to get an evidence object from a given evidence
        def get_evidence(evidence):
            return {
                "id": accession,
                "type": evidence.get("@type"),
                "key": evidence.get("@key"),
            }

        # Get evidences from the dictionary and process them
        evidences = []
        if not isinstance(dict_data.get("uniprot").get("entry").get("evidence"), list):
            evidences.append(dict_data.get("uniprot").get("entry").get("evidence"))
        else:
            evidences = dict_data.get("uniprot").get("entry").get("evidence")

        # Map the evidences data using the get_evidence function
        evidences = list(map(get_evidence, evidences))
        
        # Execute the write transaction with the evidences data
        write_transaction(query, { "evidences": evidences })

    # Task to write the sequences of a protein
    @task(task_id='write_sequences')
    def write_sequences(dict_data, accession): 
        
        # Cypher query to create the relationship between Protein and Sequence nodes with their properties
        query = """
        UNWIND $sequences AS sequence
        MATCH (p:Protein {id: sequence.id}) 
        CREATE 
            (p)-[:HAS_SEQUENCE {checksum: sequence.checksum}]->
            (:Sequence {length: sequence.length, mass: sequence.mass, modified: sequence.modified, version: sequence.version, value: sequence.value})
        """
        
        # Check if there is a single sequence or a list of sequences
        sequences = []
        if not isinstance(dict_data.get("uniprot").get("entry").get("sequence"), list):
            sequences.append(dict_data.get("uniprot").get("entry").get("sequence"))
        else:
            sequences = dict_data.get("uniprot").get("entry").get("sequence")

        # Helper function to extract sequence information and return it as a dictionary
        def get_sequence(sequence):
            return {
                "id": accession,
                "length": sequence.get("@length"), 
                "mass": sequence.get("@mass"), 
                "modified": sequence.get("@modified"), 
                "version": sequence.get("@version"), 
                "value": sequence.get("@text"), 
                "checksum": sequence.get("@checksum")
            }

        # Map the sequences using the get_sequence function
        sequences = list(map(get_sequence, sequences))

        # Execute the Cypher query with the formatted sequences data
        write_transaction(query, { "sequences": sequences })
        
    # Task to write the reference information into the graph database
    @task(task_id='write_references')
    def write_references(dict_data, accession):
        def get_reference(reference):
            return {
                "type": reference.get("citation").get("@type"),
                "name": reference.get("citation").get("@name"),
                "volume": reference.get("citation").get("@volume"),
                "id": accession
            }

        # Define the Cypher query to create a relationship between a Protein node and a Reference node
        query = """
            UNWIND $references AS reference
            MATCH (p:Protein {id: reference.id}) 
            CREATE (p)-[:HAS_REFERENCE]->(:Reference {name: reference.name, type: reference.type, volume: reference.volume})
        """

        # Extract references from the dictionary data
        references = []
        if(isinstance(dict_data.get("uniprot").get("entry").get("reference"), list)):
            references = dict_data.get("uniprot").get("entry").get("reference")
        else:
            references.append(dict_data.get("uniprot").get("entry").get("reference"))

        references = list(map(get_reference, references))

        write_transaction(query, { "references": references })

        return dict_data.get("uniprot").get("entry").get("reference")

    # Task to write the citation information of references into the graph database
    @task(task_id='write_citations_of_references')
    def write_citations_of_references(references):
        def get_citation_from_reference(reference):
            if not reference.get("citation") or not reference.get("citation").get("@name"):
                return []
            
            if(isinstance(reference.get("citation"), list)):
                return list(map(lambda c: { "title": c.get("title"), "reference": reference.get("citation").get("@name") }, reference.get("citation")))
            else:
                return [{
                    "title": reference.get("citation").get("title"), 
                    "reference": reference.get("citation").get("@name")
                }]

        # Define the Cypher query to create a relationship between a Reference node and a Citation node
        query = """
            UNWIND $citations AS citation
            MATCH (r:Reference {name: citation.reference}) CREATE (r)-[:HAS_CITATION]->(:Citation {title: citation.title})
        """

        # Map the citations data from the references and flatten the list
        citations = list(map(get_citation_from_reference, references))
        citations = [item for sublist in citations for item in sublist]

        # Execute the write transaction with the citations data
        write_transaction(query, { "citations": citations })

    # Execute the ETL tasks
    dict_data = fetch_xml_file()
    accession = write_accession(dict_data)
    write_full_name(dict_data, accession)
    write_genes(dict_data, accession)
    
    organisms = get_organisms(dict_data, accession)
    write_organisms(organisms)
    write_lineages_of_organisms(organisms)

    references = write_references(dict_data, accession)
    write_citations_of_references(references)
    write_authors_of_references(references)
    
    write_features(dict_data, accession)
    write_evidences(dict_data, accession)
    write_sequences(dict_data, accession)
    write_alternate_names(dict_data, accession)
    

# Define the DAG for the ETL process
dag = etl_uniprot_Q9Y261()

