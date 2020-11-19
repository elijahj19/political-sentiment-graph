from sparknlp.base import *
from sparknlp.annotator import *
from sparknlp.pretrained import PretrainedPipeline
import sparknlp

spark = sparknlp.start(gpu=True)
sparknlp.version()
spark.version

# Download a pre-trained pipeline
pipeline = PretrainedPipeline('explain_document_dl', lang='en')

# Your testing dataset
text = """
The Mona Lisa is a 16th century oil painting created by Leonardo.
It's held at the Louvre in Paris.
"""

# Annotate your testing dataset
result = pipeline.annotate(text)

# What's in the pipeline
list(result.keys())