import tkinter as tk
import random
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import chisquare
import scipy.stats as stats


def congruential_generator(seed, a, c, m, n):
    numbers = []
    x = seed
    for _ in range(n):
        x = (a * x + c) % m
        numbers.append(x / m)
    return numbers


def chi_squared_test(numbers, num_intervals):
    observed_freq, _ = np.histogram(
        numbers, bins=num_intervals, range=(0, 0.2))
    expected_freq = len(numbers) / num_intervals
    chi2, p = stats.chisquare(observed_freq, f_exp=expected_freq)
    return chi2, p


seed = 12345
a = 1103515245
c = 12345
m = 2**32
n = 1000
num_intervals = 10
k = 10  # Número de intervalos para el test de Chi-cuadrado

generated_numbers = congruential_generator(seed, a, c, m, n)
adjusted_numbers = [number * 0.2 for number in generated_numbers]
adjusted_numbers2 = [number * 0.8 for number in generated_numbers]

chi2_stat, p_value = chi_squared_test(adjusted_numbers, num_intervals)

print("Chi-squared test results:")
print(f"Chi2 statistic: {chi2_stat}")
print(f"P-value: {p_value}")


class MonteCarloSimulator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Simulador Monte Carlo")

        # Variables de entrada
        self.num_simulaciones = tk.StringVar()

        # Crear los elementos de la interfaz gráfica
        self.create_input_widgets()
        self.create_output_widgets()
        self.create_button()

    def create_input_widgets(self):
        input_frame = tk.Frame(self)
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Número de simulaciones:").grid(
            row=0, column=0, sticky=tk.W)
        entry_num_simulaciones = tk.Entry(
            input_frame, textvariable=self.num_simulaciones)
        entry_num_simulaciones.grid(row=0, column=1)

    def create_output_widgets(self):
        output_frame = tk.Frame(self)
        output_frame.pack(pady=10)

        tk.Label(output_frame, text="Resultados:").grid(
            row=0, column=0, sticky=tk.W)
        self.output_text = tk.Text(output_frame, height=10, width=50)
        self.output_text.grid(row=1, column=0)

    def create_button(self):
        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)

        run_button = tk.Button(
            button_frame, text="Ejecutar", command=self.run_simulation)
        run_button.pack()

    def run_simulation(self):
        num_simulaciones = int(self.num_simulaciones.get())

        # Tabla de eventos con probabilidad determinada
        eventos = [
            {"evento": "Evento A", "probabilidad": 0.8},
            {"evento": "Evento B", "probabilidad": 0.2}
        ]

        resultados = {}

        for evento in eventos:
            resultados[evento["evento"]] = 0

        for _ in range(num_simulaciones):
            numero_aleatorio = random.random()
            print(numero_aleatorio)
            acumulador = 0

            for evento in eventos:
                acumulador += evento["probabilidad"]

                if numero_aleatorio <= acumulador:
                    resultados[evento["evento"]] += 1
                    break

        self.output_text.delete("1.0", tk.END)

        for evento, cantidad in resultados.items():
            probabilidad = cantidad / num_simulaciones
            self.output_text.insert(
                tk.END, f"{evento}: {cantidad} ({probabilidad:.4f})\n")


class QueueSimulator:
    def __init__(self, arrival_rates, service_rates):
        self.arrival_rates = arrival_rates
        self.service_rates = service_rates
        self.queue_1 = []
        self.queue_2 = []
        self.current_time = 0

    def simulate(self):
        # objeto_clase1 = pseudos()  # Crear una instancia de la Clase1
        # objeto_clase1.congruencial_multiplicativo()  # Llamar al método1 de la Clase1
        arrival_time = self.generate_random_interarrival_time()
        service_time = self.generate_random_service_time()

        if len(self.queue_1) <= len(self.queue_2):
            self.queue_1.append(
                (self.current_time, self.current_time + service_time))
        else:
            self.queue_2.append(
                (self.current_time, self.current_time + service_time))

        self.current_time += arrival_time

        # Simulate for a fixed time period (10000 units)
        if self.current_time > 10000:
            return

        while len(self.queue_1) > 0 and self.queue_1[0][1] <= self.current_time:
            self.queue_1.pop(0)

        while len(self.queue_2) > 0 and self.queue_2[0][1] <= self.current_time:
            self.queue_2.pop(0)

        self.update_gui()

        self.root.after(1000, self.simulate)

    def generate_random_interarrival_time(self):
        arrival_rate = random.choice(self.arrival_rates)
        return random.expovariate(arrival_rate)

    def generate_random_service_time(self):
        service_rate = random.choice(self.service_rates)
        return random.expovariate(service_rate)

    def update_gui(self):
        self.canvas.delete('all')
        queue_1_length = len(self.queue_1)
        queue_2_length = len(self.queue_2)

        self.canvas.create_text(100, 50, text=f"Fila 1 piso: {queue_1_length}")
        self.canvas.create_text(
            100, 100, text=f"Fila 2 piso: {queue_2_length}")

        for i in range(queue_1_length):
            self.canvas.create_rectangle(
                150 + i * 30, 40, 170 + i * 30, 60, fill='red')

        for i in range(queue_2_length):
            self.canvas.create_rectangle(
                150 + i * 30, 90, 170 + i * 30, 110, fill='blue')

    def start_simulation(self):
        self.root = tk.Tk()
        self.root.title("Simulador Restaurante")

        self.canvas = tk.Canvas(self.root, width=500, height=200)
        self.canvas.pack()

        self.root.after(100, self.simulate)
        self.root.mainloop()


# Uso:
seed = 1234
a = 48271
m = 2**31 - 1
n = 3

# Llamar al método1 de la Clase1
random_numbers = adjusted_numbers
arrival_rates = adjusted_numbers2  # Tasas de llegada
service_rates = random_numbers   # Tasas de servicio


if __name__ == "__main__":
    simulator = MonteCarloSimulator()
    simulator.mainloop()
    simulator = QueueSimulator(arrival_rates, service_rates)
    simulator.start_simulation()

plt.hist(generated_numbers, bins=k)
plt.xlabel('Valor')
plt.ylabel('Frecuencia')
plt.title('Histograma de los números pseudoaleatorios generados')
plt.show()
