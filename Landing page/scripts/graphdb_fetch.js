/////////////////////////////////////////
/////////////////Base URL////////////////
/////////////////////////////////////////
let baseUrl = 'https://tair.adaptcentre.ie/graphdb/repositories/tair_public?query='

///////////////////////////////////////////
//////////////PREFIX definition////////////
///////////////////////////////////////////

let skosPrefix = 'PREFIX skos: <http://www.w3.org/2004/02/skos/core#>'

let tairPrefix = 'PREFIX tair: <http://tair.adaptcentre.ie/ontologies/tair/>'

let ontolexPrefix = 'PREFIX ontolex: <http://www.w3.org/ns/lemon/ontolex#>'

let provPrefix = 'PREFIX prov: <http://www.w3.org/ns/prov#>'

let dctPrefix = 'PREFIX dct: <http://purl.org/dc/terms/>'

const prefixes = skosPrefix + " " + tairPrefix + " " + ontolexPrefix + " " + provPrefix + " " + dctPrefix


const generateURL = (queryString) => {
    let accept = 'application/sparql-results+json'
    let acceptUrl = encodeURIComponent(accept)
    let queryMapped = encodeURIComponent(prefixes + " " + queryString)
    return baseUrl+queryMapped+'&Accept='+acceptUrl
}

const getConcepts = async (qs) => {
    //Initial query - get all chapters
    if(qs.length == 0){
        qs = "SELECT DISTINCT ?chapterLabel ?decomposes ?decomposesAltLabel WHERE { ?s skos:altLabel ?chapterLabel ; tair:decomposes* ?decomposes. ?decomposes skos:altLabel ?decomposesAltLabel FILTER REGEX(?chapterLabel, 'chapter', 'i')FILTER REGEX(?decomposesAltLabel, 'Title III', 'i') } ORDER BY ASC(?chapterLabel)"
        //qs = "SELECT DISTINCT ?chapterLabel ?decomposes WHERE { ?s skos:altLabel ?chapterLabel ; OPTIONAL { ?s tair:decomposes ?decomposes . } FILTER REGEX(?chapterLabel, 'chapter', 'i') } ORDER BY ASC(?chapterLabel)"
        //qs = "SELECT DISTINCT ?article WHERE { ?s a tair:AiActRequirementCollection ; skos:altLabel ?article . FILTER REGEX(?article,'article \\\\d+$','i')  } ORDER BY ASC(?article)"
    }

    console.log(qs)
    const url = generateURL(qs)
    console.log(url)
	const response = await fetch(url)
	const data = await response.json()
    return data.results.bindings
}

getConcepts("").then(binding => {
    var _select = document.getElementById("select_chapter")
    let counter = 1
    
    for (val of binding){        
        _select.options[_select.options.length] = new Option(val.chapterLabel.value, counter++)
    }
})

function selectArticle() {
    //Initialize HTML elements
    restartSelect("article")
    restartSelect("requirement")
    restartSelect("concept")
    restartSelect("related")
    restartParagraph("articleName")
    initializeList("constrainedByLabel")
    restartTextarea("requirementDefinition")
    restartTextarea("relatedDefinition")
    restartTextarea("conceptDefinition")
    ////////////////////////////////

    var _select = document.getElementById("select_chapter")
    let chapter_value = _select.options[_select.selectedIndex].text

    let query_getArticle = "SELECT DISTINCT ?article ?altLabel ?chapterDecomposesLabel WHERE { ?s a tair:AiActRequirementCollection ; skos:altLabel ?article ; tair:decomposes ?decomposes . ?decomposes skos:altLabel ?altLabel ; tair:decomposes ?chapterDecomposes . ?chapterDecomposes skos:altLabel ?chapterDecomposesLabel FILTER REGEX(?altLabel,'"+ chapter_value +"$','i')  FILTER REGEX(?chapterDecomposesLabel,'Title III$','i') } ORDER BY ASC(?article)"
    //let query_getArticle = "SELECT DISTINCT ?article ?altLabel WHERE { ?s a tair:AiActRequirementCollection ; skos:altLabel ?article ; tair:decomposes ?decomposes . ?decomposes skos:altLabel ?altLabel . FILTER REGEX(?altLabel,'"+ chapter_value +"$','i')  } ORDER BY ASC(?article)"

    getConcepts(query_getArticle).then(binding => {
        var _select = document.getElementById("article")
        let counter = 1
        
        for (val of binding){
            _select.options[_select.options.length] = new Option(val.article.value, counter++)
        }
    })
}


