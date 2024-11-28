# B3 Data API e Frontend

Este projeto consiste em uma API que fornece dados da B3 e uma interface web para visualização dos dados.

## Estrutura do Projeto

- `gerador_dados_b3_json_csv.py`: API Flask que fornece dados da B3
- `index.html`: Interface web para visualização dos dados
- `requirements.txt`: Dependências Python necessárias

## Instruções de Deploy

### Deploy da API (Python Anywhere)

1. Crie uma conta em [Python Anywhere](https://www.pythonanywhere.com)
2. Vá para a seção "Web" e crie uma nova aplicação web
3. Escolha Flask e Python 3.8
4. Na seção "Files", faça upload dos arquivos:
   - `gerador_dados_b3_json_csv.py`
   - `requirements.txt`
5. No console Bash, execute:
   ```bash
   pip3 install --user -r requirements.txt
   ```
6. Configure o arquivo WSGI (`/var/www/yourusername_pythonanywhere_com_wsgi.py`):
   ```python
   import sys
   path = '/home/yourusername/mysite'
   if path not in sys.path:
       sys.path.append(path)
   
   from gerador_dados_b3_json_csv import app as application
   ```
7. Reinicie a aplicação web

### Deploy do Frontend (GitHub Pages)

1. Crie um novo repositório no GitHub
2. Faça upload do arquivo `index.html`
3. Vá para Settings > Pages
4. Selecione a branch main e a pasta root
5. Ative o GitHub Pages

## Configuração após Deploy

Após o deploy, atualize a URL da API no arquivo `index.html`:

```javascript
fetch('https://seuusername.pythonanywhere.com/api/b3-data')
```

## Notas de Segurança

- Configure CORS apropriadamente na API para permitir apenas domínios confiáveis
- Considere adicionar rate limiting na API
- Mantenha as dependências atualizadas
