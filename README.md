## Objetivo
Plotar informacoes sobre as mortes relacionadas a COVID-19 (SARS-COV-2) com fontes confiaveis de dados.

## Estrutura de Diretorios
Sugiro que deixem todos os arquivos de dados em um diretorio (../app_data), assim basta um parametro de volume para que o container os encontre. Os arquivos que utiliza-se sao:

- time_series_covid19_deaths_global.csv
- time_series_covid19_cases_global.csv
- brazil_covid19.csv

## Atualizacao dos Dados
A atualizacao dos dados **NAO EH AUTOMATICA**. Atualize-os no diretorio app_data, os arquivos que deixei la sao para que voce veja o aplicativo funcionando. O que vier com a melhor solucao do pipeline de dados, eu deixarei publico por aqui tambem =)

## Python 3.7 (local)
- Instale as dependencias do arquivo requirements.txt
- Configure o config.yaml com os locais de onde voce deixou os arquivos
- Rode o arquivo __init__.py
- No seu browser, entre em http://localhost:5000

## Docker
O Dockerfile na raiz pode gerar uma imagem com o ambiente necessario, basta rodar o arquivo DockerBuild.sh.
Criada a imagem, rode o comando abaixo, substituindo path_dos_arquivos pelo diretorio local onde voce atualiza os arquivos.

docker run -p 5000:5000 -v path_dos_arquivos:/app_data renatobanzai/banzai-covid19:latest

- No seu browser, entre em http://localhost:5000

***

**Repositorios de dados** 

-Dados Globais: [Johns Hopkins](https://www.kaggle.com/unanimad/corona-virus-brazil)

-Dados Brasil: [Unanimad](https://github.com/CSSEGISandData/COVID-19)

**PS1** Estou com um note com teclado japones e desisti de colocar acentuacao.
**PS2** Playstation 2