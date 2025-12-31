from __future__ import annotations

import json
import logging
import os
import random
import sys
import time
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

import config

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

DATASET_DIR = config.DATA_DIR / "fine_tuning"
os.makedirs(DATASET_DIR, exist_ok=True)

HUMAN_SAMPLES_PT = [
    "Meu celular caiu e a tela rachou. Vou ter que trocar.",
    "O jogo foi emocionante. Meu time ganhou no final.",
    "O ônibus atrasou e cheguei atrasado no trabalho.",
    "A vizinha pediu açúcar emprestado e esqueceu de devolver.",
    "O café da padaria do bairro é o melhor que já tomei.",
    "A reunião foi cancelada porque o diretor teve um imprevisto.",
    "Ontem fui ao mercado comprar frutas. O dia estava ensolarado.",
    "Fiz uma receita nova da internet e ficou uma delícia.",
    "Meu filho tirou nota boa na escola. Ficamos orgulhosos.",
    "O ar condicionado quebrou no dia mais quente do ano.",
    "Preciso estudar para a prova de matemática da semana que vem.",
    "A praia estava lotada no fim de semana. Muito sol.",
    "A festa de aniversário foi surpresa e ele chorou de emoção.",
    "Minha avó sempre fazia bolo de chocolate nas tardes de domingo.",
    "Fiz amizade com o vizinho novo. Parece gente boa.",
    "Encontrei um amigo de infância no shopping por acaso.",
    "As crianças brincavam no parque enquanto os pais conversavam.",
    "Vou viajar para o litoral no próximo feriado com a família.",
    "Minha filha aprendeu a andar de bicicleta. Fiquei emocionado.",
    "Comprei um livro usado na feira com uma dedicatória antiga.",
    "Acordei cedo para fazer exercícios. O ar estava fresco.",
    "O time jogou bem ontem, principalmente no segundo tempo.",
    "O restaurante estava cheio mas a comida valeu a espera.",
    "Minha mãe ligou preocupada porque não respondi mensagens.",
    "O cachorro latiu a noite toda e ninguém dormiu direito.",
    "Comprei um carro usado em ótimo estado de conservação.",
    "O trânsito estava horrível hoje. Demorei duas horas pra chegar.",
    "Meu irmão vai casar em dezembro e a família toda está animada.",
    "A chuva alagou a rua e vários carros ficaram presos.",
    "Fui ao dentista tirar o siso e doeu mais do que eu esperava.",
    "O gato dormiu em cima do teclado enquanto eu trabalhava.",
    "Descobri uma cafeteria nova perto de casa que é muito boa.",
    "Minha prima teve bebê ontem. Um menino saudável de três quilos.",
    "O elevador do prédio quebrou de novo. Subi oito andares a pé.",
    "Perdi a hora e cheguei atrasado na entrevista de emprego.",
    "O médico disse que preciso fazer mais exercícios e comer melhor.",
    "Comprei um presente pro meu pai mas ainda não sei se ele vai gostar.",
    "A luz acabou durante o jogo e perdemos o final da partida.",
    "Meu sobrinho está aprendendo a falar e já chama todo mundo pelo nome.",
    "Fiz um bolo de cenoura que ficou perfeito. Minha especialidade.",
    "O chefe marcou reunião às sete da manhã. Ninguém ficou feliz.",
    "Encontrei dinheiro esquecido no bolso da calça velha.",
    "O supermercado estava em promoção e acabei comprando mais do que devia.",
    "Minha amiga está grávida de gêmeos e não sabe como vai dar conta.",
    "O professor cancelou a aula de última hora e eu já estava no caminho.",
    "Comi tanto no almoço que mal consegui trabalhar depois.",
    "O cachorro fugiu pelo portão mas conseguimos achar ele no parque.",
    "Meu computador travou no meio do trabalho e perdi tudo que tinha feito.",
    "A farmácia estava fechada e tive que ir em outra bem longe.",
    "Meu vizinho toca guitarra toda noite e já não aguento mais.",
    "Acordei com dor de cabeça e precisei tomar remédio.",
    "O filme que assisti ontem era muito longo mas valeu a pena.",
    "Minha irmã passou no concurso depois de dois anos estudando.",
    "O táxi demorou meia hora pra chegar e ainda cobrou taxa extra.",
    "Fiz um curso online de fotografia e estou gostando muito.",
    "O pneu do carro furou bem no meio da estrada.",
    "Meu pai completou setenta anos e fizemos uma festa surpresa.",
    "A internet caiu no meio da reunião importante.",
    "Comprei um ventilador novo porque o antigo não estava dando conta.",
    "Minha tia faz o melhor feijão tropeiro que já comi na vida.",
    "O mecânico disse que o conserto vai sair mais caro do que eu pensava.",
    "Recebi uma promoção no trabalho depois de cinco anos na empresa.",
    "O cachorro comeu meu chinelo enquanto eu estava dormindo.",
    "Fui ao cinema sozinho e descobri que gosto bastante.",
    "Minha sogra veio passar o fim de semana e trouxe muita comida.",
    "O ônibus quebrou no meio do caminho e tive que esperar outro.",
    "Aprendi a fazer pão caseiro durante a pandemia.",
    "O show foi cancelado por causa da chuva e não deu pra remarcar.",
    "Meu filho ganhou medalha na competição de natação da escola.",
    "A conta de luz veio muito alta esse mês por causa do ar condicionado.",
    "Descobri que meu colega de trabalho mora no mesmo prédio que eu.",
    "O carteiro entregou a encomenda errada e tive que devolver.",
    "Minha avó ensinou uma receita de bolo que está na família há gerações.",
    "O porteiro do prédio conhece todo mundo pelo nome e sobrenome.",
    "Passei mal depois de comer frutos do mar num restaurante novo.",
    "Meu carro não quis pegar de manhã e quase perdi a hora.",
    "A escola do meu filho organizou uma feira de ciências muito legal.",
    "Encontrei um disco de vinil raro numa loja de usados.",
    "O técnico da internet disse que o problema era no cabo da rua.",
    "Minha mãe guarda fotos antigas que eu nem sabia que existiam.",
    "O dentista receitou um enxaguante que deixa a boca toda dormente.",
    "Fiz uma viagem de doze horas de carro e cheguei destruído.",
    "Meu primo abriu um restaurante e a comida é muito boa.",
    "O zelador do prédio sempre avisa quando vai ter manutenção.",
    "Perdi a carteira com todos os documentos e levei um susto.",
    "Minha filha fez um desenho da família que ficou muito fofo.",
    "O cachorro do vizinho late todo dia de madrugada.",
    "Comprei um colchão novo e finalmente estou dormindo bem.",
    "Meu chefe pediu pra eu apresentar o projeto pros diretores.",
    "A padaria perto de casa faz um pão de queijo delicioso.",
    "O encanador disse que o problema é sério e vai demorar pra resolver.",
    "Minha esposa descobriu uma série nova e já assistimos tudo.",
    "O semáforo estava quebrado e causou um congestionamento enorme.",
    "Fiz amizade com uma pessoa no avião e mantemos contato até hoje.",
    "O médico mandou eu fazer uma bateria de exames de rotina.",
    "Minha sobrinha está aprendendo violão e toca todo dia.",
    "O banco bloqueou meu cartão por engano e deu trabalho resolver.",
    "Comi uma pizza ontem que estava fria mas mesmo assim boa.",
    "Meu cunhado é fanático por futebol e assiste todos os jogos.",
    "O cachorro entrou em casa todo sujo de lama depois da chuva.",
    "Ainda lembro da conversa que tive com meu avô antes dele falecer.",
    "Minha filha pediu um cachorro de presente mas ainda não decidi.",
    "Fui assaltado há dois anos e até hoje tenho medo de andar na rua.",
    "O professor de matemática do meu filho é muito paciente.",
    "Comprei uma televisão nova e a imagem é muito melhor.",
    "Minha mãe faz um arroz temperado que ninguém consegue imitar.",
    "O barbeiro do bairro corta cabelo há mais de trinta anos.",
    "Perdi o voo por causa do trânsito e tive que remarcar.",
    "Meu amigo casou com a namorada de infância depois de quinze anos.",
    "O técnico do time foi demitido depois de perder cinco jogos seguidos.",
    "Acordei no meio da noite com barulho de carro batendo.",
    "Minha tia faz um doce de leite caseiro que é o melhor do mundo.",
    "O vizinho de cima deixa a torneira pingando e o barulho é irritante.",
    "Comprei um guarda-chuva que quebrou na primeira chuva forte.",
    "Meu irmão foi morar em outro país e sentimos muita falta dele.",
    "A escola pediu material escolar numa lista enorme.",
    "O mecânico sempre dá um jeito de resolver os problemas do carro.",
    "Fiz um exame de sangue e deu tudo normal graças a Deus.",
    "Minha prima abriu uma loja de roupas e está indo muito bem.",
    "O portão da garagem emperrou e tive que sair pelo portão de pedestres.",
    "Descobri que sou alérgico a camarão depois de uma reação forte.",
    "Meu filho fez amizade com o vizinho e agora brincam todo dia.",
    "A padaria aumentou o preço do pão e todo mundo reclamou.",
    "Perdi a chave de casa e tive que chamar um chaveiro.",
    "Minha esposa cozinha melhor do que qualquer restaurante.",
    "O ônibus estava tão cheio que eu tive que ir pendurado na porta.",
    "Fui no show do meu cantor favorito e foi uma experiência incrível.",
    "O cachorro aprendeu a abrir a porta sozinho.",
    "Minha avó conta histórias de quando era jovem que são muito interessantes.",
    "O ar da cidade estava muito poluído ontem.",
    "Comprei um tênis que ficou apertado e não consegui trocar.",
    "Meu chefe é muito exigente mas também é justo.",
    "A chuva de ontem alagou o quintal todo.",
    "Passei o fim de semana inteiro lendo um livro que não conseguia largar.",
    "O médico disse que preciso emagrecer pelo menos dez quilos.",
    "Minha filha ganhou um prêmio de melhor aluna da turma.",
    "O técnico de informática conseguiu recuperar meus arquivos perdidos.",
    "Encontrei uma carteira na rua e consegui devolver pro dono.",
    "Meu vizinho tem um jardim lindo que ele cuida todo dia.",
    "A comida do hospital era terrível quando fiquei internado.",
    "Comprei um sofá novo e a sala ficou muito mais bonita.",
    "Minha mãe sempre me liga no domingo pra saber como estou.",
    "O eletricista disse que a fiação da casa está muito velha.",
    "Fiz uma aposta com meu amigo e acabei perdendo.",
    "Meu pai sempre acorda cedo mesmo no fim de semana.",
    "A farmácia perto de casa abre vinte e quatro horas.",
    "Perdi o óculos e fiquei uma semana sem conseguir ler direito.",
    "Minha esposa fez uma surpresa no meu aniversário que me emocionou.",
    "O cachorro ficou doente e tivemos que levar no veterinário.",
    "Descobri um restaurante japonês excelente perto do trabalho.",
    "Meu filho não quer ir pra escola e não sei mais o que fazer.",
    "A churrasqueira do prédio estava ocupada quando quis usar.",
    "Comprei uma bicicleta pra fazer exercício mas quase não uso.",
]

