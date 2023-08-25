/* Bootstrap 5 JS included */

// Drag and drop - single or multiple image files
// https://www.smashingmagazine.com/2018/01/drag-drop-file-uploader-vanilla-js/
// https://codepen.io/joezimjs/pen/yPWQbd?editors=1000
(function () {

  'use strict';

  // Four objects of interest: drop zones, input elements, gallery elements, and the files.
  // dataRefs = {files: [image files], input: element ref, gallery: element ref}

  const preventDefaults = event => {
    event.preventDefault();
    event.stopPropagation();
  };

  const highlight = event =>
    event.target.classList.add('highlight');

  const unhighlight = event =>
    event.target.classList.remove('highlight');

  const getInputAndGalleryRefs = element => {
    const zone = element.closest('.upload_dropZone') || false;
    const gallery = zone.querySelector('.upload_gallery') || false;
    const input = zone.querySelector('input[type="file"]') || false;
    return { input: input, gallery: gallery };
  }

  const handleDrop = event => {
    const dataRefs = getInputAndGalleryRefs(event.target);
    dataRefs.files = event.dataTransfer.files;
    handleFiles(dataRefs);
  }


  const eventHandlers = zone => {

    const dataRefs = getInputAndGalleryRefs(zone);
    if (!dataRefs.input) return;

    // Prevent default drag behaviors
    ;['dragenter', 'dragover', 'dragleave', 'drop'].forEach(event => {
      zone.addEventListener(event, preventDefaults, false);
      document.body.addEventListener(event, preventDefaults, false);
    });

    // Highlighting drop area when item is dragged over it
    ;['dragenter', 'dragover'].forEach(event => {
      zone.addEventListener(event, highlight, false);
    });
    ;['dragleave', 'drop'].forEach(event => {
      zone.addEventListener(event, unhighlight, false);
    });

    // Handle dropped files
    zone.addEventListener('drop', handleDrop, false);

    // Handle browse selected files
    dataRefs.input.addEventListener('change', event => {
      dataRefs.files = event.target.files;
      handleFiles(dataRefs);
    }, false);

  }


  // Initialise ALL dropzones
  const dropZones = document.querySelectorAll('.upload_dropZone');
  for (const zone of dropZones) {
    eventHandlers(zone);
  }


  // No 'image/gif' or PDF or webp allowed here, but it's up to your use case.
  // Double checks the input "accept" attribute
  const isImageFile = file =>
    ['image/jpeg', 'image/png', 'image/svg+xml'].includes(file.type);


  function previewFiles(dataRefs) {
    if (!dataRefs.gallery) return;
    for (const file of dataRefs.files) {
      let reader = new FileReader();
      reader.readAsDataURL(file);
      reader.onloadend = function () {
        let img = document.createElement('img');
        img.className = 'upload_img mt-2';
        img.setAttribute('alt', file.name);
        img.src = reader.result;
        dataRefs.gallery.appendChild(img);
      }
    }
  }


  // Handle both selected and dropped files
  const handleFiles = dataRefs => {

    let files = [...dataRefs.files];

    // Remove unaccepted file types
    files = files.filter(item => {
      if (!isImageFile(item)) {
        console.log('Not an image, ', item.type);
      }
      return isImageFile(item) ? item : null;
    });

    if (!files.length) return;
    dataRefs.files = files;

    previewFiles(dataRefs);
  }

})();



menu = document.getElementById('menu')
search = document.getElementById('search')
menu_toogle = document.getElementById('menu-toggle')

function navtoggle(type) {



  if (type == 'on') {
    menu_toogle.setAttribute('onclick', 'navtoggle("off")')
    menu.classList.remove('hidden')
    search.classList.remove('hidden')
  }
  if (type == 'off') {
    menu_toogle.setAttribute('onclick', 'navtoggle("on")')
    menu.classList.add('hidden')
    search.classList.add('hidden')
  }
}

menu_toogle.setAttribute('onclick', 'navtoggle("on")')
function setup(event) {
  document.getElementById('load').style.display = 'block'
  document.getElementById('msg').innerHTML = ''

  event.preventDefault(); // This line stops the form from submitting
  var title = document.getElementById('title').value
  var description = document.getElementById('description').value
  var image = document.getElementById('thumbnail').value
  var type = document.getElementById('type').value
  var tags = document.getElementById('tags').value


  download_data = []
  x = 0
  for (var x = 0; x < i; x++) {
    // This code will be executed in each iteration
    text = document.getElementById(`btn-text${x + 1}`).value
    text2 = document.getElementById(`btn-line${x + 1}`).value

    download_data.push(`{"text":"${text}", "url":"${text2}"}`)

    // You can perform any operations or actions you need here
  }
  var formData = new FormData();  // Create FormData object to hold data
  var imageFile = $("#thumbnail")[0].files[0];  // Get the selected image file

  formData.append("title", title);
  formData.append("description", description);
  formData.append("image", imageFile);
  formData.append("list", download_data);
  formData.append("type", type);
  formData.append("tags", tags);

  $.post({
    url: "/upload",  // URL to your server-side script that handles the upload
    data: formData,
    contentType: false,
    processData: false,
    success: function (response) {
      // Handle success response from the server
      window.location = '#top'
      document.getElementById('msg').innerHTML = `<h3 style="text-align: center;color: green;">Movies successfully uploaded</h3>`
      console.log("Data and image uploaded successfully:", response);
      document.getElementById('load').style.display = 'none'
    },
    error: function (error) {
      // Handle error response from the server
      window.location = '#top'
      document.getElementById('load').style.display = 'none'
      console.error("Error uploading data and image:", error);
      document.getElementById('msg').innerHTML = `<h3 style="text-align: center;color: red;">An error Occured! Try Again if error prsist contact krishna sharma!</h3>`
    }
  });

}