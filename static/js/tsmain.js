$(document).ready(function () {
  console.log("ready for this");

  var start = new Date("2020-03-19T00:00:00");
  var end = new Date();
  var days = (end - start) / (1000 * 60 * 60 * 24);
  $(".text-muted").append("&nbsp;  days from the start of the quarantine : " + Math.floor(days));

  var carrera = $("#id_carrera");
  var materia = $("#id_materia");
  var docente = $("#id_docente");

  if (carrera.val() == "") {
    materia.prop("disabled", true);
    docente.prop("disabled", true);
  } else {
    materia.prop("disabled", false);
    docente.prop("disabled", false);
  }

  carrera.change(function () {
    if ($(this).val() == "") {
      materia.empty();
      docente.empty();
      materia.prop("disabled", true);
      docente.prop("disabled", true);
    } else {
      var url = $("#conf_form").attr("data-url");
      var c_id = $(this).val();
      $.ajax({
        url: url,
        data: { carrera: c_id },
        success: function (data) {
          materia.html(data);
          docente.empty();
          materia.prop("disabled", false);
          console.log(data);
        },
      });
    }
  });

  materia.change(function () {
    docente.prop("disabled", false);
    var url = $("#conf_form").attr("data-url2");
    var c_id = carrera.val();
    $.ajax({
      url: url,
      data: { carrera: c_id },
      success: function (data) {
        docente.html(data);
      },
    });
  });

  var resultado = $(".resultado");
  resultado.change(function () {
    var url = $(this).attr("data-url3");
    var t_id = $(this).attr("data_tuto");
    var r_id = $(this).val();
    console.log(url, t_id, r_id);
    $.ajax({
      url: url,
      data: { tuto: t_id, value: r_id },
      success: function () {
        console.log("resultado guardado");
      },
    });
  });
 
  var sendmail = $("#contact-form");
  sendmail.submit(function (event) {
    event.preventDefault();
    $("input").prop("readonly", true);
    this.contact_number.value = (Math.random() * 100000) | 0;
    emailjs.sendForm("", "", this).then(
      function () {
        console.log("SUCCESS!");
        $("input").prop("readonly", false);
        sendmail.notify("mensaje enviado", "success");
        sendmail[0].reset();
      },
      function (error) {
        console.log("FAILED...", error);
        sendmail.notify("complete correctamente", "warn");
      }
    );
  });

  $("#req_inicio").change(() => {
    $("#req_inicio").removeClass("border border-danger");
  });

  var req = $(".req");
  req.click(function () {
    var url = $(this).attr("data-url");
    var carrera = $(this).attr("data-carrera");
    var materia = $(this).attr("data-materia");
    var docente = $(this).attr("data-docente");
    var horario = $(this).attr("data-horario");
    var solid = $(this).attr("data-solid");
    var fecha = $("#req_inicio").val();
    var bim = $("#bim").val();
    var canal = $("#canal").val();
    var categ = $("#categ").val();
    console.log(fecha);

    if (fecha === '') {
      $("#req_inicio").addClass("border border-danger");
    } else {
      console.log(typeof horario);

      $.ajax({
        url: url,
        data: {
          carrera: carrera,
          materia: materia,
          docente: docente,
          horario: horario,
          fecha: fecha,
          bim: bim,
          canal: canal,
          categ: categ,
          solid: solid,
        },
        success: function () {
          console.log("requirement save");
          $("tr[name=" + solid + "]").hide();
        },
      });
    }
  });
});