AI_PROMPTS = [
    "Escreva uma frase curta e informal sobre o seu dia.",
    "Fale brevemente sobre algo que aconteceu contigo recentemente.",
    "Conte um fato cotidiano simples em duas ou três frases.",
    "Descreva uma situação comum do dia a dia em poucas palavras.",
    "Escreva como se estivesse contando algo pra um amigo.",
    "Compartilhe um pensamento rápido sobre a sua rotina.",
    "Fale sobre uma coisa simples que te deixou feliz hoje.",
    "Descreva algo que você viu ou fez recentemente de forma natural.",
    "Escreva um comentário curto sobre um assunto qualquer.",
    "Conte algo que aconteceu na sua semana de forma breve.",
    "Escreva sobre tecnologia de forma simples e direta.",
    "Fale sobre um filme ou série que assistiu.",
    "Comente sobre o clima de forma casual.",
    "Descreva uma comida que você gosta.",
    "Fale sobre um lugar que você visitou.",
    "Comente sobre esportes de forma natural.",
    "Escreva sobre música brevemente.",
    "Fale sobre viagens de forma simples.",
    "Comente sobre seu trabalho ou estudos.",
    "Escreva sobre família de forma breve.",
]

AI_PROMPTS_MEDIUM = [
    "Escreva um parágrafo curto sobre inteligência artificial sem usar tópicos ou formatação.",
    "Fale sobre educação no Brasil em um parágrafo simples.",
    "Descreva a importância da leitura em um texto corrido curto.",
    "Explique reciclagem de forma breve e direta.",
    "Fale sobre saúde em um parágrafo informal.",
    "Comente sobre tecnologia moderna em um texto curto.",
    "Escreva sobre mudanças climáticas de forma concisa.",
    "Fale sobre redes sociais em um parágrafo.",
    "Descreva exercícios físicos brevemente.",
    "Escreva sobre culinária brasileira de forma simples.",
]