function setArticleName(selectedArticle) {
    let query_articleName = "SELECT DISTINCT ?prefLabel where { ?s a tair:AiActRequirementCollection ; skos:altLabel ?altLabel ; skos:prefLabel ?prefLabel . FILTER (REGEX(?altLabel,'"+selectedArticle+"$','i'))}"

    getConcepts(query_articleName).then(binding => {
        var _paragraph = document.getElementById("articleName")
        for (val of binding){
            _paragraph.innerHTML = val.prefLabel.value
        }
    })
}

function selectRequirement() {
    //Initialize HTML elements

    restartSelect("requirement")
    restartSelect("concept")
    restartSelect("related")
    restartParagraph("articleName")
    initializeList("constrainedByLabel")
    restartTextarea("requirementDefinition")
    restartTextarea("relatedDefinition")
    restartTextarea("conceptDefinition")
    ////////////////////////////////
    
    var _select = document.getElementById("article")
    let selected_article = _select.options[_select.value].text
    
    setArticleName(selected_article)
    
    let query_requirements = "SELECT DISTINCT ?altLabel ?prefLabel where { ?s a tair:AiActRequirement ; skos:altLabel ?altLabel ; skos:prefLabel ?prefLabel ; tair:decomposes* ?decomposes. ?decomposes skos:altLabel ?decomposesAltLabel . FILTER (REGEX(?decomposesAltLabel,'"+selected_article+"','i'))} ORDER BY ASC(?altLabel)"

    getConcepts(query_requirements).then(binding => {
        var _select = document.getElementById("requirement")
        let counter = 1
        for (val of binding){
            _select.options[_select.options.length] = new Option(val.altLabel.value, counter++)
        }
    })
}

function setConstrain(selected_requirement) {
    
    let query_constrainedBy = "SELECT DISTINCT ?constrainedByLabel where { ?s ?p ?o ; skos:altLabel ?altLabel ; skos:prefLabel ?prefLabel ; tair:constrainedBy ?constrainedBy. ?constrainedBy skos:altLabel ?constrainedByLabel . FILTER (REGEX(?altLabel,'^"+selected_requirement+"$','i'))}"

    getConcepts(query_constrainedBy).then(binding => {
        var _list = document.getElementById("constrainedByLabel")
        let counter = 1
        for (val of binding){
            let li = document.createElement("li")
            li.innerText = val.constrainedByLabel.value 
            _list.appendChild(li)
        }
    })
}


function showDefinition() {

    //HTML elements initialization
    restartSelect("concept")
    restartSelect("related")
    //restartParagraph("articleName")
    restartTextarea("requirementDefinition")
    restartTextarea("conceptDefinition")
    restartTextarea("relatedDefinition")
    initializeList("constrainedByLabel") 
    //initializeList("relatedLabel")
    //////////////////////////

    var _select = document.getElementById("requirement")
    let selected_requirement = _select.options[_select.value].text

    selectConcepts(selected_requirement)
    
    setConstrain(selected_requirement) 

    setRelated(selected_requirement)
    
    let query_requirements = "SELECT DISTINCT ?definition where { ?s a tair:AiActRequirement ; skos:altLabel ?altLabel ; skos:definition ?definition . FILTER (REGEX(?altLabel,'"+selected_requirement+"$','i'))}"

    getConcepts(query_requirements).then(binding => {
        var _textarea = document.getElementById("requirementDefinition")
        for (val of binding){
            _textarea.innerHTML = val.definition.value
        }
        
    })
}

