-- PROCEDURE: public.insert_conf(integer, integer, integer, character varying, date, integer, integer, integer)

-- DROP PROCEDURE public.insert_conf(integer, integer, integer, character varying, date, integer, integer, integer);

CREATE OR REPLACE PROCEDURE public.insert_conf(
	carrera integer,
	materia integer,
	docente integer,
	horario character varying,
	fecha date,
	bim integer,
	canal integer,
	categ integer)
LANGUAGE 'sql'
AS $BODY$
insert into tuto_confirmaciones 
(carrera_id, materia_id, docente_id, hs, 
 fecha_inicio, bimestre_id, canal_id, categoria_id ) values
(carrera, materia, docente, CAST(horario AS time), fecha, bim, canal, categ)
$BODY$;
