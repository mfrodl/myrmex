var monthStats = [];

$(function() {
  date = new Date();
  setMonth(date.getFullYear(), date.getMonth() + 1);
});

/*
 * Highlight day in calendar and populate form fields according to database
 */
function setDate(date) {
  $('#date').val(date);
  $('.selected').removeClass('selected');
  $('#' + date).addClass('selected');
  $('#form-fields').css('display', 'block');

  var exercisesUnits = {
    'jogging': 'kilometers',
    'yoga': 'minutes',
    'weightlifting': 'kilograms'
  };

  for (let exercise in exercisesUnits) {
    var units = exercisesUnits[exercise];
    var entry = monthStats.find(function (element) {
      return (
        element.model == 'exercise.' + exercise &&
        element.fields.date == date
      );
    });

    $('#' + exercise).val(entry ? entry.fields[units] : '');
  }
}

/*
 * Render HTML calendar for given month and pre-fetch respective exercise
 * statistics from database
 */
function setMonth(year, month) {
  $.get('/exercise/calendar/' + year + '/' + month + '/', function(data) {
    $('#calendar').html(data);
  });

  $.get('/exercise/stats/' + year + '/' + month + '/', function(data) {
    monthStats = JSON.parse(data);
  });
}
