-- FUNCTION: public.docentes_all()

-- DROP FUNCTION public.docentes_all();

CREATE OR REPLACE FUNCTION public.docentes_all(
	)
    RETURNS TABLE(nombre character varying, apellidos character varying, descripcion character varying) 
    LANGUAGE 'sql'

    COST 100
    VOLATILE 
    ROWS 1000
AS $BODY$
select nombre, apellidos, descripcion 
from tuto_docentes doc
join tuto_carreras carr on carr.carrera_id=doc.carrera_id
$BODY$;

ALTER FUNCTION public.docentes_all()
    OWNER TO goadmin;
