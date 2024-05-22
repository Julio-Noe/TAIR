import csv
from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import DCTERMS, RDF, RDFS, SKOS, XSD, PROV, OWL

standard_type = "aiAct"
public = False

#Files

input_output_file_name = standard_type+"_concepts"

input_file = csv.DictReader(open(input_output_file_name+".csv"))

tair_namespace = Namespace('http://tair.adaptcentre.ie/ontologies/tair/')

# make a graph
output_graph = Graph()

output_graph.bind("tair", tair_namespace)
output_graph.bind("skos", SKOS)
output_graph.bind("dct", DCTERMS)
#output_graph.bind("prov", PROV)

#Links
standard_type == "aiAct"

def validatingRow (row, columnName):
    if len(row[columnName]) == 0:        
        return 0
    else:
        return 1

for row in input_file:    
    #convert it from an OrderedDict to a regular Dict
    row = dict(row)
    output_graph.add( (URIRef(tair_namespace+(row['Concept'])), RDF.type, URIRef(SKOS)) )
    
    ############################scopeNote######################
    if "skos:scopeNote1" in row:
        if validatingRow(row, 'skos:scopeNote1'):            
            output_graph.add( (URIRef(tair_namespace+(row['skos:Concept'])), SKOS.scopeNote, Literal(row['skos:scopeNote1'], lang="en")) )
    
    #Check not empty column
    if validatingRow(row, 'skos:prefLabel'):
        output_graph.add( (URIRef(tair+(row['Requirement'])), SKOS.prefLabel, Literal(row['skos:prefLabel'], lang="en")) )
    if validatingRow(row, 'skos:altLabel'):
        output_graph.add( (URIRef(tair+(row['Requirement'])), SKOS.altLabel, Literal(row['skos:altLabel'], lang="en")) )
    if validatingRow(row, 'skos:definition'):
        if public != True: 
            output_graph.add( (URIRef(tair+(row['Requirement'])), SKOS.definition, Literal(row['skos:definition'], lang="en")) )
        else:
            output_graph.add( (URIRef(tair+(row['Requirement'])), SKOS.definition, Literal("", lang="en")) )

    if validatingRow(row, 'skos:related'):
        if "," in row['skos:related']:
            for related in row['skos:related'].split(","):
                output_graph.add( (URIRef(tair+(row['Requirement'])), SKOS.related, URIRef(tair+related.strip())) )
        else:
            output_graph.add( (URIRef(tair+(row['Requirement'])), SKOS.related, URIRef(tair+row['skos:related'])) )
    if validatingRow(row, 'tair:decomposes'):
        if "," in row['tair:decomposes']:
            for element in row['tair:decomposes'].split(","):
                output_graph.add( (URIRef(tair+(row['Requirement'])), URIRef(tair+"decomposes"), URIRef(tair+element.strip())) )
        else:
            output_graph.add( (URIRef(tair+(row['Requirement'])), URIRef(tair+"decomposes"), URIRef(tair+row['tair:decomposes'])) )
    if "tair:hasSpecification" in row:
        if validatingRow(row, 'tair:hasSpecification'):
            if "," in row['tair:hasSpecification']:
                for element in row['tair:hasSpecification'].split(","):
                    output_graph.add( (URIRef(tair+(row['Requirement'])), URIRef(tair+"hasSpecification"), URIRef(tair+element.strip())) )
            else:
                output_graph.add( (URIRef(tair+(row['Requirement'])), URIRef(tair+"hasSpecification"), URIRef(tair+row['tair:hasSpecification'])) )
    
output_graph.serialize(destination=input_output_file_name+".ttl", format='turtle')