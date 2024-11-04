
Piper TTS é um serviço que converte texto em áudio utilizando a tecnologia de síntese de fala. Este projeto é baseado em Flask e utiliza a biblioteca Piper para gerar áudio a partir de texto.

## Instalação

Para instalar o serviço Piper TTS, você pode utilizar a template do EasyPanel:



```json
{
  "services": [
    {
      "type": "app",
      "data": {
        "projectName": "piper-tts",
        "serviceName": "piper-tts",
        "source": {
          "type": "image",
          "image": "ggdadds/piper-tts:latest"
        },
        "domains": [
          {
            "host": "$(EASYPANEL_DOMAIN)",
            "port": 5000
          }
        ],
        "env": "FLASK_ENV=development \nAPI_KEY=123456789 \nDELETE_FILE_MINUTES=2",
        "mounts": [
          {
            "type": "volume",
            "name": "output",
            "mountPath": "/app/output"
          }
        ]
      }
    }
  ]
}
```



Aqui está um exemplo de como você pode fazer uma requisição para gerar áudio a partir de texto:

```bash
curl -X POST http://localhost:5000/audio \
     -H "Content-Type: application/json" \
     -H "x-api-key: sua_chave_aqui" \
     -d '{
           "texto": "Olá, este é um teste de geração de áudio.",
           "saida": "teste_audio",
           "voz": "faber",
           "base64": "false",
           "formato": "mp3"
         }'

```




### Descrição do JSON
- **x-api-key**: apikey setado na env do projeto
- **texto**: O texto que será convertido em áudio.
- **saida**: O nome do arquivo de saída (sem extensão).
- **voz**: Voz escolhida (faber ou edresson).
- **base64**: Define se o áudio gerado deve ser retornado como uma string Base64. Use `"true"` para ativar e `"false"` para desativar.
- **formato**: Formato do arquivo de áudio (como mp3 ou wav).




### Melhorias que serão adicionadas


- Criar um serviço para apagar os audios que foram gerados e estão dentro do tempo configurado para serem apagados ou que foram gerados, mas por algum motivo não foram apagados conforme planejado;

- Criar um cadastro de usuario com senha e autenticação por token na api;

- Criar um painel administrativo web onde é possível visualizar os logs do servidor e definir configurações;

- No painel administrativo o usuário pode visualizar suas solicitações e baixar o arquivo caso ainda não esteja apagado;

- No painel administrativo o usuário pode definir configurações como tempo de vida do arquivo a ser gerado, webhook para enviar o arquivo após ser gerado e outras configurações;

- [USUÁRIO-SENHA-TOKEN] Criar uma rota para enviar o texto e retornar o audio, após isto ser apagado;

- [USUÁRIO-SENHA-TOKEN] Criar uma rota para enviar o texto e retornar o audio e seu respectivo id, mas sem ser apagado. Definir um tempo para ser apagado;

- [USUÁRIO-SENHA-TOKEN] Criar uma rota para enviar o texto e retornar o id do audio a ser gerado, não apagar o audio. Definir um tempo para ser apagado;

- [USUÁRIO-SENHA-TOKEN] Criar uma rota para buscar um audio a partir de um id gerado pela rota anterior;

- [USUÁRIO-SENHA-TOKEN] Criar uma rota para enviar o texto e retornar o id do audio a ser gerado, assim como enviar o webhook que deve ser acionado assim que o audio for gerado para enviar o arquivo;

