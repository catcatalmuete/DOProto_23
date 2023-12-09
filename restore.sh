source common.sh

COLLECTIONS=("followes" "products" "users")

for collection in "${COLLECTIONS[@]}"; do
  mongoimport --uri $CONNECTION_STRING --collection $collection --file db/$collection.json --jsonArray
done