AI_PROMPTS_FORMAL = [
    "Escreva um parágrafo FORMAL e técnico sobre inteligência artificial. Use linguagem acadêmica.",
    "Redija um texto FORMAL sobre os desafios da educação no Brasil contemporâneo.",
    "Elabore um parágrafo FORMAL sobre o impacto das redes sociais na sociedade.",
    "Produza um texto FORMAL e objetivo sobre mudanças climáticas e meio ambiente.",
    "Escreva de forma FORMAL sobre a importância da tecnologia moderna.",
    "Redija um parágrafo FORMAL sobre o papel da leitura no desenvolvimento cognitivo.",
    "Elabore um texto FORMAL sobre os benefícios dos exercícios físicos para a saúde.",
    "Produza um parágrafo FORMAL sobre a economia digital e suas transformações.",
    "Escreva FORMALMENTE sobre sustentabilidade e preservação ambiental.",
    "Redija um texto FORMAL sobre inovação científica e desenvolvimento tecnológico.",
]

AI_PROMPTS_FORMAL_SHORT = [
    "Escreva UMA frase FORMAL sobre inteligência artificial.",
    "Escreva UMA frase FORMAL sobre educação.",
    "Escreva UMA frase FORMAL sobre tecnologia.",
    "Escreva UMA frase FORMAL sobre meio ambiente.",
    "Escreva UMA frase FORMAL sobre saúde pública.",
    "Escreva UMA frase FORMAL sobre economia.",
    "Escreva UMA frase FORMAL sobre ciência.",
    "Escreva UMA frase FORMAL sobre sociedade moderna.",
    "Escreva UMA frase FORMAL sobre desenvolvimento sustentável.",
    "Escreva UMA frase FORMAL sobre inovação.",
    "Escreva DUAS frases FORMAIS e curtas sobre inteligência artificial.",
    "Escreva DUAS frases FORMAIS e curtas sobre mudanças climáticas.",
    "Escreva DUAS frases FORMAIS e curtas sobre transformação digital.",
    "Escreva DUAS frases FORMAIS e curtas sobre globalização.",
    "Escreva DUAS frases FORMAIS e curtas sobre políticas públicas.",
    "Escreva DUAS frases FORMAIS e curtas sobre mercado de trabalho.",
    "Escreva DUAS frases FORMAIS e curtas sobre urbanização.",
    "Escreva DUAS frases FORMAIS e curtas sobre diversidade cultural.",
    "Escreva DUAS frases FORMAIS e curtas sobre ética profissional.",
    "Escreva DUAS frases FORMAIS e curtas sobre responsabilidade social.",
]


