import pytest
from services.hello_world_service import HelloWorldService

def test_greet():
    service = HelloWorldService()
    assert service.greet() == "Hello, World!"