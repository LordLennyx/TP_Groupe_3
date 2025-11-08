interface CodeFragment {
  author: string;
  code: string;
  time: string;
}

class CollabApp {
  private fragments: CodeFragment[] = [];
  private readonly storageFile: string = "collab.json";

  constructor() {
    void this.init();
    this.bindEvents();
  }

  private async init(): Promise<void> {
    try {
      await this.loadFragments();
      this.render();
      setInterval(() => void this.loadFragments(), 5000);
    } catch {
      this.showNotification("Erreur d'initialisation de l'application.");
    }
  }

  private async loadFragments(): Promise<void> {
    try {
      const res: Response = await fetch(this.storageFile);
      if (res.ok) {
        const data: unknown = await res.json();
        if (Array.isArray(data)) {
          this.fragments = data as CodeFragment[];
          this.render();
        } else {
          this.showNotification("Format de données invalide détecté.");
        }
      } else {
        this.showNotification("Erreur HTTP lors du chargement des données.");
      }
    } catch {
      this.showNotification("Erreur réseau pendant le chargement.");
    }
  }

  private bindEvents(): void {
    const sendBtn = document.getElementById("send") as HTMLButtonElement | null;
    const codeInput = document.getElementById("code") as HTMLTextAreaElement | null;

    if (!sendBtn || !codeInput) {
      this.showNotification("Éléments d'interface introuvables.");
      return;
    }

    sendBtn.addEventListener("click", () => {
      const code = codeInput.value.trim();
      if (code.length > 0) {
        void this.sendFragment(code);
        codeInput.value = "";
      }
    });

    codeInput.addEventListener("keydown", (e: KeyboardEvent) => {
      if (e.ctrlKey && e.key === "Enter") sendBtn.click();
    });
  }

  private async sendFragment(code: string): Promise<void> {
    const author: string = this.getAuthor();
    const time: string = new Date().toLocaleTimeString("fr-FR");
    this.fragments.push({ author, code, time });
    await this.saveFragments();
    this.render();
  }

  private async saveFragments(): Promise<void> {
    try {
      await fetch(this.storageFile, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(this.fragments, null, 2),
      });
    } catch {
      this.showNotification("Erreur de sauvegarde des fragments.");
    }
  }

  private render(): void {
    const container = document.getElementById("fragments") as HTMLElement | null;
    if (!container) return;
    container.innerHTML = this.fragments
      .map(
        (f) => `
        <div class="fragment">
          <div class="header">
            <strong>${this.escapeHtml(f.author)}</strong> 
            <span class="time">${this.escapeHtml(f.time)}</span>
          </div>
          <pre><code>${this.escapeHtml(f.code)}</code></pre>
        </div>`
      )
      .join("");
  }

  private getAuthor(): string {
    const name = prompt("Ton nom (LordLennyx ou Delbrique) :");
    return name && name.trim() !== "" ? name : "Anonyme";
  }

  private escapeHtml(text: string): string {
    const div: HTMLDivElement = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
  }

  private showNotification(message: string): void {
    const note: HTMLDivElement = document.createElement("div");
    note.className = "notif";
    note.textContent = message;
    document.body.appendChild(note);
    setTimeout(() => note.remove(), 4000);
  }
}

new CollabApp();
