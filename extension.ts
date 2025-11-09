interface CodeFragment {
  author: string;
  code: string;
  time: string;
}

class CollabApp {
  private fragments: CodeFragment[] = [];
  private readonly storageFile: string = "collab.json";

  constructor() {
    this.init();
    this.bindEvents();
  }

  private async init(): Promise<void> {
    await this.loadFragments();
    this.render();
    setInterval(() => this.loadFragments(), 5000);
  }

  private async loadFragments(): Promise<void> {
    try {
      const res: Response = await fetch(this.storageFile);
      if (res.ok) {
        this.fragments = await res.json() as CodeFragment[];
        this.render();
      }
    } catch (e) {
      console.error("Erreur chargement collab.json", e);
    }
  }

  private bindEvents(): void {
    const sendBtn = document.getElementById("send") as HTMLButtonElement;
    const codeInput = document.getElementById("code") as HTMLTextAreaElement;

    sendBtn?.addEventListener("click", () => {
      const code = codeInput.value.trim();
      if (code) {
        this.sendFragment(code);
        codeInput.value = "";
      }
    });

    codeInput?.addEventListener("keydown", (e: KeyboardEvent) => {
      if (e.ctrlKey && e.key === "Enter") sendBtn?.click();
    });
  }

  private async sendFragment(code: string): Promise<void> {
    const author = this.getAuthor();
    const time = new Date().toLocaleTimeString("fr-FR");
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
    } catch (e) {
      console.error("Erreur sauvegarde", e);
    }
  }

  private render(): void {
    const container = document.getElementById("fragments");
    if (!container) return;
    container.innerHTML = this.fragments
      .map(
        (f) => `
      <div class="fragment">
        <div class="header">
          <strong>${f.author}</strong> <span class="time">${f.time}</span>
        </div>
        <pre><code>${this.escapeHtml(f.code)}</code></pre>
      </div>`
      )
      .join("");
  }

  private getAuthor(): string {
    return prompt("Ton nom (LordLennyx ou Delbrique) :") || "Anonyme";
  }

  private escapeHtml(text: string): string {
    const div = document.createElement("div");
    div.textContent = text;
    return div.innerHTML;
  }
}

new CollabApp();