def generate_ai_samples_gemini(num_samples: int = 100) -> list[dict[str, Any]]:
    if not config.GEMINI_API_KEY:
        logger.warning("GEMINI_API_KEY nao configurada.")
        return []

    logger.info(f"Gerando {num_samples} amostras com Gemini...")

    try:
        import google.generativeai as genai

        genai.configure(api_key=config.GEMINI_API_KEY)
        model = genai.GenerativeModel(config.GEMINI_MODEL)

        samples = []

        informal_prompts = AI_PROMPTS + AI_PROMPTS_MEDIUM
        formal_prompts = AI_PROMPTS_FORMAL
        formal_short_prompts = AI_PROMPTS_FORMAL_SHORT

        informal_count = num_samples // 3
        formal_count = num_samples // 3
        formal_short_count = num_samples - informal_count - formal_count

        for _ in range(informal_count):
            prompt = random.choice(informal_prompts)
            system_instruction = (
                "Você é uma pessoa comum escrevendo de forma natural e informal. "
                "Responda APENAS com o texto solicitado, sem introduções, sem formatação markdown, "
                "sem listas, sem títulos, sem asteriscos. Escreva como uma pessoa real escreveria "
                "numa conversa casual. Máximo 3-4 frases."
            )

            try:
                response = model.generate_content(
                    f"{system_instruction}\n\n{prompt}",
                    generation_config={
                        "temperature": 1.0,
                        "max_output_tokens": 200,
                    },
                )

                text = response.text.strip()
                text = text.replace("*", "").replace("#", "").replace("`", "")
                text = " ".join(text.split())

                if text and 20 < len(text) < 500:
                    samples.append(
                        {
                            "text": text,
                            "label": 1,
                            "source": "gemini-informal",
                        }
                    )
                    logger.info(f"Informal {len(samples)}/{num_samples}: {text[:50]}...")

                time.sleep(0.5)

            except Exception as e:
                logger.warning(f"Falha ao gerar amostra informal: {e}")
                time.sleep(2)
                continue

        for _ in range(formal_count):
            prompt = random.choice(formal_prompts)
            system_instruction = (
                "Você é um redator acadêmico escrevendo de forma FORMAL e técnica. "
                "Responda APENAS com o texto solicitado, sem introduções, sem formatação markdown, "
                "sem listas, sem títulos, sem asteriscos. Use vocabulário culto e estrutura formal. "
                "Máximo 3-4 frases."
            )

            try:
                response = model.generate_content(
                    f"{system_instruction}\n\n{prompt}",
                    generation_config={
                        "temperature": 0.8,
                        "max_output_tokens": 250,
                    },
                )

                text = response.text.strip()
                text = text.replace("*", "").replace("#", "").replace("`", "")
                text = " ".join(text.split())

                if text and 30 < len(text) < 600:
                    samples.append(
                        {
                            "text": text,
                            "label": 1,
                            "source": "gemini-formal",
                        }
                    )
                    logger.info(f"Formal {len(samples)}/{num_samples}: {text[:50]}...")

                time.sleep(0.5)

            except Exception as e:
                logger.warning(f"Falha ao gerar amostra formal: {e}")
                time.sleep(2)
                continue

        for _ in range(formal_short_count):
            prompt = random.choice(formal_short_prompts)
            system_instruction = (
                "Você é um redator acadêmico escrevendo de forma FORMAL. "
                "Responda APENAS com o texto solicitado, sem introduções, sem formatação markdown, "
                "sem listas, sem títulos, sem asteriscos. Use vocabulário culto. "
                "MÁXIMO 1-2 frases curtas."
            )

            try:
                response = model.generate_content(
                    f"{system_instruction}\n\n{prompt}",
                    generation_config={
                        "temperature": 0.7,
                        "max_output_tokens": 100,
                    },
                )

                text = response.text.strip()
                text = text.replace("*", "").replace("#", "").replace("`", "")
                text = " ".join(text.split())

                if text and 15 < len(text) < 200:
                    samples.append(
                        {
                            "text": text,
                            "label": 1,
                            "source": "gemini-formal-short",
                        }
                    )
                    logger.info(f"Formal-short {len(samples)}/{num_samples}: {text[:50]}...")

                time.sleep(0.5)

            except Exception as e:
                logger.warning(f"Falha ao gerar amostra formal curta: {e}")
                time.sleep(2)
                continue

        logger.info(
            f"Geradas {len(samples)} amostras com Gemini ({informal_count} informal + {formal_count} formal + {formal_short_count} formal-short)."
        )
        return samples

    except ImportError:
        logger.error("Pacote 'google-generativeai' nao instalado.")
        return []


