# Detector de Doppelganger: Detector e Humanizador de Textos IA

Ritual open source em Python pra detectar e humanizar textos de IA. Local, sem dependências externas além de Hugging Face.

## Estrutura src/: 

- **detector.py:** Módulo pra detectar IA (1: importa torch e transformers; 2: define device; 3: carrega pipeline; 4: função detectar_ia).
- **humanizador.py:** Módulo pra parafrasear (1: importa transformers; 2: carrega tokenizer e model; 3: função humanizar_texto).
- **main.py:** Orquestrador (1: importa torch e módulos; 2: define device; 3: carrega tudo; 4: pede input; 5: detecta e humaniza).

### Passos pra utilização:
Clone: 
> - git clone https://github.com/AndreBFarias/Detector-de-Doppelganger.git
> - cd Detector-de-Doppelganger

Crie venv:
> - python -m venv venv && source venv/bin/activate

Instale:
> - pip install -r requirements.txt

Rode:
> - python src/main.py

Insira texto = detecção + humanização se doppelganger de IA.

### Limitações:
- Detecção falha em IAs avançadas;

### Referências:
Hugging Face: Open source, sem correntes governamentais.

>"A liberdade é a mãe da ordem." – Pierre-Joseph Proudhon, nos lembrando que código open source ordena o caos sem tiranos.

### Uso
`python src/main.py`
 
### Licença GLP 
> Livre para modificar e usar em rituais arcanos desde que tudo permaneça livre.
