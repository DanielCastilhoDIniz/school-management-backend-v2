from abc import ABC, abstractmethod


class Veiculo(ABC):

    @abstractmethod
    def buscar_cliente(self) -> None: pass


class CarroLuxo(Veiculo):
    def buscar_cliente(self) -> None:
        print("Carro de luxo esta buscando cliente...")


class CarroPopular(Veiculo):
    def buscar_cliente(self) -> None:
        print("Carro de Popular esta buscando cliente...")


class MotoLuxo(Veiculo):
    def buscar_cliente(self) -> None:
        print("Moto de luxo esta buscando cliente...")


class MotoPopular(Veiculo):
    def buscar_cliente(self) -> None:
        print("Moto popular esta buscando cliente...")


class VeiculoFactory:
    @staticmethod
    def get_carro(tipo: str) -> Veiculo:
        if tipo == "Luxo":
            return CarroLuxo()
        if tipo == "Popular":
            return CarroPopular()
        if tipo == "MotoLuxo":
            return MotoLuxo()
        if tipo == "MotoPopular":
            return MotoPopular()
        assert 0, "Veiculo não existe"


if __name__ == "__main__":
    carros_disponiveis = ["Popular", "Luxo", "MotoPopular", "MotoLuxo"]
    from random import choice

    for carro in range(10):
        carro = VeiculoFactory.get_carro(choice(carros_disponiveis))

        carro.buscar_cliente()