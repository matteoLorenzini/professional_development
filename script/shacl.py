import rdflib
import pyshacl

# Load the ontology instance and the SHACL schema
g = rdflib.Graph()
g.parse("/Users/teolor/myRepo/professional_development/model/camera_cameraLens_v2.owl", format="xml")
shacl_graph = rdflib.Graph()
shacl_graph.parse("validation.ttl", format="turtle")

# Validate the ontology instance against the SHACL schema
r = pyshacl.validate(g, shacl_graph)

# Print the validation report
conforms, report_graph, report_text = r
print(report_text)