function setRelated(selected_requirement) {
    
    
    let query_related = "SELECT DISTINCT ?relatedLabel ?type where { ?s ?p ?o ; skos:altLabel ?altLabel ; skos:related ?related . ?related skos:prefLabel ?relatedLabel ; a ?type . FILTER (REGEX(?altLabel,'^"+selected_requirement+"$','i'))}"

    getConcepts(query_related).then(binding => {
        var _select = document.getElementById("related")
        let counter = 1
        for (val of binding){
            _select.options[_select.options.length] = new Option(val.relatedLabel.value, val.type.value)            
        }
    })
}

function selectConcepts(selected_requirement){

    let query_concepts = "SELECT DISTINCT ?concept ?conceptType WHERE { ?s a tair:AiActRequirement ; skos:altLabel ?altLabel ; tair:uses ?conceptURI. ?conceptURI skos:prefLabel ?concept ; a ?conceptType. FILTER (REGEX(?altLabel,'"+selected_requirement+"$','i')) }"

    getConcepts(query_concepts).then(binding => {
        var _select = document.getElementById("concept")
        for (val of binding){
             _select.options[_select.options.length] = new Option(val.concept.value, val.conceptType.value)
        }
        
    })

}

function setConceptDefinition () {
    var _select = document.getElementById("concept")
    let selected_concept = _select.options[_select.selectedIndex].text

    console.log("setConceptDefinition - text = " + selected_concept + " value = " + _select.value)

    let query_conceptDefinition = "SELECT DISTINCT ?definition where { ?s a <"+_select.value+"> ; skos:prefLabel ?prefLabel ; skos:definition ?definition . FILTER (REGEX(?prefLabel,'^"+selected_concept+"$','i'))}"

    getConcepts(query_conceptDefinition).then(binding => {
        var _textarea = document.getElementById("conceptDefinition")
        let typeConcept = ""
        for (val of binding){
            if (_select.value.toUpperCase().indexOf("CONCEPT") > 0)
                typeConcept = "Concept"
            else
                typeConcept = "Lexical entry"

            _textarea.innerHTML = typeConcept + " - " + val.definition.value
        }
        
    })

}

function setRelatedDefinition() {

    var _select = document.getElementById("related")
    let selected_related = _select.options[_select.selectedIndex].text

    console.log("setRelatedDefinition = "+ _select.value + " selected_related = " + selected_related)



    let query_relatedDefinition = "SELECT DISTINCT ?prefLabel ?altLabel ?typePrefLabel where { <"+_select.value+"> dct:description ?typePrefLabel . ?s a <"+_select.value+"> ; skos:prefLabel ?prefLabel ; skos:altLabel ?altLabel . FILTER (REGEX(?prefLabel,'^"+selected_related+"$','i'))}"  
    
    getConcepts(query_relatedDefinition).then(binding => {
        var _textarea = document.getElementById("relatedDefinition")
        for (val of binding){
            _textarea.innerHTML = val.typePrefLabel.value + " - " + val.altLabel.value + " - " +val.prefLabel.value
        }
        
    })  
}

/////////////////////////////////////////////////////////////////
////////////////////Support functions////////////////////////////
////////////////////////////////////////////////////////////////

const reduceString = (uri) => {
    let tairPosition = uri.indexOf("tair") + "tair/".length
    return uri.substring(tairPosition)
}


function restartSelect(name){
    console.log("restarting... " + name)
    document.getElementById(name).options.length = 0
    var _select = document.getElementById(name)
    _select.options[_select.options.length] = new Option("Select " + name + "...", 0)
}

function restartTextarea(name){
    console.log("restartTextarea = " + name)
    var _textarea = document.getElementById(name)

    _textarea.innerHTML = ""
}

function restartParagraph(name){
    var paragraph = document.getElementById(name)
    paragraph.innerHTML = " "
}

function initializeList(listId){
    var _list = document.getElementById(listId)
    var numElements = _list.childElementCount
    var items = _list.getElementsByTagName("li")

    for(var i = 0; i < items.length; ++i) {
        _list.removeChild(items[i])
    }
}

