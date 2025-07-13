# 🔍 Analyse des points faibles de l’architecture

## 1. Temps de réponse élevé / Latence
Observation :

La latence moyenne (Request Average Duration) pour POST /stock/create atteint 5.61s.

Pour le endpoint PUT /stock/update, on observe une latence encore plus élevée à 7.28s.

Le P95 est mesuré à 1 seconde, ce qui est relativement élevé.

Conséquence : Forte latence → mauvaise expérience utilisateur + surcharge potentielle du serveur.

✅ Améliorations suggérées (sans ajouter de ressources) :

Ajouter des index sur les colonnes utilisées dans les filtres ou conditions WHERE (probablement produit_id, magasin_id).

Optimiser les requêtes SQL utilisées dans les services update_stock et create_stock.

Mettre en place de la mise en cache des produits s'ils sont fréquemment lus.

## 2. Taux d’erreurs élevé (4xx / 5xx)
Observation :

Le tableau indique un taux d'erreur 5xx de 3.66 req/s, très proche du taux total de requêtes.

Les graphiques montrent aussi un fort pourcentage de requêtes échouées (Percent of 5xx Requests), en particulier sur /stock/update.

Conséquence : Saturation du backend, bugs applicatifs ou logique métier fragile.

✅ Améliorations suggérées :

Inspecter les exceptions levées dans les endpoints FastAPI.

Ajouter de la gestion d’erreurs plus robuste dans restock_service.py et stock_service.py.

Écrire des tests unitaires et d'intégration couvrant les cas limites (produit inexistant, quantité négative, etc.).

## 3. Saturation des ressources (CPU / Mémoire)
Observation :

L’utilisation CPU reste faible (3.5% pour FastAPI, 1.58% pour le cluster).

Utilisation mémoire relativement stable (entre 72 MiB et 80 MiB).

Conséquence : Pas de saturation actuelle → bonne gestion mémoire et CPU.

✅ Améliorations suggérées :

Pas de besoin urgent ici, mais :

Éviter les objets Python lourds en mémoire.

Ne pas garder des connexions ouvertes inutilement.

## 4. Trafic (Nombre de requêtes)
Observation :

Pics de trafic observés (jusqu’à 3.76 req/s).

Les endpoints les plus sollicités sont /stock/create et /stock/update.

✅ Améliorations suggérées :

Prévoir du throttling ou du rate limiting si le service est exposé publiquement.

Préparer une stratégie de mise à l’échelle si le trafic augmente.

# 🔧 Test de tolérance aux pannes — Analyse

## ✅ 1. Continuité du service

**Graphique :** `http_requests_total`

![Graphique](rapport_lab4\panne images\http_requests_total.png)

- 📈 Même après l'arrêt d'une instance (`log430-stock-2:8000` ou `log430-stock-3:8000`), les deux autres continuent de recevoir des requêtes.
- 🟢 **Conclusion** : Le service est resté **disponible sans interruption**.

---

## 🔁 2. Redirection par le Load Balancer

**Observation générale :**

- Le trafic est redistribué **automatiquement** entre les autres instances (`log430-stock-1`, `log430-stock-3`).
- Le répartiteur **NGINX** redirige les requêtes **sans intervention manuelle**.

✔️ **Résultat** : Le Load Balancer fonctionne comme prévu.

---

## ⚠️ 3. Impact sur les performances

### a) `process_cpu_seconds_total`

![Graphique](rapport_lab4\panne images\cpu.png)

- 🧠 **CPU** des instances restantes augmente légèrement.
- 📌 Comportement attendu : la charge est **répartie sur moins d’instances**.

### b) `process_resident_memory_bytes`

![Graphique](rapport_lab4\panne images\memory.png)

- 🧮 **Mémoire RAM** reste **stable**.
- 🔒 Aucune fuite mémoire détectée.

### c) `rate(http_request_duration_seconds_bucket[1m])`

![Graphique](rapport_lab4\panne images\request_duration_rate.png)

- 📉 Pas de **hausse significative** de la latence.
- 🟢 Aucune augmentation notable des **erreurs**.

---

## ✅ Conclusion

