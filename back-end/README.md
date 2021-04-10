## back-end of Auto-signer

### Quick start
Configure .env first

```dotenv
DB_USER=<USER>
DB_PASS=<PASS>
DB_HOST=<HOSTNAME>
DB_NAME=<DBNAME>
DB_SRV=0  # set to 1 to use mongo+srv://, or else mongo://
```
Then run
```shell
./run_dev.sh
```