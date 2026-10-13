# Registro editorial histórico del borrador

Este registro se extrajo de `docs/tesis.md` el 2026-10-13 para mantener el manuscrito con la estructura FISI. Para el estado vigente consultar `docs/matriz-brechas.md` y `docs/notas-verificacion.md`.

## Notas de trabajo / TODO

> ✅ Los 5 puntos originales de este TODO fueron auditados y resueltos en el Sprint 1 (2026-07-14). El detalle completo de cada verificación está en `docs/notas-verificacion.md`. Resumen:
>
> 1. ~~DOI duplicado/contradictorio de Abraham et al. (2020)~~ → Resuelto: ninguno de los 2 DOIs correspondía realmente a "Abraham et al." Se reemplazó por Abualese y Al-Rousan (2023), verificado.
> 2. ~~Clasificación OWASP de SQLi inconsistente (A01 vs A03)~~ → Resuelto: confirmado A03 en owasp.org, corregido en el glosario.
> 3. ~~Cita textual de Jain & Gupta (2020, p. 45)~~ → Resuelto: la cita textual se retiró (no se pudo verificar); la referencia de arquitectura modular se corrigió a Aljebry et al. (2022).
> 4. ~~Estadísticas sin fuente primaria~~ → Parcialmente resuelto: Fortinet y el 88% de Movistar quedaron confirmados; OSIPTEL, INEI, CERT-Perú y el 36% de Movistar **siguen sin verificar** y quedan marcados ⚠️ en el cuerpo del documento y en `notas-verificacion.md`, sección 4.
> 5. ~~Todos los DOIs deben confirmarse~~ → Resuelto: se auditaron los 8 DOIs originales contra Crossref; ninguno correspondía a la cita real. Se reemplazaron 5 por papers reales verificados y se eliminaron 3 entradas duplicadas sin correspondencia. Ver `notas-verificacion.md`, sección 1, para el detalle completo.

**Pendientes abiertos para los siguientes sprints** (ver también `docs/sprints.md` y `docs/notas-verificacion.md` sección 4):

- Verificar directamente en fuente primaria: cifra del 36% de víctimas (Movistar 2023), estadística de INEI 2023, reporte de CERT-Perú 2023, y encontrar (o retirar) el dato de crecimiento de CMS atribuido a OSIPTEL.
- Encontrar una fuente real que respalde las técnicas de fingerprinting de CMS (hoy sin atribución externa, tras retirar la cita a "Kumar, 2019").
- Confirmar contra el texto completo de los papers ya verificados (Abualese y Al-Rousan 2023, Amankwah et al. 2020, Syarifudin et al. 2025, Prabakar et al. 2013, Aljebry et al. 2022) las cifras puntuales que aún quedan marcadas ⚠️ en las Tablas 2.1 y 3.1.
