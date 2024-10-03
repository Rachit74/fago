function imageToggle(imageID) {
    var image = document.getElementById('post-image-' + imageID)
    var toggle_link = document.getElementById('post-toggle-link-' + imageID)


    if (image.style.display == 'none' || image.style.display == '') {
        image.style.display = 'block';
        toggle_link.innerHTML = "Hide Image";
    } else {
        image.style.display = 'none';
        toggle_link.innerHTML = "Show Image";
    };
};


// Toggle Notification badge
function showNotifications(){
  const container = document.getElementById('notification-container');
  if (container.classList.contains('d-none')) {
    container.classList.remove('d-none');
  } else {
    container.classList.add('d-none');
  }
}


function getCookie(name) {
    let cookieValue = '';
    if (document.cookie && document.cookie != '') {
      const cookies = document.cookie.split(';');
      for (i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        // Does this cookie string begins with the name we want
        if (cookie.substring(0, name.length + 1) == (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    };
    return cookieValue;
  }
  
  
  function removeNotification(removeNotificationURL, redirectURL) {
    const csrftoken = getCookie('csrftoken');
    let xmlhttp = new XMLHttpRequest();
  
    xmlhttp.onreadystatechange = function() {
      if (xmlhttp.readyState == XMLHttpRequest.DONE) {
        if (xmlhttp.status == 200) {
          window.location.replace(redirectURL);
        } else {
          alert('There was an error!');
        }
      }
    };
  
    xmlhttp.open("DELETE", removeNotificationURL, true);
    xmlhttp.setRequestHeader("X-CSRFToken", csrftoken);
    xmlhttp.send();
  }

