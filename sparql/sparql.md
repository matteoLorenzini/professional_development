* Find all classes in the ontology

```
SELECT DISTINCT ?class
WHERE {
  ?class a owl:Class.
}
```

* Find all properties in the ontology

```
SELECT DISTINCT ?property
WHERE {
  ?property a owl:Property.
}
```

* Find all subclasses of a specific class (Note: replace :MyClass with the name of the class you are interested in)

```
SELECT DISTINCT ?subclass
WHERE {
  :MyClass rdfs:subClassOf* ?subclass.
}
```

* Find all instances of a specific class (Note: replace :MyClass with the name of the class you are interested in)

```
SELECT DISTINCT ?instance
WHERE {
  ?instance a :MyClass.
}
```

* Find all classes that have a specific property (Note: replace http://example.com/ontology# with the namespace of the ontology, and make sure to use the correct prefix in the query)

```
SELECT DISTINCT ?class
WHERE {
  ?class ?property ?value.
  FILTER(isURI(?value))
  FILTER(STRSTARTS(str(?property), "http://example.com/ontology#"))
}
```

* Count the number of individuals for each class

```
SELECT ?class (COUNT(?individual) AS ?count)
WHERE {
  ?individual a ?class .
}
GROUP BY ?class
ORDER BY DESC(?count)
```

* Count the number of properties for each class

```
SELECT ?class (COUNT(?property) AS ?count)
WHERE {
  ?property a rdf:Property .
  ?domain rdfs:subClassOf* ?class .
  ?property rdfs:domain ?domain .
}
GROUP BY ?class
ORDER BY DESC(?count)
```

* Find the classes with the highest average number of properties per individual

```
SELECT ?class (AVG(?count) AS ?avgCount)
WHERE {
  ?individual a ?class .
  {
    SELECT ?individual (COUNT(?property) AS ?count)
    WHERE {
      ?individual ?property ?value .
    }
    GROUP BY ?individual
  }
}
GROUP BY ?class
ORDER BY DESC(?avgCount)
```


* Find the most commonly used properties in the ontology

```
SELECT ?property (COUNT(?subject) AS ?count)
WHERE {
  ?subject ?property ?object .
  FILTER(isURI(?property))
}
GROUP BY ?property
ORDER BY DESC(?count)
LIMIT 10
```
* Query to retrieve all direct superclasses and subclasses of a given class (Replace <class_uri> with the URI of the class you want to retrieve the direct superclasses and subclasses for.)

```
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?superclass ?subclass
WHERE {
  ?subclass rdfs:subClassOf ?superclass .
  FILTER (?superclass = <class_uri>)
}
```

* Query to retrieve all classes that are in the same path of inheritance as a given class (Replace <class_uri> with the URI of the class you want to retrieve the related classes for.)

```
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?class1 ?class2
WHERE {
  ?class1 rdfs:subClassOf* ?class2 .
  FILTER (?class1 = <class_uri>)
}
```

* Query to retrieve all classes that have a common superclass with a given class (Replace <class_uri> with the URI of the class you want to retrieve the related classes for. This query retrieves all classes that have a common superclass with the given class, excluding the given class itself)

```
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT DISTINCT ?class
WHERE {
  ?class rdfs:subClassOf ?superclass1 .
  <class_uri> rdfs:subClassOf ?superclass2 .
  ?superclass1 rdfs:subClassOf* ?superclass2 .
  FILTER (?class != <class_uri>)
}
```

* List all digital cameras with their brand and mounting type

```
PREFIX : <http://example.com/camera-ontology#>
PREFIX camera: <http://example.com/camera#>
PREFIX brand: <http://example.com/brand#>
PREFIX mounting: <http://example.com/mounting#>

SELECT ?camera ?brand ?mountingType WHERE {
  ?camera rdf:type camera:DigitalCamera ;
          :hasBrand ?brand ;
          :hasMountingType ?mountingType .
}
```

* List all camera lenses compatible with the Nikon Z7

```
PREFIX : <http://example.com/camera-ontology#>
PREFIX camera: <http://example.com/camera#>

SELECT ?lens WHERE {
  ?lens rdf:type camera:CameraLens ;
        :isCompatibleWith camera:Nikon_Z7 .
}

```

* List all third-party brands

```
PREFIX brand: <http://example.com/brand#>

SELECT ?brand WHERE {
  ?brand rdf:type brand:ThirdPartyBrand .
}
```
* Retrieves camera lenses that are compatible with the Nikon Z7 and also includes a DBpedia description of each lens

```
PREFIX  :     <http://example.com/camera-ontology#>
PREFIX  dbo:  <http://dbpedia.org/ontology/>
PREFIX  dbp:  <http://dbpedia.org/resource/>
PREFIX  camera: <http://example.com/camera#>
PREFIX  rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

SELECT DISTINCT  ?lens ?dbpDescription
WHERE
  { ?lens  rdf:type           camera:CameraLens ;
           :isCompatibleWith  camera:Nikon_Z7
    SERVICE <http://dbpedia.org/sparql>
      { ?dbpLens  dbo:product   ?lensName ;
                  dbo:abstract  ?dbpDescription
        FILTER ( lang(?dbpDescription) = "en" )
        FILTER contains(?lensName, "Nikon Z7")
      }
  }
```
* List all cameras that are compatible with the Nikon Z mount

```
PREFIX : <http://example.com/camera-ontology#>
PREFIX camera: <http://example.com/camera#>

SELECT ?camera WHERE {
  ?camera rdf:type camera:DigitalCamera ;
          :hasMountingType mounting:Z_Mount .
}
```

* List all camera lenses that are compatible with the EF mount and made by Canon

```
PREFIX : <http://example.com/camera-ontology#>
PREFIX camera: <http://example.com/camera#>
PREFIX brand: <http://example.com/brand#>
PREFIX mounting: <http://example.com/mounting#>

SELECT ?lens WHERE {
  ?lens rdf:type camera:CameraLens ;
        :hasBrand brand:Canon ;
        :hasMountingType mounting:EF_Mount ;
        :isCompatibleWith ?camera .
  ?camera rdf:type camera:DigitalCamera .
}
```

* List all cameras that have a sensor size specification

```
PREFIX : <http://example.com/camera-ontology#>
PREFIX camera: <http://example.com/camera#>

SELECT ?camera WHERE {
  ?camera rdf:type camera:Camera ;
          :hasSensorSize ?sensorSize .
}
```

* List all camera lenses that are compatible with a camera of brand Nikon

```
PREFIX : <http://example.com/camera-ontology#>
PREFIX camera: <http://example.com/camera#>
PREFIX brand: <http://example.com/brand#>

SELECT ?lens WHERE {
  ?lens rdf:type camera:CameraLens ;
        :isCompatibleWith ?camera ;
        ?camera :hasBrand brand:Nikon .
}
```

* List all mirrorless cameras with their brand and mounting type

```
PREFIX : <http://example.com/camera-ontology#>
PREFIX camera: <http://example.com/camera#>
PREFIX brand: <http://example.com/brand#>
PREFIX mounting: <http://example.com/mounting#>

SELECT ?camera ?brand ?mountingType WHERE {
  ?camera rdf:type camera:MirrorlessCamera ;
          :hasBrand ?brand ;
          :hasMountingType ?mountingType .
}
```

* List all camera lenses that have a brand specification

```
PREFIX : <http://example.com/camera-ontology#>
PREFIX camera: <http://example.com/camera#>

SELECT ?lens WHERE {
  ?lens rdf:type camera:CameraLens ;
        :hasBrand ?brand .
}
```

* Retrieve all camera lenses that are not compatible with any digital camera

```
PREFIX : <http://example.com/camera-ontology#>
PREFIX camera: <http://example.com/camera#>
PREFIX brand: <http://example.com/brand#>
PREFIX mounting: <http://example.com/mounting#>
SELECT ?lens
WHERE {
  ?lens rdf:type camera:CameraLens .
  FILTER NOT EXISTS {
    ?camera rdf:type camera:DigitalCamera .
    ?camera :isCompatibleWith ?lens .
  }
}
```

* Retrieve all digital cameras that have a sensor size of "Full Frame"

```
PREFIX : <http://example.com/camera-ontology#>
PREFIX camera: <http://example.com/camera#>
PREFIX brand: <http://example.com/brand#>
PREFIX mounting: <http://example.com/mounting#>
SELECT ?camera
WHERE {
  ?camera rdf:type camera:DigitalCamera .
  ?camera :hasSensorSize "Full Frame" .
}
```

* Retrieve all digital cameras and their compatible lenses

```
PREFIX : <http://example.com/camera-ontology#>
PREFIX camera: <http://example.com/camera#>
PREFIX brand: <http://example.com/brand#>
PREFIX mounting: <http://example.com/mounting#>
SELECT ?camera ?lens
WHERE {
  ?camera rdf:type camera:DigitalCamera .
  ?camera :hasBrand ?brand .
  ?lens rdf:type camera:CameraLens .
  ?lens :hasBrand ?lensBrand .
  ?camera :isCompatibleWith ?lens .
}
```

* Retrieve all third-party brand digital cameras

```
PREFIX : <http://example.com/camera-ontology#>
PREFIX camera: <http://example.com/camera#>
PREFIX brand: <http://example.com/brand#>
PREFIX mounting: <http://example.com/mounting#>
SELECT ?camera ?brand
WHERE {
  ?camera rdf:type camera:DigitalCamera .
  ?camera :hasBrand ?brand .
  ?brand rdf:type brand:ThirdPartyBrand .
}
```

* Retrieve all digital cameras that are compatible with a Nikon Z7 camera and have a mounting type of Z_Mount

```
PREFIX : <http://example.com/camera-ontology#>
PREFIX camera: <http://example.com/camera#>
PREFIX brand: <http://example.com/brand#>
PREFIX mounting: <http://example.com/mounting#>
SELECT ?camera
WHERE {
  ?camera rdf:type camera:DigitalCamera .
  ?camera :hasBrand ?brand .
  ?camera :hasMountingType mounting:Z_Mount .
  ?lens rdf:type camera:CameraLens .
  ?lens :hasBrand brand:Nikon .
  ?lens :hasMountingType mounting:Z_Mount .
  ?camera :isCompatibleWith ?lens .
  ?lens :isCompatibleWith camera:Nikon_Z7 .
}
```

* Federated query over Wikidata SPARQL endpoint

```
PREFIX  :     <http://example.com/camera-ontology#>
PREFIX  schema: <http://schema.org/>
PREFIX  rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX  mounting: <http://example.com/mounting#>
PREFIX  wdt:  <http://www.wikidata.org/prop/direct/>
PREFIX  rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX  camera: <http://example.com/camera#>
PREFIX  brand: <http://example.com/brand#>
PREFIX  wd:   <http://www.wikidata.org/entity/>

SELECT DISTINCT  ?camera ?description
WHERE
  { ?camera  rdf:type  camera:MirrorlessCamera
    SERVICE <https://query.wikidata.org/sparql>
      { wd:Q62927  schema:description  ?description
        FILTER ( lang(?description) = "en" )
      }
  }
  ```