def build_balanced_dataset() -> None:
    human_samples = [{"text": text, "label": 0, "source": "manual"} for text in HUMAN_SAMPLES_PT]
    logger.info(f"Amostras humanas: {len(human_samples)}")

    ai_samples = generate_ai_samples_gemini(len(human_samples))
    logger.info(f"Amostras IA: {len(ai_samples)}")

    all_samples = human_samples + ai_samples
    random.shuffle(all_samples)

    total = len(all_samples)
    train_end = int(total * 0.8)
    val_end = int(total * 0.9)

    dataset = {
        "train": all_samples[:train_end],
        "validation": all_samples[train_end:val_end],
        "test": all_samples[val_end:],
    }

    for split_name, samples in dataset.items():
        path = DATASET_DIR / f"{split_name}.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(samples, f, ensure_ascii=False, indent=2)
        logger.info(f"Salvo {split_name}: {len(samples)} amostras")

    stats = {
        "total": total,
        "human": len(human_samples),
        "ai": len(ai_samples),
        "train": len(dataset["train"]),
        "validation": len(dataset["validation"]),
        "test": len(dataset["test"]),
    }

    with open(DATASET_DIR / "stats.json", "w") as f:
        json.dump(stats, f, indent=2)

    logger.info(f"Dataset criado: {stats}")

    logger.info("\n=== Exemplos Humanos ===")
    for s in random.sample(human_samples, min(3, len(human_samples))):
        logger.info(f"[H] {s['text'][:80]}...")

    logger.info("\n=== Exemplos IA ===")
    for s in random.sample(ai_samples, min(3, len(ai_samples))):
        logger.info(f"[IA] {s['text'][:80]}...")


if __name__ == "__main__":
    build_balanced_dataset()


# "A perfeicao nao e alcancavel, mas se perseguirmos a perfeicao podemos alcancar a excelencia." - Vince Lombardi
