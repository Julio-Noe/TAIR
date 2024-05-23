import csv
from rdflib import Graph, Literal, Namespace, URIRef
from rdflib.namespace import DCTERMS, RDF, RDFS, SKOS

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

tair_concept = tair_namespace+'Concept'
tair_concept_label = "Concept defined by a legal document, e.g., regulation or standard"
standard_elaboratedBy = ''
standard_specifiedBy = ''
    
output_graph.add( (URIRef(tair_concept), RDF.type, URIRef(SKOS.Concept)) )
output_graph.add( (URIRef(tair_concept), RDFS.label, Literal(tair_concept_label, lang="en")) )

def validatingRow (row, columnName):
    if len(row[columnName]) == 0:        
        return 0
    else:
        return 1

for row in input_file:    
    #convert it from an OrderedDict to a regular Dict
    row = dict(row)
    output_graph.add( (URIRef(tair_namespace+(row['skos:Concept'])), RDF.type, URIRef(tair_concept)) )
    
    ############################scopeNote######################
    if "skos:scopeNote1" in row:
        if validatingRow(row, 'skos:scopeNote1'):            
            output_graph.add( (URIRef(tair_namespace+(row['skos:Concept'])), SKOS.scopeNote, Literal(row['skos:scopeNote1'], lang="en")) )
    if "skos:scopeNote2" in row:
        if validatingRow(row, 'skos:scopeNote2'):            
            output_graph.add( (URIRef(tair_namespace+(row['skos:Concept'])), SKOS.scopeNote, Literal(row['skos:scopeNote2'], lang="en")) )
    if "skos:scopeNote3" in row:
        if validatingRow(row, 'skos:scopeNote3'):            
            output_graph.add( (URIRef(tair_namespace+(row['skos:Concept'])), SKOS.scopeNote, Literal(row['skos:scopeNote3'], lang="en")) )
    if "skos:scopeNote4" in row:
        if validatingRow(row, 'skos:scopeNote4'):            
            output_graph.add( (URIRef(tair_namespace+(row['skos:Concept'])), SKOS.scopeNote, Literal(row['skos:scopeNote4'], lang="en")) )
    
    if "skos:changeNote" in row:
        if validatingRow(row, 'skos:changeNote'):            
            output_graph.add( (URIRef(tair_namespace+(row['skos:Concept'])), SKOS.changeNote, Literal(row['skos:changeNote'], lang="en")) )
    
    
    #Check not empty column
    if validatingRow(row, 'skos:prefLabel'):
        output_graph.add( (URIRef(tair_namespace+(row['skos:Concept'])), SKOS.prefLabel, Literal(row['skos:prefLabel'], lang="en")) )
    if validatingRow(row, 'skos:altLabel'):
        output_graph.add( (URIRef(tair_namespace+(row['skos:Concept'])), SKOS.altLabel, Literal(row['skos:altLabel'], lang="en")) )
    if validatingRow(row, 'skos:definition'):
        if public != True: 
            output_graph.add( (URIRef(tair_namespace+(row['skos:Concept'])), SKOS.definition, Literal(row['skos:definition'], lang="en")) )
        else:
            output_graph.add( (URIRef(tair_namespace+(row['skos:Concept'])), SKOS.definition, Literal("", lang="en")) )

    if "skos:narrower" in row:
        if validatingRow(row, 'skos:narrower'):
            if "," in row['skos:narrower']:
                for narrower in row['skos:narrower'].split(","):
                    output_graph.add( (URIRef(tair_namespace+(row['skos:Concept'])), SKOS.narrower, URIRef(tair_namespace+narrower.strip())) )
            else:
                output_graph.add( (URIRef(tair_namespace+(row['skos:Concept'])), SKOS.related, URIRef(tair_namespace+row['skos:broader'])) )
    
    if validatingRow(row, 'skos:broader'):
        if "," in row['skos:broader']:
            for broader in row['skos:broader'].split(","):
                output_graph.add( (URIRef(tair_namespace+(row['skos:Concept'])), SKOS.broader, URIRef(tair_namespace+broader.strip())) )
        else:
            output_graph.add( (URIRef(tair_namespace+(row['skos:Concept'])), SKOS.related, URIRef(tair_namespace+row['skos:broader'])) )
    
    if validatingRow(row, 'skos:related'):
        if "," in row['skos:related']:
            for related in row['skos:related'].split(","):
                output_graph.add( (URIRef(tair_namespace+(row['skos:Concept'])), SKOS.related, URIRef(tair_namespace+related.strip())) )
        else:
            output_graph.add( (URIRef(tair_namespace+(row['skos:Concept'])), SKOS.related, URIRef(tair_namespace+row['skos:related'])) )
    
    '''
    if validatingRow(row, 'dct:source'):
        output_graph.add( (URIRef(tair_namespace+(row['skos:Concept'])), DCTERMS.source, URIRef(tair_namespace+row['dct:source'])) )
    '''
    if validatingRow(row, 'dct:source'):
        output_graph.add( (URIRef(tair_namespace+(row['skos:Concept'])), DCTERMS.source, Literal(row['dct:source'], lang="en")) )

    if validatingRow(row, 'dct:isVersionOf'):
        output_graph.add( (URIRef(tair_namespace+(row['skos:Concept'])), DCTERMS.isVersionOf, URIRef(tair_namespace+row['dct:isVersionOf'])) )
    
    if validatingRow(row, 'rdf:seeAlso'):
        output_graph.add( (URIRef(tair_namespace+(row['skos:Concept'])), RDFS.seeAlso, URIRef(tair_namespace+row['rdf:seeAlso'])) )

    
output_graph.serialize(destination=input_output_file_name+".ttl", format='turtle')