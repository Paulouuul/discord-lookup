import pytest
from discord_lookup.utils import snowflake_to_timestamp


def test_snowflake_to_timestamp():
    result = snowflake_to_timestamp("319116687695675392")
    assert "2017" in result
    assert "/" in result

def test_invalid_snowflake():
    with pytest.raises(ValueError):
        snowflake_to_timestamp("invalido")