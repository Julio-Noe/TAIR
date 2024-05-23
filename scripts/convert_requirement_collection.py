import csv
from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import DCTERMS, RDF, RDFS, SKOS, XSD, PROV, OWL

standard_type = "aiAct"
public = False

#Files

input_output_file_name = standard_type+"_requirement_collection"

input_file = csv.DictReader(open(input_output_file_name+".csv"))

tair = Namespace('http://tair.adaptcentre.ie/ontologies/tair/')

# make a graph
output_graph = Graph()

output_graph.bind("tair", tair)
output_graph.bind("skos", SKOS)
output_graph.bind("dct", DCTERMS)
output_graph.bind("prov", PROV)

#Links
requirement_collection = tair+'RequirementCollection'
standard_type == "aiAct"
input_requirement_collection = tair+'AiActRequirementCollection'
requirement_collection_label = "AI Act requirement collection"
standard_source = 'https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:52021PC0206'
standard_elaboratedBy = ''
standard_specifiedBy = ''
    
output_graph.add( (URIRef(input_requirement_collection), RDF.type, URIRef(requirement_collection)) )
output_graph.add( (URIRef(input_requirement_collection), RDFS.label, Literal(requirement_collection_label, lang="en")) )

###########################SpecifiedBy###################
if len(standard_specifiedBy) != 0:
    #output_graph.add( (URIRef(tairr+(row['Requirement'])), URIRef(tairp+"specifiedBy"), URIRef(standard_specifiedBy))) 
    output_graph.add( (URIRef(input_requirement_collection), URIRef(tair+"specifiedBy"), URIRef(standard_specifiedBy))) 
############################ElaboratedBy###############
if len(standard_elaboratedBy) != 0:
    output_graph.add( (URIRef(input_requirement_collection), URIRef(tair+"elaboratedBy"), Literal(standard_elaboratedBy, lang="en"))) 
###########################Description#######################
if len(requirement_collection_label) != 0:
    output_graph.add( (URIRef(input_requirement_collection), DCTERMS.description, Literal(requirement_collection_label, lang="en")) )
###########################Source#######################
if len(standard_source) != 0:
    output_graph.add( (URIRef(input_requirement_collection), DCTERMS.source, URIRef(standard_source)) )
#Function definitions

def validatingRow (row, columnName):
    if len(row[columnName]) == 0:        
        return 0
    else:
        return 1

for row in input_file:    
    #convert it from an OrderedDict to a regular Dict
    row = dict(row)
    output_graph.add( (URIRef(tair+(row['Requirement'])), RDF.type, URIRef(input_requirement_collection)) )
    
    ##########################ConformsTo"""""""""""""""""""
    #if len(standard_conformTo) != 0:
        #output_graph.add( (URIRef(tairr+(row['Requirement'])), DCTERMS.conformsTo, Literal(standard_conformTo, lang="en")) )
    #    output_graph.add( (URIRef(tair+(row['Requirement'])), DCTERMS.conformsTo, Literal(standard_conformTo, lang="en")) )
        
    ############################scopeNote######################
    if "skos:scopeNote" in row:
        if validatingRow(row, 'skos:scopeNote'):
            #output_graph.add( (URIRef(tairr+(row['Requirement'])), SKOS.scopeNote, Literal(row['skos:scopeNote'], lang="en")) )
            output_graph.add( (URIRef(tair+(row['Requirement'])), SKOS.scopeNote, Literal(row['skos:scopeNote'], lang="en")) )
    
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