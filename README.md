
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
