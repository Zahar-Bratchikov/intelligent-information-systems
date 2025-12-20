import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from models import (
    relative_majority,
    condorcet_winner,
    copeland_score,
    simpson_score,
    borda_count
)


class CollectiveDecisionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Экспертная система")
        self.root.geometry("800x700")

        # Данные
        self.alternatives: list[str] = []
        self.voters: list[str] = []
        self.profile: list[list[str]] = []

        self.create_widgets()

    def create_widgets(self):
        frame_top = ttk.Frame(self.root, padding="10")
        frame_top.pack(fill=tk.X)

        ttk.Button(frame_top, text="Добавить вариант голосования", command=self.add_alternative).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_top, text="Добавить избирателя", command=self.add_voter).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_top, text="Провести голосование", command=self.collect_votes).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_top, text="Показать результаты", command=self.show_results).pack(side=tk.LEFT, padx=5)

        ttk.Label(self.root, text="Варианты голосования:").pack(anchor=tk.W, padx=10, pady=(10, 0))
        self.alternatives_listbox = tk.Listbox(self.root, height=6)
        self.alternatives_listbox.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(self.root, text="Избиратели:").pack(anchor=tk.W, padx=10)
        self.voters_listbox = tk.Listbox(self.root, height=6)
        self.voters_listbox.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(self.root, text="Профиль голосования:").pack(anchor=tk.W, padx=10)
        self.profile_text = tk.Text(self.root, height=10)
        self.profile_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

    def add_alternative(self):
        alt = simpledialog.askstring("Новый вариант", "Введите вариант для голосования:")
        if alt and alt.strip():
            alt = alt.strip()
            if alt not in self.alternatives:
                self.alternatives.append(alt)
                self.alternatives_listbox.insert(tk.END, alt)
            else:
                messagebox.showwarning("Повтор", "Такой вариант уже существует.")

    def add_voter(self):
        name = simpledialog.askstring("Новый избиратель", "Введите имя избирателя:")
        if name and name.strip():
            name = name.strip()
            if name not in self.voters:
                self.voters.append(name)
                self.voters_listbox.insert(tk.END, name)
            else:
                messagebox.showwarning("Повтор", "Такой избиратель уже существует.")

    def collect_votes(self):
        if not self.alternatives:
            messagebox.showerror("Ошибка", "Сначала добавьте варианты голосования.")
            return
        if not self.voters:
            messagebox.showerror("Ошибка", "Сначала добавьте избирателей.")
            return

        self.profile = []
        for voter in self.voters:
            ranking = self.ask_ranking(voter, self.alternatives.copy())
            if ranking is None:
                return
            self.profile.append(ranking)

        self.update_profile_display()

    def ask_ranking(self, voter_name: str, alts: list[str]) -> list[str] | None:
        """Показывает диалог для ранжирования альтернатив."""
        ranking_window = tk.Toplevel(self.root)
        ranking_window.title(f"Голосование: {voter_name}")
        ranking_window.geometry("400x300")
        ranking_window.transient(self.root)
        ranking_window.grab_set()

        ttk.Label(ranking_window, text=f"Ранжируйте варианты для {voter_name}:").pack(pady=10)

        order_vars = []
        for _ in alts:
            var = tk.StringVar()
            order_vars.append(var)
            cb = ttk.Combobox(ranking_window, textvariable=var, values=alts, state="readonly")
            cb.pack(pady=2)

        # Установим начальные уникальные значения
        for i, var in enumerate(order_vars):
            var.set(alts[i % len(alts)])

        result = []

        def on_ok():
            selected = [var.get() for var in order_vars]
            if len(selected) != len(set(selected)):
                messagebox.showerror("Ошибка", "Все значения должны быть уникальны!")
                return
            if not all(s in alts for s in selected):
                messagebox.showerror("Ошибка", "Недопустимое значение!")
                return
            result.append(selected)
            ranking_window.destroy()

        ttk.Button(ranking_window, text="OK", command=on_ok).pack(pady=10)
        ranking_window.wait_window()
        return result[0] if result else None

    def update_profile_display(self):
        self.profile_text.delete(1.0, tk.END)
        for i, ranking in enumerate(self.profile):
            voter = self.voters[i]
            self.profile_text.insert(tk.END, f"{voter}: {ranking}\n")

    def show_results(self):
        if not self.profile or not self.alternatives:
            messagebox.showerror("Ошибка", "Нет данных для анализа.")
            return

        maj_winner, maj_counts = relative_majority(self.profile, self.alternatives)
        cond_winner = condorcet_winner(self.profile, self.alternatives)
        cop_scores = copeland_score(self.profile, self.alternatives)
        cop_winner = max(cop_scores, key=cop_scores.get)
        sim_scores = simpson_score(self.profile, self.alternatives)
        sim_winner = max(sim_scores, key=sim_scores.get)
        bor_scores = borda_count(self.profile, self.alternatives)
        bor_winner = max(bor_scores, key=bor_scores.get)

        report = f"""РЕЗУЛЬТАТЫ ГОЛОСОВАНИЯ

1. Относительное большинство:
   Победитель: {maj_winner}
   Голоса за 1-е место: {maj_counts}

2. Победитель по Кондорсе:
   {'Найден: ' + cond_winner if cond_winner else 'Отсутствует (парадокс Кондорсе)'}

3. Правило Копленда:
   Очки: {cop_scores}
   Победитель: {cop_winner}

4. Правило Симпсона:
   Мин. поддержка: {sim_scores}
   Победитель: {sim_winner}

5. Модель Борда:
   Очки: {bor_scores}
   Победитель: {bor_winner}
"""

        result_window = tk.Toplevel(self.root)
        result_window.title("Результаты")
        result_window.geometry("600x500")
        text = tk.Text(result_window, wrap=tk.WORD)
        text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        text.insert(tk.END, report)
        text.config(state=tk.DISABLED)


if __name__ == "__main__":
    root = tk.Tk()
    app = CollectiveDecisionApp(root)
    root.mainloop()