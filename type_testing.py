from typing import Generic, Protocol, TypeVar, Union


class A:
    def m(self):
        return 1

    def ma(self):
        return 1


class B:
    def m(self):
        return 2

    def mb(self):
        return 2


class C:
    ...


class Uni:
    def __init__(self, a_or_b: Union[A, B]):
        self.a_or_b = a_or_b


# a = Uni(A())
# a.a_or_b.m
# a.a_or_b.ma
# a.a_or_b.mb


class WithM(Protocol):
    def m(self):
        ...


DriverType = TypeVar("DriverType", bound=WithM)


class Gen(Generic[DriverType]):
    def __init__(self, a_or_b: DriverType):
        self.a_or_b = a_or_b


# class Typ:
#     def __init__(self, a_or_b: T):
#         self.a_or_b = a_or_b


# b = Typ(A())
# b.a_or_b.m
# b.a_or_b.ma
# b.a_or_b.mb


# a = Gen(A())
# a.a_or_b.m
# a.a_or_b.ma
# a.a_or_b.mb

# b = Gen(B())
# b.a_or_b.m
# b.a_or_b.ma
# b.a_or_b.mb

# c = Gen(C())
