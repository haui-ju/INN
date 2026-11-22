## Purpose
Define la skill que crea el cascarón inicial de los repositorios de la app bajo `project/app/` a partir del TRD y del plan de implementación: generadores por stack, git local, archivos de entorno, README, herramientas de calidad y un OpenSpec por repo, con confirmación previa, simulación e idempotencia.

## ADDED Requirements

### Requirement: Fuentes y componentes que aplican
La skill `24-make-app-scaffold` SHALL leer el TRD de la corrida vigente de la definición técnica (skill 22) y el `plan.json` de cada componente de la corrida vigente del plan de implementación (skill 23), y SHALL crear una carpeta en `project/app/` solo por cada componente que el TRD declare (`frontend`, `backend`, `database`, `openrpa`). Si falta alguna fuente, SHALL detenerse e indicar qué paso ejecutar.

#### Scenario: Proyecto sin frontend
- **WHEN** el TRD declara backend, base de datos y OpenRPA
- **THEN** la skill crea `project/app/backend`, `project/app/database` y `project/app/openrpa` y no crea `project/app/frontend`

#### Scenario: TRD ausente
- **WHEN** el config no tiene corrida vigente del TRD
- **THEN** la skill no escribe nada y avisa el paso que falta

### Requirement: Plan de comandos y confirmación
Antes de escribir o ejecutar nada, la skill SHALL mostrar por componente el comando del generador, los archivos que creará y qué comandos usan la red, y SHALL esperar la confirmación del usuario. Todo comando que use la red SHALL confirmarse de forma explícita, y la skill SHALL ofrecer un modo de simulación que solo imprime los comandos y no modifica el disco.

#### Scenario: Comando de red
- **WHEN** el generador del frontend descarga paquetes
- **THEN** la skill lo lista como comando de red y no lo ejecuta hasta que el usuario lo confirma

#### Scenario: Simulación
- **WHEN** el usuario elige la simulación
- **THEN** la skill imprime los comandos y los archivos previstos y no crea carpetas ni ejecuta comandos

### Requirement: Generador por stack desde el playbook
La skill SHALL obtener el comando de cada componente de la tabla stack → comando de `common/app-scaffold/guia.md`, usando el stack y el nombre del proyecto que declara el TRD, y SHALL negarse a inventar un comando para un stack que la tabla no incluya, pidiendo al usuario que lo defina.

#### Scenario: Frontend con Next.js
- **WHEN** el TRD elige Next.js con `pnpm`
- **THEN** el comando previsto es `pnpm create next-app@latest <name> --yes` con el nombre del TRD

#### Scenario: Stack sin comando
- **WHEN** el TRD elige un stack que la tabla no contempla
- **THEN** la skill lo informa y pregunta el comando al usuario antes de continuar

### Requirement: Git solo local
Cada repo SHALL iniciarse con `git init` local y la skill NUNCA SHALL crear, vincular ni subir a un repositorio remoto, ni ejecutar `git push`.

#### Scenario: Repo recién creado
- **WHEN** termina el cascarón del backend
- **THEN** `project/app/backend` es un repositorio git sin remotos configurados

### Requirement: Archivos de entorno y exclusiones
Cada repo SHALL tener un `.gitignore` que excluya como mínimo `.env`, las dependencias, los entornos virtuales, las salidas de build y los archivos de credenciales, un `.env` con valores de ejemplo y un `.env.example` con las mismas variables. La skill NUNCA SHALL escribir un secreto real ni agregar `.env` al índice de git.

#### Scenario: Backend con IA
- **WHEN** el TRD declara el modelo de OpenAI y un bot de Telegram
- **THEN** `.env.example` incluye `OPENAI_API_KEY` y `TELEGRAM_BOT_TOKEN` con valores de ejemplo, y `.gitignore` excluye `.env`

#### Scenario: Valor que parece real
- **WHEN** un valor de `.env` o `.env.example` coincide con el formato de una clave real
- **THEN** la validación lo informa

### Requirement: README en español por repo
Cada repo SHALL tener un `README.md` en español con la arquitectura del repo, cómo instalarlo y ejecutarlo, y una tabla de variables de entorno con su descripción y por qué valor reemplazar el de ejemplo.

#### Scenario: Variable sin descripción
- **WHEN** `.env.example` define `DATABASE_URL` y el README no la describe
- **THEN** la validación informa la variable

### Requirement: Calidad y contenedores según el TRD
La skill SHALL crear los archivos de linter, formateador, Docker y, si el TRD lo pide, de CI de cada repo, tomados de las plantillas de `common/app-scaffold/models/` para el stack elegido.

#### Scenario: Backend en Python con Docker
- **WHEN** el TRD declara un backend de Python con Docker
- **THEN** el repo incluye su `Dockerfile`, su configuración de linter y de formateador y el comando para ejecutarlos en el README

### Requirement: OpenSpec por repo con los changes del plan
Cada repo SHALL tener su propio `openspec/` inicializado y un stub por cada change del `plan.json` de su componente, en el orden y con los nombres del plan, y la skill NO SHALL crear changes que el plan no declare.

#### Scenario: Backend con cuatro changes
- **WHEN** el plan declara cuatro changes para el backend
- **THEN** `project/app/backend/openspec/changes/` contiene exactamente esos cuatro

### Requirement: Idempotencia sin sobrescribir
Al volver a ejecutarse, la skill SHALL detectar lo que ya existe y SHALL NOT sobrescribir ningún archivo existente sin preguntar; ofrecerá omitir, conservar o reemplazar cada uno.

#### Scenario: README existente
- **WHEN** `project/app/backend/README.md` ya existe
- **THEN** la skill pregunta si conservarlo o reemplazarlo y conserva el actual por omisión

### Requirement: Corrida, registro y actualización
La skill SHALL escribir `project/app-scaffold/<DD-MM-AAAA-HH-MM-SS>/` con un manifiesto de los componentes, comandos ejecutados y archivos creados, y un `README.md` de procedencia, y SHALL registrarla en el config. Los repos de `project/app/` no se copian al bifurcar. La skill `24-make-app-scaffold-update` SHALL poder agregar un componente o regenerar archivos concretos sin rehacer los demás.

#### Scenario: Corrida registrada
- **WHEN** termina el cascarón
- **THEN** el config apunta a la corrida y el manifiesto lista cada comando y archivo

#### Scenario: Agregar un componente
- **WHEN** el TRD incorpora un frontend después de crear el backend
- **THEN** el update crea solo `project/app/frontend` y deja el backend intacto

### Requirement: Validación del cascarón
La validación SHALL comprobar que cada componente del TRD tiene su carpeta, que cada repo tiene `.git` sin remotos, `.gitignore` con las exclusiones mínimas, `.env.example`, README en español, `openspec/` con los changes del plan y que ningún `.env` está en el índice; SHALL informar archivo y causa de cada incidencia.

#### Scenario: .env en el índice
- **WHEN** `.env` figura en el índice de git de un repo
- **THEN** la validación informa el archivo y exige quitarlo

### Requirement: Idioma
Los identificadores, nombres de archivo y comentarios de código generados SHALL estar en inglés; el README de cada repo y los mensajes al usuario SHALL estar en español.

#### Scenario: Archivos generados
- **WHEN** se crea el backend
- **THEN** sus archivos y carpetas tienen nombres en inglés y su README está en español
