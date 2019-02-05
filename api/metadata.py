from maxfw.core import MAX_API, MetadataAPI, METADATA_SCHEMA
from config import MODEL_META_DATA

class ModelMetadataAPI(MetadataAPI):

    @MAX_API.marshal_with(METADATA_SCHEMA)
    def get(self):
        """Return the metadata associated with the model"""
        return MODEL_META_DATA