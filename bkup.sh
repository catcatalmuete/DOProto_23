source common.sh

COLLECTIONS=("followes" "products" "users")

for collection in "${COLLECTIONS[@]}"; do
  mongoexport --uri $CONNECTION_STRING --collection $collection --out db/$collection.json
done