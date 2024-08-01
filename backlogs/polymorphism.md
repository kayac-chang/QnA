
如果服務只支援一種 Store 的情況，直接調用實際的 Class Instance。

```py
class FaissVectorStore:
    def add(value: list[float]) -> None: ...

    def search(query: str) -> str: ...

stores: dict[str, FaissVectorStore] = {} # ========> 注意這邊是 dict[str, FaissVectorStore]

@router.post('/')
def create_vector_store() -> str:
    id = uuid()

    stores[id] = FaissVectorStore()

    return id

@router.post('/{id}')
def add(id: str, value: list[float]) -> None:
    stores[id].add(value)

@router.get('/{id}')
def search(query: str) -> str:
    return stores[id].search(query)
```

假設服務希望支援兩種以上的 Store，
調用方理應不用知道具體的 Class Instance，只要確定該 Instance 一定會實作 add 與 search。

所以調用方申明了只要傳進來的 Instance 支援 interface VectorStore，
至於具體 Instance 是由哪個 Class 實作，對調用方來說就不是這麼重要。

```py
class FaissVectorStore:
    def add(value: list[float]) -> None: ...

    def search(query: str) -> str: ...

class PGVectorStore:
    def add(value: list[float]) -> None: ...

    def search(query: str) -> str: ...


stores: dict[str, VectorStore] = {} # ========> dict[str, VectorStore] 的這個 VectorStore 希望是一個 interface，而非 BaseClass

@router.post('/')
def create_vector_store(type: Literal['faiss', 'pgvector']) -> str:
    id = uuid()

    match type:
        case 'faiss':
            stores[id] = FaissVectorStore()
        case 'pgvector':
            stores[id] = PGVectorStore()

    return id

@router.post('/{id}')
def add(id: str, value: list[float]) -> None:
    stores[id].add(value)

@router.get('/{id}')
def search(query: str) -> str:
    return stores[id].search(query)
```

在 python 中並沒有原生的 interface syntax，
但是有很多種方法可以搞出類似 interface 的效果，
這邊示範的是透過 Protocol 型別的方式實踐 interface。

```py
class VectorStore(Protocol):
    @abstractmethod
    async def add(self, *embeddings: Embedding) -> None:
        raise NotImplementedError

    @abstractmethod
    async def search(self, query: Embedding, k: int = 1) -> list[SimilarityResult]:
        raise NotImplementedError
```

Protocol 的好處是，Class 可以不用刻意去繼承某個介面，
但是同樣可以達到 type check 的效果。

```py

class FaissVectorStore:
    def add(value: list[float]) -> None: ...

    def search(query: str) -> str: ...

class PGVectorStore:
    def add(value: list[float]) -> None: ...

    def search(query: str) -> str: ...


class VectorStore(Protocol):
    @abstractmethod
    async def add(self, *embeddings: Embedding) -> None:
        raise NotImplementedError

    @abstractmethod
    async def search(self, query: Embedding, k: int = 1) -> list[SimilarityResult]:
        raise NotImplementedError

stores: dict[str, VectorStore] = {} # ====> 因為這邊型別已經告知 dict[str, VectorStore]，value 的型別必須要符合 VectorStore

@router.post('/')
def create_vector_store(type: Literal['faiss', 'pgvector']) -> str:
    id = uuid()

    match type:
        case 'faiss':
            stores[id] = FaissVectorStore() # ====> 這邊會 type check
        case 'pgvector':
            stores[id] = PGVectorStore() # ====> 這邊會 type check

    return id

@router.post('/{id}')
def add(id: str, value: list[float]) -> None:
    stores[id].add(value)

@router.get('/{id}')
def search(query: str) -> str:
    return stores[id].search(query)
```
