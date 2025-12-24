import random
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import copy

# ==========================================
# 1. Налаштування симуляції
# ==========================================
ROOF_WIDTH = 50
ROOF_HEIGHT = 30
NUM_PANELS = 40
PANEL_SIZE = 3  # квадратна панель 3x3
PENALTY_OVERLAP = 1000
PENALTY_SHADOW = 500

# Параметри ГА
POP_SIZE = 100
GENERATIONS = 150
MUTATION_RATE = 0.2
CROSSOVER_RATE = 0.7
ELITE_SIZE = 5

# Штучні джерела тіні (наприклад, димарі на даху)
SHADOWS = [
    [10, 10, 5, 5],  # x, y, width, height
    [35, 20, 4, 6]
]


class SolarPanelsGA:
    def __init__(self):
        # Можливі місця розташування панелей
        self.positions = []
        for _ in range(NUM_PANELS):
            x = random.uniform(0, ROOF_WIDTH - PANEL_SIZE)
            y = random.uniform(0, ROOF_HEIGHT - PANEL_SIZE)
            self.positions.append((x, y))

    def create_individual(self):
        # Кожна панель або ставиться (1) або ні (0)
        return [random.choice([0, 1]) for _ in range(NUM_PANELS)]

    def calculate_metrics(self, individual):
        total_energy = 0
        penalty = 0
        placed = []

        for i, place in enumerate(individual):
            if place == 0:
                continue
            x, y = self.positions[i]
            panel_rect = [x, y, PANEL_SIZE, PANEL_SIZE]

            # Перевірка перекриття з іншими панелями
            overlap = False
            for px, py, pw, ph in placed:
                if (x < px + pw and x + PANEL_SIZE > px and
                        y < py + ph and y + PANEL_SIZE > py):
                    overlap = True
                    break
            if overlap:
                penalty += PENALTY_OVERLAP

            # Перевірка тіні
            in_shadow = False
            for sx, sy, sw, sh in SHADOWS:
                if (x < sx + sw and x + PANEL_SIZE > sx and
                        y < sy + sh and y + PANEL_SIZE > sy):
                    in_shadow = True
                    break
            if in_shadow:
                penalty += PENALTY_SHADOW

            energy = 10  # базова енергія панелі
            if not in_shadow:
                energy += 5  # бонус за сонячне розташування

            total_energy += energy
            placed.append(panel_rect)

        fitness = total_energy - penalty
        return fitness, total_energy, penalty

    def calculate_fitness(self, individual):
        fit, _, _ = self.calculate_metrics(individual)
        return fit

    def crossover(self, parent1, parent2):
        if random.random() > CROSSOVER_RATE:
            return parent1[:], parent2[:]
        point = random.randint(1, len(parent1) - 1)
        return parent1[:point] + parent2[point:], parent2[:point] + parent1[point:]

    def mutate(self, individual):
        for i in range(len(individual)):
            if random.random() < MUTATION_RATE:
                individual[i] = 1 - individual[i]  # перемикання 0↔1
        return individual

    def tournament_selection(self, population, fitnesses, k=3):
        selected = []
        for _ in range(POP_SIZE):
            candidates_idx = random.sample(range(POP_SIZE), k)
            winner_idx = max(candidates_idx, key=lambda i: fitnesses[i])
            selected.append(population[winner_idx])
        return selected

    def run(self):
        population = [self.create_individual() for _ in range(POP_SIZE)]
        best_solution = None
        best_fitness = -float('inf')
        history_energy = []
        history_penalty = []

        for gen in range(GENERATIONS):
            fitnesses = [self.calculate_fitness(ind) for ind in population]
            gen_max = max(fitnesses)
            best_idx = fitnesses.index(gen_max)
            fit, energy, pen = self.calculate_metrics(population[best_idx])

            history_energy.append(energy)
            history_penalty.append(pen)

            if fit > best_fitness:
                best_fitness = fit
                best_solution = copy.deepcopy(population[best_idx])

            selected = self.tournament_selection(population, fitnesses)
            next_pop = []
            # Еліта
            zipped = sorted(zip(fitnesses, population), reverse=True)
            next_pop.extend([copy.deepcopy(ind) for fit, ind in zipped[:ELITE_SIZE]])

            while len(next_pop) < POP_SIZE:
                p1 = random.choice(selected)
                p2 = random.choice(selected)
                c1, c2 = self.crossover(p1, p2)
                next_pop.append(self.mutate(c1))
                if len(next_pop) < POP_SIZE:
                    next_pop.append(self.mutate(c2))

            population = next_pop

        self.visualize(best_solution, history_energy, history_penalty)

    def visualize(self, solution, history_energy, history_penalty):
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 7))

        # === 1. Дах ===
        ax1.set_xlim(0, ROOF_WIDTH)
        ax1.set_ylim(0, ROOF_HEIGHT)
        ax1.set_title("Оптимальне розташування панелей")
        ax1.set_aspect('equal')
        ax1.grid(True, linestyle=':', alpha=0.5)

        # Тіні
        for s in SHADOWS:
            rect = patches.Rectangle((s[0], s[1]), s[2], s[3], color='gray', alpha=0.5, label='Тінь')
            ax1.add_patch(rect)

        # Панелі
        for i, val in enumerate(solution):
            if val == 0: continue
            x, y = self.positions[i]
            color = 'yellow'
            # Перевірка тіні
            in_shadow = False
            for sx, sy, sw, sh in SHADOWS:
                if (x < sx + sw and x + PANEL_SIZE > sx and
                        y < sy + sh and y + PANEL_SIZE > sy):
                    in_shadow = True
                    break
            if in_shadow:
                color = 'orange'
            rect = patches.Rectangle((x, y), PANEL_SIZE, PANEL_SIZE, color=color, edgecolor='black')
            ax1.add_patch(rect)

        # === 2. Графіки ===
        ax2.plot(history_energy, label='Енергія', color='green')
        ax2.plot(history_penalty, label='Штраф', color='red', linestyle='--')
        ax2.set_title("Динаміка енергії та штрафів")
        ax2.set_xlabel("Покоління")
        ax2.set_ylabel("Величина")
        ax2.legend()
        ax2.grid(True, linestyle=':', alpha=0.5)

        plt.show()


if __name__ == "__main__":
    ga = SolarPanelsGA()
    ga.run()
