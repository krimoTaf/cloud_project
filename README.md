# Projet Cloud avec Amazon Web Services


### Sommaire
1. [Presentation du projet](#pres_projet)

2. [Presentation de Amazon Web Services](#pres_aws)

3. [Pourquoi avoir choisi Amazon Web Services](#why_aws)

4. [Configuration du projet **Docker** & Flask **WSGI Server (Gunicorn)**](#conf_docker)

5. [Création de compte AWS et ajout d'un utilisateur avec les droit nécessaire et les clé d'access AWS](#iam)

6. [Utilisation et configuration de Amazon Cloud Compute Service (EC2)](#ec2)

7. [Utilisation et configuration de Amazon Relational Databases Service (RDS)](#rds)

8. [Utilisation et configuration de Amazon Simple Storage Service (S3)](#s3)

9. [Application Flask et base de donnée Postgresql](#app)


<br /><br /><br />

## Presentation du projet <a id="pres_projet"></a>
Ce projet consiste a heberger une application **Flask** sur le cloud de **Amazon Web Service**, l'applicaiton consiste on system de Blog ou chaque personne pourra crée un compte pour publier un Poste, commenter et mettre un j'aime a d'autre publication.

L'application est connecter a une base de donnée **Postgresql** et deployer via un contenaire **Docker**.

Ce projet vise à héberger une application **Flask** sur le **cloud d'Amazon Web Services**. L'application consiste en un système de blog permettant à chaque personne de créer un compte pour publier des articles, commenter et apprécier les publications des autres utilisateurs.

L'application est connectée à une base de données **Postgresql** et est déployée via un conteneur **Docker** pour garantir une meilleure portabilité et une facilité de déploiement sur différentes plates-formes.


![The cloud blog project ](cloud_project.png)

Les technologies suivantes ont ete utiliser :

- Docker
    - Image Nginx
        - container Nginx avec un loadbalancer qui lance deux instance de notre applicaiton Flask
    - Image Python
        - Configuration de l'application Flask et des variables d'environement
- Python
    - Flask
    - Gunicorn server
    - Markdown converter
    - Faker pour peuplé notre base de donnée avec des donnée aléatoire
    - Pyshorteners to create short link from AWS S3
- Bootstrap
- Javascript (Ajax)
- Amazon Relational Databases Service (RDS)
    - Base de donnée Postgresql
    - Accessible uniquement notre instance EC2
- Amazon Cloud Compute Service (EC2)
    - Serveur Linux Ubuntu
    - Accees SSH
    - Installation de Docker
- Amazon Simple Storage Service (S3)
    - Pour stoker les images des utilisateures (les Avatars et les Images des postes) apres compression avec Python

<br /><br />

## Presentation de Amazon Web Services <a id="pres_aws"></a>

Amazon Web Services (AWS) est une plateforme de services cloud proposée par Amazon, qui offre des solutions d'Infrastructure-as-a-Service (IaaS), de Plateforme-as-a-Service (PaaS) et de Software-as-a-Service (SaaS). Elle fournit une large gamme de services pour héberger des applications et des données sur le cloud.

Les services IaaS proposés par AWS comprennent des solutions de calcul, de stockage, de réseau, de base de données, de sécurité, d'analyse, d'Internet des objets (IoT) et d'apprentissage automatique, qui permettent aux clients d'AWS de bénéficier de la mise à l'échelle rapide de leurs ressources informatiques, de réduire les coûts d'infrastructure et d'améliorer leur agilité commerciale.

Les services PaaS d'AWS offrent aux clients une plateforme pour développer, exécuter et gérer leurs applications sans avoir à se soucier de l'infrastructure sous-jacente. AWS Elastic Beanstalk et AWS Lambda sont des exemples de services PaaS d'AWS.

Les services SaaS proposés par AWS comprennent des applications logicielles prêtes à l'emploi, telles que des solutions de messagerie et de collaboration, de gestion de la relation client, de gestion de projet et de gestion des ressources humaines, qui peuvent être utilisées directement par les entreprises sans avoir à installer ou à gérer de logiciels supplémentaires.

En résumé, AWS est une plateforme de services cloud fiable, flexible et évolutive, qui offre une infrastructure cloud puissante pour aider les entreprises à développer et à gérer leurs applications et leurs données en toute sécurité, avec des options IaaS, PaaS et SaaS pour répondre aux besoins de tous les types d'entreprises.

Amazon Web Services (AWS) a été lancé en 2006 par Amazon en réponse à la nécessité de disposer d'une infrastructure évolutive et rentable pour gérer sa propre activité de commerce électronique. AWS a commencé par offrir des services de stockage et de calcul sur le cloud, mais a rapidement élargi sa gamme de services pour inclure des solutions de réseau, de base de données, de sécurité, de machine learning et bien d'autres.

En 2008, AWS a introduit Amazon Elastic Compute Cloud (EC2), qui est rapidement devenu l'un des services les plus populaires d'AWS. En 2010, AWS a lancé Amazon Virtual Private Cloud (VPC), permettant aux clients de créer un réseau privé virtuel dans le cloud. AWS a également introduit Amazon S3 et Amazon RDS cette même année.

Au fil des ans, AWS a continué à innover en lançant de nouveaux services tels que AWS Lambda, qui permet aux développeurs de créer des applications serverless, et Amazon Aurora, une base de données relationnelle hautement disponible et évolutive.

Aujourd'hui, AWS est le leader du marché des services cloud et fournit des solutions d'infrastructure et de plateforme pour des milliers d'entreprises dans le monde entier, des startups aux grandes entreprises en passant par les gouvernements et les organisations à but non lucratif.

<br /><br />

## Pourquoi avoir choisi Amazon Web Services <a id="why_aws"></a>

AWS est effectivement le leader du marché des fournisseurs de cloud computing et est actuellement la technologie la plus demandée dans le domaine de l'informatique. Selon les données du marché, AWS possède une part de marché d'environ 34% en Q4 2022 [source](https://www.crn.com.au/news/cloud-market-share-q4-2022-microsoft-and-google-gain-on-aws-590641#:~:text=For%20example%2C%20AWS%20market%20share,share%20growth%20year%20over%20year.), ce qui est bien plus élevé que celle de ses concurrents, notamment Azure de Microsoft et Google Cloud.

En plus de sa longue expérience dans le domaine, AWS propose également le plus grand nombre de services et de fonctionnalités parmi les fournisseurs cloud, avec plus de 200 services disponibles.

Enfin beaucoup d'opportunité de travail s'offre à vous, en ayant une bonne maîtrise d'AWS, le marché du cloud augmente et avec lui les parts de marché d'Amazon et différentes opportunités.

<br/><br/>

## Configuration du projet **Docker** - **Nginx** - **Flask** - **Gunicorn** <a id="conf_docker"></a>


Afin d'etre le plus portable possible, j'ai utiliser **Docker** afin de configurer toutes mon application sous un container pret a etre deployer.

### Image Docker

Afin de servire notre application, j'ai utiliser un serveur **Nginx** avec l'image __nginx__, puis une image Python qui est la __python:3-alpine__ .

Tous ca configurer via un **Dockerfile** qui permets d'installer les dependances nessaicaire.

Pour Python un fichier requirement.txt a ete crée afin d'installer les packages tell que :
 - Flask
 - Gunicorn : serveur de production pour une application Flask

### Dockerfile

#### Dockerfile Applicaiton Flask

Le Dockerfile de notre applicaiton Flask nous permets d'installer les dependance et de lancer notre applicaiton. Chose importante dnous recuperons des informations sensible de connexion a la base de donnée et a notre bucket S3 via des variables d'environement preconfigurer sur notre serveur que nous envoyons a notre container via la configuration de notre fichier DockerCompose que nous verons plus bas.

```
FROM python:3-alpine

# Create app directory
WORKDIR /app

# Install app dependencies
COPY requirements.txt ./

RUN pip install -r requirements.txt

# Bundle app source
COPY . .

CMD flask --app tcb init-db;gunicorn -w 4 -b 0.0.0.0:5000 'tcb:create_app()'



EXPOSE 3000
```

#### Dockerfile Nginx serveur

Rien de special dans notre fichier Dockerfile pour le serveur Nginx, nous nous assurons simplement de charger le bon fichier de configuration **nginx.conf**

```
FROM nginx

# Override the default nginx configuration file
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/nginx.conf
```

Le fichier de configuration de Nginx nous permets de lancer deux instance de notre application. l'adresse IP presente dans la configuration est l'adresse IP de notre VM EC2.

```
events {}
http {
    # Define the group of servers available
    upstream 16.16.159.200 {
        server app;
        server tcb_app_1:5000;
        server tcb_app_2:5000;
    }
    server {
        # Server group will respond to port 80
        listen 80;
        server_name app.com;
	location / {
            proxy_pass http://16.16.159.200;
        }
    }
}
```

Nous pouvons voir **tcb_app_1** et **tcb_app_2** qui represente nos deux instance lancer par Nginx.


### Docker Compose 

Grace a Docker compose nous pouvons excuter le build de nos deux service Flask et Nginx, on passons a notre applicaiton flask les variable nécessaire pour le foncitonnement de l'application, ces variables represente comme suit :

- SECRET_KEY : clée de cryptage de l'applicaiton Flask
- DB_HOST: l'adresse de notre base de données RDS
- DATABASE: la base de donnée sur laquell nous devons nous connecter
- DB_USER: le user de la base
- DB_PASSWORD: mot de passe de la base
- AWS_ACCESS_KEY: clée d'accées AWS pour S3
- AWS_SECRET_KEY: clée secrete AWS pour S3
- AWS_S3_LINK: l'adresse de notre bucket S3 afin de stocker nos images


```
version: '3.7'

services:
  # Build the app services
  app:
    build: app
    environment:
     - SECRET_KEY=${SECRET_KEY}
     - DB_HOST=${DB_HOST}
     - DATABASE=${DATABASE}
     - DB_USER=${DB_USER}
     - DB_PASSWORD=${DB_PASSWORD}
     - AWS_ACCESS_KEY=${AWS_ACCESS_KEY}
     - AWS_SECRET_KEY=${AWS_SECRET_KEY}
     - AWS_S3_LINK=${AWS_S3_LINK}
  nginx:
    container_name: nginx
    build: nginx
    # Bind the port 80 of container to machine port 80
    ports:
      - 80:80
    # Make app as nginx dependency service
    depends_on:
      - app

```


**Aperçu de nos container Docker lancer sur notre VM EC2**
![docker containre ls](docker_ls.png)

Nous pouvons voir notre serveur Nginx qui ecoute sur le port 80 et qui vas servir nos deux instance Flask qui ecoute sur le port 5000 comme configurer sur Gunicorn.

**Aperçu de nos images Nginx et Flask**
![docker image ls ](docker_image.png)

<br /> <br /> 

## Création de compte AWS et ajout d'un utilisateur avec les droit nécessaire et les clé  d'access AWS <a id="iam"> </a>

### Inscription
Rien de plus simple que de crée un compte AWS il vous suffit d'aller a l'adresse suivante et vous inscrire (une carte bancaire est nécessaire pour l'inscription) [lien AWS](https://portal.aws.amazon.com/billing/signup?nc2=h_ct&src=header_signup&redirect_url=https%3A%2F%2Faws.amazon.com%2Fregistration-confirmation#/start/email).

Vous aurrez accées a differents service gratuitement pendant 12 mois, mais avec des usages limité, si vous depasser le quota qu'il vous a ete fournis vous receverez des couts en fin du mois. Vous pouvez vous renseignez sur les differents services et leurs gratuités [ici liste des services ](https://aws.amazon.com/fr/free/?trk=efd55251-080c-4c00-a462-2977a465057e&sc_channel=ps&ef_id=EAIaIQobChMIyfTU4vfF_gIVnhEGAB3IWwmgEAAYASAAEgIn3PD_BwE:G:s&s_kwcid=AL!4422!3!563933958360!p!!g!!amazon%20aws!15356572758!127983197897&all-free-tier.sort-by=item.additionalFields.SortRank&all-free-tier.sort-order=asc&awsf.Free%20Tier%20Types=*all&awsf.Free%20Tier%20Categories=*all).


### Nouveau Utilisateur IAM 

Dans cette etape nous allons crée un nouvel utilisateur et lui ratacher les autorisation pour l'accés a S3 et a EC2.

Pour faire cela il faut ce rendre a la console direction [IAM Identity and Access Management (IAM)](https://us-east-1.console.aws.amazon.com/iam/home#/home).

![IAM](IAM.png).


apres cela acceder a Utilisateurs et ajouter un nouvelle utilisateur en lui donnant les autorisation suivantes :

![IAM](add_user.png).

##### Creation de nouvelle clée

Rendez-vous a la fenetre **Informations d'identification de sécurité** puis **Clés d'accès** et Créer une clée d'accès.

![IAM](add_key.png).


Vous avez maintenant votre pert de clé que vous pouvez utilisez pour vous connecter a vos different service AWS via du terminale avec AWS-CLI ou directement via notre applicaiton Flask avec le package **Boto3**.



## Utilisation et configuration de Amazon Cloud Compute Service (EC2) <a id="ec2"></a>

Maintenant nous allons crée notre instance **EC2** pour cela rien de plus simple il suffit d'acceder au lien suivant [EC2](https://eu-north-1.console.aws.amazon.com/ec2/home?region=eu-north-1#Home:).

Puis Lancer une instance, ace moment la vous pouvez configurer votre instance, et surtout recupere votre clée afin d'accéder par **SSH**.

![EC2 Instance](ec2.png).

Dans mon cas j'ai choisi une instance *micro3* sous **Ubuntu**. Apres le lancement de votre instance vous pouvez y acceder via SSH pour installer **Docker** et transferet tous vos documents via **SFTP**.

![EC2 ssh](ssh.png).
![EC2 apt-get update](apt_get_update.png).
![EC2 install docker](apt_get_docker.png).


<br /> <br/>


### Utilisation et configuration de Amazon Relational Databases Service (RDS) <a id="rds"> </a>

Nous allons utiliser le service Amazon Relational Databases afin de crée une base de donnée **Postgres** accessible via notre application qui est lancé sur notre serveur Ubuntu sur l'instance EC2 via Docker que nous avons crée.

Pour cela nous allons crée une nouvelle base de donnée via le lien [RDS suivant](https://eu-north-1.console.aws.amazon.com/rds/home?region=eu-north-1#).

![RDS](db_create.png).


Nous choisisons une base de donnée Postgres 

![RDS](db_psgql.png).

Puis l'offre gratuite

![RDS](db_free.png).

Puis un nom d'utilsiateur et mot de passe, avec le type d'instance a lancer (micro3 suffit). 

**Trés important preciser que la connéctivité en choisissant " se connecter a une ressource EC2" et vous selectionner votre instance, cela nous permet d'avoir notre base de donnée sur le meme VPC (Virtual Private Cloud) pour quel soit accessible via notre instance EC2**.

![RDS](db_ec2.png).


On peut maintenant recuper notre adresse et port pour la base apres son lancement qui peut prendre un peut de temps.

![RDS](db_host.png).


<br/><br/>

## Utilisation et configuration de Amazon Simple Storage Service (S3) <a id="s3"></a>

Maintenant il nous reste plus qu'a crée un nouveau bucket S3 via le lien suivant : [S3](https://s3.console.aws.amazon.com/s3/buckets?region=eu-north-1).


![S3](s3.png).

Crée un nouveau compartiment apres cela il nous faut rendre son **accées public**.

### Bucket Accessible publiquement

Nous devons changer les autorisation et la stratégie de notre Bucket pour le rendre accessible publiquement.


1. Decochet Bloquer tous les acces publique 

![S3 public](public.png).

2. Ajoutter la strategie suivante :
    ```
    {
        "Version": "2008-10-17",
        "Statement": [
            {
                "Sid": "AllowPublicRead",
                "Effect": "Allow",
                "Principal": {
                    "AWS": "*"
                },
                "Action": "s3:GetObject",
                "Resource": "arn:aws:s3:::tcb-cloud/*"
            }
        ]
    }
    ```

![S3 strat](strat.png).

Voila maintenant votre bucket est accessible via le lien aws fourni, vous pouvez aussi crée un point d'acces specifique avec des parametre specifique pour acceder a votre bucket.

<br/><br/>


## Application Flask et base de donnée Postgresql <a id="app"></a>

Comme expliquer plus haut mon application consiste on un blog ou toute personne peut s'inscrire poster des articles et interagire avec les autres bloggeur via les commentaires et les like


J'ai utiliser une base de données Postgres, accessible via le driver python **[Psycopg](https://www.psycopg.org/docs/index.html)**.

J'ai peuplé ma base avec un package python **Faker** qui me permet de remplire ma base avec des données aléatoire Nom, Prenom, Sex et avatar genere apartir d'une image du site ``` "https://xsgames.co/randomusers/avatar.php?g="+gender ``` ou gender est une variable representant male ou female.

J'ai aussi utiliser le package **markdown** qui me permet d'avoir un moteur markdown pour convertir du markdown vers du **HTML** pour ecrir les article.

### Upload Image to S3
J'utilise aussi une fonctionnaliter d'upload d'image afin de les integrer dans les articles pour chaque utilisateurs, et cela en envoyant l'image sur **S3** avec pour chaque utilisateur un compartiment propre a lui comme ci-dessous, j'utilise un packge me permettant de créer des short link afin de ne pas avoir un enorme lien aws poitant vers le bucket S3.

![Images Upload](images_up.png).


![Images Upload](up_img.png).



### Database structure

Voici la structure de ma base de donnée

![DB diagram](db_diagrame.png).

**Code**

```
DROP TABLE IF EXISTS image;
DROP TABLE IF EXISTS likes;
DROP TABLE IF EXISTS comment;
DROP TABLE IF EXISTS post;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
  id SERIAL PRIMARY KEY,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  gender TEXT NOT NULL,
  avatar TEXT
);


CREATE TABLE post (
  id SERIAL PRIMARY KEY,
  author_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  title TEXT NOT NULL,
  body TEXT NOT NULL,
  FOREIGN KEY (author_id) REFERENCES users (id)
);


CREATE TABLE comment (
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL,
  post_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  body TEXT NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users (id),
  FOREIGN KEY (post_id) REFERENCES post (id)
);

CREATE TABLE likes (
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL,
  post_id INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users (id),
  FOREIGN KEY (post_id) REFERENCES post (id)
);


CREATE TABLE image (
  id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL,
  name TEXT,
  link TEXT,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users (id)
);

```


### Application structure
```
└── tcb/
    ├── docker_compose.yml
    ├── nginx/
    │   ├── Dockerfile
    │   ├── nginx.conf
    └── app/
        ├── Dockerfile
        ├── requirements.txt
        ├── test/
        └──  tcb/
            ├── __init__.py
            ├── auth.py
            ├── blog.py
            ├── comment.py
            ├── db.py
            ├── download_avatar.py
            ├── fake_data.py
            ├── image_compress.py
            ├── likes.py
            ├── schema.sql
            ├── search.py
            ├── static/
            │   ├── images
            │   ├── style.css
            ├── temp/
            ├── templates/
            │    ├── base.html
            │    ├── auth/
            │    │    ├── login.html
            │    │    ├── register.html
            │    └── blog/
            │        ├── index.html
            │        ├── create.html
            │        ├── post.html
            │        ├── update.html
            ├── upload_file.py
            └── upload_s3.py

```


### Ajax and Javascript

J'utilise beaucoup de javascript afin de rendre l'applicaiton plus interactif 
et l'ajax afin d'ajoutter des like et commentaire sans recharger la page 

**Exemple**

```
    $.ajax({
        type: 'POST',
        url: '/comment',
        data: {
            post_id: {{post['id']}},
            user_id: {{g.user['id']}},
            body : comment.val()
        },
        success: function(response) {
            comments.append(newCommentHTML(response['comment_id'],response['user_id'], date, comment.val()) );
            comment.val('');
        },
        error: function(error) {
            console.log(error);
            console.log("no"); 
        }
    });
```


VOILA !

