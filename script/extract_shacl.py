import rdflib
from rdflib.namespace import RDF, RDFS, OWL, SH

# Load the ontology
g = rdflib.Graph()
g.parse("product_compatibility.owl", format="xml")

# Create a new graph for the SHACL shapes
shapes_graph = rdflib.Graph()

# Define a function to create a SHACL shape for a given class
def create_shape_for_class(class_uri):
    # Create a new blank node for the shape
    shape_bnode = rdflib.BNode()

    # Define the shape as a sh:NodeShape that targets the class URI
    shapes_graph.add((shape_bnode, RDF.type, SH.NodeShape))
    shapes_graph.add((shape_bnode, SH.targetClass, rdflib.URIRef(class_uri)))

    # Iterate over the properties of the class
    for prop, _, _ in g.triples((None, RDF.type, rdflib.URIRef(class_uri))):
        # Create a new blank node for the property shape
        prop_shape_bnode = rdflib.BNode()

        # Define the property shape as a sh:PropertyShape that targets the property URI
        shapes_graph.add((prop_shape_bnode, RDF.type, SH.PropertyShape))
        shapes_graph.add((prop_shape_bnode, SH.path, rdflib.URIRef(prop)))

        # Add constraints to the property shape based on the domain and range of the property
        for domain, _, _ in g.triples((rdflib.URIRef(prop), RDFS.domain, None)):
            shapes_graph.add((prop_shape_bnode, SH.in, rdflib.URIRef(domain)))
        for range_, _, _ in g.triples((rdflib.URIRef(prop), RDFS.range, None)):
            if range_ == OWL.Thing:
                shapes_graph.add((prop_shape_bnode, SH.datatype, SH.IRI))
            else:
                shapes_graph.add((prop_shape_bnode, SH.datatype, rdflib.URIRef(range_)))

        # Add the property shape to the class shape
        shapes_graph.add((shape_bnode, SH.property, prop_shape_bnode))

    return shape_bnode

# Iterate over the classes in the ontology and create a SHACL shape for each one
for class_uri, _, _ in g.triples((None, RDF.type, OWL.Class)):
    shapes_graph.add((create_shape_for_class(class_uri), RDFS.label, rdflib.Literal(class_uri)))

# Serialize the shapes graph as Turtle and save it to a file
shapes_graph.serialize(destination="product_compatibility_shacl.ttl", format="turtle")

