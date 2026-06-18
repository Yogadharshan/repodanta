"""Regression tests: startup path must not initialize the embedding model."""
import sys
from unittest.mock import MagicMock, patch


def _clear_repodanta():
    for key in list(sys.modules.keys()):
        if key == "repodanta" or key.startswith("repodanta."):
            del sys.modules[key]


def test_cli_import_does_not_init_model():
    """Importing cli.py must not trigger SentenceTransformer instantiation."""
    st_mock = MagicMock()
    _clear_repodanta()
    with patch.dict("sys.modules", {"sentence_transformers": st_mock}):
        import repodanta.cli  # noqa: F401
        st_mock.SentenceTransformer.assert_not_called()


def test_version_command_does_not_init_model(capsys):
    """version command must print a version string without loading the model."""
    st_mock = MagicMock()
    _clear_repodanta()
    with patch.dict("sys.modules", {"sentence_transformers": st_mock}):
        with patch("sys.argv", ["repodanta", "version"]):
            import repodanta.cli
            repodanta.cli.run()
        st_mock.SentenceTransformer.assert_not_called()
    captured = capsys.readouterr()
    assert captured.out.strip()


def test_embedder_model_not_loaded_at_import():
    """SentenceTransformer must not be instantiated when embedder is imported."""
    st_mock = MagicMock()
    _clear_repodanta()
    with patch.dict("sys.modules", {"sentence_transformers": st_mock}):
        import repodanta.embedder  # noqa: F401
        st_mock.SentenceTransformer.assert_not_called()


def test_embedder_model_initialized_once():
    """_get_model() must call SentenceTransformer exactly once across repeated calls."""
    st_mock = MagicMock()
    _clear_repodanta()
    with patch.dict("sys.modules", {"sentence_transformers": st_mock}):
        import repodanta.embedder
        repodanta.embedder._get_model()
        repodanta.embedder._get_model()
        repodanta.embedder._get_model()
        assert st_mock.SentenceTransformer.call_count == 1
