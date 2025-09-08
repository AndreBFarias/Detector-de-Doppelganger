<div align="center">

[![opensource](https://badges.frapsoft.com/os/v1/open-source.png?v=103)](#)
[![licence](https://badges.frapsoft.com/os/gpl/gpl.png?v=103)](https://www.gnu.org/licenses/gpl-3.0)
[![compare](https://img.shields.io/github/commits-since/AndreBFarias/DetectorDeDoppelganger/latest/master)](https://github.com/AndreBFarias/DetectorDeDoppelganger/compare)
[![Python](https://img.shields.io/badge/python-3.x-green.svg)](https://www.python.org/)
[![Estrelas](https://img.shields.io/github/stars/AndreBFarias/DetectorDeDoppelganger.svg?style=social)](https://github.com/AndreBFarias/DetectorDeDoppelganger/stargazers)
[![Contribuições](https://img.shields.io/badge/contribuições-bem--vindas-brightgreen.svg)](https://github.com/AndreBFarias/DetectorDeDoppelganger/issues)
</div>

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
