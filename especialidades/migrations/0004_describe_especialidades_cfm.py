from django.db import migrations


DESCRICOES = {
    "Acupuntura": "Atua na prevenção e no tratamento de condições de saúde por meio de técnicas médicas de acupuntura.",
    "Alergia e Imunologia": "Diagnostica e trata alergias, imunodeficiências e outras alterações do sistema imunológico.",
    "Anestesiologia": "Realiza anestesia, controle da dor e acompanhamento das funções vitais antes, durante e após procedimentos.",
    "Angiologia": "Cuida das doenças clínicas dos vasos sanguíneos e linfáticos.",
    "Cardiologia": "Previne, diagnostica e trata doenças do coração e do sistema circulatório.",
    "Cirurgia Cardiovascular": "Realiza procedimentos cirúrgicos no coração e nos grandes vasos.",
    "Cirurgia da Mão": "Trata cirurgicamente lesões, deformidades e doenças da mão e do membro superior.",
    "Cirurgia de Cabeça e Pescoço": "Realiza tratamento cirúrgico de tumores e outras doenças da cabeça e do pescoço.",
    "Cirurgia do Aparelho Digestivo": "Trata cirurgicamente doenças do sistema digestório e de seus órgãos associados.",
    "Cirurgia Geral": "Realiza avaliação e tratamento cirúrgico, especialmente de doenças do abdome, parede abdominal e urgências.",
    "Cirurgia Oncológica": "Realiza o tratamento cirúrgico de tumores e participa do cuidado integrado ao paciente com câncer.",
    "Cirurgia Pediátrica": "Realiza tratamento cirúrgico de doenças em recém-nascidos, crianças e adolescentes.",
    "Cirurgia Plástica": "Realiza procedimentos reparadores e estéticos para restaurar forma, função e aparência corporal.",
    "Cirurgia Torácica": "Trata cirurgicamente doenças do tórax, incluindo pulmões, vias aéreas e parede torácica.",
    "Cirurgia Vascular": "Realiza tratamento cirúrgico e por procedimentos das doenças arteriais, venosas e linfáticas.",
    "Clínica Médica": "Oferece cuidado integral ao adulto, diagnosticando e tratando doenças clínicas de diferentes sistemas.",
    "Coloproctologia": "Diagnostica e trata doenças do intestino grosso, reto e ânus.",
    "Dermatologia": "Diagnostica e trata doenças da pele, cabelos, unhas e mucosas.",
    "Endocrinologia e Metabologia": "Cuida de alterações hormonais e metabólicas, como diabetes, obesidade e doenças da tireoide.",
    "Endoscopia": "Realiza procedimentos endoscópicos para diagnóstico e tratamento de doenças, principalmente do aparelho digestivo.",
    "Gastroenterologia": "Diagnostica e trata doenças do esôfago, estômago, intestinos, fígado, pâncreas e vias biliares.",
    "Genética Médica": "Investiga, diagnostica e orienta pacientes e famílias sobre doenças genéticas e hereditárias.",
    "Geriatria": "Promove o cuidado integral da pessoa idosa, considerando saúde, funcionalidade e qualidade de vida.",
    "Ginecologia e Obstetrícia": "Cuida da saúde reprodutiva feminina e acompanha a gestação, o parto e o pós-parto.",
    "Hematologia e Hemoterapia": "Diagnostica e trata doenças do sangue e atua no uso terapêutico de sangue e seus componentes.",
    "Homeopatia": "Realiza cuidado médico utilizando princípios e medicamentos homeopáticos de forma individualizada.",
    "Infectologia": "Previne, diagnostica e trata doenças causadas por vírus, bactérias, fungos, parasitas e outros agentes infecciosos.",
    "Mastologia": "Diagnostica e trata doenças benignas e malignas das mamas.",
    "Medicina de Emergência": "Atende condições agudas e potencialmente graves que exigem avaliação e intervenção imediatas.",
    "Medicina de Família e Comunidade": "Oferece cuidado contínuo e integral a pessoas e famílias em todas as fases da vida.",
    "Medicina do Trabalho": "Previne e acompanha problemas de saúde relacionados ao trabalho e às condições ocupacionais.",
    "Medicina do Tráfego": "Avalia e promove a saúde e a segurança das pessoas nos diferentes meios de transporte.",
    "Medicina Esportiva": "Cuida da saúde de praticantes de atividade física e atletas, incluindo prevenção e desempenho seguro.",
    "Medicina Física e Reabilitação": "Trata limitações funcionais e coordena a reabilitação de pessoas com deficiências ou incapacidades.",
    "Medicina Intensiva": "Cuida de pacientes graves que necessitam de monitoramento contínuo e suporte avançado em terapia intensiva.",
    "Medicina Legal e Perícia Médica": "Aplica conhecimentos médicos em avaliações periciais, questões legais e investigação médico-legal.",
    "Medicina Nuclear": "Utiliza radiofármacos para diagnóstico, avaliação funcional e tratamento de determinadas doenças.",
    "Medicina Preventiva e Social": "Atua na prevenção de doenças, promoção da saúde, epidemiologia e organização de serviços de saúde.",
    "Nefrologia": "Diagnostica e trata doenças dos rins, distúrbios relacionados e necessidade de terapia renal substitutiva.",
    "Neurocirurgia": "Realiza tratamento cirúrgico de doenças do cérebro, coluna, medula e nervos periféricos.",
    "Neurologia": "Diagnostica e trata doenças do cérebro, medula, nervos e músculos.",
    "Nutrologia": "Avalia a relação entre nutrientes e saúde, prevenindo e tratando distúrbios nutricionais e metabólicos.",
    "Oftalmologia": "Previne, diagnostica e trata doenças dos olhos e alterações da visão.",
    "Oncologia Clínica": "Realiza o tratamento clínico do câncer e acompanha o paciente ao longo do cuidado oncológico.",
    "Ortopedia e Traumatologia": "Diagnostica e trata doenças e lesões dos ossos, articulações, músculos, tendões e ligamentos.",
    "Otorrinolaringologia": "Diagnostica e trata doenças dos ouvidos, nariz, seios da face, garganta e estruturas relacionadas.",
    "Patologia": "Analisa tecidos, células e órgãos para diagnosticar doenças e apoiar decisões clínicas.",
    "Patologia Clínica/Medicina Laboratorial": "Interpreta e supervisiona exames laboratoriais utilizados na prevenção, no diagnóstico e no acompanhamento de doenças.",
    "Pediatria": "Acompanha a saúde, o crescimento e o desenvolvimento de crianças e adolescentes.",
    "Pneumologia": "Diagnostica e trata doenças dos pulmões e das vias respiratórias.",
    "Psiquiatria": "Diagnostica, trata e previne transtornos mentais, emocionais e comportamentais.",
    "Radiologia e Diagnóstico por Imagem": "Utiliza métodos de imagem para diagnosticar doenças e orientar procedimentos médicos.",
    "Radioterapia": "Utiliza radiação ionizante no tratamento do câncer e de outras condições específicas.",
    "Reumatologia": "Diagnostica e trata doenças das articulações, músculos, ossos e condições autoimunes sistêmicas.",
    "Urologia": "Diagnostica e trata doenças do sistema urinário e do sistema reprodutor masculino.",
}


def describe_especialidades(apps, schema_editor):
    Especialidade = apps.get_model("especialidades", "Especialidade")
    for nome, descricao in DESCRICOES.items():
        Especialidade.objects.filter(
            nome__iexact=nome,
            descricao="",
        ).update(descricao=descricao)


class Migration(migrations.Migration):
    dependencies = [
        ("especialidades", "0003_normalize_especialidade_legacy"),
    ]

    operations = [
        migrations.RunPython(describe_especialidades, migrations.RunPython.noop),
    ]