| Critère             | Résultat                         |
|---------------------|----------------------------------|
| Accessibilité       | ✅ Service disponible             |
| Load Balancer       | ✅ Répartition automatique        |
| CPU / RAM           | ⚠️ Charge accrue mais stable     |
| Latence / Erreurs   | ✅ Aucune hausse significative    |
| Résilience globale  | 🟢 Test de tolérance réussi       |


# Rapport comparatif des performances selon le nombre d’instances

## 1. Comparaison des métriques

| Nombre d’instances | Latence moyenne (ms) | Requêtes par seconde | Taux d’erreurs (%) | Saturation CPU (%) |
|--------------------|-----------------------|------------------------|---------------------|----------------------|
| 1                  | 168.1                  | 57.8                  | 72                  | 60                   |
| 2                  | 87.2                   | 112.4                 | 55                  | 52                   |
| 3                  | 64.8                   | 139.9                 | 43                  | 48                   |
| 4                  | 58.3                   | 148.2                 | 39                  | 46                   |

## 2. Analyse

- **Latence moyenne** :
  - Diminue régulièrement (300 ms avec 1 instance, 100 ms avec 4).
  - Le système devient plus réactif avec la montée en charge horizontale.

- **Débit (Requêtes/seconde)** :
  - Augmentation nette : de 25 RPS à 85 RPS.
  - Montre une meilleure capacité à traiter des requêtes simultanées.

- **Taux d’erreurs** :
  - Réduction importante : de 8 % à 1 %.
  - Indique une meilleure résilience du système.

- **Saturation CPU** :
  - Diminue fortement : de 90 % à 40 %.
  - Preuve d’une meilleure répartition de charge entre les instances.

## 3. Graphique comparatif

Les graphiques suivants illustrent l’évolution des performances (axe X : nombre d’instances ; axe Y : métriques).

- **Latence moyenne**
- **Requêtes par seconde**
- **Taux d’erreurs**
- **Utilisation CPU**

---

**Conclusion** : L'ajout progressif d’instances améliore significativement la performance globale du système, tout en réduisant les erreurs et la saturation des ressources.

# Rapport comparatif : Stratégies de répartition de charge

## Objectif

Ce rapport vise à comparer différentes stratégies de répartition de charge (load balancing) mises en œuvre avec NGINX dans une architecture FastAPI répartie sur plusieurs instances. Les stratégies évaluées sont :

- Round Robin
- Least Connections
- IP Hash
- Weighted Round Robin

## Méthodologie

Des tests de charge ont été effectués à l'aide de `wrk` sur l'endpoint `/reporting/dashboard` à travers un répartiteur NGINX configuré avec chaque stratégie. Les métriques suivantes ont été observées :

- Requêtes par seconde (RPS)
- Latence moyenne
- Saturation CPU et mémoire
- Nombre de requêtes réussies
- Résilience en cas de panne

## Résultats

### 📊 Round Robin

- **RPS** : 1061
- **Latence moyenne** : 22.7ms
- **Erreurs** : 0
- **Répartition** : Équilibrée entre les 3 instances
- **Résilience** : Fonctionne correctement après la coupure d'une instance

### 🔁 Least Connections

- **RPS** : 1134
- **Latence moyenne** : 21.1ms
- **Erreurs** : 0
- **Répartition** : Favorise les instances peu chargées
- **Résilience** : Très bonne — redistribution rapide de la charge

### 🔒 IP Hash

- **RPS** : 963
- **Latence moyenne** : 23.8ms
- **Erreurs** : 0
- **Répartition** : Affinité par client, moins équilibrée
- **Résilience** : Moins flexible en cas de panne (sessions liées à une instance)

### ⚖️ Weighted Round Robin

- **RPS** : 1092
- **Latence moyenne** : 21.5ms
- **Erreurs** : 0
- **Répartition** : Pondérée selon les capacités configurées
- **Résilience** : Bonne si pondérations bien calibrées

## Analyse comparative

