import sqlalchemy
from simqle.utility import bind_sql

def test_bind_sql_without_params(mocker):
    mock_text = mocker.patch("simqle.utility.text", return_value="some bound sql text")

    # without params
    bound_sql = bind_sql("some sql text", None)
    assert bound_sql == "some bound sql text"

    mock_text.assert_called_once_with("some sql text")


def test_bind_sql_with_params(mocker):
    class MockBoundSQL():
        @staticmethod
        def bindparams(param):
            return MockBoundSQL()

    mock_text = mocker.patch("simqle.utility.text", return_value=MockBoundSQL)

    # with params
    params = {"str key": "some string", "int key": 4}

    mock_VARCHAR = mocker.patch("simqle.utility.VARCHAR", return_value="some varchar")
    mock_bindparam = mocker.patch("simqle.utility.bindparam", return_value="some param")

    bound_sql = bind_sql("some sql text", params)

    mock_VARCHAR.assert_called_once()
