from typing import Callable
from unittest.mock import MagicMock, call, mock_open, patch

from project.my_functions import (
    my_upper_callback,
    my_upper_file,
    my_upper_readlines,
    my_writer,
)


def test_callable():

    with patch("project.my_functions.Callback") as mocked_callback:

        mocked_callback.return_value = "My result"

        got = my_upper_callback(mocked_callback)

        mocked_callback.assert_called_with("This is a test")
        assert got == "MY RESULT"


@patch("project.my_functions.Callback")
def test_callable_as_parameter(mocked_callback: MagicMock):

    mocked_callback.return_value = "My result"

    got = my_upper_callback(mocked_callback)

    mocked_callback.assert_called_with("This is a test")
    assert got == "MY RESULT"


def test_with_file():

    data = "first line\nsecond line\nthird line\n"

    with patch("builtins.open", mock_open(read_data=data), create=True) as mock_file:

        got = my_upper_file("filename")
        mock_file.assert_called_once_with("filename", "r")

        assert got == "FIRST LINE\nSECOND LINE\nTHIRD LINE\n"


def test_with_readlines():

    data = "first line\nsecond line\nthird line\n"

    with patch("builtins.open", mock_open(read_data=data), create=True) as mock_file:

        got = my_upper_readlines("filename")
        mock_file.assert_called_once_with("filename", "r")

        assert got == "FIRST LINE\nSECOND LINE\nTHIRD LINE\n"


def test_write_file():

    with patch("builtins.open", mock_open(), create=True) as mock_file:

        my_writer("filename", "some stuff")

        mock_file.assert_called_once_with("filename", "w")
        handle = mock_file()
        # print(handle.mock_calls)
        handle.write.assert_called_once_with("some stuff")


def test_mock_assertion():
    mock = MagicMock()
    mock.method()
    mock.method.assert_called()

    mock.method2()
    mock.method2.assert_called_once()

    mock.method3(1, 2, 3, test="wow")
    mock.method3.assert_called_with(1, 2, 3, test="wow")

    mock.method4("foo", bar="baz")
    mock.method4.assert_called_once_with("foo", bar="baz")

    mock.method5(1, 2, arg="thing")
    mock.method5("some", "thing", "else")
    mock.method5.assert_any_call(1, 2, arg="thing")

    mock.method6(1)
    mock.method6(2)
    mock.method6(3)
    mock.method6(4)
    mock.method6.assert_has_calls([call(2), call(3)])
    mock.method6.assert_has_calls([call(4), call(2), call(3)], any_order=True)

    mock.method7.assert_not_called()

    mock.method8("hello")
    assert mock.method8.called == True
    mock.method8.reset_mock()
    assert mock.method8.called == False

    assert mock.method9.call_count == 0
    mock.method9()
    mock.method9()
    assert mock.method9.call_count == 2


def test_returns():
    mock = MagicMock()
    mock.method1.return_value = "fish"
    assert mock.method1() == "fish"

    mock.method2 = MagicMock(return_value=3)
    assert mock.method2.return_value == 3

    mock.method3.side_effect = Exception()
    try:
        mock.method3()
    except Exception as e:
        print(e)

    mock.method4.side_effect = [1, 2, 3]
    assert mock.method4() == 1
    assert mock.method4() == 2
    assert mock.method4() == 3

    mock.method5 = MagicMock(side_effect=lambda x: x + 1)
    assert mock.method5(2) == 3
    assert mock.method5(5) == 6
    assert mock.method5(9) == 10

    mock.method6.side_effect = lambda x: {"a": 1, "b": 2, "c": 3}[x]
    assert mock.method6("a") == 1
    assert mock.method6("b") == 2
    assert mock.method6("c") == 3

    mock.method7 = MagicMock()
    result7 = mock.method7(1, 2, 3)
    mock.method7.first(a=3)
    mock.method7.second()
    int(mock.method7)  # *1
    int(mock.method7())  # *2
    result7(1)
    expected = [
        call(1, 2, 3),
        call.first(a=3),
        call.second(),
        call.__int__(),  # *1
        call(),  # *2
        call().__int__(),  # *2
        call()(1),
    ]
    assert mock.method7.mock_calls == expected