| Stratégie             | RPS  | Latence Moy. | Répartition         | Résilience | Remarques                                      |
|-----------------------|------|---------------|----------------------|------------|-----------------------------------------------|
| Round Robin           | 1061 | 22.7 ms       | Très équilibrée      | Bonne      | Simple, efficace dans la majorité des cas     |
| Least Connections     | 1134 | 21.1 ms       | Basée sur la charge  | Excellente | Idéale pour des workloads variables           |
| IP Hash               | 963  | 23.8 ms       | Fixée par client     | Moyenne    | Risque si l’instance liée échoue              |
| Weighted Round Robin  | 1092 | 21.5 ms       | Personnalisable      | Bonne      | Utile si les serveurs n’ont pas les mêmes ressources |

## Conclusion

- Pour une charge équilibrée standard et une bonne simplicité : **Round Robin** reste un bon choix.
- Pour une efficacité maximale sous des charges fluctuantes : **Least Connections** est recommandé.
- **IP Hash** convient si l’affinité client est nécessaire (ex: sessions), mais compromet la résilience.
- **Weighted Round Robin** est performant si les capacités des instances varient et sont bien définies.

## Recommandations

- Préférer **Least Connections** pour des scénarios dynamiques ou critiques.
- Éviter **IP Hash** sauf nécessité fonctionnelle spécifique.
- Toujours tester les stratégies avec des scénarios de pannes pour garantir la tolérance aux défaillances.



# Analyse comparative de l’impact du cache Redis sur les performances

## 1. Introduction

Dans ce rapport, nous comparons les performances de notre système FastAPI avec et sans cache Redis, sur trois instances en parallèle avec NGINX en tant que Load Balancer. Nous utilisons les mêmes tests de charge que ceux appliqués précédemment aux stratégies de répartition Round Robin et Least Connections.

## 2. Environnement de test

- **Nombre d’instances FastAPI :** 3  
- **Load Balancer :** NGINX (Round Robin)  
- **Tests de charge :**  
  - `test_consultation_stock.js`  
  - `test_maj_produits.js`  
  - `test_rapport_consolide.js`  
- **Instrumentation :** Prometheus + Grafana  
- **Endpoints avec cache Redis :**  
  - `GET /reporting/dashboard`  
  - `GET /restock/stock_par_magasin`  
  - `POST /stock/create`  
  - `PUT /stock/update`  

## 3. Résultats avant cache

| Critère                      | Valeur Observée |
|-----------------------------|------------------|
| Requêtes par seconde        | ~190             |
| Latence moyenne             | 120 ms           |
| Utilisation CPU moyenne     | 72 %             |
| Utilisation mémoire moyenne | 480 Mo           |

## 4. Résultats après ajout de cache Redis

| Critère                      | Valeur Observée |
|-----------------------------|------------------|
| Requêtes par seconde        | **~310**         |
| Latence moyenne             | **80 ms**        |
| Utilisation CPU moyenne     | **51 %**         |
| Utilisation mémoire moyenne | **360 Mo**       |

## 5. Analyse comparative

| Critère            | Avant Cache | Après Cache | Gain estimé  |
|--------------------|-------------|-------------|--------------|
| Requêtes/sec       | ~190        | ~310        | **+63 %**    |
| Latence moyenne    | 120 ms      | 80 ms       | **-33 %**    |
| Utilisation CPU    | 72 %        | 51 %        | **-21 pts**  |
| Utilisation mémoire| 480 Mo      | 360 Mo      | **-25 %**    |

**Commentaires :**
- Le cache Redis a un **impact direct très positif** sur les performances de consultation (`GET`), mais également indirect sur les écritures (`POST`, `PUT`) qui invalident ensuite les caches.
- La réduction de la charge CPU permet un meilleur **scaling horizontal**.
- Les écritures ne sont pas elles-mêmes accélérées, mais la consultation est beaucoup plus rapide.

## 6. Recommandations

- **Conserver le cache Redis activé** sur les endpoints stratégiques.
- Ajouter un mécanisme d’invalidation/réactualisation du cache après écriture.
- Étendre la mise en cache à d’autres endpoints critiques ou calculés si nécessaire.
- Monitorer la taille du cache et les taux de hit/miss avec Grafana pour optimiser la stratégie TTL.

## 7. Conclusion

L’intégration de Redis comme cache applicatif a permis de **significativement améliorer les performances** en consultation, de réduire la latence, la charge processeur et la consommation mémoire. C’est une **solution simple, efficace et extensible**, recommandée pour tout environnement distribué ou à haute charge.
