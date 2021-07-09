-- FUNCTION: public.media()

-- DROP FUNCTION public.media();

CREATE FUNCTION public.media()
    RETURNS trigger
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE NOT LEAKPROOF
AS $BODY$
begin

insert into tuto_tutorias ( confirmacion_id, fecha, hora)
select  tuto_confirmaciones.confirmacion_id,  fecha_inicio, hs
from tuto_confirmaciones
left join tuto_tutorias on tuto_tutorias.confirmacion_id=tuto_confirmaciones.confirmacion_id
left join tuto_resultados on tuto_resultados.resultado_id=tuto_tutorias.resultado_id
order by  tuto_confirmaciones.confirmacion_id desc
limit 1;

insert into tuto_tutorias ( confirmacion_id, fecha, hora)
select  tuto_confirmaciones.confirmacion_id,  fecha_inicio + interval '7 day', hs
from tuto_confirmaciones
left join tuto_tutorias on tuto_tutorias.confirmacion_id=tuto_confirmaciones.confirmacion_id
left join tuto_resultados on tuto_resultados.resultado_id=tuto_tutorias.resultado_id
order by  tuto_confirmaciones.confirmacion_id desc
limit 1;

insert into tuto_tutorias ( confirmacion_id, fecha, hora)
select  tuto_confirmaciones.confirmacion_id,  fecha_inicio + interval '14 day', hs
from tuto_confirmaciones
left join tuto_tutorias on tuto_tutorias.confirmacion_id=tuto_confirmaciones.confirmacion_id
left join tuto_resultados on tuto_resultados.resultado_id=tuto_tutorias.resultado_id
order by  tuto_confirmaciones.confirmacion_id desc
limit 1;

insert into tuto_tutorias ( confirmacion_id, fecha, hora)
select  tuto_confirmaciones.confirmacion_id,  fecha_inicio + interval '21 day', hs
from tuto_confirmaciones
left join tuto_tutorias on tuto_tutorias.confirmacion_id=tuto_confirmaciones.confirmacion_id
left join tuto_resultados on tuto_resultados.resultado_id=tuto_tutorias.resultado_id
order by  tuto_confirmaciones.confirmacion_id desc
limit 1;

 RETURN NULL;
end
$BODY$;

ALTER FUNCTION public.media()
    OWNER TO goadmin;
