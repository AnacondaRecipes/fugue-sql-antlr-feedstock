import os
import pytest

# Force Python parser mode for all tests
os.environ["FUGUE_SQL_ANTLR_PARSE_MODE"] = "py"

@pytest.fixture(autouse=True)
def set_parse_mode():
    """Automatically set parse_mode to 'py' for all tests."""
    # This fixture runs before each test
    os.environ["FUGUE_SQL_ANTLR_PARSE_MODE"] = "py"

@pytest.fixture(autouse=True)
def monkeypatch_parse_mode(monkeypatch):
    """Monkey patch the parser to force Python mode."""
    try:
        from fugue_sql_antlr.parser import FugueSQLParser
        
        # Store original __init__ method
        original_init = FugueSQLParser.__init__
        
        def patched_init(self, *args, **kwargs):
            # Force parse_mode to 'py' if not explicitly set to 'auto'
            if 'parse_mode' in kwargs and kwargs['parse_mode'] == 'cpp':
                kwargs['parse_mode'] = 'py'
            elif 'parse_mode' not in kwargs:
                kwargs['parse_mode'] = 'py'
            return original_init(self, *args, **kwargs)
        
        # Apply the patch
        monkeypatch.setattr(FugueSQLParser, '__init__', patched_init)
    except ImportError:
        # If the module is not available, skip the patch
        pass
