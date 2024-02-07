**WIP**

# DSS-Extensions: repositório central

**Este repositório será povoado a partir do período de julho/agosto de 2022. Verifique regularmente ou use o recurso de "Watch" do GitHub para se manter atualizado.**

Este repositório no GitHub será usado para concentrar documentação, discussão, resultados de benchmarks, e arquivos para tradução/i18n dos projetos hospedados na organização DSS-Extensions. *Como lembrete, os projetos aqui hospedados não têm suporte do EPRI.*

As DSS-Extensions foram originalmente criadas para expor o motor oficial do OpenDSS para múltiplas linguagens de programação e múltiplas plataformas/arquiteturas com um mínimo de mudanças. 
Desde de 2019, este objetivo inicial foi alcançado, de forma que o novo objetivo se tornou realizar a modernização da nova biblioteca base (DSS C-API) e adicionar extensões e modificações úseis para o motor do DSS.

Os projetos atualmente hospedados neste organização empregam diversas linguagens (Pascal, C, C++, Python, Julia, C#, MATLAB) e também recebemos pedidos e comentários de usuários interessados em linguagens como Java, Go, e Rust. Desta forma, novas "extensions" poderação ser publicadas futuramente para atender outros usuários.
Para evitar inviabilizar a manutenção de uma das interfaces para uma linguagem específica ao atualizar a biblioteca base, às vezes nós precisamos preservar certos aspectos da implementação atual. Este repositório é o local ideal para levantar preocupações e sugestões sobre tais tópicos.

Vários "issues" de antes de 2022 que estavam nos outros subprojetos foram transferidos para o controle deste repositório central. Mesmo que o texto ainda sugira o subprojeto/linguagem de programação original, estes representam desafios ou tarefas compartilhadas entre todos os subprojetos.

A aba de discussões ("Discussions") foi ativada aqui, mas é importante observar que nossa intenção não é fragmentar a comunidade do OpenDSS. Nós recomendamos pesquisar, verificar e considerar submeter comentários e questões gerais sobre o OpenDSS no fórum oficial, hospedado no SourceForge (se possível, testar com o OpenDSS oficial, via interface gráfica ou API COM, é preferível):
- Fórum de oficial do OpenDSS: https://sourceforge.net/p/electricdss/discussion/
- Documentação oficial do OpenDSS pode ser consultada em https://sourceforge.net/p/electricdss/code/HEAD/tree/trunk/Version8/Distrib/Doc/ e [OpenDSS_COM.chm](https://sourceforge.net/p/electricdss/code/HEAD/tree/trunk/Version8/Distrib/x64/OpenDSS_COM.chm?format=raw) (maioria em inglês)
- Busca melhorada: recomendados empregar um motor de pesquisa como Google com `inurl:https://sourceforge.net/p/electricdss/discussion/` e suas palavras-chave; [exemplo](https://www.google.com/search?q=inurl%3Ahttps%3A%2F%2Fsourceforge.net%2Fp%2Felectricdss%2Fdiscussion%2F+DSS+Extensions).


## Documentação das APIs

Atualmente temos os seguintes sites. Atualmente, maioria apenas em inglês.

- [Documentação do código Pascal da DSS C-API](https://dss-extensions.org/dss-extensions/pascal/): Documentação gerada a partir do código-fonte em Pascal, criada empregando o software PasDoc. Pode ser útil para alguém estudando a implementação do OpenDSS, em especial a nossa implementação. [O diagrama de classes](http://dss-extensions.org/dss-extensions/pascal/GVClasses.svg) é especialmente útil para uma visão geral.
- [Arquivos de cabeçalho DSS C-API e dss.hpp](https://dss-extensions.org/dss_capi/): Documentação gerada a partir dos cabeçalhos/headers C da biblioteca base e da nova biblioteca de cabeçalhos para C++ (ainda em desenvolvimento mas bastante completa), incluindo a API clássica e das mais novas extensões de API.
- [Referência do DSS-Python reference](https://dss-extensions.org/DSS-Python/): Algumas notas gerais e documentação geral da API; além da API clássica, inclui documentação inicial da nova API, atualmente chamada de `Obj`.
- [Referência do DSS Sharp](https://dss-extensions.org/dss_sharp/): Documentação geral da API gerada empregando o software Sandcastle Help File Builder.
- [OpenDSSDirect.jl](https://dss-extensions.org/OpenDSSDirect.jl/stable/): Notas gerais e documentação da API; precisa de algumas atualizações para incluir novos itens.
- [OpenDSSDirect.py](https://dss-extensions.org/OpenDSSDirect.py/): Notas gerais e documentação da API; também precisa de algumas atualizações para incluir novos itens.

Para [DSS_MATLAB](https://github.com/dss-extensions/dss_matlab/), o próprio MATLAB é capaz de gerar documentação através da [função `help`](https://www.mathworks.com/help/matlab/ref/help.html).

## Perguntas frequentes

**1. DSS-Extensions é um projeto brinquedo/experimental?**

**Não.** Este é um conjunto de projetos já com uma boa maturidade. Os principais desenvolvedores e contribuintes são pesquisados e/ou trabalham na área. Realizamos validação cruzada dos resultados do nosso motor DSS frequentemente, e sempre antes do lançamento de uma nova versão da DSS C-API.

Com um grupo, a maioria dos projetos foram consolidados em 2018 e 2019.

É importante lembrar que os códigos/números de versões são arbitrários. Verificar o histórico de um projeto e mesmo seu uso pela comunidade é mais importante que simplesmente observar o número exposto no rótulo da versão. 
Por exemplo, a maioria dos objetivos iniciais da DSS C-API foram alcançados na versão 0.10; como surgiu a oportunidade de complementar e incrementar a biblioteca, o plano atual é lançar uma v1.0 assim que os novos itens sejam integrados e a API de baixo nível (DSS C-API) esteja estável.

**2. Há suporte do EPRI para este projeto?**

**Não.** Caso você precise de suporte oficial do EPRI, considere entrar em contato com a equipe do EPRI.

**3. Este trabalho é baseado no `OpenDSSDirect.DLL` (DCSL) do OpenDSS do EPRI?**

**Não.** Isto é algo citado bastante de forma errada.

Não é necessário instalar o OpenDSS oficial e seus binários para usar DSS-Extensions. Nós recomendamos que os novos usuários tentem seguir os guias e tutoriais oficiais e usem a versão oficial, ao menos até se sentirem confortáveis com o modelo de execução e controle do OpenDSS.

O núcleo do projeto DSS-Extensions é a biblioteca DSS C-API. Ela usa uma interface desenvolvida de forma independente, pensando em alto desempenho, dentro das limitações da estrutura pré-existente do código fonte em Pascal. Nem a DSS C-API nem o grupo DSS-Extensions foi baseado no OpenDSSDirect.DLL/DCSL.

At first, the code was heavily based on the original code from the OpenDSS COM DLL (`OpenDSSengine.DLL`), with many modifications to achieve the initial goals. By doing that, we managed to reach the goal of good compatibility with the COM implementation, sidestepping the many issues we found when trying to do the same using the official `OpenDSSDirect.DLL`. For public data points, consider that several bugs in the projects OpenDSSDirect.py and OpenDSSDirect.jl were automatically addressed when they were migrated from the official OpenDSSDirect.DLL to DSS C-API.

Through the years, most of the code of the **API** was slowly rewritten or refactored to include more error checks, more messages, and reduce code duplication. As of DSS C-API v0.12.x series, a lot of the OpenDSS **engine internals** has been replaced or refactored, so the work that goes into DSS-Extensions is much more than "copy code from EPRI and recompile with Free Pascal". Even the KLUSolve library was rewritten to address our needs, hence the library file is `libklusolvex` in the past few years.

Some historical context is available in https://sourceforge.net/p/electricdss/discussion/861976/thread/525c13df/ and other posts in the official OpenDSS forum.

**4. Why two Python packages, "DSS-Python" and "OpenDSSDirect.py"?**

Mostly for historical reasons.

When DSS C-API was first developed at Unicamp/Brazil, DSS-Python was a requirement to allow platform-independent code. The same Python code was required to run with the official OpenDSS COM DLL, and the our new Python module. If there were any doubts about the results we obtained in our Linux-based cluster, the same batch of scenarios (e.g. thousands of Monte Carlo simulations) would be re-evaluated using the official version on a cluster of Windows desktop machines.

At the point DSS-Python and DSS C-API were publicly announced, OpenDSSDirect.py ("ODD.py" for short) already existed as a project hosted and used at NREL for some time. 

Implementation-wise, there are different set of conventions between the two modules. Mostly, DSS-Python mimics the COM implementation of OpenDSS, using (sometimes abusing) the concept of property to pass data. ODD.py is based on functions instead, and has a more flat organization of modules/classes.

Since 2018 we accrued many users, which can be seen from the PyPI download numbers. In the long term, we plan to keep at least minimal maintenance of the two packages, while providing an alternative, clean-slate package to expose more interesting and modern approaches.

See also https://sourceforge.net/p/electricdss/discussion/beginners/thread/8031cde60e/?limit=25#4aca/5791/8bbb

**5. What are some features from EPRI's OpenDSS not available under DSS-Extensions?**

There is a document at [known_differences](https://github.com/dss-extensions/dss_capi/blob/master/docs/known_differences.md) listing more. Notably:

- DSS-Extensions do not integrate with some of EPRI's Windows-only software, like the plotting tools ("OpenDSS Viewer" and the old `DSSView.exe`), OpenDSS-GIS and others. It seems most of these are also closed-source software.

- A few components were not ported (yet) or removed due to lack of test cases and other concerns. We are always open to revisit those if there are enough requests from users.

- Plotting is not available for all DSS-Extensions. We are implementing a plotting backend under DSS-Python as a proof of concept.

- The diakoptics features are currently disabled. The plan is to reintroduce them soon after some internal changes. Check the issues on the DSS C-API repository for details.

**5. What are some features from DSS-Extensions not available in EPRI's OpenDSS?**

Again, more at [known_differences](https://github.com/dss-extensions/dss_capi/blob/master/docs/known_differences.md). 

At lot of the features below are still being documented.

- Consistent support for Windows, macOS and Linux.

- Consistent support for Intel x86, x86-64, ARM32 (currently armv7) and ARM64 (aarch64).

- Besides the parallel-machine mechanism based on actors from the official OpenDSS, we also allow multiple independent DSS engines in a single process. This enables user-controlled threads and other interest use-cases. Since our PM implementation is based on this concept of independent engines, it tends to present less errors and is more flexible than the official implementation.

- For some components, our engine allows incremental updates to the system Y matrix, which can result in good performance gains.

- A more flexible system for loading load-shape data, which also allows using float32 loadshapes for saving memory.

- A new set of functions to load circuits from ZIP archives.

- Experimental functions to access all DSS data classes, including initial support for exporting JSON-encoded data.

- A lot of feature and configuration toggles, some for maintaining backwards compatibility with older versions or with the official OpenDSS APIs.

- Many new functions to expose some of the missing classes from the COM API, and many functions that were added to due requests from various users.

- More of the engine internals are exposed through APIs. This is required for experts to achieve high performance on some tasks.

**6. Can I please get some examples/documentation?**

Em breve! Esta é uma de nossas prioridades.

**7. Por que `<inserir funcionalidade>` não funciona?**

Algumas recursos são limitados a seguir a implementação oficial, incluindo limitações. Para todo o restante, caso encontre bugs ou comportamentos adversos em geral, por favor considere reportá-los. Caso seja possível compartilhar um caso teste simples, melhor ainda.