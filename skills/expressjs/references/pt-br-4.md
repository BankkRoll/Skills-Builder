# Melhores Práticas de Produção: desempenho e confiabilidade and more

# Melhores Práticas de Produção: desempenho e confiabilidade

> Descubra desempenho e confiabilidade melhores práticas para aplicativos Express na produção, cobrindo otimizações de código e configurações de ambiente para um desempenho ideal.

# Melhores Práticas de Produção: desempenho e confiabilidade

Este artigo discute as melhores práticas de desempenho e de confiabilidade
para aplicativos Express implementados para produção.

Este tópico se enquadra claramente no mundo de “devops”, abordando o desenvolvimento tradicional e as operações. Assim, as informações são divididas em duas partes:

- [Itens a fazer no seu código](#code) (a parte do dev).
  - Use a compactação gzip
  - Não use funções síncronas
  - Faça o registro de logs corretamente
  - [Tratar exceções corretamente](#handle-exceptions-properly)
- [Itens a fazer no seu ambiente / configuração](#env) (a parte de ops).
  - Configure o NODE_ENV para “produção”
  - Executar o seu aplicativo (e Node) diretamente com o sistema
    de inicialização. Isto é de certa forma mais simples, mas você não
    obtém as vantagens adicionais do uso de um gerenciador de processos.
  - Execute seu aplicativo em um cluster
  -
  - Use um balanceador de carga
  - Use um proxy reverso

## Itens a fazer no seu código

A seguir serão apresentados alguns itens que podem ser feitos no seu código
para melhorar o desempenho dos aplicativos:

- Use a compactação gzip
- Não use funções síncronas
- Faça o registro de logs corretamente
- [Tratar exceções corretamente](#handle-exceptions-properly)

### Use a compactação gzip

A compactação Gzip pode diminuir bastante o tamanho do corpo de resposta e assim aumentar a velocidade de um aplicativo da web. Use o middleware [compression](https://www.npmjs.com/package/compression) para fazer a compactação gzip no seu aplicativo do Express. Por exemplo:

```
const compression = require('compression')
const express = require('express')
const app = express()

app.use(compression())
```

Para um website com tráfego intenso na produção, a melhor maneira de colocar a compactação em prática, é implementá-la em um
nível de proxy reverso (consulte [Use um proxy reverso](#proxy)). Neste caso, não é necessário usar o middleware de compactação. Para obter detalhes sobre a ativação da compactação gzip no Nginx, consulte o Módulo
ngx_http_gzip_module na documentação do Nginx.

### Não use funções síncronas

Funções e métodos síncronos impedem o avanço da execução do processo até que eles retornem. Uma
única chamada a uma função síncrona pode retornar em poucos microssegundos ou milissegundos, entretanto, em websites com tráfego
intenso, essas chamadas se somam e reduzem o desempenho do
aplicativo. Evite o uso delas na produção.

Apesar de o Node e muitos módulos fornecerem versões síncronas e assíncronas de suas funções, sempre use as versões assíncronas na produção. O único momento em que o uso de uma função síncrona pode ser justificado é na primeira inicialização.

Se estiver usando o Node.js + ou o  .+, é possível usar a sinalização `--trace-sync-io` da linha de comandos para imprimir um aviso e um rastreio de pilha sempre que o seu aplicativo usar uma API síncrona. Obviamente, não seria desejado usar isto na produção, mas sim antes, para garantir que seu código está pronto para produção. Consulte a Atualização
semanal para o io.js 2.1.0 para obter mais informações.

### Lide com exceções adequadamente

Em geral, existem duas razões para registrar logs em seu aplicativo: Para depuração e para registro de logs de atividade do aplicativo (essencialmente, todo o resto). Usar
o `console.log()` ou o `console.err()` para imprimir mensagens de log no
terminal é uma prática comum em desenvolvimento. Mas essas
funções são síncronas quando o destino é um terminal ou um arquivo, portanto elas não são adequadas para produção, a não ser que
a saída seja canalizada para outro programa.

#### Para depuração

Se estiver registrando logs com o propósito de depuração, então ao invés de usar o `console.log()`, use um módulo
especial para depuração como o [debug](https://www.npmjs.com/package/debug). Este
módulo permite que seja usada a variável de ambiente DEBUG para controlar quais mensagens de depuração são enviadas para o
`console.err()`, se houver. Para manter o seu aplicativo puramente assíncrono, você deverá canalizar o
`console.err()` para outro programa. Mas nesse ponto, você não fará a depuração na produção, não é?

#### Para atividade do aplicativo

Se estiver registrando logs de atividade do aplicativo (por
exemplo, rastreamento de tráfico ou chamadas de API), ao invés de
usar o `console.log()`, use uma biblioteca de
registro de logs como [Winston](https://www.npmjs.com/package/pino) ou Bunyan.

### Lide com exceções adequadamente

Aplicativos do Node caem ao encontrarem uma exceção não
capturada. O não tratamento de exceções e a não tomada das ações
apropriadas irão fazer com que o seu aplicativo do Express caia e
fique off-line. Se seguir os conselhos em [Assegurando que o seu aplicativo reinicie automaticamente](#restart)
abaixo, então seu aplicativo se recuperará de uma queda. Felizmente, aplicativos Express tipicamente possuem um tempo curto de inicialização. Contudo,
é desejável evitar quedas em primeiro lugar e, para fazer isso, é
necessário tratar exceções adequadamente.

Para garantir que está tratando todas as exceções, use as seguintes técnicas:

- [Use try-catch](#try-catch)
- [Use promessas](#promises)

Antes de se aprofundar nestes tópicos, você deveria ter um
entendimento básico de manipulação de erros do Node/Express: usando
retornos de chamada erros-first, e propagação de erros no
middleware. O Node usa uma convenção “retorno de chamada erros-first” para retorno de erros de funções assíncronas, onde o
primeiro parâmetro para a função de retorno de chamada é o objeto de erro, seguido dos dados de resultado nos parâmetros subsequentes. Para indicar que não ocorreram erros, passe null como o primeiro parâmetro. A função de retorno de chamada deve correspondentemente seguir a
convenção de retorno de chamada erros-first para tratar o erro de forma significativa. E no Express, a melhor prática é usar a função next() para propagar erros pela cadeia de middlewares.

Para obter mais informações sobre os fundamentos de manipulação de erros, consulte:

- [Manipulação de Erros no Node.js](https://www.tritondatacenter.com/node-js/production/design/errors)

#### Usar try-catch

Try-catch é uma construção da linguagem JavaScript que pode ser usada para capturar exceções em um código síncrono. Use try-catch, por exemplo, para tratar erros de análise sintática de JSON como mostrado abaixo.

Aqui está um exemplo de uso de try-catch para tratar uma
potencial exceção causadora de queda de processo.
Esta função middleware aceita um parâmetro de campo de consulta chamado “params” que é um objeto JSON.

```
app.get('/search', (req, res) => {
  // Simulating async operation
  setImmediate(() => {
    const jsonStr = req.query.params
    try {
      const jsonObj = JSON.parse(jsonStr)
      res.send('Success')
    } catch (e) {
      res.status(400).send('Invalid JSON string')
    }
  })
})
```

Entretanto, o try-catch funciona apenas para códigos síncronos. Como
a plataforma Node é a princípio assíncrona (particularmente em um ambiente de produção), o try-catch deixará de capturar muitas
exceções.

#### Use promessas

Quando um erro é lançado em uma função `async` ou uma promessa rejeitada é aguardada dentro de uma função `async`, esses erros serão passados para o manipulador de erros como se chamando `next(err)`

```
app.get('/', async (req, res, next) => {
  const data = await userData() // If this promise fails, it will automatically call `next(err)` to handle the error.

  res.send(data)
})

app.use((err, req, res, next) => {
  res.status(err.status ?? 500).send({ error: err.message })
})
```

Além disso, você pode usar funções assíncronas para o seu middleware, e o roteador irá lidar com erros se a promessa falhar, por exemplo:

```
app.use(async (req, res, next) => {
  req.locals.user = await getUser(req)

  next() // This will be called if the promise does not throw an error.
})
```

A melhor prática é lidar com os erros o mais próximo possível do site. Então enquanto isso é manipulado no roteador, É melhor encontrar o erro no middleware e lidar com ele sem depender de um middleware separado para manipular erros.

#### O que não fazer

Uma coisa que *não* deveria fazer é escutar a eventos `uncaughtException`, emitidos quando uma exceção
emerge regressando ao loop de eventos. Incluir um listener de eventos para `uncaughtException` irá mudar o comportamento
padrão do processo que está encontrando uma exceção; o processo irá continuar a execução apesar da exceção. Essa pode parecer como uma boa maneira de prevenir que o seu
aplicativo caia, mas continuar a execução do aplicativo após uma
exceção não capturada é uma prática perigosa e não é recomendada, porque o estado do processo se torna não confiável e imprevisível.

Adicionalmente, usar o `uncaughtException` é oficialmente reconhecido como [grosseiro](https://nodejs.org/api/process.html#process_event_uncaughtexception)
e existe uma [proposta](https://github.com/nodejs/node-v0.x-archive/issues/2582)
de removê-lo do núcleo. Portando escutar por um `uncaughtException` é simplesmente uma má ideia. É
por isso que recomendamos coisas como múltiplos processos e
supervisores: o processo de queda e reinicialização é frequentemente a
forma mais confiável de se recuperar de um erro.

Também não recomendamos o uso de [domínios](https://nodejs.org/api/domain.html). Ele
geralmente não resolve o problema e é um módulo descontinuado.

## Coisa a se fazer no seu ambiente / configuração

A seguir serão apresentados alguns itens que podem ser feitos no seu ambiente de sistema para melhorar o desempenho dos seus aplicativos:

- Configure o NODE_ENV para “produção”
- Executar o seu aplicativo (e Node) diretamente com o sistema
  de inicialização. Isto é de certa forma mais simples, mas você não
  obtém as vantagens adicionais do uso de um gerenciador de processos.
- Execute seu aplicativo em um cluster
-
- Use um balanceador de carga
- Use um proxy reverso

### Configure o NODE_ENV para “produção”

A variável de ambiente NODE_ENV especifica o ambiente no qual um aplicativo está executando (geralmente, desenvolvimento ou
produção). Uma das coisas mais simples que podem ser feitas para
melhorar o desempenho é configurar NODE_ENV para “production”.

Configurando NODE_ENV para “produção” faz com que o Express:

- Armazene em Cache os modelos de visualização.
- Armazene em Cache arquivos CSS gerados a partir de extensões CSS.
- Gere menos mensagens de erro detalhadas

Testes
indicam que apenas fazendo isso pode melhorar o desempenho por um fator de três!

Se precisar escrever código específico por ambiente, é possível verificar o valor de NODE_ENV com `process.env.NODE_ENV`. Esteja
ciente de que verificar o valor de qualquer variável de ambiente incorre em perda de desempenho, e por isso deve ser feito raramente.

Em desenvolvimento, você tipicamente configura variáveis de ambiente no seu shell interativo, por exemplo, usando o
`export` ou o seu arquivo `.bash_profile`. Mas
em geral você não deveria fazer isto em um servidor de produção; ao invés disso, use o sistema de inicialização do seu sistema
operacional (systemd). A próxima seção fornece mais detalhes sobre a utilização do seu sistema de inicialização em geral,
mas configurando NODE_ENV é tão importante para o desempenho (e fácil de fazer), que está destacado aqui.

Com o systemd, use a diretiva `Environment` no seu arquivo de unidade. Por exemplo:

```
# /etc/systemd/system/myservice.service
Environment=NODE_ENV=production
```

Para obter mais informações, consulte Usando
Variáveis de Ambiente em Unidades systemd.

### Assegure que o seu aplicativo reinicie automaticamente

Em produção, não é desejado que seu aplicativo fique off-line,
nunca. Isto significa que é necessário certificar-se de que ele
reinicie tanto se o aplicativo cair quanto se o próprio servidor
cair. Apesar de se esperar que nenhum desses eventos ocorram,
realisticamente você deve considerar ambas as eventualidades:

- Usando um gerenciador de processos para reiniciar o aplicativo (e o Node) quando ele cair.
- Usando o sistema de inicialização fornecido pelo seu sistema operacional para reiniciar o gerenciador de processos quando o
  sistema operacional cair. Também é possível usar o sistema de inicialização sem um gerenciador de processos.

Aplicativos do Node caem se encontrarem uma exceção não
capturada. A principal coisa que precisa ser feita é assegurar que o
seu aplicativo esteja bem testado e trate todas as exceções (consulte
[tratar exceções adequadamente](#exceptions) para
obter detalhes). Mas por segurança, posicione um mecanismo para
assegurar que se e quando o seu aplicativo cair, ele irá
automaticamente reiniciar.

#### Use um gerenciador de processos

Em desenvolvimento, você iniciou o seu aplicativo de forma simples a partir da linha de comandos com  o `node server.js` ou
algo similar. Mas fazer isso na produção é uma receita para o desastre. Se o aplicativo cair, ele ficará off-line até ser reiniciado. Para
assegurar que o seu aplicativo reinicie se ele cair, use um gerenciador de processos. Um
gerenciador de processos é um “contêiner” para aplicativos que facilita a implementação, fornece alta disponibilidade, e permite o
gerenciamento do aplicativo em tempo real.

Em adição à reinicialização do seu aplicativo quando cai, um
gerenciador de processos pode permitir que você:

- Ganhe insights sobre o desempenho em tempo de execução e o consumo de recursos.
- Modifique configurações dinamicamente para melhorar o desempenho.
- Controle de agrupamento (pm2).

Historicamente, foi popular usar um gerente de processo Node.js, como [PM2](https://github.com/Unitech/pm2). Veja a documentação deles, se você quiser fazer isso. No entanto, recomendamos a utilização de seu sistema de inicio para gerenciamento de processos.

#### Use um sistema de inicialização

A próxima camada de confiabilidade é para assegurar que o seu
aplicativo reinicie quando o servidor reiniciar. Os sistemas podem
ainda assim cair por uma variedade de razões. Para assegurar que o
seu aplicativo reinicie se o servidor cair, use o sistema de
inicialização integrado no seu sistema operacional. O sistema principal de iniciação em uso hoje é [systemd](https://wiki.debian.org/systemd).

Existem duas formas de usar sistemas de inicialização com o seu aplicativo Express:

- Executar o seu aplicativo em um gerenciador de processos, e instalar o gerenciador de processos com o sistema de inicialização. O gerenciador de processos irá reiniciar seu aplicativo quando o
  aplicativo cair, e o sistema de inicialização irá reiniciar o
  gerenciador de processos quando o sistema operacional reiniciar. Esta é a abordagem recomendada.
- Execute seu aplicativo (e Node) diretamente com o sistema iniciação. Isto é um pouco mais simples, mas você não obtém as vantagens adicionais de usar um gerente de processo.

##### Systemd

O Systemd é um sistema Linux e gerenciador de serviço. A
maioria das distribuições principais do Linux adotaram o systemd como
sistema de inicialização padrão.

Um arquivo de configuração de serviço do systemd é chamado
de *arquivo de unidade*, com um nome de arquivo
terminando em .service. Aqui está um exemplo de arquivo de unidade
para gerenciar um aplicativo Node diretamente (substitua o texto em
negrito com valores para o seu sistema e aplicativo): Substitua os valores colocados em `<angle brackets>` do seu sistema e aplicativo:

```
[Unit]
Description=<Awesome Express App>

[Service]
Type=simple
ExecStart=/usr/local/bin/node </projects/myapp/index.js>
WorkingDirectory=</projects/myapp>

User=nobody
Group=nogroup

# Environment variables:
Environment=NODE_ENV=production

# Allow many incoming connections
LimitNOFILE=infinity

# Allow core dumps for debugging
LimitCORE=infinity

StandardInput=null
StandardOutput=syslog
StandardError=syslog
Restart=always

[Install]
WantedBy=multi-user.target
```

Para obter mais informações sobre o systemd, consulte a
referência
do systemd (página do manual).

### Execute seu aplicativo em um cluster

Em um sistema com múltiplos núcleos, é possível aumentar o
desempenho de um aplicativo Node em muitas vezes ativando um cluster
de processos. Um cluster executa múltiplas instâncias do aplicativo,
idealmente uma instância em cada núcleo da CPU, assim distribuindo a carga e as
tarefas entre as instâncias.

![Balanceamento entre instâncias de aplicação usando a API de cluster](https://expressjs.com/images/clustering.png)

IMPORTANTE: Como as instâncias do aplicativo são executadas em processos separados, elas não compartilham o mesmo espaço de memória. Isto é, os objetos são locais para cada instância do aplicativo. Portanto, não é possível manter o estado no código do aplicativo. Entretanto, é possível usar um armazenamento de dados em memória como o [Redis](http://redis.io/) para armazenar dados
relativos à sessão e ao estado. Este alerta aplica-se a essencialmente todas as formas de escalonamento horizontal, seja a
clusterização com múltiplos processos ou múltiplos servidores físicos.

Em aplicativos clusterizados, processos de trabalho podem cair individualmente sem afetar o restante dos processos. Fora as vantagens de desempenho, o isolamento de falhas é outra razão para executar um cluster de processos de aplicativos. Sempre que processo de trabalho cair, certifique-se de registrar os logs do evento e spawn um novo processo usando cluster.fork().

#### Usando o módulo de cluster do Node

É possível agrupar com o [módulo cluster do Node](https://nodejs.org/api/cluster.html). Isto permite que um processo principal faça o
spawn de processos de trabalho e distribua conexões recebidas entre
os trabalhadores.

#### Usando PM2

Se você publicar sua aplicação com PM2, então você pode aproveitar o clustering *without* para modificar o código da sua aplicação. Você deve garantir sua [application is stateless](https://pm2.keymetrics.io/docs/usage/specifics/#stateless-apps) primeiro, significando que nenhum dado local é armazenado no processo (como sessões, conexões de websocket e coisas parecidas).

Ao executar um aplicativo com PM2, você pode habilitar o **cluster mode** para executá-lo em um cluster com várias instâncias de sua escolha, como o número de CPUs disponíveis na máquina. Você pode alterar manualmente o número de processos no cluster usando a ferramenta de linha de comando `pm2` sem parar o aplicativo.

Para ativar o modo de agrupamento, inicie seu aplicativo assim:

```
# Start 4 worker processes
$ pm2 start npm --name my-app -i 4 -- start
# Auto-detect number of available CPUs and start that many worker processes
$ pm2 start npm --name my-app -i max -- start
```

Isto também pode ser configurado dentro de um arquivo de processo PM2 (`ecosystem.config.js` ou similar) configurando `exec_mode` para `cluster` e `instances` para o número de workers para começar.

Quando em execução, o aplicativo pode ser alterado assim:

```
# Add 3 more workers
$ pm2 scale my-app +3
# Scale to a specific number of workers
$ pm2 scale my-app 2
```

Para obter mais informações sobre clustering com PM2, consulte [Cluster Mode](https://pm2.keymetrics.io/docs/usage/cluster-mode/) na documentação PM2.

### Armazene em cache os resultados das solicitações

Outra estratégia para melhorar o desempenho na produção é
armazenar em cache o resultado de solicitações, para que o seu
aplicativo não repita a operação para entregar a mesma solicitação
repetidamente.

Use um servidor de cache como [Varnish](https://www.varnish-cache.org/) ou [Nginx](https://blog.nginx.org/blog/nginx-caching-guide) (veja também [Nginx Caching](https://serversforhackers.com/nginx-caching/)) para melhorar muito a velocidade e o desempenho de sua aplicação.

### Use um balanceador de carga

Não importa o quão otimizado um aplicativo é, uma única
instância pode manipular apenas uma quantidade limitada de carga e
tráfego. Uma maneira de escalar um aplicativo é executar múltiplas
instâncias do mesmo e distribuir o tráfego através de um balanceador
de carga. Configurar um balanceador de carga pode melhorar o
desempenho e velocidade do aplicativo, e permiti-lo escalar mais do
que é possível com uma instância única.

Um balanceador de carga é geralmente um proxy reverso que
orquestra o tráfego para e de múltiplas instâncias de aplicativo e
servidores. Você pode facilmente configurar um balanceador de carga ‘load balancer’ para o seu aplicativo usando [Nginx](https://nginx.org/en/docs/http/load_balancing.html) ou [HAProxy](https://www.digitalocean.com/community/tutorials/an-introduction-to-haproxy-and-load-balancing-concepts).

Com o balanceamento de carga, você pode ter que garantir que
solicitações que estão associadas com um ID de sessão em particular
conectam ao processo que as originou. Isto é conhecido como
*afinidade de sessão*, ou *sessões
pegajosas*, e podem ser endereçadas pela sugestão acima para
usar um armazenamento de dados como o Redis para os dados da sessão
(dependendo do seu aplicativo). Para uma discussão, consulte por
[Usando múltiplos nós](https://socket.io/docs/v4/using-multiple-nodes/).

### Use um proxy reverso

Um proxy reverso fica em frente a um aplicativo web e executa
operações de suporte nas solicitações, fora o direcionamento de
solicitações para o aplicativo. Ele pode lidar com páginas de erro,
compactação, armazenamento em cache, entrega de arquivos, e
balanceamento de carga entre outras coisas.

Entregar tarefas que não requerem conhecimento do estado do
aplicativo para um proxy reverso libera o Express para executar
tarefas especializadas de aplicativos. Por este motivo, é recomendado executar Express atrás de um proxy reverso como [Nginx](https://www.nginx.org/) ou [HAProxy](https://www.haproxy.org/) em produção.

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/pt-br/advanced/best-practice-performance.md          )

---

# Melhores Práticas em Produção: Segurança

> Descubra as melhores práticas de segurança cruciais para aplicativos Express em produção, incluindo o uso de TLS, validação de entrada, cookies seguros e prevenção de vulnerabilidades.

# Melhores Práticas em Produção: Segurança

## Visão Geral

O termo *“produção”* refere-se ao estágio no ciclo de vida do software onde um aplicativo ou API está geralmente
disponível para os seus usuários finais ou consumidores. Em contrapartida, no estágio de *“desenvolvimento”*,
você ainda está ativamente escrevendo e testando o código, e o aplicativo não está aberto para acesso externo. Os ambiente de sistema correspondentes são conhecidos como ambientes de *produção* e *desenvolvimento*,
respectivamente.

Os ambientes de desenvolvimento e produção são geralmente
configurados de forma diferente e possuem requisitos completamente
diferentes. O que é bom em desenvolvimento pode não ser aceitável na produção. Por exemplo, em um ambiente de desenvolvimento você pode
desejar registros detalhados de erros para depuração, enquanto o
mesmo comportamento pode se tornar um risco de segurança em um
ambiente de produção. E em desenvolvimento, você não precisa se
preocupar com a escalabilidade, confiabilidade, e desempenho,
enquanto estas preocupações se tornam críticas na produção.

Observação

Se acredita que descobriu uma vulnerabilidade de segurança em Express, consulte
[Políticas de Segurança e Procedimentos](https://expressjs.com/en/resources/contributing.html#security-policies-and-procedures).

Este artigo discute algumas melhores práticas de segurança para
aplicativos do Express implementadas na produção.

- [Práticas recomendadas: Segurança](#production-best-practices-security)
  - [Overview](#overview)
  - [Não usar versões descontinuadas ou vulneráveis do Express](#dont-use-deprecated-or-vulnerable-versions-of-express)
  - [Use TLS](#use-tls)
  - [Não confie na entrada do usuário](#do-not-trust-user-input)
    - [Impedir redirecionamentos abertos](#prevent-open-redirects)
  - [Use Helmet](#use-helmet)
  - [Reduzir impressão digital](#reduce-fingerprinting)
  - A [hsts](https://github.com/helmetjs/hsts) configura o cabeçalho `Strict-Transport-Security`
    que impinge conexões seguras (HTTP sobre SSL/TLS) com o servidor.
    - A principal diferença entre esses dois módulos é como eles salvam os dados de cookies de sessão.  O middleware [express-session](https://www.npmjs.com/package/express-session)
      armazena os dados da sessão no servidor; ele salva apenas o ID da
      sessão no cookie, não os dados da sessão.  Por padrão, ele usa
      armazenamento em memória e não é projetado para um ambiente de
      produção.  Em produção, será necessário configurar um armazenamento de
      sessão escalável; consulte a lista de armazenamentos
      de sessão compatíveis.
    - A [ieNoOpen](https://github.com/helmetjs/ienoopen) configura o `X-Download-Options` para o IE8+.
  - [Impedir ataques brute-force contra a autorização](#prevent-brute-force-attacks-against-authorization)
  - [Garanta que suas dependências sejam seguras](#ensure-your-dependencies-are-secure)
    - A [hidePoweredBy](https://github.com/helmetjs/hide-powered-by) remove o cabeçalho `X-Powered-By`.
  - [Considerações adicionais](#additional-considerations)

## Não use versões descontinuadas ou vulneráveis do Express

Os Express 2.x e 3.x não são mais mantidos. Problemas de
segurança e desempenho nestas versões não serão corrigidos. Não use-as! Se
não tiver migrado para a versão 4, siga o [guia de migração](https://expressjs.com/pt-br/guide/migrating-4.html).

Assegure-se também de que não esteja usando nenhuma das versões
vulneráveis do Express listadas na [Página de
atualizações de segurança](https://expressjs.com/pt-br/advanced/security-updates.html). Se estiver, atualize para uma das
liberações estáveis, preferivelmente a mais recente.

## Use TLS

Se o seu aplicativo negocia com ou transmite dados sensíveis,
use a Segurança
da Camada de Transporte (TLS) para proteger a conexão e os
dados. Esta tecnologia criptografa os dados antes deles serem
enviados do cliente para o servidor, assim evitando alguns ataques
comuns (e fáceis). Apesar de solicitações Ajax e POST não parecerem
visivelmente óbvias e parecerem “ocultas” em navegadores, o seu
tráfego de rede é vulnerável a [sniffing de pacotes](https://en.wikipedia.org/wiki/Packet_analyzer) e
[ataques man-in-the-middle](https://en.wikipedia.org/wiki/Man-in-the-middle_attack).

Você pode estar familiarizado com a criptografia Secure Sockets Layer(SSL). O
TLS é simplesmente a próxima progressão do. Em outras palavras, se você estava usando o SSL antes, considere fazer o
upgrade para o TLS. Em geral, recomendamos o Nginx para lidar com o TLS. Para
obter uma boa referência para configurar o TLS no Nginx (e outros servidores), consulte
Configurações
Recomendadas de Servidores (Mozilla Wiki).

Além disso, uma ferramenta útil para obter um certificado TLS
gratuito é a Let’s
Encrypt, uma autoridade de certificação (CA) gratuita,
automatizada, e aberta fornecida pelo
Grupo de Pesquisas de
Segurança da Internet (ISRG).

## Não confiar em entrada do usuário

Para aplicativos web, um dos requisitos de segurança mais críticos é a validação e tratamento adequado dos dados de entrada do usuário. Isto tem muitas formas e não as cobriremos todas aqui.
Em última análise, a responsabilidade de validar e manipular corretamente os tipos de entrada de usuário que seu aplicativo aceita é sua.

### Impedir redirecionamentos abertos

Um exemplo de entrada de usuário potencialmente perigosa é um *open redirect*, onde um aplicativo aceita uma URL como entrada de usuário (muitas vezes na consulta de URL, por exemplo `? rl=https://exemplo.com`) e usa `res.redirect` para definir o cabeçalho `location` e
return um status de 3xx.

Uma aplicação deve validar que suporta redirecionamento para a URL de entrada, para evitar enviar usuários para links maliciosos, como sites de phishing, entre outros riscos.

Aqui está um exemplo de verificar URLs antes de usar `res.redirect` ou `res.location`:

```
app.use((req, res) => {
  try {
    if (new Url(req.query.url).host !== 'example.com') {
      return res.status(400).end(`Unsupported redirect to host: ${req.query.url}`)
    }
  } catch (e) {
    return res.status(400).end(`Invalid url: ${req.query.url}`)
  }
  res.redirect(req.query.url)
})
```

## Use Helmet

O [Helmet](https://www.npmjs.com/package/helmet) pode
ajudar a proteger o seu aplicativo de algumas vulnerabilidades da web
bastante conhecidas configurando os cabeçalhos HTTP adequadamente.

Helmet é uma função middleware que define cabeçalhos de resposta HTTP relacionados à segurança. Helmet define os seguintes cabeçalhos por padrão:

- `Content-Security-Policy`: Uma poderosa lista de permissões do que pode acontecer na sua página, que mitiga muitos ataques
- `Cross-Origin-Opener-Policy`: Ajuda a isolar sua página
- `Cross-Origin-Resource-Policy`: Bloqueia outros de carregar seus recursos entre origens
- `Origin-Agent-Cluster`: Altera o isolamento do processo para ser baseado na origem
- `Referrer-Policy`: controla o cabeçalho [Referer](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Referer)
- `Strict-Transport-Security`: Diz aos navegadores para preferir HTTPS
- `X-Content-Type-Options`: Avoids [MIME sniffing](https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types#mime_sniffing)
- `X-DNS-Prefetch-Control`: Controla o pré-carregamento de DNS
- `X-Download-Options`: Força os downloads a serem salvos (apenas no Internet Explore)
- `X-Frame-Options`: Cabeçalho de legado que mitiga ataques [Clickjacking](https://en.wikipedia.org/wiki/Clickjacking)
- `X-Perting-Cross-Domain-Policies`: Controla o comportamento entre domínios para produtos Adobe, como a Acrobat
- `X-Powered-By`: Informações sobre o servidor web. Removido porque poderia ser utilizado em ataques simples
- `X-XSS-Protection`: Cabeçalho de legado que tenta mitigar [ataques XSS](https://developer.mozilla.org/en-US/docs/Glossary/Cross-site_scripting), mas piora as coisas, então o Helmet desabilita isso

Cada cabeçalho pode ser configurado ou desativado. Para ler mais sobre isso, por favor, vá para [a documentação do site](https://helmetjs.github.io/).

Instale o Helmet como qualquer outro módulo:

```
$ npm install helmet
```

Em seguida use-o no seu código:

```
// ...

const helmet = require('helmet')
app.use(helmet())

// ...
```

## Reduzir impressão digital

Ele pode ajudar a fornecer uma camada extra de segurança para reduzir a capacidade dos invasores de determinar
o software que um servidor usa, conhecido como “impressão digital.” Embora não seja um problema de segurança em si,
reduzir a capacidade de imprimir impressão digital a um aplicativo melhora sua posição geral de segurança.
O software do servidor pode ser impresso por peculiares em como ele responde a solicitações específicas, por exemplo em
os cabeçalhos de resposta HTTP.

Por padrão, o Express envia o cabeçalho de resposta `X-Powered-By` que você pode
desabilitar usando o método `app.disable()`:

```
app.disable('x-powered-by')
```

Observação

Desativar o cabeçalho `X-Powered-By` não impede que um atacante sofisticado determine que um aplicativo está executando o Express. Isso pode
desencorajar uma exploração casual, mas existem outras maneiras de determinar se um aplicativo está executando Express.

Express também envia suas próprias mensagens formatadas “404 Not Found” e erro de formatação
mensagens de resposta. Elas podem ser alteradas por
[adicionando seu próprio manipulador para 404](https://expressjs.com/en/starter/faq.html#how-do-i-handle-404-responses)
e
[escrevendo seu próprio manipulador de erro](https://expressjs.com/en/guide/error-handling.html#writing-error-handlers):

```
// last app.use calls right before app.listen():

// custom 404
app.use((req, res, next) => {
  res.status(404).send("Sorry can't find that!")
})

// custom error handler
app.use((err, req, res, next) => {
  console.error(err.stack)
  res.status(500).send('Something broke!')
})
```

## Use cookies de maneira segura

Para assegurar que os cookies não deixem o seu aplicativo
aberto a ataques, não use o cookie de sessão padrão e configure as
opções de segurança de cookies adequadamente.

Existem dois módulos de middleware principais para sessão de
cookies:

- [express-session](https://www.npmjs.com/package/express-session)
  que substitui o middleware `express.session`
  integrado no Express 3.x.
- [cookie-session](https://www.npmjs.com/package/cookie-session)
  que substitui o middleware `express.cookieSession` integrado no Express 3.x.

A principal diferença entre estes dois módulos é como eles salvam os dados da sessão de cookie. The [express-session](https://www.npmjs.com/package/express-session) middleware stores session data on the server; it only saves the session ID in the cookie itself, not session data. By default, it uses in-memory storage and is not designed for a production environment. In production, you’ll need to set up a scalable session-store; see the list of [compatible session stores](https://github.com/expressjs/session#compatible-session-stores).

Em contrapartida, o middleware [cookie-session](https://www.npmjs.com/package/cookie-session)
implementa um armazenamento apoiado em cookies: ele serializa a sessão inteira para o cookie, ao invés de apenas a chave da sessão.  Use apenas quando os dados da sessão são relativamente pequenos e facilmente codificados como números primitivos(ao invés de objetos). Only use it when session data is relatively small and easily encoded as primitive values (rather than objects). Apesar de navegadores supostamente suportarem pelo menos 4096 bytes por cookie, para assegurar que você não exceda o limite, não exceda
um tamanho de  4093 bytes por domínio. Além disso, esteja ciente de que os dados do cookie serão visíveis para o cliente, portanto se
houver razão para mantê-los seguros ou obscuros, então o express-session pode ser uma escolha melhor.

### Não use o nome do cookie da sessão padrão

Usando o nome do cookie da sessão padrão pode deixar o seu
aplicativo aberto a ataques. O problema de segurança levantado é
parecido ao do `X-Powered-By`: um invasor em
potencial poderia usá-lo para identificar o servidor e direcionar
ataques de acordo com ele.

Para evitar este problema, use nomes de cookie genéricos; por
exemplo usando o middleware [express-session](https://www.npmjs.com/package/express-session):

```
const session = require('express-session')
app.set('trust proxy', 1) // trust first proxy
app.use(session({
  secret: 's3Cur3',
  name: 'sessionId'
}))
```

### Configure as opções de segurança de cookie

Configure as seguintes opções de cookie para aprimorar a
segurança:

- `secure` - Assegura que o navegador só envie o cookie por HTTPS.
- `httpOnly` - Assegura que o cookie seja enviado apenas por HTTP(S), não por cliente JavaScript, ajudando
  assim a se proteger contra ataques de cross-site scripting.
- `domain` - indica o domínio do cookie; use-o para comparação contra o domínio do servidor em que a URL está
  sendo solicitada. Se elas corresponderem, verifique o atributo de caminho em seguida.
- `path` - indica o caminho do cookie; use-o para comparação contra o caminho da solicitação. Se este e o domínio corresponderem, então envie o cookie na solicitação.
- `expires` - use para configurar uma data de
  expiração para cookies persistentes.

Aqui está um exemplo usando o middleware [cookie-session](https://www.npmjs.com/package/cookie-session):

```
const session = require('cookie-session')
const express = require('express')
const app = express()

const expiryDate = new Date(Date.now() + 60 * 60 * 1000) // 1 hour
app.use(session({
  name: 'session',
  keys: ['key1', 'key2'],
  cookie: {
    secure: true,
    httpOnly: true,
    domain: 'example.com',
    path: 'foo/bar',
    expires: expiryDate
  }
}))
```

## Prevent brute-force attacks against authorization

Make sure login endpoints are protected to make private data more secure.

A simple and powerful technique is to block authorization attempts using two metrics:

1. The number of consecutive failed attempts by the same user name and IP address.
2. The number of failed attempts from an IP address over some long period of time. For example, block an IP address if it makes 100 failed attempts in one day.

[rate-limiter-flexible](https://github.com/animir/node-rate-limiter-flexible) package provides tools to make this technique easy and fast. You can find [an example of brute-force protection in the documentation](https://github.com/animir/node-rate-limiter-flexible/wiki/Overall-example#login-endpoint-protection)

## Ensure your dependencies are secure

Using npm to manage your application’s dependencies is powerful and convenient. But the packages that you use may contain critical security vulnerabilities that could also affect your application. The security of your app is only as strong as the “weakest link” in your dependencies.

Since npm@6, npm automatically reviews every install request. Also, you can use `npm audit` to analyze your dependency tree.

```
$ npm audit
```

If you want to stay more secure, consider [Snyk](https://snyk.io/).

Snyk offers both a [command-line tool](https://www.npmjs.com/package/snyk) and a [Github integration](https://snyk.io/docs/github) that checks your application against [Snyk’s open source vulnerability database](https://snyk.io/vuln/) for any known vulnerabilities in your dependencies. Install the CLI as follows:

```
$ npm install -g snyk
$ cd your-app
```

Use this command to test your application for vulnerabilities:

```
$ snyk test
```

### Evitar outras vulnerabilidades conhecidas

Fique atento às recomendações do
Node Security
Project que podem afetar o Express ou outros módulos usados
pelo seu aplicativo. Em geral, o Node Security Project é um excelente
recurso para conhecimento e ferramentas sobre segurança do Node.

Finalmente, os aplicativos do Express - como outros aplicativos web - podem estar vulneráveis a uma variedade de ataques baseados na
web. Familiarize-se com [vulnerabilidades web](https://www.owasp.org/www-project-top-ten/) conhecidas e tome precauções para evitá-las.

## Considerações adicionais

Aqui estão algumas recomendações adicionais da excelente Lista
de Verificação de Segurança do Node.js. Refira-se a esta postagem do blog para obter todos os detalhes destas recomendações:

- Sempre filtrar e limpar a entrada do usuário para se proteger de ataques de cross-site scripting (XSS) e injeção de comando.
- Proteja-se contra ataques de injeção de SQLs usando consultas parametrizadas ou instruções preparadas.
- Use a ferramenta de software livre [sqlmap](http://sqlmap.org/) para detectar
  vulnerabilidades de injeção de SQL no seu aplicativo.
- Use as ferramentas [nmap](https://nmap.org/) e [sslyze](https://github.com/nabla-c0d3/sslyze) para
  testar a configuração das suas cifras SSL, chaves, e renegociação, bem como a validade do seu certificado.
- Use o [safe-regex](https://www.npmjs.com/package/safe-regex) para assegurar que suas expressões regulares não estejam suscetíveis
  a ataques [negação de serviço de expressões regulares](https://www.owasp.org/index.php/Regular_expression_Denial_of_Service_-_ReDoS).

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/pt-br/advanced/best-practice-security.md          )

---

# Desenvolvendo mecanismos de modelo para o Express

> Learn how to develop custom template engines for Express.js using app.engine(), with examples on creating and integrating your own template rendering logic.

# Desenvolvendo mecanismos de modelo para o Express

Use o método `app.engine(ext, callback)`
para criar seu próprio mecanismo de modelo. `ext`
refere-se à extensão do arquivo, e  `callback` é a
função de mecanismo de modelo, que aceita os seguintes itens como
parâmetros: a localização do arquivo, o objeto de opções, e a função
de retorno de chamada.

O código a seguir é um exemplo de implementação de um mecanismo
de modelo muito simples para renderização de arquivos `.ntl`.

```
const fs = require('fs') // this engine requires the fs module
app.engine('ntl', (filePath, options, callback) => { // define the template engine
  fs.readFile(filePath, (err, content) => {
    if (err) return callback(err)
    // this is an extremely simple template engine
    const rendered = content.toString()
      .replace('#title#', `<title>${options.title}</title>`)
      .replace('#message#', `<h1>${options.message}</h1>`)
    return callback(null, rendered)
  })
})
app.set('views', './views') // specify the views directory
app.set('view engine', 'ntl') // register the template engine
```

Seu aplicativo estará agora habilitado a renderizar arquivos `.ntl`. Crie
um arquivo chamado `index.ntl` no diretório
`views` com o seguinte conteúdo.

```pug
#title#
#message#
```

Em seguida, crie a seguinte rota no seu aplicativo.

```
app.get('/', (req, res) => {
  res.render('index', { title: 'Hey', message: 'Hello there!' })
})
```

Ao fazer uma solicitação à página inicial, o `index.ntl` será renderizado como HTML.

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/pt-br/advanced/developing-template-engines.md          )

---

# Health Checks and Graceful Shutdown

> Learn how to implement health checks and graceful shutdown in Express apps to enhance reliability, manage deployments, and integrate with load balancers like Kubernetes.

# Health Checks and Graceful Shutdown

## Graceful shutdown

When you deploy a new version of your application, you must replace the previous version. The process manager you’re using will first send a SIGTERM signal to the application to notify it that it will be killed. Once the application gets this signal, it should stop accepting new requests, finish all the ongoing requests, clean up the resources it used,  including database connections and file locks then exit.

### Exemplo

```
const server = app.listen(port)

process.on('SIGTERM', () => {
  debug('SIGTERM signal received: closing HTTP server')
  server.close(() => {
    debug('HTTP server closed')
  })
})
```

## Health checks

A load balancer uses health checks to determine if an application instance is healthy and can accept requests. For example, [Kubernetes has two health checks](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-probes/):

- `liveness`, that determines when to restart a container.
- `readiness`, that determines when a container is ready to start accepting traffic. When a pod is not ready, it is removed from the service load balancers.

  [Edit this page](https://github.com/expressjs/expressjs.com/edit/gh-pages/pt-br/advanced/healthcheck-graceful-shutdown.md          )
