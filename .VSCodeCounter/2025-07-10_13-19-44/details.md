# Details

Date : 2025-07-10 13:19:44

Directory c:\\Users\\ludok\\Documents\\ETS\\Été2025\\LOG430 - Architecture logicielle\\LOG430-Lab0

Total : 52 files,  1800 codes, 193 comments, 603 blanks, all 2596 lines

[Summary](results.md) / Details / [Diff Summary](diff.md) / [Diff Details](diff-details.md)

## Files
| filename | language | code | comment | blank | total |
| :--- | :--- | ---: | ---: | ---: | ---: |
| [.github/workflows/pipeline.yml](/.github/workflows/pipeline.yml) | YAML | 71 | 0 | 21 | 92 |
| [.pylintrc](/.pylintrc) | Ini | 24 | 0 | 6 | 30 |
| [Dockerfile](/Dockerfile) | Docker | 9 | 6 | 9 | 24 |
| [README.md](/README.md) | Markdown | 204 | 0 | 114 | 318 |
| [api/\_\_init\_\_.py](/api/__init__.py) | Python | 0 | 0 | 1 | 1 |
| [api/auth.py](/api/auth.py) | Python | 10 | 0 | 4 | 14 |
| [api/reporting\_routes.py](/api/reporting_routes.py) | Python | 25 | 20 | 9 | 54 |
| [api/restock\_routes.py](/api/restock_routes.py) | Python | 23 | 21 | 8 | 52 |
| [api/schemas.py](/api/schemas.py) | Python | 27 | 0 | 6 | 33 |
| [api/stock\_route.py](/api/stock_route.py) | Python | 50 | 28 | 12 | 90 |
| [data\_access\_layer/\_\_init\_\_.py](/data_access_layer/__init__.py) | Python | 0 | 0 | 1 | 1 |
| [data\_access\_layer/database.py](/data_access_layer/database.py) | Python | 8 | 5 | 6 | 19 |
| [data\_access\_layer/init\_db.py](/data_access_layer/init_db.py) | Python | 5 | 1 | 3 | 9 |
| [data\_access\_layer/models.py](/data_access_layer/models.py) | Python | 30 | 5 | 11 | 46 |
| [data\_access\_layer/product\_dao.py](/data_access_layer/product_dao.py) | Python | 41 | 11 | 16 | 68 |
| [data\_access\_layer/schema.py](/data_access_layer/schema.py) | Python | 28 | 5 | 5 | 38 |
| [data\_access\_layer/seed\_db.py](/data_access_layer/seed_db.py) | Python | 28 | 3 | 5 | 36 |
| [docker-compose.yaml](/docker-compose.yaml) | YAML | 59 | 0 | 10 | 69 |
| [docs/ADR/ADR-BD.md](/docs/ADR/ADR-BD.md) | Markdown | 14 | 0 | 9 | 23 |
| [docs/ADR/ADR-Separation.md](/docs/ADR/ADR-Separation.md) | Markdown | 15 | 0 | 9 | 24 |
| [docs/UML/class\_diagram.puml](/docs/UML/class_diagram.puml) | PlantUML | 41 | 0 | 9 | 50 |
| [docs/UML/deployment.puml](/docs/UML/deployment.puml) | PlantUML | 24 | 0 | 6 | 30 |
| [docs/UML/implementation.puml](/docs/UML/implementation.puml) | PlantUML | 32 | 0 | 10 | 42 |
| [docs/UML/sequence\_diagrams/annulation\_vente.puml](/docs/UML/sequence_diagrams/annulation_vente.puml) | PlantUML | 12 | 0 | 1 | 13 |
| [docs/UML/sequence\_diagrams/enregistrer\_vente.puml](/docs/UML/sequence_diagrams/enregistrer_vente.puml) | PlantUML | 11 | 0 | 1 | 12 |
| [docs/UML/sequence\_diagrams/recherche\_produit.puml](/docs/UML/sequence_diagrams/recherche_produit.puml) | PlantUML | 10 | 0 | 1 | 11 |
| [docs/UML/sequence\_diagrams/restock.puml](/docs/UML/sequence_diagrams/restock.puml) | PlantUML | 19 | 0 | 4 | 23 |
| [docs/UML/sequence\_diagrams/tableau\_de\_bord.puml](/docs/UML/sequence_diagrams/tableau_de_bord.puml) | PlantUML | 17 | 0 | 4 | 21 |
| [docs/UML/sequence\_diagrams/voir\_stock.puml](/docs/UML/sequence_diagrams/voir_stock.puml) | PlantUML | 12 | 0 | 1 | 13 |
| [docs/UML/use\_cases.puml](/docs/UML/use_cases.puml) | PlantUML | 22 | 0 | 5 | 27 |
| [hello\_world.py](/hello_world.py) | Python | 20 | 5 | 7 | 32 |
| [k6/test\_consultation\_stock.js](/k6/test_consultation_stock.js) | JavaScript | 16 | 0 | 3 | 19 |
| [k6/test\_maj\_produits.js](/k6/test_maj_produits.js) | JavaScript | 54 | 2 | 12 | 68 |
| [k6/test\_rapport\_consolide.js](/k6/test_rapport_consolide.js) | JavaScript | 13 | 0 | 3 | 16 |
| [k6/test\_stress.js](/k6/test_stress.js) | JavaScript | 37 | 0 | 9 | 46 |
| [logger.py](/logger.py) | Python | 7 | 1 | 4 | 12 |
| [nginx.conf](/nginx.conf) | Properties | 20 | 0 | 5 | 25 |
| [presentation\_layer/\_\_init\_\_.py](/presentation_layer/__init__.py) | Python | 0 | 0 | 1 | 1 |
| [presentation\_layer/main.py](/presentation_layer/main.py) | Python | 32 | 2 | 9 | 43 |
| [prometheus/prometheus.yml](/prometheus/prometheus.yml) | YAML | 15 | 0 | 4 | 19 |
| [rapport.md](/rapport.md) | Markdown | 192 | 0 | 111 | 303 |
| [requirements.txt](/requirements.txt) | pip requirements | 79 | 0 | 0 | 79 |
| [service\_layer/\_\_init\_\_.py](/service_layer/__init__.py) | Python | 0 | 0 | 1 | 1 |
| [service\_layer/reporting\_service.py](/service_layer/reporting_service.py) | Python | 120 | 9 | 25 | 154 |
| [service\_layer/restock\_service.py](/service_layer/restock_service.py) | Python | 47 | 18 | 14 | 79 |
| [service\_layer/stock\_service.py](/service_layer/stock_service.py) | Python | 58 | 8 | 18 | 84 |
| [tests/\_\_init\_\_.py](/tests/__init__.py) | Python | 0 | 0 | 1 | 1 |
| [tests/test\_dao.py](/tests/test_dao.py) | Python | 47 | 7 | 14 | 68 |
| [tests/test\_endpoints.py](/tests/test_endpoints.py) | Python | 46 | 12 | 16 | 74 |
| [tests/test\_reporting\_service.py](/tests/test_reporting_service.py) | Python | 45 | 8 | 13 | 66 |
| [tests/test\_restock\_service.py](/tests/test_restock_service.py) | Python | 39 | 6 | 11 | 56 |
| [tests/test\_stock\_service.py](/tests/test_stock_service.py) | Python | 42 | 10 | 15 | 67 |

[Summary](results.md) / Details / [Diff Summary](diff.md) / [Diff Details](diff-details.md)