from abc import ABC, abstractmethod


class ISites(ABC):

    __object_id: str = "i_sites"

    @abstractmethod
    async def scrapy(self) -> bool:
        """"""
        raise NotImplementedError("Método não implementado!")

    @abstractmethod
    async def save_datas(self) -> bool:
        """"""
        raise NotImplementedError("Método não implementado!")

    @property
    @abstractmethod
    def url(self) -> str:
        """Deve retornar a URL específica da subclasse."""
        pass

    @property
    @abstractmethod
    def object_id(self) -> str:
        """Deve retornar o id específico da subclasse."""
        pass
