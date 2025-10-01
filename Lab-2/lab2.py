from collections import defaultdict, deque

class KnowledgeBase:
    def __init__(self):
        self.graph = defaultdict(list)

    def add_relation(self, subj, relation, obj):
        self.graph[subj].append((obj, relation))
        if relation == "part_of":
            self.graph[obj].append((subj, "has_part"))

    def find_connection(self, start, end):
        if start not in self.graph or end not in self.graph:
            return None

        visited = set()
        queue = deque([(start, [])])

        while queue:
            node, path = queue.popleft()
            if node == end:
                return path

            if node in visited:
                continue
            visited.add(node)

            for neighbor, relation in self.graph[node]:
                if neighbor not in visited:
                    queue.append((neighbor, path + [(node, relation, neighbor)]))
        return None

    def print_tree(self, root, relation="is_a", level=1, prefix=""):
        children = [subj for subj, rels in self.graph.items()
                    for obj, rel in rels if obj == root and rel == relation]

        for i, child in enumerate(children):
            branch = "└── " if i == len(children) - 1 else "├── "
            print(prefix + branch + f"{child} (рівень {level + 1})")
            new_prefix = prefix + ("    " if i == len(children) - 1 else "│   ")
            self.print_tree(child, relation, level + 1, new_prefix)


kb = KnowledgeBase()

kb.add_relation("Ссавець", "is_a", "Тварина")
kb.add_relation("Птах", "is_a", "Тварина")
kb.add_relation("Риба", "is_a", "Тварина")

kb.add_relation("Хижак", "is_a", "Ссавець")
kb.add_relation("Травоїдний", "is_a", "Ссавець")
kb.add_relation("Домашня_тварина", "is_a", "Ссавець")

kb.add_relation("Вовк", "is_a", "Хижак")
kb.add_relation("Лисиця", "is_a", "Хижак")
kb.add_relation("Олень", "is_a", "Травоїдний")
kb.add_relation("Кінь", "is_a", "Травоїдний")
kb.add_relation("Собака", "is_a", "Домашня_тварина")
kb.add_relation("Кіт", "is_a", "Домашня_тварина")

kb.add_relation("Хижий_птах", "is_a", "Птах")
kb.add_relation("Домашній_птах", "is_a", "Птах")
kb.add_relation("Перелітний_птах", "is_a", "Птах")

kb.add_relation("Орел", "is_a", "Хижий_птах")
kb.add_relation("Сокіл", "is_a", "Хижий_птах")
kb.add_relation("Курка", "is_a", "Домашній_птах")
kb.add_relation("Гуска", "is_a", "Домашній_птах")
kb.add_relation("Лелека", "is_a", "Перелітний_птах")
kb.add_relation("Ластівка", "is_a", "Перелітний_птах")

kb.add_relation("Прісноводна_риба", "is_a", "Риба")
kb.add_relation("Морська_риба", "is_a", "Риба")

kb.add_relation("Короп", "is_a", "Прісноводна_риба")
kb.add_relation("Окунь", "is_a", "Прісноводна_риба")
kb.add_relation("Тунець", "is_a", "Морська_риба")
kb.add_relation("Скумбрія", "is_a", "Морська_риба")

kb.add_relation("Голова", "part_of", "Тварина")
kb.add_relation("Тулуб", "part_of", "Тварина")
kb.add_relation("Хвіст", "part_of", "Тварина")

kb.add_relation("Нога", "part_of", "Ссавець")
kb.add_relation("Шерсть", "part_of", "Ссавець")

kb.add_relation("Крило", "part_of", "Птах")
kb.add_relation("Пір’я", "part_of", "Птах")

kb.add_relation("Плавець", "part_of", "Риба")
kb.add_relation("Луска", "part_of", "Риба")

kb.add_relation("Вовк", "lives_in", "Ліс")
kb.add_relation("Лисиця", "lives_in", "Ліс")
kb.add_relation("Олень", "lives_in", "Ліс")
kb.add_relation("Орел", "lives_in", "Ліс")
kb.add_relation("Лелека", "lives_in", "Ліс")

kb.add_relation("Собака", "lives_in", "Село")
kb.add_relation("Кіт", "lives_in", "Село")
kb.add_relation("Курка", "lives_in", "Село")
kb.add_relation("Гуска", "lives_in", "Село")
kb.add_relation("Кінь", "lives_in", "Село")

kb.add_relation("Тунець", "lives_in", "Море")
kb.add_relation("Скумбрія", "lives_in", "Море")
kb.add_relation("Сокіл", "lives_in", "Море")

kb.add_relation("Короп", "lives_in", "Річка/Озеро")
kb.add_relation("Окунь", "lives_in", "Річка/Озеро")
kb.add_relation("Лелека", "lives_in", "Річка/Озеро")
kb.add_relation("Ластівка", "lives_in", "Річка/Озеро")


def query(kb, concept1, concept2):
    path = kb.find_connection(concept1, concept2)
    if path is None:
        path = kb.find_connection(concept2, concept1)
    if path:
        print(f"Так, '{concept1}' пов'язаний з '{concept2}':")
        for step in path:
            subj, rel, obj = step
            print(f"  {subj} -[{rel}]-> {obj}")
    else:
        print(f"Ні, '{concept1}' не пов'язаний з '{concept2}'")


query(kb, "Собака", "Шерсть")
print()
query(kb, "Орел", "Луска")
print()
query(kb, "Короп", "Лелека")
print()
query(kb, "Вовк", "Ліс")
