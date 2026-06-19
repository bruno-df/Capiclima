# Session: Refatoração — Página Apoie e Parceiros

## Contexto do Projeto

- **Projeto:** Capiclima (Django CMS para ONG)
- **Stack:** Django Admin, modelos Python, templates HTML/CSS
- **Commits:** português, atômico por tarefa (uma tarefa = um commit)

---

## Regras Globais

- Siga sempre a sequência **RESEARCH → PLAN → IMPLEMENT**
- Após a fase PLAN, **aguarde aprovação** antes de implementar
- Um commit por tarefa, mensagem em português
- Em caso de dúvida entre tarefas, pergunte antes de agir
- Não modifique arquivos fora do escopo de cada tarefa
- Não misture alterações entre as tarefas abaixo

---

## Tarefa 1 — Centralizar gestão da página Apoie no Django Admin

### RESEARCH

Antes de qualquer alteração, mapeie:

1. O model atual da página "Apoie" — nome, campos existentes, arquivo
2. O model "Configuração do site" — localize o campo `doacoes` (ou equivalente) e seu tipo
3. O arquivo `admin.py` onde ambos os models estão registrados
4. Qualquer view ou template que leia o campo `doacoes` de "Configuração do site"

Documente: caminho dos arquivos, nomes exatos dos models e campos.
**NÃO edite nenhum arquivo nesta fase.**

---

### PLAN

Com base no mapeamento, escreva o plano de implementação com os passos exatos:

- Qual campo será adicionado ao model da página Apoie
- Como o campo `doacoes` será removido de "Configuração do site"
- Quais views/templates precisam ser atualizados para ler do novo model
- Qual migration será gerada (descreva o que ela fará)

**Aguarde aprovação do plano antes de implementar.**

---

### IMPLEMENT

Execute o plano aprovado:

1. **Model Apoie** — adicione campo `pix` (CharField ou TextField, conforme tipo original) e mova o campo `doacoes` de "Configuração do site" para este model
2. **Model Configuração do site** — remova o campo `doacoes`
3. **Django Admin** — garanta que a seção "Apoie" no admin exiba apenas campos relacionados à página Apoie; o campo `pix` deve ser editável
4. **Views/templates** — atualize todas as referências ao campo `doacoes` para ler do novo model da página Apoie
5. **Migrations** — gere e aplique as migrations necessárias

**Commit:** `refactor(admin): centraliza campos da página Apoie no model ApoiePage`

---

### Constraints

- NÃO altere campos não relacionados à página Apoie em nenhum model
- NÃO apague dados existentes — use migration de transferência de dados se necessário
- NÃO registre o model em seção diferente de "Apoie" no admin

### Critérios de Aceite

- [ ] Campo `doacoes` não existe mais em "Configuração do site"
- [ ] Todos os campos da página Apoie estão agrupados na seção "Apoie" do admin
- [ ] Campo `pix` é editável no admin
- [ ] Site renderiza corretamente as informações de doação após a mudança
- [ ] Migrations aplicam sem erro

---

## Tarefa 2 — Reduzir bloco de parceiros e remover efeito hover

### RESEARCH

Antes de qualquer alteração, mapeie:

1. O template HTML que renderiza a seção "Parceiros"
2. O arquivo CSS (ou bloco `<style>`) que define o tamanho do bloco/card de cada parceiro
3. A classe ou seletor CSS responsável pelo efeito de hover (ex.: `transform`, `scale`, `box-shadow`, `transition`, ou qualquer propriedade que cause o "pop-up")
4. Se os ícones dos parceiros vêm de um model Django ou são estáticos

Documente: caminhos dos arquivos, nomes de classes CSS, propriedades exatas do hover.
**NÃO edite nenhum arquivo nesta fase.**

---

### PLAN

Com base no mapeamento, descreva:

- Quais propriedades CSS serão alteradas para reduzir o bloco
- Qual tamanho alvo para o ícone (sugestão: máx. 60–80px de altura)
- Quais propriedades de hover serão removidas ou neutralizadas
- Se haverá alteração no template HTML ou apenas no CSS

**Aguarde aprovação do plano antes de implementar.**

---

### IMPLEMENT

Execute o plano aprovado:

1. **Tamanho do bloco** — reduza o container/card de cada parceiro para que o espaço ocupado seja proporcional ao ícone; remova padding/margin excessivos que inflam o bloco
2. **Tamanho do ícone** — limite a imagem do parceiro (ex.: `max-height: 60px`, `width: auto`) para que seja exibida como ícone compacto
3. **Remover efeito hover** — elimine completamente quaisquer propriedades CSS de transformação, escala, sombra ou transição aplicadas ao passar o mouse; o parceiro deve ser exibido como imagem estática simples, sem nenhuma interação visual ao hover

**Commit:** `style(parceiros): reduz bloco para ícone compacto e remove efeito hover`

---

### Constraints

- NÃO altere o layout de outras seções da página
- NÃO remova os links dos parceiros (se existirem), apenas o efeito visual
- NÃO altere o model Django nem lógica de backend relacionada a parceiros
- A imagem deve continuar carregando normalmente; apenas o estilo visual muda

### Critérios de Aceite

- [ ] Bloco de cada parceiro é visivelmente compacto (proporcional ao ícone)
- [ ] Ícone do parceiro tem tamanho pequeno (aprox. 60–80px de altura)
- [ ] Nenhum efeito visual ocorre ao passar o mouse sobre o parceiro
- [ ] Layout das demais seções da página não foi afetado
