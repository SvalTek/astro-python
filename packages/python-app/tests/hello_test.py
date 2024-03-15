"""Hello unit test module."""

from hello import hello


def test_hello():
    """Test the hello function."""
    assert hello() == "Hello astro-python"
