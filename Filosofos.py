import threading
import random
import time

class Filosofo(threading.Thread):
    def __init__(self, nombre, tenedor_izquierdo, tenedor_derecho):
        # Inicializa la clase Thread
        threading.Thread.__init__(self)
        self.nombre = nombre
        self.tenedor_izquierdo = tenedor_izquierdo
        self.tenedor_derecho = tenedor_derecho

    def run(self):
        # Método principal que se ejecuta cuando se inicia el hilo
        while True:
            self.pensar()
            self.comer()

    def pensar(self):
        # Simula el tiempo que el filósofo pasa pensando
        print(f"{self.nombre} está pensando.")
        time.sleep(random.randint(1, 5))  # Espera un tiempo aleatorio entre 1 y 5 segundos

    def comer(self):
        print(f"{self.nombre} tiene hambre y quiere comer.")
        tenedor1, tenedor2 = self.tenedor_izquierdo, self.tenedor_derecho

        while True:
            # Intenta adquirir el primer tenedor
            tenedor1.acquire()
            # Intenta adquirir el segundo tenedor sin bloquear
            locked = tenedor2.acquire(False)
            if locked:
                break  # Si se adquieren ambos tenedores, sale del bucle
            tenedor1.release()  # Si no se pudo adquirir el segundo, suelta el primero
            print(f"{self.nombre} no pudo adquirir ambos tenedores, intentando de nuevo.")
            # Cambia el orden de los tenedores para evitar interbloqueo
            tenedor1, tenedor2 = tenedor2, tenedor1

        print(f"{self.nombre} comienza a comer.")
        time.sleep(random.randint(1, 5))  # Simula el tiempo que tarda en comer
        print(f"{self.nombre} termina de comer y suelta los tenedores.")

        # Suelta los tenedores
        tenedor2.release()
        tenedor1.release()

if __name__ == "__main__":
    num_filosofos = 5
    # Crea una lista de candados (locks) que representan los tenedores
    tenedores = [threading.Lock() for _ in range(num_filosofos)]
    nombres = ["Platón", "Aristóteles", "Sócrates", "Kant", "Nietzsche"]

    # Crea una lista de filósofos
    filosofos = [Filosofo(nombres[i], tenedores[i], tenedores[(i + 1) % num_filosofos]) 
                 for i in range(num_filosofos)]

    # Inicia todos los hilos de los filósofos
    for f in filosofos:
        f.start()

    # Espera a que todos los hilos terminen (lo cual nunca sucederá en este caso)
    for f in filosofos:
        f.join()
