"use strict"


var allButtonsOnPage = document.querySelectorAll('.button');

allButtonsOnPage.forEach(function(button) {
  button.addEventListener('click', function() {
    id = this.id
    console.log('hello')
    console.log(id)
    
    const formInputs = {
      'event_id': id
    }

    console.log(formInputs)

    $.post('/removeevents', formInputs, (res) => {
    alert('You have removed an event!')
    location.reload();
      // console.log(events)
    })
  });
});


$('.button').on('click',function() {
  $(this).find("i").toggleClass("far fas selected-heart border-heart");
});