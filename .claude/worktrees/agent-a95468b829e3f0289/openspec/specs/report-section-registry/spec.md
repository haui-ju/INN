# report-section-registry Specification

## Purpose
Define el registro de las secciones del informe en `project/config.yaml`: qué secciones existen, qué skill aporta cada una y cuáles están disponibles según las corridas vigentes, para que el informe pueda armarse en cualquier punto del pipeline con lo que ya se ejecutó.

## Requirements

### Requirement: Secciones aportadas por cada skill
`pipeline.json` SHALL declarar, en cada skill de generación que produce contenido del informe, las secciones del índice que aporta (`secciones`), y cada sección del informe SHALL pertenecer a una sola skill.

#### Scenario: Sección con dos skills
- **WHEN** `pipeline.json` declara la misma sección en dos skills
- **THEN** la validación del kit informa la sección y las dos skills

#### Scenario: Sección sin skill
- **WHEN** una sección del índice no figura en ninguna skill
- **THEN** la validación informa la sección como huérfana

### Requirement: Lista de secciones en el config
El config SHALL contener `informe.secciones`, una entrada por cada sección declarada en `pipeline.json`, con la skill que la aporta, la corrida vigente (`run`) y su estado `disponible` o `pendiente`, y `00-init` SHALL crearla con todas las secciones pendientes.

#### Scenario: Config recién creado
- **WHEN** `00-init` termina
- **THEN** `informe.secciones` lista todas las secciones del informe con estado `pendiente` y sin corrida

#### Scenario: Comentarios conservados
- **WHEN** una skill actualiza `informe.secciones`
- **THEN** el archivo conserva los comentarios de todos los campos

### Requirement: Registro de secciones al terminar una skill
Al registrar una corrida con `register`, el kit SHALL marcar como `disponible` todas las secciones de esa skill y apuntar su `run` a la corrida vigente del paso, y un `-update` SHALL actualizar ese `run` cuando su fork pasa a ser la corrida vigente.

#### Scenario: Skill terminada
- **WHEN** `04-make-strategic-analysis` registra su corrida
- **THEN** las secciones 1.5, 1.6 y 1.7 pasan a `disponible` con el `run` de esa corrida

#### Scenario: Update con validación fallida
- **WHEN** el fork de un update no pasa la validación
- **THEN** las secciones conservan el `run` anterior

#### Scenario: Paso fijado
- **WHEN** el paso está fijado y se registra una corrida nueva
- **THEN** las secciones siguen apuntando a la corrida fijada

### Requirement: Consulta de secciones disponibles
El kit SHALL ofrecer una consulta que liste las secciones disponibles y las pendientes con la skill que produce cada pendiente, para que el ensamblado del informe use solo las disponibles.

#### Scenario: Informe parcial
- **WHEN** solo se ejecutaron las skills hasta `05-make-problem-objectives`
- **THEN** la consulta devuelve disponibles 1.1 a 1.10 y pendientes 2.1 en adelante, cada una con su skill

#### Scenario: Ninguna sección disponible
- **WHEN** no se ejecutó ninguna skill de contenido
- **THEN** la consulta devuelve todas las secciones como pendientes

### Requirement: Corrida inexistente en una sección
Si la carpeta del `run` de una sección disponible no existe, el kit SHALL tratar la sección como pendiente y avisar la causa, sin borrar el registro.

#### Scenario: Carpeta borrada
- **WHEN** la corrida de la sección 2.4 fue eliminada del disco
- **THEN** la consulta la lista como pendiente e indica que falta la carpeta

### Requirement: Coherencia del registro con el pipeline
La validación del config SHALL rechazar `informe.secciones` que contenga una sección que `pipeline.json` no declara, y SHALL completar como pendientes las secciones nuevas de `pipeline.json` que falten en el config.

#### Scenario: Sección desconocida
- **WHEN** el config lista la sección 9.9 que no está en `pipeline.json`
- **THEN** la validación informa la sección y no escribe

#### Scenario: Sección nueva en el pipeline
- **WHEN** `pipeline.json` agrega una sección y el config no la tiene
- **THEN** el kit la agrega al config como pendiente al validar
