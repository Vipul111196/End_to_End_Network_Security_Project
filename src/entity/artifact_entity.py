from dataclasses import dataclass

@dataclass # Dataclass is a decorator that is used to create a class with pre-defined attributes
class DataIngestionArtifact:
    trained_file_path:str
    test_file_path:str

