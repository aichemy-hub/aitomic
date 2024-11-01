import aitomic


def test_foo() -> None:
    assert aitomic.foo(12) == "Hello, World! Also: 12"
