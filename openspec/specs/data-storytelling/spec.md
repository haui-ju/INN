# data-storytelling Specification

## Purpose
Define la skill `10-make-storytelling` y su `-update`, que redactan la sección 4 del informe como una narrativa de hallazgos construida solo con los valores y las capturas reales del dashboard, orientada a las decisiones del dueño y del jefe de cocina.

## Requirements

### Requirement: Playbook y modelos del storytelling
El repositorio SHALL incluir `common/10-storytelling/guia.md` (estructura de contexto, hallazgo y decisión, elección de la captura que sostiene cada hallazgo, lenguaje condicionado a datos generados y errores frecuentes) y `common/10-storytelling/models/` con una plantilla por entregable (ficha, instrucciones, formato, ejemplo y checklist) y un `README.md`.

#### Scenario: Skill que necesita el formato
- **WHEN** `10-make-storytelling` va a escribir la sección
- **THEN** lee antes la guía y la plantilla y respeta su formato

### Requirement: Fuentes de la skill del storytelling
La skill SHALL leer el brief vigente (usuarios, decisiones y objetivos), `modelo.json`, la corrida vigente de `09-make-dashboard` (`valores.json` y `capturas/`) y la sección 1.8 a 1.10, y SHALL bloquear cuando falten los valores reales.

#### Scenario: Sin valores reales
- **WHEN** la corrida de `09-make-dashboard` no trae `valores.json`
- **THEN** la skill se detiene e indica que primero hay que entregar los valores del dashboard

### Requirement: Hallazgos trazados a los objetivos
La sección 4 SHALL presentar hallazgos `HLZ-nn`, cada uno con su objetivo específico `OE-nn`, el KPI, el valor real frente a su meta, la captura que lo muestra y la decisión que apoya, y cada `OE` del brief SHALL tener al menos un hallazgo.

#### Scenario: Objetivo sin hallazgo
- **WHEN** un `OE-nn` del brief no aparece en ningún hallazgo
- **THEN** la validación informa el objetivo

#### Scenario: Hallazgo sin captura
- **WHEN** un hallazgo no cita ninguna captura de las que entregó el equipo
- **THEN** la validación informa el hallazgo

### Requirement: Cifras solo de los valores reales
Toda cifra de un hallazgo SHALL coincidir con `valores.json` de `09-make-dashboard`, y la skill SHALL NOT completar, estimar ni redondear de forma que cambie una cifra no entregada.

#### Scenario: Cifra que no está en los valores
- **WHEN** un hallazgo cita 11 % de margen y `valores.json` dice 8 %
- **THEN** la validación informa la cifra y el valor correcto

### Requirement: Lenguaje condicionado a datos generados
Con `modo_datos: generado`, la sección SHALL decir al comienzo que los hallazgos se basan en datos generados para el proyecto y SHALL evitar afirmar que describen el negocio real de una empresa.

#### Scenario: Datos generados
- **WHEN** `modo_datos` es `generado`
- **THEN** la sección 4 declara el origen de los datos y la validación falla si no lo hace

### Requirement: Sección 4 y registro
La corrida SHALL escribir `secciones/4.md` con su encabezado exacto, las capturas marcadas con `<!-- captura: <id> -->`, títulos de tabla `Tabla N: …` y `referencias.md` en APA 7, SHALL registrar la sección con `register` y SHALL tener una homóloga `10-make-storytelling-update` que copia la corrida vigente como «-fork» y cambia solo lo pedido.

#### Scenario: Corrida completa
- **WHEN** la skill termina
- **THEN** el validador no informa incidencias y `12-make-report` incluye la sección 4 con sus capturas numeradas

#### Scenario: Cambia un valor del dashboard
- **WHEN** el equipo corrige un valor en `09-make-dashboard-update`
- **THEN** `10-make-storytelling-update` actualiza solo los hallazgos que lo citan
