[![build status](https://travis-ci.org/wvoliveira/inleads.svg?branch=master)](https://travis-ci.org/wvoliveira/inleads)

InLeads
-------

Simplesmente coleta dados do banco SQL Server e joga no console.  
No caso, estamos utilizando para o logstash coletar essas informações e jogar no Elasticsearch.  

How to
-----

Download e configure
```bash
git clone https://github.com/wvoliveira/inleads.git
cp conf/example.ini conf/own.ini
```
 
Altere o arquivo conf/own.ini conforme suas credenciais de acesso, nível de log e procedures que serão executadas:
```
[sql_conf]
conf = name_section in /etc/odbc.ini
database = database
user = user
pass = pass

[logging]
level = INFO
file = /var/log/inleads.log

[procedures]
nome = EXEC dbo.PROCEDURE
```

Agora só rodar:
```bash
./inleads.py -c conf/own.ini
```

Os logs não vão para o console, então fique de olho no arquivo de log. Fiz isso, pois por padrão o resultado das procedures já vão para o console.
