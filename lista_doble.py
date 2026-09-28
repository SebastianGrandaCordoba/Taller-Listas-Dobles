class Nodo:
    """Nodo de una lista doble: dato + puntero anterior + puntero siguiente."""

    def __init__(self, producto):
        self.producto = producto
        self.prev = None
        self.next = None


class ListaDoble:
    """
    Lista doblemente enlazada implementada manualmente.
    Contiene head, tail y length.
    """

    def __init__(self):
        self.head = None
        self.tail = None
        self.length = 0

    def append(self, producto):
        """Inserta al final."""
        nuevo = Nodo(producto)

        if self.head is None:
            self.head = nuevo
            self.tail = nuevo
        else:
            nuevo.prev = self.tail
            self.tail.next = nuevo
            self.tail = nuevo

        self.length += 1

    def prepend(self, producto):
        """Inserta al inicio."""
        nuevo = Nodo(producto)

        if self.head is None:
            self.head = nuevo
            self.tail = nuevo
        else:
            nuevo.next = self.head
            self.head.prev = nuevo
            self.head = nuevo

        self.length += 1

    def traverse_to_index(self, index):
        """Busca un nodo por índice usando next o prev."""
        if index < 0 or index >= self.length:
            raise IndexError("La posición está fuera de rango.")

        if index <= self.length // 2:
            actual = self.head
            for _ in range(index):
                actual = actual.next
        else:
            actual = self.tail
            for _ in range(self.length - 1, index, -1):
                actual = actual.prev

        return actual

    def insert(self, index, producto):
        """Inserta en cualquier posición."""
        if index < 0 or index > self.length:
            raise IndexError("La posición debe estar entre 0 y la longitud.")

        if index == 0:
            self.prepend(producto)
            return

        if index == self.length:
            self.append(producto)
            return

        nuevo = Nodo(producto)
        anterior = self.traverse_to_index(index - 1)
        siguiente = anterior.next

        anterior.next = nuevo
        nuevo.prev = anterior
        nuevo.next = siguiente
        siguiente.prev = nuevo

        self.length += 1

    def remove(self, index):
        """Elimina un nodo y corrige los enlaces prev/next."""
        if self.length == 0:
            raise ValueError("La lista está vacía.")

        nodo = self.traverse_to_index(index)

        if self.length == 1:
            self.head = None
            self.tail = None
        elif nodo == self.head:
            self.head = nodo.next
            self.head.prev = None
        elif nodo == self.tail:
            self.tail = nodo.prev
            self.tail.next = None
        else:
            nodo.prev.next = nodo.next
            nodo.next.prev = nodo.prev

        self.length -= 1
        return nodo.producto

    def recorrido_adelante(self):
        actual = self.head
        resultado = []
        while actual:
            resultado.append(actual)
            actual = actual.next
        return resultado

    def recorrido_atras(self):
        actual = self.tail
        resultado = []
        while actual:
            resultado.append(actual)
            actual = actual.prev
        return resultado

    def stock_total(self):
        total = 0
        actual = self.head
        while actual:
            total += actual.producto["stock"]
            actual = actual.next
        return total
