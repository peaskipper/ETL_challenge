#### Pre-requisite
# Adls storage account is setup and access is granted using IAM or service princial 

# Store configs in case of access through service principal

# configs_spn = {
#     "client.id": dbutils.secrets.get(scope="scope_name", key="client_id"),
#     "client.secret": dbutils.secrets.get(scope="scope_name", key="client_secret"),
#     "client.endpoint": dbutils.secrets.get(scope="scope_name", key="tenant_id"),
# }

# Store configs for adls location
storage_account = "adls_storage_account_name_dev_001"
container_name = "adls_raw_container_dev_001"
path = "/raw/ext_tbl/usecase/"

