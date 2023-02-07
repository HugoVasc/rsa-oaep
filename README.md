# Trabalho 2 - Segurança Computacional

Aluno: Hugo Silva de Vasconcelos
Matrícula: 18/0102028

## Definições

### RSA

É um algoritmo de criptografia assimétrica que permite que mensagens sejam codificadas com uma chave e decodificadas com uma outra chave distinta. O algoritmo utiliza duas chaves: uma chave pública, conhecida por todos, e uma chave privada, conhecida apenas pelo destinatário. O remetente codifica a mensagem usando a chave pública, e o destinatário a decodifica usando sua chave privada, ou vice-versa. As chaves são relacionadas entre si por um método matemático que, tendo conhecimento de apenas uma chave, a probabilidade de se descobrir a outra é próxima de 0. A segurança do algoritmo é baseada na dificuldade na geração e fatoração de números grandes originados a partir de números primos.

### RSA-OAEP

O RSA-OAEP (Optimal Asymmetric Encryption Padding) é uma versão do algoritmo RSA de criptografia que inclui um processo de preenchimento (padding) ótimo para aumentar a segurança da criptografia. Em vez de simplesmente codificar a mensagem, o RSA-OAEP adiciona informações extras (preenchimento) antes da codificação com o objetivo de tornar a mensagem mais difícil de ser decifrada por atacantes. Além disso, o RSA-OAEP inclui uma função hash para garantir a integridade da mensagem e uma função de preenchimento (padrão) para ajudar a impedir ataques. Em resumo, o RSA-OAEP é uma versão mais segura do algoritmo RSA para criptografia de chave pública.

