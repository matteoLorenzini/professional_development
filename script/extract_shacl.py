import rdflib
import pyshacl

# Load the ontology file
g = rdflib.Graph()
g.parse("/Users/teolor/myRepo/professional_development/model/camera_cameraLens_v2.owl")

# Generate the SHACL shapes based on the ontology
shapes_graph = pyshacl.ShapesGraph(g)

# Serialize the SHACL shapes to a file
shapes_graph.graph.serialize(destination="validation.ttl", format="turtle")

